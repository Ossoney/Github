import fitz  # PyMuPDF
import re
import json
import os
import sys
from collections import Counter

class ProcesadorRAG:
    def __init__(self):
        # Configuración de patrones regex jurídicos
        self.PATRON_CAPITULO = r"(CAPÍTULO\s+\d+|Capítulo\s+\d+|TEMA\s+\d+)\s*\n+(.*)"
        
        # Patrones para NER (Reconocimiento de Entidades)
        self.REGEX_ARTICULOS = r"(?:art\.|artículo|arts\.)\s*(\d+(?:\.\d+)?(?:\s*bis)?)"
        self.REGEX_NORMAS = r"(?:Ley|LO|Real Decreto|RD|Decreto-Ley)\s*(\d+/\d+)"
        self.REGEX_SENTENCIAS = r"(?:STC|SSTC|Sentencia)\s*(\d+/\d+)"

        # Configuración de Overlap
        self.OVERLAP_FRASES = 2  # Número de frases a solapar

    def _detectar_headers_footers(self, doc):
        """Detecta líneas repetitivas (encabezados/pies) para eliminarlas."""
        lineas = []
        total_paginas = len(doc)
        muestreo = min(50, total_paginas) 
        
        for i in range(muestreo):
            page = doc[i]
            text = page.get_text("text")
            lines = [l.strip() for l in text.split('\n') if l.strip()]
            if lines:
                lineas.append(lines[0]) 
                lineas.append(lines[-1]) 
        
        frecuencia = Counter(lineas)
        # Umbral: si aparece en más del 40% de las páginas, es ruido
        ruido = {linea for linea, count in frecuencia.items() if count > (muestreo * 0.4)}
        return ruido

    def _limpiar_texto(self, text_pagina, ruido_detectado):
        """Limpia headers, footers y números de página."""
        lineas_limpias = []
        for linea in text_pagina.split('\n'):
            linea_strip = linea.strip()
            if linea_strip in ruido_detectado: continue
            if re.match(r'^\s*\d+\s*$', linea_strip): continue # Números de pág
            lineas_limpias.append(linea)
        return '\n'.join(lineas_limpias)

    def _extraer_entidades_legales(self, texto):
        """Extrae referencias legales (arts, leyes, sentencias)."""
        arts = re.findall(self.REGEX_ARTICULOS, texto, re.IGNORECASE)
        normas = re.findall(self.REGEX_NORMAS, texto, re.IGNORECASE)
        stc = re.findall(self.REGEX_SENTENCIAS, texto, re.IGNORECASE)
        
        referencias = []
        referencias.extend([f"art. {a}" for a in arts])
        referencias.extend([f"Ley {n}" for n in normas])
        referencias.extend([f"STC {s}" for s in stc])
        return list(set(referencias))

    def _get_overlap_text(self, texto_previo):
        """Obtiene las últimas frases para contexto."""
        if not texto_previo: return ""
        frases = re.split(r'(?<=\.)\s+', texto_previo.strip())
        return " ".join(frases[-self.OVERLAP_FRASES:])

    def procesar_pdf(self, ruta_pdf):
        print(f"⚙️  Analizando: {os.path.basename(ruta_pdf)}...")
        doc = fitz.open(ruta_pdf)
        
        # 1. Detección de Ruido
        ruido = self._detectar_headers_footers(doc)
        if ruido:
            print(f"   🧹 Eliminando {len(ruido)} patrones de encabezado/pie.")

        # 2. Extracción Limpia
        full_text = ""
        for page in doc:
            full_text += self._limpiar_texto(page.get_text("text"), ruido) + "\n"

        # 3. Segmentación
        chunks = []
        capitulos = re.split(r"(?=CAPÍTULO\s+\d+|Capítulo\s+\d+|TEMA\s+\d+)", full_text)
        chunk_counter = 1
        contenido_chunk_anterior = ""

        print("   ✂️  Segmentando y enriqueciendo metadatos...")
        
        for cap in capitulos:
            if not cap.strip(): continue
            
            # Título Capítulo
            match = re.search(self.PATRON_CAPITULO, cap)
            tema_actual = "Introducción / Preámbulo"
            if match:
                titulo_limpio = match.group(2).strip().replace('\n', ' ')
                tema_actual = f"{match.group(1)}: {titulo_limpio}"
            
            # Epígrafes
            secciones = re.split(r"(?=\n\d+\.\s+|\n\d+\.\d+\.\s+)", cap)
            
            for sec in secciones:
                if len(sec.strip()) < 50: continue
                contenido_limpio = sec.strip()
                
                # Enriquecimiento
                texto_overlap = self._get_overlap_text(contenido_chunk_anterior)
                refs_legales = self._extraer_entidades_legales(contenido_limpio)
                
                # Título Epígrafe
                title_match = re.match(r"(\d+(\.\d+)*\.?)\s+(.*)", contenido_limpio)
                epigrafe_titulo = title_match.group(0).split('\n')[0] if title_match else "Sección General"
                
                # Clasificación
                es_hot = (re.match(r"^\d+\.\s", contenido_limpio) is not None) or \
                         any(x in contenido_limpio.lower() for x in ["concepto", "definición"])
                
                nivel = "teoría general"
                if any(x in contenido_limpio.lower() for x in ["ue ", "unión europea"]): nivel = "supranacional"
                elif any(x in contenido_limpio.lower() for x in ["constitución", "tc "]): nivel = "interno"

                # Objeto Chunk
                chunk_obj = {
                    "id": chunk_counter,
                    "content": contenido_limpio,
                    "context_overlap": texto_overlap,
                    "embedding_text": f"{tema_actual} - {epigrafe_titulo}. {contenido_limpio}",
                    "metadata": {
                        "source": os.path.basename(ruta_pdf),
                        "tema": tema_actual,
                        "epigrafe": epigrafe_titulo,
                        "hot": es_hot,
                        "nivel": nivel,
                        "legal_refs": refs_legales,
                        "char_count": len(contenido_limpio)
                    }
                }
                chunks.append(chunk_obj)
                chunk_counter += 1
                contenido_chunk_anterior = contenido_limpio

        return chunks

# --- FUNCIONES DE GUARDADO ---

def guardar_json(datos, nombre_base):
    path = f"{nombre_base}_rag_pro.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    return path

def guardar_txt_legible(datos, nombre_base):
    path = f"{nombre_base}_rag_pro.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"REPORTE DE PROCESAMIENTO RAG: {nombre_base}\n")
        f.write("="*60 + "\n\n")
        
        for chunk in datos:
            meta = chunk['metadata']
            f.write(f"🆔 CHUNK {chunk['id']} | {meta['nivel'].upper()}\n")
            f.write(f"📍 {meta['tema']} > {meta['epigrafe']}\n")
            
            if meta['hot']: f.write("🔥 CONCEPTO CLAVE (HOT)\n")
            if meta['legal_refs']: f.write(f"§ CITAS: {', '.join(meta['legal_refs'])}\n")
            
            f.write("-" * 20 + " CONTENIDO " + "-" * 20 + "\n")
            f.write(chunk['content'] + "\n")
            f.write("\n" + "="*60 + "\n\n")
            
    return path

# --- MAIN ---

def main():
    print("\n⚖️  PROCESADOR RAG JURÍDICO (DUAL OUTPUT)")
    print("===========================================")
    
    pdfs = [f for f in os.listdir('.') if f.lower().endswith(".pdf")]
    
    if not pdfs:
        print("❌ No hay PDFs en esta carpeta.")
        return

    print(f"Archivos disponibles:")
    for i, p in enumerate(pdfs):
        print(f"[{i+1}] {p}")
    
    try:
        idx = int(input("\n👉 Selecciona archivo: ")) - 1
        if 0 <= idx < len(pdfs):
            archivo = pdfs[idx]
            nombre_base = os.path.splitext(archivo)[0]
            
            procesador = ProcesadorRAG()
            chunks = procesador.procesar_pdf(archivo)
            
            # Guardar ambos formatos
            path_json = guardar_json(chunks, nombre_base)
            path_txt = guardar_txt_legible(chunks, nombre_base)
            
            print(f"\n✅ PROCESO COMPLETADO ({len(chunks)} chunks)")
            print(f"📄 JSON generado: {path_json}")
            print(f"📝 TXT generado:  {path_txt}")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada no válida.")

if __name__ == "__main__":
    main()
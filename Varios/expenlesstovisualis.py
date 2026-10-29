import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def seleccionar_archivo():
    root = tk.Tk()
    root.withdraw()
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona el reporte de ExpenLess (CSV)",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    return ruta_archivo

def transformar_reporte():
    archivo_origen = seleccionar_archivo()
    
    if not archivo_origen:
        print("No se seleccionó ningún archivo. Operación cancelada.")
        return

    nombre_base = os.path.splitext(archivo_origen)[0]
    archivo_destino = f"{nombre_base}_formato_visualis.xlsx"

    print(f"\nProcesando: {os.path.basename(archivo_origen)}...")

    try:
        # 1. Leer el archivo (manejando líneas corruptas)
        df = pd.read_csv(archivo_origen, on_bad_lines='skip')

        # 2. Limpieza de datos nulos en campos críticos
        df = df.dropna(subset=['Account Description', 'Amount', 'Transaction Date'])

        # 3. Crear estructura para Visualis con los nuevos campos
        new_df = pd.DataFrame()

        new_df['fecha'] = df['Transaction Date']
        new_df['cuenta'] = df['Account Description']
        
        # Mapeo de ingresos y gastos
        new_df['tipo (ingreso o gasto)'] = df['Expense or Income'].map({1.0: 'Ingreso', -1.0: 'Gasto'}).fillna('Otro')
        
        new_df['categoría'] = df['Category Name']
        new_df['subcategoría'] = df['Subcategory Name']
        new_df['importe o monto'] = df['Amount']
        new_df['moneda'] = df['Currency symbol']
        
        # Combinar nombre y descripción original
        new_df['descripción'] = df['Transaction Name'].fillna(df['Transaction Description']).fillna('')

        # --- NUEVOS CAMPOS ---
        # Intentamos obtener etiquetas y emoción (si no existen en el CSV, se dejan en blanco)
        col_etiquetas = 'Tags Name' if 'Tags Name' in df.columns else None
        col_emocion = 'Emotion' if 'Emotion' in df.columns else None

        new_df['etiquetas'] = df[col_etiquetas].fillna('') if col_etiquetas else ''
        new_df['estado emocional'] = df[col_emocion].fillna('') if col_emocion else ''
        # ---------------------

        # 4. Reordenar columnas incluyendo las nuevas especificaciones
        columnas_ordenadas = [
            'fecha', 'cuenta', 'tipo (ingreso o gasto)', 'categoría', 
            'subcategoría', 'importe o monto', 'moneda', 'descripción',
            'etiquetas', 'estado emocional'
        ]
        
        # Aseguramos que todas las columnas existan antes de reordenar
        new_df = new_df[columnas_ordenadas]

        # 5. Guardar en Excel
        new_df.to_excel(archivo_destino, index=False)
        print(f"---")
        print(f"✅ ¡Éxito! Archivo guardado como:")
        print(f"👉 {archivo_destino}")

    except Exception as e:
        print(f"❌ Error durante la transformación: {e}")

if __name__ == "__main__":
    transformar_reporte()
    input("\nPresiona Enter para finalizar...")
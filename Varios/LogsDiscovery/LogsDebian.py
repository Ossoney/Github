import re
import subprocess
import csv
from datetime import datetime

def analizar_y_exportar_logs(archivo_salida="reporte_incidencias.csv"):
    # Definición de patrones de búsqueda para incidencias
    patrones = {
        "CRITICAL": re.compile(r"CRITICAL|FATAL|SEGFAULT", re.IGNORECASE),
        "ERROR": re.compile(r"ERROR|FAILED|FAILURE", re.IGNORECASE),
        "WARNING": re.compile(r"WARNING|denied|Out of memory", re.IGNORECASE)
    }
    
    try:
        # Obtención de logs del sistema
        resultado = subprocess.check_output(["journalctl", "-n", "1000", "--no-pager"], text=True)
        lineas = resultado.splitlines()
        
        incidencias = []

        for linea in lineas:
            for nivel, regex in patrones.items():
                if regex.search(linea):
                    incidencias.append({
                        "fecha_hora": " ".join(linea.split()[:3]),
                        "nivel": nivel,
                        "mensaje": linea.strip()
                    })
                    break

        # Exportación a CSV
        if incidencias:
            with open(archivo_salida, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["fecha_hora", "nivel", "mensaje"])
                writer.writeheader()
                writer.writerows(incidencias)
            print(f"Análisis completado. Se han exportado {len(incidencias)} incidencias a '{archivo_salida}'.")
        else:
            print("No se encontraron incidencias relevantes.")

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar journalctl: {e}")
    except PermissionError:
        print("Error: Ejecute el script con sudo para acceder a los logs del sistema.")

if __name__ == "__main__":
    analizar_y_exportar_logs()
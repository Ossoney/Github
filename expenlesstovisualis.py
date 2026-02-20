import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def seleccionar_archivo():
    # Crear una ventana oculta de Tkinter
    root = tk.Tk()
    root.withdraw()
    # Abrir el selector de archivos
    ruta_archivo = filedialog.askopenfilename(
        title="Selecciona el reporte de ExpenLess (CSV)",
        filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
    )
    return ruta_archivo

def transformar_reporte():
    # 1. Preguntar al usuario por el archivo
    archivo_origen = seleccionar_archivo()
    
    if not archivo_origen:
        print("No se seleccionó ningún archivo. Operación cancelada.")
        return

    # Definir nombre de salida basado en el nombre original
    nombre_base = os.path.splitext(archivo_origen)[0]
    archivo_destino = f"{nombre_base}_formato_visualis.xlsx"

    print(f"\nProcesando: {os.path.basename(archivo_origen)}...")

    try:
        # 2. Leer el archivo (manejando líneas corruptas típicas de reportes CSV)
        df = pd.read_csv(archivo_origen, on_bad_lines='skip')

        # 3. Limpieza: quitar filas sin datos esenciales
        df = df.dropna(subset=['Account Description', 'Amount', 'Transaction Date'])

        # 4. Crear estructura para Visualis
        new_df = pd.DataFrame()

        new_df['fecha'] = df['Transaction Date']
        new_df['cuenta'] = df['Account Description']
        
        # Mapeo de ingresos y gastos
        new_df['tipo (ingreso o gasto)'] = df['Expense or Income'].map({1.0: 'Ingreso', -1.0: 'Gasto'}).fillna('Otro')
        
        new_df['categoría'] = df['Category Name']
        new_df['subcategoría'] = df['Subcategory Name']
        new_df['importe o monto'] = df['Amount']
        new_df['moneda'] = df['Currency symbol']
        
        # Combinar nombre y descripción para no perder info
        new_df['descripción'] = df['Transaction Name'].fillna(df['Transaction Description']).fillna('')

        # 5. Reordenar columnas
        columnas_ordenadas = [
            'fecha', 'cuenta', 'tipo (ingreso o gasto)', 'categoría', 
            'subcategoría', 'importe o monto', 'moneda', 'descripción'
        ]
        new_df = new_df[columnas_ordenadas]

        # 6. Guardar en Excel
        new_df.to_excel(archivo_destino, index=False)
        print(f"---")
        print(f"✅ ¡Éxito! Archivo guardado como:")
        print(f"👉 {archivo_destino}")

    except Exception as e:
        print(f"❌ Error durante la transformación: {e}")

if __name__ == "__main__":
    transformar_reporte()
    input("\nPresiona Enter para cerrar...") # Para que la ventana no se cierre de golpe
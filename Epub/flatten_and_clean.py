import os
import shutil
import argparse
import sys

def get_unique_destination_path(dest_folder, filename):
    """
    Si filename ya existe en dest_folder, genera un nombre como nombre_1.ext, nombre_2.ext, etc.
    """
    name, ext = os.path.splitext(filename)
    dest_path = os.path.join(dest_folder, filename)
    counter = 1
    while os.path.exists(dest_path):
        new_filename = f"{name}_{counter}{ext}"
        dest_path = os.path.join(dest_folder, new_filename)
        counter += 1
    return dest_path

def flatten_and_clean(folder_path, extension, dry_run=False):
    folder_path = os.path.abspath(folder_path)
    if not os.path.isdir(folder_path):
        raise ValueError(f"La ruta especificada no es una carpeta válida: {folder_path}")

    # Normalizar extensión: asegurarse de que comience por punto y esté en minúsculas
    if not extension.startswith('.'):
        extension = '.' + extension
    target_ext = extension.lower()

    print(f"\nProcesando carpeta: {folder_path}")
    print(f"Buscando archivos con extensión: {target_ext}")
    if dry_run:
        print("[MODO SIMULACIÓN - DRY RUN: No se realizarán cambios]")

    # 1. Encontrar todos los archivos objetivo dentro del árbol
    target_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            _, ext = os.path.splitext(file)
            if ext.lower() == target_ext:
                full_path = os.path.join(root, file)
                target_files.append(full_path)

    print(f"Total de archivos '{target_ext}' encontrados: {len(target_files)}")

    # 2. Mover/Copiar los archivos a la carpeta raíz de destino
    kept_files_in_root = set()

    for src_file in target_files:
        src_dir, filename = os.path.split(src_file)
        
        # Si el archivo ya está directamente en la carpeta raíz
        if os.path.samefile(src_dir, folder_path):
            kept_files_in_root.add(os.path.normcase(os.path.abspath(src_file)))
            continue

        # Si está en una subcarpeta, calcular ruta de destino evitando colisiones
        dest_file = get_unique_destination_path(folder_path, filename)
        print(f"  -> Moviendo a la raíz: {os.path.basename(src_file)} -> {os.path.basename(dest_file)}")
        
        if not dry_run:
            shutil.move(src_file, dest_file)
            kept_files_in_root.add(os.path.normcase(os.path.abspath(dest_file)))
        else:
            kept_files_in_root.add(os.path.normcase(os.path.abspath(dest_file)))

    # 3. Eliminar todo lo demás en la carpeta raíz (subcarpetas y otros archivos)
    print("\nLimpiando archivos no deseados y subcarpetas...")
    items = os.listdir(folder_path)
    deleted_files = 0
    deleted_dirs = 0

    for item in items:
        item_path = os.path.join(folder_path, item)
        norm_item_path = os.path.normcase(os.path.abspath(item_path))

        # Si es un directorio, eliminarlo por completo
        if os.path.isdir(item_path):
            print(f"  [X] Eliminando subcarpeta: {item}")
            deleted_dirs += 1
            if not dry_run:
                shutil.rmtree(item_path)
        else:
            # Si es un archivo pero no forma parte de los archivos conservados
            if norm_item_path not in kept_files_in_root:
                print(f"  [X] Eliminando archivo sobrante: {item}")
                deleted_files += 1
                if not dry_run:
                    os.remove(item_path)

    print(f"\n¡Completado!")
    print(f"- Archivos '{target_ext}' conservados: {len(kept_files_in_root)}")
    print(f"- Archivos no deseados eliminados: {deleted_files}")
    print(f"- Subcarpetas eliminadas: {deleted_dirs}")

def launch_gui():
    import tkinter as tk
    from tkinter import filedialog, messagebox

    root = tk.Tk()
    root.title("Aplanar y Limpiar Carpeta")
    root.geometry("520x260")
    root.resizable(False, False)

    folder_var = tk.StringVar()
    ext_var = tk.StringVar(value="epub")
    dry_run_var = tk.BooleanVar(value=False)

    def select_folder():
        chosen = filedialog.askdirectory(title="Seleccionar carpeta de trabajo")
        if chosen:
            folder_var.set(chosen)

    def run_process():
        folder = folder_var.get().strip()
        ext = ext_var.get().strip()
        is_dry = dry_run_var.get()

        if not folder:
            messagebox.showwarning("Atención", "Por favor selecciona una carpeta.")
            return
        if not ext:
            messagebox.showwarning("Atención", "Por favor especifica la extensión (ej. epub, pdf, txt).")
            return

        if not is_dry:
            confirm = messagebox.askyesno(
                "Confirmación de Borrado",
                f"¿Estás seguro?\n\nSe moverán todos los archivos .{ext.lstrip('.')} a la carpeta principal y SE BORRARÁ todo lo demás (subcarpetas y otros archivos).\n\nEsta acción no se puede deshacer.",
                icon="warning"
            )
            if not confirm:
                return

        try:
            flatten_and_clean(folder, ext, dry_run=is_dry)
            msg = "Proceso completado con éxito."
            if is_dry:
                msg += "\n(Modo simulación: no se aplicaron cambios reales. Revisa la consola)."
            messagebox.showinfo("Listo", msg)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error:\n{str(e)}")

    # UI Layout
    frame = tk.Frame(root, padx=15, pady=15)
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Carpeta de trabajo:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 2))
    entry_folder = tk.Entry(frame, textvariable=folder_var, width=42)
    entry_folder.grid(row=1, column=0, padx=(0, 5), pady=(0, 10))
    btn_browse = tk.Button(frame, text="Examinar...", command=select_folder)
    btn_browse.grid(row=1, column=1, pady=(0, 10))

    tk.Label(frame, text="Extensión de archivo (ej. epub, pdf, jpg):", font=("Segoe UI", 9, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 2))
    entry_ext = tk.Entry(frame, textvariable=ext_var, width=15)
    entry_ext.grid(row=3, column=0, sticky="w", pady=(0, 10))

    chk_dry = tk.Checkbutton(frame, text="Modo simulación (Dry Run: no borra ni mueve nada)", variable=dry_run_var)
    chk_dry.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 15))

    btn_start = tk.Button(frame, text="Iniciar proceso", bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5, command=run_process)
    btn_start.grid(row=5, column=0, columnspan=2)

    root.mainloop()

def main():
    parser = argparse.ArgumentParser(
        description="Aplana una carpeta extrayendo archivos de una extensión específica y elimina todo lo demás."
    )
    parser.add_argument("-f", "--folder", help="Ruta de la carpeta principal")
    parser.add_argument("-e", "--ext", help="Extensión de archivos a conservar (ej. epub, pdf, cbr)")
    parser.add_argument("--dry-run", action="store_true", help="Simula el proceso sin mover ni borrar archivos")
    parser.add_argument("--gui", action="store_true", help="Abre la interfaz gráfica")

    args = parser.parse_args()

    # Si se pasan argumentos por línea de comandos
    if args.folder and args.ext:
        flatten_and_clean(args.folder, args.ext, dry_run=args.dry_run)
    elif args.gui or len(sys.argv) == 1:
        # Por defecto abre GUI si se ejecuta sin argumentos o con --gui
        launch_gui()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

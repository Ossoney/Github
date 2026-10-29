import os
import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from renamer import (
    VIDEO_EXTENSIONS,
    parse_filename,
    fetch_episode_titles,
    generate_new_name,
)

class SeriesRenameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Renombrador de Series de TV")
        self.geometry("950x600")
        self.minsize(800, 450)

        self.current_folder: Path = None
        self.files_data = []  # list of dicts: {path, old_name, new_name, status}

        self._init_ui()

    def _init_ui(self):
        # Top Frame - Folder & Settings
        top_frame = ttk.Frame(self, padding="10")
        top_frame.pack(fill=tk.X)

        # Folder selection
        lbl_folder = ttk.Label(top_frame, text="Carpeta:")
        lbl_folder.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)

        self.ent_folder = ttk.Entry(top_frame, width=50)
        self.ent_folder.grid(row=0, column=1, sticky=tk.EW, padx=5, pady=5)

        btn_browse = ttk.Button(top_frame, text="Examinar...", command=self.on_browse)
        btn_browse.grid(row=0, column=2, padx=5, pady=5)

        # Show name override
        lbl_show = ttk.Label(top_frame, text="Nombre Serie (opcional):")
        lbl_show.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        self.ent_show = ttk.Entry(top_frame, width=30)
        self.ent_show.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)

        # Option: Fetch episode titles from Internet
        self.var_fetch_titles = tk.BooleanVar(value=True)
        chk_titles = ttk.Checkbutton(
            top_frame, 
            text="Buscar títulos de capítulos en Internet (TVmaze)", 
            variable=self.var_fetch_titles
        )
        chk_titles.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Analyze button
        self.btn_analyze = ttk.Button(top_frame, text="🔍 Analizar y Previsualizar", command=self.on_analyze)
        self.btn_analyze.grid(row=2, column=2, padx=5, pady=5)

        top_frame.columnconfigure(1, weight=1)

        # Middle Frame - Treeview Table
        mid_frame = ttk.Frame(self, padding="10")
        mid_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("old", "arrow", "new", "status")
        self.tree = ttk.Treeview(mid_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("old", text="Nombre Actual")
        self.tree.heading("arrow", text="➔")
        self.tree.heading("new", text="Nombre Propuesto")
        self.tree.heading("status", text="Estado")

        self.tree.column("old", width=380, anchor=tk.W)
        self.tree.column("arrow", width=30, anchor=tk.CENTER)
        self.tree.column("new", width=380, anchor=tk.W)
        self.tree.column("status", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(mid_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom Frame - Action buttons & Status
        bot_frame = ttk.Frame(self, padding="10")
        bot_frame.pack(fill=tk.X)

        self.lbl_status = ttk.Label(bot_frame, text="Listo. Selecciona una carpeta de serie.", foreground="gray")
        self.lbl_status.pack(side=tk.LEFT, padx=5)

        self.btn_rename = ttk.Button(bot_frame, text="✏️ Renombrar Archivos", command=self.on_rename, state=tk.DISABLED)
        self.btn_rename.pack(side=tk.RIGHT, padx=5)

    def on_browse(self):
        folder = filedialog.askdirectory(title="Selecciona la carpeta de la serie")
        if folder:
            self.ent_folder.delete(0, tk.END)
            self.ent_folder.insert(0, folder)
            self.current_folder = Path(folder)
            # Default show name from folder
            self.ent_show.delete(0, tk.END)
            self.ent_show.insert(0, self.current_folder.name.title())
            self.on_analyze()

    def on_analyze(self):
        folder_str = self.ent_folder.get().strip()
        if not folder_str:
            messagebox.showwarning("Atención", "Por favor introduce o selecciona una carpeta.")
            return

        folder = Path(folder_str)
        if not folder.exists() or not folder.is_dir():
            messagebox.showerror("Error", "La carpeta indicada no existe.")
            return

        self.current_folder = folder
        show_override = self.ent_show.get().strip()
        fetch_titles = self.var_fetch_titles.get()

        # Disable buttons while analyzing
        self.btn_analyze.config(state=tk.DISABLED)
        self.btn_rename.config(state=tk.DISABLED)
        self.lbl_status.config(text="Analizando archivos y consultando títulos...", foreground="blue")
        self.tree.delete(*self.tree.get_children())

        # Run in thread so GUI doesn't freeze during network requests
        thread = threading.Thread(
            target=self._analyze_worker, 
            args=(folder, show_override, fetch_titles),
            daemon=True
        )
        thread.start()

    def _analyze_worker(self, folder: Path, show_override: str, fetch_titles: bool):
        files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTENSIONS]
        files.sort(key=lambda x: x.name)

        self.files_data = []
        for file in files:
            new_name = generate_new_name(file, show_override=show_override, fetch_titles=fetch_titles)
            if new_name:
                status = "Pendiente" if new_name != file.name else "Sin cambios"
            else:
                new_name = file.name
                status = "Ignorado"

            self.files_data.append({
                "path": file,
                "old_name": file.name,
                "new_name": new_name,
                "status": status
            })

        self.after(0, self._update_tree_after_analysis)

    def _update_tree_after_analysis(self):
        for item in self.files_data:
            self.tree.insert("", tk.END, values=(item["old_name"], "➔", item["new_name"], item["status"]))

        valid_count = sum(1 for item in self.files_data if item["status"] == "Pendiente")
        self.btn_analyze.config(state=tk.NORMAL)
        if valid_count > 0:
            self.btn_rename.config(state=tk.NORMAL)
            self.lbl_status.config(
                text=f"{len(self.files_data)} archivos encontrados. {valid_count} listos para renombrar.",
                foreground="green"
            )
        else:
            self.btn_rename.config(state=tk.DISABLED)
            self.lbl_status.config(
                text=f"{len(self.files_data)} archivos analizados. No hay cambios pendientes.",
                foreground="gray"
            )

    def on_rename(self):
        pending = [item for item in self.files_data if item["status"] == "Pendiente"]
        if not pending:
            return

        confirm = messagebox.askyesno(
            "Confirmar renombrado",
            f"¿Estás seguro de que deseas renombrar {len(pending)} archivos en:\n{self.current_folder}?"
        )
        if not confirm:
            return

        success_count = 0
        error_count = 0

        for item in self.files_data:
            if item["status"] == "Pendiente":
                old_path = item["path"]
                new_path = old_path.parent / item["new_name"]
                try:
                    old_path.rename(new_path)
                    item["path"] = new_path
                    item["old_name"] = item["new_name"]
                    item["status"] = "Completado"
                    success_count += 1
                except Exception as ex:
                    item["status"] = f"Error: {ex}"
                    error_count += 1

        # Refresh tree
        self.tree.delete(*self.tree.get_children())
        for item in self.files_data:
            self.tree.insert("", tk.END, values=(item["old_name"], "➔", item["new_name"], item["status"]))

        self.btn_rename.config(state=tk.DISABLED)
        if error_count == 0:
            messagebox.showinfo("Éxito", f"Se han renombrado {success_count} archivos correctamente.")
            self.lbl_status.config(text=f"¡Completado! {success_count} archivos renombrados.", foreground="green")
        else:
            messagebox.showwarning("Aviso", f"Renombrados: {success_count}. Errores: {error_count}.")
            self.lbl_status.config(text=f"Completado con {error_count} errores.", foreground="red")

if __name__ == "__main__":
    app = SeriesRenameApp()
    # If a path was passed via args, set it
    if len(sys.argv) > 1 and os.path.isdir(sys.argv[1]):
        app.ent_folder.insert(0, sys.argv[1])
        app.current_folder = Path(sys.argv[1])
        app.ent_show.insert(0, app.current_folder.name.title())
        app.on_analyze()
    app.mainloop()

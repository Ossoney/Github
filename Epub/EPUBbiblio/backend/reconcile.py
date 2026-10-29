import os
import time
import logging
import threading
from database import SessionLocal, Book, Library, BookLibrary
from epub_parser import extract_metadata
from classify_thematic_libraries import classify_book, extract_subjects_from_epub

reconciliation_state = {
    "running": False,
    "last_sync": None,
    "deleted_count": 0,
    "added_count": 0,
    "total_checked": 0,
    "current_status": "Inactivo"
}

_reconciliation_lock = threading.Lock()

def reconcile_libraries_task():
    """
    Conciliación rápida en segundo plano:
    1. Escanea las rutas físicas reales de las bibliotecas con disco.
    2. Compara con la base de datos en memoria (operación O(1)).
    3. Si hay libros eliminados del disco, los purga con sus dependencias.
    4. Si hay libros nuevos en disco, los procesa e indexa en segundo plano.
    """
    global reconciliation_state
    if not _reconciliation_lock.acquire(blocking=False):
        logging.info("Reconciliación omitida: ya hay una tarea en curso.")
        return

    try:
        reconciliation_state["running"] = True
        reconciliation_state["current_status"] = "Explorando disco y base de datos..."
        t0 = time.time()
        logging.info("Iniciando reconciliación automática de bibliotecas en segundo plano...")

        db = SessionLocal()
        try:
            # Obtener bibliotecas que tienen ruta física real
            physical_libs = db.query(Library).filter(Library.path != None, Library.path != "").all()
            if not physical_libs:
                logging.info("Reconciliación: no hay bibliotecas con ruta física configurada.")
                return

            lib_map = {l.name: l.id for l in db.query(Library).all()}

            # 1. Explorar archivos reales en disco
            disk_map = {}  # {normalized_path: (real_path, library_id)}
            for lib in physical_libs:
                if not os.path.exists(lib.path):
                    logging.warning(f"Reconciliación: la ruta {lib.path} no existe actualmente.")
                    continue
                lib_type = (lib.library_type or "all").lower()
                if lib_type == "pdf":
                    allowed = (".pdf",)
                elif lib_type == "epub":
                    allowed = (".epub",)
                else:
                    allowed = (".epub", ".pdf")

                for root, dirs, files in os.walk(lib.path):
                    for f in files:
                        ext = os.path.splitext(f)[1].lower()
                        if ext in allowed:
                            full_path = os.path.abspath(os.path.join(root, f))
                            norm = os.path.normcase(full_path)
                            if norm not in disk_map:
                                disk_map[norm] = (full_path, lib.id)

            # 2. Consultar registros actuales en base de datos
            db_records = db.query(Book.id, Book.file_path).all()
            db_map = {os.path.normcase(os.path.abspath(r[1])): (r[0], r[1]) for r in db_records if r[1]}

            reconciliation_state["total_checked"] = len(disk_map)

            # 3. Detectar diferencias
            disk_keys = set(disk_map.keys())
            db_keys = set(db_map.keys())

            deleted_keys = db_keys - disk_keys
            new_keys = disk_keys - db_keys

            logging.info(f"Reconciliación: {len(deleted_keys)} borrados en disco, {len(new_keys)} nuevos por incorporar.")

            # 4. Purgar eliminados
            deleted_count = 0
            if deleted_keys:
                reconciliation_state["current_status"] = f"Purgando {len(deleted_keys)} libros eliminados..."
                deleted_ids = [db_map[k][0] for k in deleted_keys]
                chunk_size = 500
                for i in range(0, len(deleted_ids), chunk_size):
                    chunk = deleted_ids[i:i + chunk_size]
                    books_to_del = db.query(Book).filter(Book.id.in_(chunk)).all()
                    for b in books_to_del:
                        db.delete(b)
                    db.commit()
                    deleted_count += len(chunk)
                logging.info(f"Reconciliación: se purgaron {deleted_count} libros inexistentes.")

            # 5. Incorporar libros nuevos
            added_count = 0
            if new_keys:
                reconciliation_state["current_status"] = f"Incorporando {len(new_keys)} libros nuevos..."
                batch_size = 50
                for k in new_keys:
                    real_path, lib_id = disk_map[k]
                    try:
                        metadata = extract_metadata(real_path)
                        if metadata:
                            new_book = Book(**metadata, library_id=lib_id)
                            db.add(new_book)
                            db.flush()

                            # Asociar a la biblioteca física y a la principal (id=1)
                            db.add(BookLibrary(book_id=new_book.id, library_id=lib_id))
                            if lib_id != 1:
                                db.add(BookLibrary(book_id=new_book.id, library_id=1))

                            # Auto-clasificación temática
                            try:
                                tags = extract_subjects_from_epub(real_path)
                                if tags:
                                    new_book.tags = ", ".join(tags)
                                categories = classify_book(tags, new_book.title, new_book.description)
                                for cat_name in categories:
                                    cat_id = lib_map.get(cat_name)
                                    if cat_id:
                                        db.add(BookLibrary(book_id=new_book.id, library_id=cat_id))
                            except Exception:
                                pass

                            added_count += 1
                            if added_count % batch_size == 0:
                                db.commit()
                                reconciliation_state["current_status"] = f"Incorporando libros ({added_count}/{len(new_keys)})..."
                    except Exception as e:
                        logging.warning(f"Error procesando nuevo libro {real_path}: {e}")

                db.commit()
                logging.info(f"Reconciliación: se añadieron {added_count} libros nuevos al catálogo.")

            elapsed = time.time() - t0
            reconciliation_state["deleted_count"] = deleted_count
            reconciliation_state["added_count"] = added_count
            reconciliation_state["last_sync"] = time.strftime("%Y-%m-%d %H:%M:%S")
            reconciliation_state["current_status"] = "Completado"
            logging.info(f"Reconciliación finalizada en {elapsed:.2f} s. (Borrados: {deleted_count}, Añadidos: {added_count})")

        except Exception as e:
            logging.error(f"Error crítico durante la reconciliación: {e}")
            db.rollback()
            reconciliation_state["current_status"] = f"Error: {e}"
        finally:
            db.close()
    finally:
        reconciliation_state["running"] = False
        _reconciliation_lock.release()

def start_reconciliation_thread():
    """Lanza la reconciliación en un hilo daemon para que nunca bloquee el servidor ni la web."""
    t = threading.Thread(target=reconcile_libraries_task, daemon=True, name="ReconcileThread")
    t.start()
    return t

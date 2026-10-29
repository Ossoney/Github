import os
import json
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = os.path.join(BASE_DIR, "data", "pdf_cache.db")

class CacheDB:
    def __init__(self, db_path=DB_FILE):
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path, timeout=10.0)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pdf_cache (
                    filepath TEXT PRIMARY KEY,
                    mtime REAL,
                    filesize INTEGER,
                    pages INTEGER,
                    title TEXT,
                    author TEXT,
                    isbns TEXT,
                    dois TEXT,
                    shingles TEXT,
                    is_scanned INTEGER
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_filesize ON pdf_cache(filesize)")
            conn.commit()

    def get_cached(self, filepath, mtime, filesize):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT pages, title, author, isbns, dois, shingles, is_scanned
                FROM pdf_cache
                WHERE filepath = ? AND mtime = ? AND filesize = ?
            """, (str(filepath), mtime, filesize))
            row = cur.fetchone()
            if row:
                return {
                    'pages': row[0],
                    'title': row[1],
                    'author': row[2],
                    'isbns': set(json.loads(row[3])) if row[3] else set(),
                    'dois': set(json.loads(row[4])) if row[4] else set(),
                    'shingles': set(json.loads(row[5])) if row[5] else set(),
                    'is_scanned': bool(row[6])
                }
        return None

    def save_cached_batch(self, items):
        if not items:
            return
        with self._get_connection() as conn:
            conn.executemany("""
                INSERT OR REPLACE INTO pdf_cache
                (filepath, mtime, filesize, pages, title, author, isbns, dois, shingles, is_scanned)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    str(it['filepath']),
                    it['mtime'],
                    it['filesize'],
                    it['pages'],
                    it['title'],
                    it['author'],
                    json.dumps(list(it['isbns'])),
                    json.dumps(list(it['dois'])),
                    json.dumps(list(it['shingles'])),
                    1 if it.get('is_scanned') else 0
                )
                for it in items
            ])
            conn.commit()

cache_db = CacheDB()

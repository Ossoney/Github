from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, Float, String, Text, DateTime, ForeignKey, 
    UniqueConstraint, event, text
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from paths import DB_PATH

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH.replace('\\', '/')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

import unicodedata
import re

def normalize_for_search(text):
    if not text:
        return ""
    # Quitar acentos, diacríticos y normalizar a minúsculas
    text = unicodedata.normalize('NFKD', str(text))
    text = ''.join(c for c in text if not unicodedata.combining(c))
    # Convertir guiones, puntos y signos en espacios para igualar búsquedas compuestas
    text = re.sub(r'[-_.,;:!?\'"()\[\]{}/\\+*~`^]', ' ', text)
    return ' '.join(text.lower().split())

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    dbapi_connection.create_function("NORM_SEARCH", 1, normalize_for_search)
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Library(Base):
    __tablename__ = "libraries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    path = Column(String, nullable=True)
    library_type = Column(String, default="all", nullable=True)  # "all", "epub", "pdf"
    created_at = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="library", cascade="all, delete-orphan")
    user_access = relationship("UserLibrary", back_populates="library", cascade="all, delete-orphan")
    book_links = relationship("BookLibrary", back_populates="library", cascade="all, delete-orphan")

class UserLibrary(Base):
    __tablename__ = "user_libraries"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), primary_key=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="libraries")
    library = relationship("Library", back_populates="user_access")

class BookLibrary(Base):
    __tablename__ = "book_libraries"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False, index=True)

    __table_args__ = (UniqueConstraint('book_id', 'library_id', name='_book_library_uc'),)

    book = relationship("Book", back_populates="libraries")
    library = relationship("Library", back_populates="book_links")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String)
    cover_path = Column(String)
    file_path = Column(String, index=True)
    format = Column(String, default="epub", nullable=True)  # "epub", "pdf"
    progress = Column(String)  # Mantenido por compatibilidad histórica
    tags = Column(String, default="", nullable=True)  # Géneros y etiquetas detectadas
    isbn = Column(String, index=True, default="", nullable=True)  # Código ISBN para búsquedas exactas
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="SET NULL"), nullable=True, index=True)
    external_rating = Column(Float, default=0.0, nullable=True)
    external_reviews_count = Column(Integer, default=0, nullable=True)
    external_rating_synced = Column(Integer, default=0, nullable=True)

    library = relationship("Library", back_populates="books")
    libraries = relationship("BookLibrary", back_populates="book", cascade="all, delete-orphan")
    reviews = relationship("BookReview", back_populates="book", cascade="all, delete-orphan")
    reports = relationship("BookReport", back_populates="book", cascade="all, delete-orphan")
    reading_progress = relationship("UserProgress", back_populates="book", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="reader")  # "master" | "reader"
    status = Column(String, default="pending")  # "pending" | "active" | "rejected"
    daily_download_limit = Column(Integer, default=1, nullable=True)  # Límite diario configurable (None = Ilimitado)
    created_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    reading_progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("BookReview", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("BookReport", back_populates="user", cascade="all, delete-orphan")
    libraries = relationship("UserLibrary", back_populates="user", cascade="all, delete-orphan")
    downloads = relationship("UserDownload", back_populates="user", cascade="all, delete-orphan")

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="sessions")

class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    progress = Column(String, nullable=False)
    percentage = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='_user_book_progress_uc'),)

    user = relationship("User", back_populates="reading_progress")
    book = relationship("Book", back_populates="reading_progress")

class BookReview(Base):
    __tablename__ = "book_reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1 a 5
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'book_id', name='_user_book_review_uc'),)

    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")

class BookReport(Base):
    """Incidencias reportadas por lectores desde el modal de Valorar."""
    __tablename__ = "book_reports"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    report_type = Column(String, default="other", nullable=False)  # 'wrong_genre' | 'other'
    message = Column(Text, nullable=False)
    status = Column(String, default="pending", nullable=False)     # 'pending' | 'reviewed'
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="reports")
    user = relationship("User", back_populates="reports")

class UserDownload(Base):
    """Registro histórico de descargas directas de libros por usuario."""
    __tablename__ = "user_downloads"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False, index=True)
    downloaded_at = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="downloads")
    book = relationship("Book")

# Crear tablas nuevas
Base.metadata.create_all(bind=engine)

def migrate_database():
    """Migración transparente para incorporar library_id, tags, book_libraries y bibliotecas temáticas."""
    with engine.connect() as conn:
        result = conn.execute(text("PRAGMA table_info(books)"))
        columns = [row[1] for row in result.fetchall()]
        if "library_id" not in columns:
            conn.execute(text("ALTER TABLE books ADD COLUMN library_id INTEGER REFERENCES libraries(id)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_books_library_id ON books(library_id)"))
            conn.commit()

        if "tags" not in columns:
            conn.execute(text("ALTER TABLE books ADD COLUMN tags TEXT DEFAULT ''"))
            conn.commit()

        if "isbn" not in columns:
            conn.execute(text("ALTER TABLE books ADD COLUMN isbn TEXT DEFAULT ''"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS ix_books_isbn ON books(isbn)"))
            conn.commit()

        if "format" not in columns:
            conn.execute(text("ALTER TABLE books ADD COLUMN format TEXT DEFAULT 'epub'"))
            conn.execute(text("UPDATE books SET format = 'epub' WHERE format IS NULL"))
            conn.commit()

        # Migración tabla libraries: library_type
        lib_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(libraries)")).fetchall()]
        if "library_type" not in lib_cols:
            conn.execute(text("ALTER TABLE libraries ADD COLUMN library_type TEXT DEFAULT 'all'"))
            conn.commit()

        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_books_external_rating ON books(external_rating)"))
        conn.commit()

        # Migración tabla users: daily_download_limit (y transición desde weekly_download_limit)
        user_cols = [row[1] for row in conn.execute(text("PRAGMA table_info(users)")).fetchall()]
        if "daily_download_limit" not in user_cols:
            conn.execute(text("ALTER TABLE users ADD COLUMN daily_download_limit INTEGER DEFAULT 1"))
            conn.commit()
            if "weekly_download_limit" in user_cols:
                # Si existía weekly_download_limit y era None (ilimitado), mantenerlo ilimitado; de lo contrario por defecto 1 al día
                conn.execute(text("UPDATE users SET daily_download_limit = CASE WHEN weekly_download_limit IS NULL THEN NULL ELSE 1 END"))
                conn.commit()

        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS book_libraries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL REFERENCES books(id) ON DELETE CASCADE,
                library_id INTEGER NOT NULL REFERENCES libraries(id) ON DELETE CASCADE,
                UNIQUE(book_id, library_id)
            )
        """))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_book_libraries_book_id ON book_libraries(book_id)"))
        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_book_libraries_library_id ON book_libraries(library_id)"))
        conn.commit()

        # Poblar book_libraries inicial si está vacía
        bl_count = conn.execute(text("SELECT count(*) FROM book_libraries")).scalar() or 0
        if bl_count == 0:
            conn.execute(text("""
                INSERT OR IGNORE INTO book_libraries (book_id, library_id)
                SELECT id, library_id FROM books WHERE library_id IS NOT NULL
            """))
            conn.commit()

        # FTS5: Tabla virtual de búsqueda ultra-rápida y triggers de sincronización
        conn.execute(text("""
            CREATE VIRTUAL TABLE IF NOT EXISTS books_fts USING fts5(
                title, author, content=books, content_rowid=id,
                tokenize='unicode61 remove_diacritics 2'
            )
        """))
        fts_count = conn.execute(text("SELECT count(*) FROM books_fts")).scalar() or 0
        books_count = conn.execute(text("SELECT count(*) FROM books")).scalar() or 0
        if fts_count < books_count:
            conn.execute(text("INSERT OR IGNORE INTO books_fts(rowid, title, author) SELECT id, title, author FROM books"))
            conn.commit()

        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS books_ai AFTER INSERT ON books BEGIN
                INSERT INTO books_fts(rowid, title, author) VALUES (new.id, new.title, new.author);
            END;
        """))
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS books_ad AFTER DELETE ON books BEGIN
                INSERT INTO books_fts(books_fts, rowid, title, author) VALUES('delete', old.id, old.title, old.author);
            END;
        """))
        conn.execute(text("""
            CREATE TRIGGER IF NOT EXISTS books_au AFTER UPDATE ON books BEGIN
                INSERT INTO books_fts(books_fts, rowid, title, author) VALUES('delete', old.id, old.title, old.author);
                INSERT INTO books_fts(rowid, title, author) VALUES (new.id, new.title, new.author);
            END;
        """))
        conn.commit()

    db = SessionLocal()
    try:
        main_lib = db.query(Library).filter(Library.id == 1).first()
        if not main_lib:
            main_lib = Library(id=1, name="Biblioteca Principal", path="")
            db.add(main_lib)
            db.commit()
            db.refresh(main_lib)

        # Asignar libros huérfanos a la Biblioteca Principal (id=1)
        db.execute(text("UPDATE books SET library_id = 1 WHERE library_id IS NULL"))
        db.commit()

        # Renombrar Biblioteca 2 a "⭐ Ciencia Ficción (VIP)" si conserva un nombre anterior
        lib2 = db.query(Library).filter(Library.id == 2).first()
        if lib2 and lib2.name != "⭐ Ciencia Ficción (VIP)":
            lib2.name = "⭐ Ciencia Ficción (VIP)"
            db.commit()
    finally:
        db.close()

# Ejecutar migración automática
migrate_database()

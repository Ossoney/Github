from sqlalchemy import create_engine, Column, Integer, String, event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from paths import DB_PATH

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH.replace('\\', '/')}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.close()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String)
    cover_path = Column(String)
    file_path = Column(String, index=True)
    progress = Column(String) # Almacena el CFI de la última posición leída

Base.metadata.create_all(bind=engine)

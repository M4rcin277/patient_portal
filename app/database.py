import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None


if load_dotenv:
    load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./patient_portal.db")


def pobierz_argumenty_polaczenia(database_url: str):
    if database_url.startswith("sqlite"):
        return {"check_same_thread": False}

    return {}

engine = create_engine(
    DATABASE_URL,
    connect_args=pobierz_argumenty_polaczenia(DATABASE_URL),
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def utworz_tabele():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

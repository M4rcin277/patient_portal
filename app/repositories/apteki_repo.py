from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.apteka import Apteka


def zamien_apteke_na_slownik(apteka: Apteka):
    return {
        "id": apteka.id,
        "nazwa": apteka.nazwa,
        "adres": apteka.adres,
        "godziny": apteka.godziny,
    }


def pobierz_apteki(db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        apteki = db.scalars(select(Apteka).order_by(Apteka.id)).all()
        return [zamien_apteke_na_slownik(apteka) for apteka in apteki]
    finally:
        if czy_zamknac_db:
            db.close()

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.placowka import Placowka


def zamien_placowke_na_slownik(placowka: Placowka):
    return {
        "id": placowka.id,
        "nazwa": placowka.nazwa,
        "miasto": placowka.miasto,
        "adres": placowka.adres,
        "telefon": placowka.telefon,
    }


def pobierz_placowki(db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        placowki = db.scalars(select(Placowka).order_by(Placowka.nazwa)).all()
        return [zamien_placowke_na_slownik(placowka) for placowka in placowki]
    finally:
        if czy_zamknac_db:
            db.close()

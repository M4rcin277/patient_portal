from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.lekarz import Lekarz


def zamien_lekarza_na_slownik(lekarz: Lekarz):
    return {
        "id": lekarz.id,
        "imie": lekarz.imie,
        "nazwisko": lekarz.nazwisko,
        "specjalizacja": lekarz.specjalizacja,
        "miasto": lekarz.miasto,
        "lokalizacja": lekarz.lokalizacja,
        "tryb_wizyty": lekarz.tryb_wizyty,
    }


def pobierz_wszystkich_lekarzy(db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        lekarze = db.scalars(select(Lekarz).order_by(Lekarz.id)).all()
        return [zamien_lekarza_na_slownik(lekarz) for lekarz in lekarze]
    finally:
        if czy_zamknac_db:
            db.close()


def znajdz_lekarza(lekarz_id: int, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        lekarz = db.get(Lekarz, lekarz_id)

        if lekarz:
            return zamien_lekarza_na_slownik(lekarz)
    finally:
        if czy_zamknac_db:
            db.close()

    return None

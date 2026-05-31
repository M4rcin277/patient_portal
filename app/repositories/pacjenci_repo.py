from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.pacjent import Pacjent


def zamien_pacjenta_na_slownik(pacjent: Pacjent):
    return {
        "id": pacjent.id,
        "imie": pacjent.imie,
        "nazwisko": pacjent.nazwisko,
        "email": pacjent.email,
        "telefon": pacjent.telefon,
        "data_urodzenia": pacjent.data_urodzenia.isoformat()
        if pacjent.data_urodzenia
        else None,
        "adres": pacjent.adres,
    }


def znajdz_pacjenta(pacjent_id: int, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        pacjent = db.get(Pacjent, pacjent_id)

        if pacjent:
            return zamien_pacjenta_na_slownik(pacjent)
    finally:
        if czy_zamknac_db:
            db.close()

    return None

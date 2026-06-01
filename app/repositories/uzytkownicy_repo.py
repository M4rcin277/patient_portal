from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.uzytkownik import Uzytkownik
from app.services.auth import zahashuj_haslo


def zamien_uzytkownika_na_slownik(uzytkownik: Uzytkownik):
    return {
        "id": uzytkownik.id,
        "email": uzytkownik.email,
        "haslo_hash": uzytkownik.haslo_hash,
        "rola": uzytkownik.rola,
        "pacjent_id": uzytkownik.pacjent_id,
        "lekarz_id": uzytkownik.lekarz_id,
    }


def znajdz_uzytkownika_po_emailu(email: str, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = select(Uzytkownik).where(Uzytkownik.email == email.lower())
        uzytkownik = db.scalar(zapytanie)

        if uzytkownik:
            return zamien_uzytkownika_na_slownik(uzytkownik)
    finally:
        if czy_zamknac_db:
            db.close()

    return None


def dodaj_uzytkownika_pacjenta(
    email: str,
    haslo: str,
    pacjent_id: int,
    db: Session | None = None,
):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        uzytkownik = Uzytkownik(
            email=email.lower(),
            haslo_hash=zahashuj_haslo(haslo),
            rola="pacjent",
            pacjent_id=pacjent_id,
            lekarz_id=None,
        )

        db.add(uzytkownik)
        db.commit()
        db.refresh(uzytkownik)

        return zamien_uzytkownika_na_slownik(uzytkownik)
    finally:
        if czy_zamknac_db:
            db.close()

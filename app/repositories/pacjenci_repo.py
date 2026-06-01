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
        "grupa_krwi": pacjent.grupa_krwi,
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


def znajdz_pacjenta_po_emailu(email: str, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        pacjent = db.query(Pacjent).filter(Pacjent.email == email.lower()).first()

        if pacjent:
            return zamien_pacjenta_na_slownik(pacjent)
    finally:
        if czy_zamknac_db:
            db.close()

    return None


def dodaj_pacjenta(
    imie: str,
    nazwisko: str,
    email: str,
    telefon: str,
    data_urodzenia,
    adres: str | None,
    grupa_krwi: str | None = None,
    db: Session | None = None,
):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        pacjent = Pacjent(
            imie=imie,
            nazwisko=nazwisko,
            email=email.lower(),
            telefon=telefon,
            data_urodzenia=data_urodzenia,
            adres=adres,
            grupa_krwi=grupa_krwi,
        )

        db.add(pacjent)
        db.commit()
        db.refresh(pacjent)

        return zamien_pacjenta_na_slownik(pacjent)
    finally:
        if czy_zamknac_db:
            db.close()


def zaktualizuj_pacjenta(
    pacjent_id: int,
    imie: str,
    nazwisko: str,
    telefon: str,
    data_urodzenia,
    adres: str | None,
    grupa_krwi: str | None,
    db: Session | None = None,
):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        pacjent = db.get(Pacjent, pacjent_id)

        if pacjent is None:
            return None

        pacjent.imie = imie
        pacjent.nazwisko = nazwisko
        pacjent.telefon = telefon
        pacjent.data_urodzenia = data_urodzenia
        pacjent.adres = adres
        pacjent.grupa_krwi = grupa_krwi
        db.commit()
        db.refresh(pacjent)

        return zamien_pacjenta_na_slownik(pacjent)
    finally:
        if czy_zamknac_db:
            db.close()

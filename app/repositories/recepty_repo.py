from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.lekarz import Lekarz
from app.models.recepta import Recepta
from app.models.recepta_lek import ReceptaLek


KOLORY_RECEPT = ["purple", "green", "blue", "yellow", "violet"]
IKONY_RECEPT = [
    "bi-capsule",
    "bi-capsule",
    "bi-prescription2",
    "bi-file-earmark-medical",
    "bi-eyedropper",
]


def formatuj_date(data: date):
    return data.strftime("%d.%m.%Y")


def formatuj_liczbe_dni(data_waznosci: date):
    liczba_dni = (data_waznosci - date.today()).days

    if liczba_dni < 0:
        return "wygasła"
    if liczba_dni == 1:
        return "1 dzień"

    return f"{liczba_dni} dni"


def policz_leki_recepty(db: Session, recepta_id: int):
    zapytanie = select(ReceptaLek).where(ReceptaLek.recepta_id == recepta_id)

    return len(db.scalars(zapytanie).all())


def pobierz_recepty_pacjenta(pacjent_id: int, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = (
            select(Recepta)
            .where(Recepta.pacjent_id == pacjent_id)
            .order_by(Recepta.wazna_do)
        )
        recepty = db.scalars(zapytanie).all()
        wynik = []

        for indeks, recepta in enumerate(recepty):
            lekarz = db.get(Lekarz, recepta.lekarz_id) if recepta.lekarz_id else None
            wynik.append(
                {
                    "id": recepta.id,
                    "lekarz": (
                        f"{lekarz.imie} {lekarz.nazwisko}" if lekarz else "Nieznany"
                    ),
                    "wystawiono": formatuj_date(recepta.wystawiono),
                    "wazna_do": formatuj_date(recepta.wazna_do),
                    "dni": formatuj_liczbe_dni(recepta.wazna_do),
                    "liczba_lekow": policz_leki_recepty(db, recepta.id),
                    "kolor": KOLORY_RECEPT[indeks % len(KOLORY_RECEPT)],
                    "ikona": IKONY_RECEPT[indeks % len(IKONY_RECEPT)],
                }
            )

        return wynik
    finally:
        if czy_zamknac_db:
            db.close()

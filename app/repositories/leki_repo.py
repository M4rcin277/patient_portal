from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.lek import Lek
from app.models.lekarz import Lekarz
from app.models.pacjent_lek import PacjentLek


def pobierz_leki_pacjenta(pacjent_id: int, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = (
            select(PacjentLek)
            .where(PacjentLek.pacjent_id == pacjent_id)
            .order_by(PacjentLek.id)
        )
        przypisane_leki = db.scalars(zapytanie).all()
        wynik = []

        for przypisany_lek in przypisane_leki:
            lek = db.get(Lek, przypisany_lek.lek_id)
            lekarz = (
                db.get(Lekarz, przypisany_lek.lekarz_id)
                if przypisany_lek.lekarz_id
                else None
            )
            wynik.append(
                {
                    "id": przypisany_lek.id,
                    "nazwa": lek.nazwa if lek else "Nieznany lek",
                    "substancja": lek.substancja if lek else "",
                    "dawkowanie": przypisany_lek.dawkowanie,
                    "zalecenie": przypisany_lek.zalecenie,
                    "lekarz": (
                        f"{lekarz.imie} {lekarz.nazwisko}" if lekarz else "Nieznany"
                    ),
                    "status": przypisany_lek.status,
                    "do_kiedy": przypisany_lek.do_kiedy,
                    "ikona": przypisany_lek.ikona,
                    "kolor": przypisany_lek.kolor,
                }
            )

        return wynik
    finally:
        if czy_zamknac_db:
            db.close()


def przygotuj_harmonogram_lekow(leki_pacjenta):
    godziny = ["08:00", "13:00", "20:00"]
    pory = ["Rano", "Południe", "Wieczór"]
    harmonogram = []

    for indeks, lek in enumerate(leki_pacjenta[:3]):
        harmonogram.append(
            {
                "pora": pory[indeks % len(pory)],
                "godzina": godziny[indeks % len(godziny)],
                "leki": lek["nazwa"],
                "status": "Do przyjęcia" if indeks == 0 else "Zaplanowane",
            }
        )

    return harmonogram

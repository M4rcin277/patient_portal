from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.historia_medyczna import HistoriaMedyczna
from app.models.lekarz import Lekarz
from app.pomocnicy import formatuj_date_po_polsku


def pobierz_historie_medyczna_pacjenta(
    pacjent_id: int,
    db: Session | None = None,
):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = (
            select(HistoriaMedyczna)
            .where(HistoriaMedyczna.pacjent_id == pacjent_id)
            .order_by(HistoriaMedyczna.data.desc())
        )
        wpisy = db.scalars(zapytanie).all()
        wynik = []

        for wpis in wpisy:
            lekarz = db.get(Lekarz, wpis.lekarz_id) if wpis.lekarz_id else None
            data_tekstem = wpis.data.isoformat()
            wynik.append(
                {
                    "data": data_tekstem,
                    "data_czytelna": formatuj_date_po_polsku(data_tekstem),
                    "data_krotka": wpis.data.strftime("%d.%m.%Y"),
                    "lekarz": (
                        f"{lekarz.imie} {lekarz.nazwisko}" if lekarz else "Nieznany"
                    ),
                    "typ": wpis.typ,
                    "tytul": wpis.tytul,
                    "opis": wpis.opis,
                    "etykieta": wpis.etykieta,
                    "ikona": wpis.ikona,
                }
            )

        return wynik
    finally:
        if czy_zamknac_db:
            db.close()

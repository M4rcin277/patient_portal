from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.plan_opieki import PlanOpieki


def zamien_plan_opieki_na_slownik(element: PlanOpieki):
    return {
        "ikona": element.ikona,
        "data": element.data,
        "podpis": element.podpis,
        "tytul": element.tytul,
        "opis": element.opis,
        "etykieta": element.etykieta,
    }


def pobierz_plan_opieki_pacjenta(pacjent_id: int, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = (
            select(PlanOpieki)
            .where(PlanOpieki.pacjent_id == pacjent_id)
            .order_by(PlanOpieki.kolejnosc)
        )
        plan_opieki = db.scalars(zapytanie).all()

        return [
            zamien_plan_opieki_na_slownik(element) for element in plan_opieki
        ]
    finally:
        if czy_zamknac_db:
            db.close()

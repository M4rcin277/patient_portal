from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.godzina_przyjec import GodzinaPrzyjec


def pobierz_godziny_przyjec(db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        godziny = db.scalars(
            select(GodzinaPrzyjec.godzina).order_by(GodzinaPrzyjec.godzina)
        ).all()
        return list(godziny)
    finally:
        if czy_zamknac_db:
            db.close()

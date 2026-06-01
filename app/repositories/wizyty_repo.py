from datetime import date, time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.wizyta import Wizyta
from app.repositories.godziny_przyjec_repo import pobierz_godziny_przyjec


def zamien_wizyte_na_slownik(wizyta: Wizyta):
    return {
        "id": wizyta.id,
        "pacjent_id": wizyta.pacjent_id,
        "lekarz_id": wizyta.lekarz_id,
        "data": wizyta.data.isoformat(),
        "godzina": wizyta.godzina.strftime("%H:%M"),
        "status": wizyta.status,
        "notatka": wizyta.notatka,
    }


def zamien_date(data: str):
    return date.fromisoformat(data)


def zamien_godzine(godzina: str):
    return time.fromisoformat(godzina)


def pobierz_wszystkie_wizyty(db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        wizyty = db.scalars(select(Wizyta).order_by(Wizyta.data, Wizyta.godzina)).all()
        return [zamien_wizyte_na_slownik(wizyta) for wizyta in wizyty]
    finally:
        if czy_zamknac_db:
            db.close()


def znajdz_wizyte(wizyta_id: int, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        wizyta = db.get(Wizyta, wizyta_id)

        if wizyta:
            return zamien_wizyte_na_slownik(wizyta)
    finally:
        if czy_zamknac_db:
            db.close()

    return None


def pobierz_wizyty_pacjenta(pacjent_id: int, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = (
            select(Wizyta)
            .where(Wizyta.pacjent_id == pacjent_id)
            .where(Wizyta.status != "odwolana")
            .order_by(Wizyta.data, Wizyta.godzina)
        )
        wizyty = db.scalars(zapytanie).all()

        return [zamien_wizyte_na_slownik(wizyta) for wizyta in wizyty]
    finally:
        if czy_zamknac_db:
            db.close()


def dodaj_wizyte(
    pacjent_id: int,
    lekarz_id: int,
    data: str,
    godzina: str,
    notatka: str,
    db: Session | None = None,
):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        wizyta = Wizyta(
            pacjent_id=pacjent_id,
            lekarz_id=lekarz_id,
            data=zamien_date(data),
            godzina=zamien_godzine(godzina),
            status="zaplanowana",
            notatka=notatka,
        )

        db.add(wizyta)
        db.commit()
        db.refresh(wizyta)

        return zamien_wizyte_na_slownik(wizyta)
    finally:
        if czy_zamknac_db:
            db.close()


def ustaw_status_wizyty(wizyta_id: int, status: str, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        wizyta = db.get(Wizyta, wizyta_id)

        if wizyta is None:
            return None

        wizyta.status = status
        db.commit()
        db.refresh(wizyta)

        return zamien_wizyte_na_slownik(wizyta)
    finally:
        if czy_zamknac_db:
            db.close()


def zaktualizuj_termin_wizyty(
    wizyta_id: int,
    data: str,
    godzina: str,
    status: str,
    db: Session | None = None,
):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        wizyta = db.get(Wizyta, wizyta_id)

        if wizyta is None:
            return None

        wizyta.data = zamien_date(data)
        wizyta.godzina = zamien_godzine(godzina)
        wizyta.status = status
        db.commit()
        db.refresh(wizyta)

        return zamien_wizyte_na_slownik(wizyta)
    finally:
        if czy_zamknac_db:
            db.close()


def pobierz_wolne_godziny(lekarz_id: int, data: str, db: Session | None = None):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = (
            select(Wizyta.godzina)
            .where(Wizyta.lekarz_id == lekarz_id)
            .where(Wizyta.data == zamien_date(data))
            .where(Wizyta.status != "odwolana")
        )
        zajete_godziny = {
            godzina.strftime("%H:%M") for godzina in db.scalars(zapytanie).all()
        }

        return [
            godzina
            for godzina in pobierz_godziny_przyjec(db)
            if godzina not in zajete_godziny
        ]
    finally:
        if czy_zamknac_db:
            db.close()


def termin_jest_zajety(
    lekarz_id: int,
    data: str,
    godzina: str,
    pomin_wizyte_id: int | None = None,
    db: Session | None = None,
):
    czy_zamknac_db = db is None
    db = db or SessionLocal()

    try:
        zapytanie = (
            select(Wizyta)
            .where(Wizyta.lekarz_id == lekarz_id)
            .where(Wizyta.data == zamien_date(data))
            .where(Wizyta.godzina == zamien_godzine(godzina))
            .where(Wizyta.status != "odwolana")
        )

        if pomin_wizyte_id is not None:
            zapytanie = zapytanie.where(Wizyta.id != pomin_wizyte_id)

        return db.scalar(zapytanie.limit(1)) is not None
    finally:
        if czy_zamknac_db:
            db.close()

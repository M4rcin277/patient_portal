from datetime import datetime

from app.repositories.lekarze_repo import znajdz_lekarza
from app.repositories.pacjenci_repo import znajdz_pacjenta
from app.repositories.wizyty_repo import (
    dodaj_wizyte,
    ustaw_status_wizyty,
    termin_jest_zajety,
    zaktualizuj_termin_wizyty,
    znajdz_wizyte,
)


class PacjentNieIstnieje(Exception):
    pass


class LekarzNieIstnieje(Exception):
    pass


class TerminZajety(Exception):
    pass


class NiepoprawnyTermin(Exception):
    pass


class TerminWPrzeszlosci(Exception):
    pass


class WizytaNieIstnieje(Exception):
    pass


class BrakDostepuDoWizyty(Exception):
    pass


class WizytaNieaktywna(Exception):
    pass


def przygotuj_datetime_terminu(data: str, godzina: str):
    try:
        return datetime.strptime(f"{data} {godzina}", "%Y-%m-%d %H:%M")
    except ValueError:
        raise NiepoprawnyTermin()


def termin_jest_w_przeszlosci(data: str, godzina: str):
    termin = przygotuj_datetime_terminu(data, godzina)
    return termin < datetime.now()


def sprawdz_termin_nie_jest_w_przeszlosci(data: str, godzina: str):
    if termin_jest_w_przeszlosci(data, godzina):
        raise TerminWPrzeszlosci()


def sprawdz_dostep_do_wizyty(wizyta_id: int, pacjent_id: int, db=None):
    wizyta = znajdz_wizyte(wizyta_id, db)

    if wizyta is None:
        raise WizytaNieIstnieje()

    if wizyta["pacjent_id"] != pacjent_id:
        raise BrakDostepuDoWizyty()

    if wizyta["status"] == "odwolana":
        raise WizytaNieaktywna()

    return wizyta


def utworz_wizyte(
    pacjent_id: int,
    lekarz_id: int,
    data: str,
    godzina: str,
    notatka: str,
    db=None,
):
    pacjent = znajdz_pacjenta(pacjent_id, db)
    lekarz = znajdz_lekarza(lekarz_id, db)

    if pacjent is None:
        raise PacjentNieIstnieje()

    if lekarz is None:
        raise LekarzNieIstnieje()

    sprawdz_termin_nie_jest_w_przeszlosci(data, godzina)

    if termin_jest_zajety(lekarz_id, data, godzina, db=db):
        raise TerminZajety()

    return dodaj_wizyte(
        pacjent_id=pacjent_id,
        lekarz_id=lekarz_id,
        data=data,
        godzina=godzina,
        notatka=notatka,
        db=db,
    )


def odwolaj_wizyte(wizyta_id: int, pacjent_id: int, db=None):
    wizyta = sprawdz_dostep_do_wizyty(wizyta_id, pacjent_id, db)

    sprawdz_termin_nie_jest_w_przeszlosci(wizyta["data"], wizyta["godzina"])

    return ustaw_status_wizyty(wizyta["id"], "odwolana", db)


def przesun_wizyte(
    wizyta_id: int,
    pacjent_id: int,
    data: str,
    godzina: str,
    db=None,
):
    wizyta = sprawdz_dostep_do_wizyty(wizyta_id, pacjent_id, db)

    sprawdz_termin_nie_jest_w_przeszlosci(data, godzina)

    if termin_jest_zajety(
        wizyta["lekarz_id"],
        data,
        godzina,
        pomin_wizyte_id=wizyta["id"],
        db=db,
    ):
        raise TerminZajety()

    return zaktualizuj_termin_wizyty(
        wizyta_id=wizyta["id"],
        data=data,
        godzina=godzina,
        status="przesunieta",
        db=db,
    )

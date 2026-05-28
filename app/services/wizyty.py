from datetime import datetime

from app.dane import wizyty
from app.pomocnicy import termin_jest_zajety, znajdz_lekarza, znajdz_pacjenta


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


def znajdz_wizyte(wizyta_id: int):
    for wizyta in wizyty:
        if wizyta["id"] == wizyta_id:
            return wizyta

    return None


def sprawdz_dostep_do_wizyty(wizyta_id: int, pacjent_id: int):
    wizyta = znajdz_wizyte(wizyta_id)

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
):
    pacjent = znajdz_pacjenta(pacjent_id)
    lekarz = znajdz_lekarza(lekarz_id)

    if pacjent is None:
        raise PacjentNieIstnieje()

    if lekarz is None:
        raise LekarzNieIstnieje()

    sprawdz_termin_nie_jest_w_przeszlosci(data, godzina)

    if termin_jest_zajety(lekarz_id, data, godzina):
        raise TerminZajety()

    wizyta = {
        "id": len(wizyty) + 1,
        "pacjent_id": pacjent_id,
        "lekarz_id": lekarz_id,
        "data": data,
        "godzina": godzina,
        "status": "zaplanowana",
        "notatka": notatka,
    }

    wizyty.append(wizyta)

    return wizyta


def odwolaj_wizyte(wizyta_id: int, pacjent_id: int):
    wizyta = sprawdz_dostep_do_wizyty(wizyta_id, pacjent_id)

    sprawdz_termin_nie_jest_w_przeszlosci(wizyta["data"], wizyta["godzina"])

    wizyta["status"] = "odwolana"

    return wizyta


def przesun_wizyte(
    wizyta_id: int,
    pacjent_id: int,
    data: str,
    godzina: str,
):
    wizyta = sprawdz_dostep_do_wizyty(wizyta_id, pacjent_id)

    sprawdz_termin_nie_jest_w_przeszlosci(data, godzina)

    if termin_jest_zajety(
        wizyta["lekarz_id"],
        data,
        godzina,
        pomin_wizyte_id=wizyta["id"],
    ):
        raise TerminZajety()

    wizyta["data"] = data
    wizyta["godzina"] = godzina
    wizyta["status"] = "przesunieta"

    return wizyta

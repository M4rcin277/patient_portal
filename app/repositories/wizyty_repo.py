from app.dane import godziny_przyjec, wizyty


def pobierz_wszystkie_wizyty():
    return wizyty


def znajdz_wizyte(wizyta_id: int):
    for wizyta in wizyty:
        if wizyta["id"] == wizyta_id:
            return wizyta

    return None


def pobierz_wizyty_pacjenta(pacjent_id: int):
    wizyty_pacjenta = []

    for wizyta in wizyty:
        if wizyta["pacjent_id"] == pacjent_id and wizyta["status"] != "odwolana":
            wizyty_pacjenta.append(wizyta)

    return wizyty_pacjenta


def dodaj_wizyte(pacjent_id: int, lekarz_id: int, data: str, godzina: str, notatka: str):
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


def pobierz_wolne_godziny(lekarz_id: int, data: str):
    zajete_godziny = []
    for wizyta in wizyty:
        if (
            wizyta["lekarz_id"] == lekarz_id
            and wizyta["data"] == data
            and wizyta["status"] != "odwolana"
        ):
            zajete_godziny.append(wizyta["godzina"])

    wolne_godziny = []

    for godzina in godziny_przyjec:
        if godzina not in zajete_godziny:
            wolne_godziny.append(godzina)

    return wolne_godziny


def termin_jest_zajety(
    lekarz_id: int,
    data: str,
    godzina: str,
    pomin_wizyte_id: int | None = None,
):
    for wizyta in wizyty:
        if (
            wizyta["id"] != pomin_wizyte_id
            and wizyta["lekarz_id"] == lekarz_id
            and wizyta["data"] == data
            and wizyta["godzina"] == godzina
            and wizyta["status"] != "odwolana"
        ):
            return True

    return False

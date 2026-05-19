from app.dane import godziny_przyjec, lekarze, pacjenci, wizyty


def znajdz_pacjenta(pacjent_id: int):
    for pacjent in pacjenci:
        if pacjent["id"] == pacjent_id:
            return pacjent

    return None


def znajdz_lekarza(lekarz_id: int):
    for lekarz in lekarze:
        if lekarz["id"] == lekarz_id:
            return lekarz

    return None


def przygotuj_wizyte_dla_pacjenta(wizyta):
    lekarz = znajdz_lekarza(wizyta["lekarz_id"])

    return {
        "id": wizyta["id"],
        "lekarz": f"{lekarz['imie']} {lekarz['nazwisko']}",
        "specjalizacja": lekarz["specjalizacja"],
        "data": wizyta["data"],
        "godzina": wizyta["godzina"],
        "status": wizyta["status"],
        "notatka": wizyta["notatka"],
    }


def pobierz_wolne_godziny(lekarz_id: int, data: str):
    zajete_godziny = []
    for wizyta in wizyty:
        if wizyta["lekarz_id"] == lekarz_id and wizyta["data"] == data:
            zajete_godziny.append(wizyta["godzina"])

    wolne_godziny = []

    for godzina in godziny_przyjec:
        if godzina not in zajete_godziny:
            wolne_godziny.append(godzina)

    return wolne_godziny


def termin_jest_zajety(lekarz_id: int, data: str, godzina: str):
    for wizyta in wizyty:
        if (
            wizyta["lekarz_id"] == lekarz_id
            and wizyta["data"] == data
            and wizyta["godzina"] == godzina
        ):
            return True

    return False

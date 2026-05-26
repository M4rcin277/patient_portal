from calendar import monthrange
from datetime import date, datetime

from app.dane import godziny_przyjec, lekarze, pacjenci, wizyty


POLSKIE_MIESIACE = [
    "stycznia",
    "lutego",
    "marca",
    "kwietnia",
    "maja",
    "czerwca",
    "lipca",
    "sierpnia",
    "września",
    "października",
    "listopada",
    "grudnia",
]

POLSKIE_MIESIACE_NAGLOWEK = [
    "Styczeń",
    "Luty",
    "Marzec",
    "Kwiecień",
    "Maj",
    "Czerwiec",
    "Lipiec",
    "Sierpień",
    "Wrzesień",
    "Październik",
    "Listopad",
    "Grudzień",
]

POLSKIE_MIESIACE_SKROT = [
    "STY",
    "LUT",
    "MAR",
    "KWI",
    "MAJ",
    "CZE",
    "LIP",
    "SIE",
    "WRZ",
    "PAZ",
    "LIS",
    "GRU",
]


def zamien_wizyte_na_datetime(wizyta):
    return datetime.strptime(
        f"{wizyta['data']} {wizyta['godzina']}",
        "%Y-%m-%d %H:%M",
    )


def formatuj_date_po_polsku(data_tekstem: str):
    data = date.fromisoformat(data_tekstem)
    miesiac = POLSKIE_MIESIACE[data.month - 1]

    return f"{data.day} {miesiac} {data.year}"


def przygotuj_historie_medyczna(historia_medyczna):
    wpisy = []

    for wpis in historia_medyczna:
        przygotowany_wpis = wpis.copy()
        data_wpisu = date.fromisoformat(wpis["data"])
        przygotowany_wpis["data_czytelna"] = formatuj_date_po_polsku(wpis["data"])
        przygotowany_wpis["data_krotka"] = data_wpisu.strftime("%d.%m.%Y")
        wpisy.append(przygotowany_wpis)

    return sorted(wpisy, key=lambda wpis: wpis["data"], reverse=True)


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
    data_wizyty = date.fromisoformat(wizyta["data"])

    return {
        "id": wizyta["id"],
        "lekarz": f"{lekarz['imie']} {lekarz['nazwisko']}",
        "specjalizacja": lekarz["specjalizacja"],
        "lokalizacja": lekarz["lokalizacja"],
        "data": wizyta["data"],
        "data_czytelna": formatuj_date_po_polsku(wizyta["data"]),
        "data_dzien": f"{data_wizyty.day:02d}",
        "data_miesiac_skrot": POLSKIE_MIESIACE_SKROT[data_wizyty.month - 1],
        "data_rok": data_wizyty.year,
        "godzina": wizyta["godzina"],
        "status": wizyta["status"],
        "notatka": wizyta["notatka"],
    }


def pobierz_wizyty_pacjenta(pacjent_id: int):
    wizyty_pacjenta = []

    for wizyta in wizyty:
        if wizyta["pacjent_id"] == pacjent_id:
            wizyty_pacjenta.append(przygotuj_wizyte_dla_pacjenta(wizyta))

    return wizyty_pacjenta


def pobierz_nadchodzace_wizyty(wizyty_pacjenta):
    teraz = datetime.now()

    nadchodzace_wizyty = []
    for wizyta in wizyty_pacjenta:
        if zamien_wizyte_na_datetime(wizyta) >= teraz:
            nadchodzace_wizyty.append(wizyta)

    return sorted(nadchodzace_wizyty, key=zamien_wizyte_na_datetime)


def znajdz_najblizsza_wizyte(wizyty_pacjenta):
    if wizyty_pacjenta:
        return wizyty_pacjenta[0]

    return None


def pobierz_poprzedni_miesiac(rok: int, miesiac: int):
    if miesiac == 1:
        return {"rok": rok - 1, "miesiac": 12}

    return {"rok": rok, "miesiac": miesiac - 1}


def pobierz_nastepny_miesiac(rok: int, miesiac: int):
    if miesiac == 12:
        return {"rok": rok + 1, "miesiac": 1}

    return {"rok": rok, "miesiac": miesiac + 1}


def przygotuj_kalendarz_wizyt(
    wizyty_pacjenta,
    najblizsza_wizyta,
    wybrany_rok=None,
    wybrany_miesiac=None,
):
    dzisiaj = date.today()

    if wybrany_rok and wybrany_miesiac and 1 <= wybrany_miesiac <= 12:
        data_kalendarza = date(wybrany_rok, wybrany_miesiac, 1)
    elif najblizsza_wizyta:
        data_kalendarza = date.fromisoformat(najblizsza_wizyta["data"])
    else:
        data_kalendarza = dzisiaj

    rok = data_kalendarza.year
    miesiac = data_kalendarza.month
    poprzedni_miesiac = pobierz_poprzedni_miesiac(rok, miesiac)
    nastepny_miesiac = pobierz_nastepny_miesiac(rok, miesiac)
    pierwszy_dzien_tygodnia, liczba_dni = monthrange(rok, miesiac)
    _, liczba_dni_poprzedniego_miesiaca = monthrange(
        rok if miesiac > 1 else rok - 1,
        miesiac - 1 if miesiac > 1 else 12,
    )

    wizyty_w_miesiacu = {}
    for wizyta in wizyty_pacjenta:
        data_wizyty = date.fromisoformat(wizyta["data"])
        if data_wizyty.year == rok and data_wizyty.month == miesiac:
            wizyty_w_miesiacu[data_wizyty.day] = wizyta

    dni = []

    for przesuniecie in range(pierwszy_dzien_tygodnia):
        dni.append(
            {
                "numer": liczba_dni_poprzedniego_miesiaca
                - pierwszy_dzien_tygodnia
                + przesuniecie
                + 1,
                "wyciszony": True,
                "ma_wizyte": False,
            }
        )

    for numer_dnia in range(1, liczba_dni + 1):
        wizyta = wizyty_w_miesiacu.get(numer_dnia)
        data_dnia = date(rok, miesiac, numer_dnia)
        typ_wizyty = None

        if wizyta:
            if data_dnia == dzisiaj:
                typ_wizyty = "dzisiaj"
            elif data_dnia > dzisiaj:
                typ_wizyty = "przyszla"
            else:
                typ_wizyty = "miniona"

        dni.append(
            {
                "numer": numer_dnia,
                "wyciszony": False,
                "ma_wizyte": wizyta is not None,
                "wizyta": wizyta,
                "typ_wizyty": typ_wizyty,
            }
        )

    while len(dni) < 42:
        dni.append(
            {
                "numer": "",
                "wyciszony": True,
                "ma_wizyte": False,
            }
        )

    podpis = "Brak wizyt w tym miesiącu"
    wizyty_z_wybranego_miesiaca = sorted(
        wizyty_w_miesiacu.values(),
        key=zamien_wizyte_na_datetime,
    )

    if wizyty_z_wybranego_miesiaca:
        pierwsza_wizyta_w_miesiacu = wizyty_z_wybranego_miesiaca[0]
        podpis = (
            f"{pierwsza_wizyta_w_miesiacu['data_czytelna']}, "
            f"{pierwsza_wizyta_w_miesiacu['godzina']} - "
            f"{pierwsza_wizyta_w_miesiacu['specjalizacja']}"
        )

    return {
        "miesiac": f"{POLSKIE_MIESIACE_NAGLOWEK[miesiac - 1]} {rok}",
        "poprzedni_miesiac": poprzedni_miesiac,
        "nastepny_miesiac": nastepny_miesiac,
        "dni": dni,
        "podpis": podpis,
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

from datetime import date, timedelta

from app.dane import godziny_przyjec, lekarze
from app.pomocnicy import (
    formatuj_date_po_polsku,
    termin_jest_zajety,
    znajdz_pacjenta,
)
from app.services.wizyty import termin_jest_w_przeszlosci


def przygotuj_termin_dla_szybkiego_zapisu(lekarz, data_terminu, godzina):
    data_tekst = data_terminu.isoformat()

    if termin_jest_w_przeszlosci(data_tekst, godzina):
        return None

    if termin_jest_zajety(lekarz["id"], data_tekst, godzina):
        return None

    dzisiaj = date.today()
    przesuniecie = (data_terminu - dzisiaj).days

    if przesuniecie == 0:
        dzien_etykieta = "Dzisiaj"
        filtr_dnia = "dzisiaj"
    elif przesuniecie == 1:
        dzien_etykieta = "Jutro"
    elif przesuniecie == 2:
        dzien_etykieta = "Pojutrze"
    else:
        dzien_etykieta = formatuj_date_po_polsku(data_tekst)

    if przesuniecie == 0:
        filtr_dnia = "dzisiaj"
    elif przesuniecie <= 7:
        filtr_dnia = "tydzien"
    elif przesuniecie <= 30:
        filtr_dnia = "miesiac"
    else:
        filtr_dnia = "ponad_miesiac"

    return {
        "lekarz": lekarz,
        "data": data_tekst,
        "dzien_etykieta": dzien_etykieta,
        "data_etykieta": formatuj_date_po_polsku(data_tekst),
        "filtr_dnia": filtr_dnia,
        "godzina": godzina,
        "online": "Online" in lekarz.get("tryb_wizyty", ""),
    }


def przygotuj_dostepne_terminy_szybkiego_zapisu():
    dzisiaj = date.today()
    przesuniecia_dni = [0, 1, 2, 3, 5, 8, 14, 21, 34, 45, 60]
    dostepne_terminy = []

    for indeks, lekarz in enumerate(lekarze):
        for pozycja_dnia, przesuniecie in enumerate(przesuniecia_dni):
            data_terminu = dzisiaj + timedelta(days=przesuniecie)
            godzina = godziny_przyjec[
                (indeks + pozycja_dnia) % len(godziny_przyjec)
            ]
            termin = przygotuj_termin_dla_szybkiego_zapisu(
                lekarz,
                data_terminu,
                godzina,
            )

            if termin is not None:
                dostepne_terminy.append(termin)

    return dostepne_terminy


def przygotuj_terminy_lekarza(lekarz_id: int, liczba_dni: int = 90):
    lekarz = next((lekarz for lekarz in lekarze if lekarz["id"] == lekarz_id), None)

    if lekarz is None:
        return []

    dzisiaj = date.today()
    terminy = []

    for przesuniecie in range(liczba_dni + 1):
        data_terminu = dzisiaj + timedelta(days=przesuniecie)

        for godzina in godziny_przyjec:
            termin = przygotuj_termin_dla_szybkiego_zapisu(
                lekarz,
                data_terminu,
                godzina,
            )

            if termin is not None:
                terminy.append(termin)

    return terminy


def przygotuj_kontekst_szybkiego_zapisu(
    blad: str | None = None,
    lekarz_id: int | None = None,
):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)
    dostepne_terminy = przygotuj_dostepne_terminy_szybkiego_zapisu()
    wybrany_lekarz = next(
        (lekarz for lekarz in lekarze if lekarz["id"] == lekarz_id),
        None,
    )
    dzisiaj = date.today()
    kontekst = {
        "pacjent": pacjent,
        "aktywna_strona": "szybki_zapis",
        "lekarze": lekarze,
        "godziny_przyjec": godziny_przyjec,
        "dostepne_terminy": dostepne_terminy,
        "rekomendowane_terminy": dostepne_terminy[:3],
        "najblizszy_dostepny_termin": (
            dostepne_terminy[0] if dostepne_terminy else None
        ),
        "wybrany_lekarz": wybrany_lekarz,
        "terminy_wybranego_lekarza": (
            przygotuj_terminy_lekarza(lekarz_id) if wybrany_lekarz else []
        ),
        "minimalna_data_rezerwacji": dzisiaj.isoformat(),
        "maksymalna_data_rezerwacji": (dzisiaj + timedelta(days=90)).isoformat(),
    }

    if blad is not None:
        kontekst["blad"] = blad

    return kontekst

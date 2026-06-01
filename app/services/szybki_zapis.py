from datetime import date, timedelta

from app.pomocnicy import formatuj_date_po_polsku
from app.repositories.godziny_przyjec_repo import pobierz_godziny_przyjec
from app.repositories.lekarze_repo import pobierz_wszystkich_lekarzy, znajdz_lekarza
from app.repositories.pacjenci_repo import znajdz_pacjenta
from app.repositories.wizyty_repo import termin_jest_zajety
from app.services.wizyty import termin_jest_w_przeszlosci


def przygotuj_termin_dla_szybkiego_zapisu(lekarz, data_terminu, godzina, db=None):
    data_tekst = data_terminu.isoformat()

    if termin_jest_w_przeszlosci(data_tekst, godzina):
        return None

    if termin_jest_zajety(lekarz["id"], data_tekst, godzina, db=db):
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


def wybierz_godzine_dla_dnia(godziny_przyjec, indeks_startowy, data_terminu):
    if data_terminu > date.today():
        return godziny_przyjec[indeks_startowy % len(godziny_przyjec)]

    for przesuniecie in range(len(godziny_przyjec)):
        godzina = godziny_przyjec[
            (indeks_startowy + przesuniecie) % len(godziny_przyjec)
        ]

        if not termin_jest_w_przeszlosci(data_terminu.isoformat(), godzina):
            return godzina

    return None


def przygotuj_dostepne_terminy_szybkiego_zapisu(db=None):
    dzisiaj = date.today()
    przesuniecia_dni = [0, 1, 2, 3, 5, 8, 14, 21, 34, 45, 60]
    godziny_przyjec = pobierz_godziny_przyjec(db)
    dostepne_terminy = []

    for indeks, lekarz in enumerate(pobierz_wszystkich_lekarzy(db)):
        for pozycja_dnia, przesuniecie in enumerate(przesuniecia_dni):
            data_terminu = dzisiaj + timedelta(days=przesuniecie)
            godzina = wybierz_godzine_dla_dnia(
                godziny_przyjec,
                indeks + pozycja_dnia,
                data_terminu,
            )

            if godzina is None:
                continue

            termin = przygotuj_termin_dla_szybkiego_zapisu(
                lekarz,
                data_terminu,
                godzina,
                db,
            )

            if termin is not None:
                dostepne_terminy.append(termin)

    return dostepne_terminy


def przygotuj_terminy_lekarza(lekarz_id: int, liczba_dni: int = 90, db=None):
    lekarz = znajdz_lekarza(lekarz_id, db)
    godziny_przyjec = pobierz_godziny_przyjec(db)

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
                db,
            )

            if termin is not None:
                terminy.append(termin)

    return terminy


def przygotuj_kontekst_szybkiego_zapisu(
    pacjent_id: int,
    blad: str | None = None,
    lekarz_id: int | None = None,
    db=None,
):
    pacjent = znajdz_pacjenta(pacjent_id, db)
    godziny_przyjec = pobierz_godziny_przyjec(db)
    dostepne_terminy = przygotuj_dostepne_terminy_szybkiego_zapisu(db)
    wybrany_lekarz = znajdz_lekarza(lekarz_id, db) if lekarz_id is not None else None
    dzisiaj = date.today()
    kontekst = {
        "pacjent": pacjent,
        "aktywna_strona": "szybki_zapis",
        "lekarze": pobierz_wszystkich_lekarzy(db),
        "godziny_przyjec": godziny_przyjec,
        "dostepne_terminy": dostepne_terminy,
        "rekomendowane_terminy": dostepne_terminy[:3],
        "najblizszy_dostepny_termin": (
            dostepne_terminy[0] if dostepne_terminy else None
        ),
        "wybrany_lekarz": wybrany_lekarz,
        "terminy_wybranego_lekarza": (
            przygotuj_terminy_lekarza(lekarz_id, db=db) if wybrany_lekarz else []
        ),
        "minimalna_data_rezerwacji": dzisiaj.isoformat(),
        "maksymalna_data_rezerwacji": (dzisiaj + timedelta(days=90)).isoformat(),
    }

    if blad is not None:
        kontekst["blad"] = blad

    return kontekst

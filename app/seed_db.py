from datetime import date, datetime, time

from sqlalchemy import func, select

from app import models
from app.seed_data import (
    apteki,
    godziny_przyjec,
    historia_medyczna,
    lekarze,
    leki_pacjenta,
    pacjenci,
    plan_opieki,
    recepty_pacjenta,
    wizyty,
)
from app.database import SessionLocal
from app.models.apteka import Apteka
from app.models.godzina_przyjec import GodzinaPrzyjec
from app.models.historia_medyczna import HistoriaMedyczna
from app.models.lek import Lek
from app.models.lekarz import Lekarz
from app.models.pacjent import Pacjent
from app.models.pacjent_lek import PacjentLek
from app.models.placowka import Placowka
from app.models.plan_opieki import PlanOpieki
from app.models.recepta import Recepta
from app.models.recepta_lek import ReceptaLek
from app.models.specjalizacja import Specjalizacja
from app.models.uzytkownik import Uzytkownik
from app.models.wizyta import Wizyta


def tabela_ma_dane(db, model):
    liczba_rekordow = db.scalar(select(func.count()).select_from(model))

    return liczba_rekordow > 0


def dodaj_dane_startowe(db, model, dane, nazwa_tabeli: str):
    if tabela_ma_dane(db, model):
        print(f"Tabela {nazwa_tabeli} ma juz dane. Pomijam.")
        return

    db.add_all(dane)
    db.commit()
    print(f"Dodano dane startowe do tabeli {nazwa_tabeli}.")


def przygotuj_pacjentow():
    przygotowani_pacjenci = []

    for pacjent in pacjenci:
        przygotowani_pacjenci.append(
            Pacjent(
                id=pacjent["id"],
                imie=pacjent["imie"],
                nazwisko=pacjent["nazwisko"],
                email=pacjent["email"],
                telefon=pacjent["telefon"],
                data_urodzenia=date.fromisoformat(pacjent["data_urodzenia"]),
                adres=pacjent["adres"],
            )
        )

    return przygotowani_pacjenci


def przygotuj_lekarzy():
    przygotowani_lekarze = []

    for lekarz in lekarze:
        przygotowani_lekarze.append(
            Lekarz(
                id=lekarz["id"],
                imie=lekarz["imie"],
                nazwisko=lekarz["nazwisko"],
                specjalizacja=lekarz["specjalizacja"],
                miasto=lekarz["miasto"],
                lokalizacja=lekarz["lokalizacja"],
                tryb_wizyty=lekarz["tryb_wizyty"],
            )
        )

    return przygotowani_lekarze


def przygotuj_wizyty():
    przygotowane_wizyty = []

    for wizyta in wizyty:
        przygotowane_wizyty.append(
            Wizyta(
                id=wizyta["id"],
                pacjent_id=wizyta["pacjent_id"],
                lekarz_id=wizyta["lekarz_id"],
                data=date.fromisoformat(wizyta["data"]),
                godzina=time.fromisoformat(wizyta["godzina"]),
                status=wizyta["status"],
                notatka=wizyta["notatka"],
            )
        )

    return przygotowane_wizyty


def przygotuj_godziny_przyjec():
    return [
        GodzinaPrzyjec(id=indeks, godzina=godzina)
        for indeks, godzina in enumerate(godziny_przyjec, start=1)
    ]


def przygotuj_plan_opieki():
    return [
        PlanOpieki(
            id=indeks,
            pacjent_id=1,
            kolejnosc=indeks,
            ikona=element["ikona"],
            data=element["data"],
            podpis=element["podpis"],
            tytul=element["tytul"],
            opis=element["opis"],
            etykieta=element["etykieta"],
        )
        for indeks, element in enumerate(plan_opieki, start=1)
    ]


def przygotuj_apteki():
    return [
        Apteka(
            id=apteka["id"],
            nazwa=apteka["nazwa"],
            adres=apteka["adres"],
            godziny=apteka["godziny"],
        )
        for apteka in apteki
    ]


def przygotuj_uzytkownikow():
    return [
        Uzytkownik(
            id=1,
            email="jan.kowalski@example.com",
            haslo_hash="demo-hash-do-zmiany",
            rola="pacjent",
            pacjent_id=1,
            lekarz_id=None,
        )
    ]


def przygotuj_specjalizacje():
    nazwy_specjalizacji = sorted({lekarz["specjalizacja"] for lekarz in lekarze})

    return [
        Specjalizacja(
            id=indeks,
            nazwa=nazwa,
            opis=f"Konsultacje i wizyty w specjalizacji: {nazwa}.",
        )
        for indeks, nazwa in enumerate(nazwy_specjalizacji, start=1)
    ]


def przygotuj_placowki():
    unikalne_placowki = {}

    for lekarz in lekarze:
        klucz = (lekarz["lokalizacja"], lekarz["miasto"])
        unikalne_placowki[klucz] = {
            "nazwa": lekarz["lokalizacja"],
            "miasto": lekarz["miasto"],
        }

    return [
        Placowka(
            id=indeks,
            nazwa=dane_placowki["nazwa"],
            miasto=dane_placowki["miasto"],
            adres=None,
            telefon=None,
        )
        for indeks, dane_placowki in enumerate(unikalne_placowki.values(), start=1)
    ]


def przygotuj_leki():
    przygotowane_leki = []

    for lek in leki_pacjenta:
        przygotowane_leki.append(
            Lek(
                id=lek["id"],
                nazwa=lek["nazwa"],
                substancja=lek["substancja"],
                dawka=None,
                postac=None,
            )
        )

    return przygotowane_leki


def przygotuj_leki_pacjenta():
    przygotowane_leki = []

    for lek in leki_pacjenta:
        przygotowane_leki.append(
            PacjentLek(
                id=lek["id"],
                pacjent_id=1,
                lek_id=lek["id"],
                lekarz_id=znajdz_lekarza_id_po_nazwie(lek["lekarz"]),
                dawkowanie=lek["dawkowanie"],
                zalecenie=lek["zalecenie"],
                status=lek["status"],
                do_kiedy=lek["do_kiedy"],
                ikona=lek["ikona"],
                kolor=lek["kolor"],
            )
        )

    return przygotowane_leki


def znajdz_lekarza_id_po_nazwie(nazwa_lekarza: str):
    for lekarz in lekarze:
        pelna_nazwa = f"{lekarz['imie']} {lekarz['nazwisko']}"

        if pelna_nazwa == nazwa_lekarza:
            return lekarz["id"]

    return None


def przygotuj_recepty():
    przygotowane_recepty = []

    for recepta in recepty_pacjenta:
        przygotowane_recepty.append(
            Recepta(
                id=recepta["id"],
                pacjent_id=1,
                lekarz_id=znajdz_lekarza_id_po_nazwie(recepta["lekarz"]),
                kod=f"RX-{recepta['id']:04d}",
                wystawiono=datetime.strptime(
                    recepta["wystawiono"],
                    "%d.%m.%Y",
                ).date(),
                wazna_do=datetime.strptime(recepta["wazna_do"], "%d.%m.%Y").date(),
                status="aktywna",
            )
        )

    return przygotowane_recepty


def przygotuj_recepta_leki():
    powiazania = []

    for recepta in recepty_pacjenta:
        for numer_leku in range(1, recepta["liczba_lekow"] + 1):
            lek_id = ((recepta["id"] + numer_leku - 2) % len(leki_pacjenta)) + 1
            powiazania.append(
                ReceptaLek(
                    id=len(powiazania) + 1,
                    recepta_id=recepta["id"],
                    lek_id=lek_id,
                    dawkowanie="Zgodnie z zaleceniem lekarza",
                    ilosc="1 op.",
                )
            )

    return powiazania


def przygotuj_historie_medyczna():
    przygotowane_wpisy = []

    for indeks, wpis in enumerate(historia_medyczna, start=1):
        przygotowane_wpisy.append(
            HistoriaMedyczna(
                id=indeks,
                pacjent_id=1,
                lekarz_id=znajdz_lekarza_id_po_nazwie(wpis["lekarz"]),
                wizyta_id=None,
                data=date.fromisoformat(wpis["data"]),
                typ=wpis["typ"],
                tytul=wpis["tytul"],
                opis=wpis["opis"],
                etykieta=wpis["etykieta"],
                ikona=wpis["ikona"],
            )
        )

    return przygotowane_wpisy


def seeduj_baze():
    db = SessionLocal()

    try:
        dodaj_dane_startowe(db, Pacjent, przygotuj_pacjentow(), "pacjenci")
        dodaj_dane_startowe(db, Lekarz, przygotuj_lekarzy(), "lekarze")
        dodaj_dane_startowe(db, Wizyta, przygotuj_wizyty(), "wizyty")
        dodaj_dane_startowe(
            db,
            GodzinaPrzyjec,
            przygotuj_godziny_przyjec(),
            "godziny_przyjec",
        )
        dodaj_dane_startowe(
            db,
            PlanOpieki,
            przygotuj_plan_opieki(),
            "plan_opieki",
        )
        dodaj_dane_startowe(db, Apteka, przygotuj_apteki(), "apteki")
        dodaj_dane_startowe(db, Uzytkownik, przygotuj_uzytkownikow(), "uzytkownicy")
        dodaj_dane_startowe(
            db,
            Specjalizacja,
            przygotuj_specjalizacje(),
            "specjalizacje",
        )
        dodaj_dane_startowe(db, Placowka, przygotuj_placowki(), "placowki")
        dodaj_dane_startowe(db, Lek, przygotuj_leki(), "leki")
        dodaj_dane_startowe(
            db,
            PacjentLek,
            przygotuj_leki_pacjenta(),
            "pacjent_leki",
        )
        dodaj_dane_startowe(db, Recepta, przygotuj_recepty(), "recepty")
        dodaj_dane_startowe(
            db,
            ReceptaLek,
            przygotuj_recepta_leki(),
            "recepta_leki",
        )
        dodaj_dane_startowe(
            db,
            HistoriaMedyczna,
            przygotuj_historie_medyczna(),
            "historia_medyczna",
        )
    finally:
        db.close()


def main():
    seeduj_baze()


if __name__ == "__main__":
    main()

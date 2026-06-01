from datetime import date
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.pomocnicy import (
    pobierz_nadchodzace_wizyty,
    pobierz_wizyty_pacjenta,
    przygotuj_kalendarz_wizyt,
    znajdz_najblizsza_wizyte,
)
from app.database import get_db
from app.repositories.apteki_repo import pobierz_apteki
from app.repositories.godziny_przyjec_repo import pobierz_godziny_przyjec
from app.repositories.historia_repo import pobierz_historie_medyczna_pacjenta
from app.repositories.leki_repo import (
    dodaj_lek_pacjenta,
    pobierz_leki_pacjenta,
    przygotuj_harmonogram_lekow,
)
from app.repositories.lekarze_repo import pobierz_wszystkich_lekarzy
from app.repositories.objawy_repo import (
    pobierz_ostatnie_zgloszenie_objawow,
    zapisz_zgloszenie_objawow,
)
from app.repositories.pacjenci_repo import znajdz_pacjenta
from app.repositories.placowki_repo import pobierz_placowki
from app.repositories.plan_opieki_repo import pobierz_plan_opieki_pacjenta
from app.repositories.recepty_repo import pobierz_recepty_pacjenta
from app.services.statusy_wizyt import (
    STATUSY_WIZYT,
    przekieruj_do_wizyt,
    status_wizyty_z_wyjatku,
)
from app.services.szybki_zapis import przygotuj_kontekst_szybkiego_zapisu
from app.services.wizyty import (
    BrakDostepuDoWizyty,
    LekarzNieIstnieje,
    NiepoprawnyTermin,
    PacjentNieIstnieje,
    TerminWPrzeszlosci,
    TerminZajety,
    WizytaNieaktywna,
    WizytaNieIstnieje,
    odwolaj_wizyte,
    przesun_wizyte,
    utworz_wizyte,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/logowanie")
def widok_logowania(request: Request):
    return templates.TemplateResponse(request, "logowanie.html", {})


@router.get("/panel-pacjenta")
def panel_pacjenta(
    request: Request,
    rok: int | None = None,
    miesiac: int | None = None,
    db: Session = Depends(get_db),
):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)
    plan_opieki = pobierz_plan_opieki_pacjenta(pacjent_id, db)
    godziny_przyjec = pobierz_godziny_przyjec(db)
    moje_wizyty = pobierz_wizyty_pacjenta(pacjent_id, db)
    nadchodzace_wizyty = pobierz_nadchodzace_wizyty(moje_wizyty)
    najblizsza_wizyta = znajdz_najblizsza_wizyte(nadchodzace_wizyty)
    kalendarz_wizyt = przygotuj_kalendarz_wizyt(
        nadchodzace_wizyty,
        najblizsza_wizyta,
        rok,
        miesiac,
    )
    kolejna_wizyta = None

    if len(nadchodzace_wizyty) > 1:
        kolejna_wizyta = nadchodzace_wizyty[1]

    aktywne_recepty = "0"
    nowe_wyniki = "0"

    for element in plan_opieki:
        if element["tytul"] == "Aktywne recepty":
            aktywne_recepty = element["etykieta"].split()[0]
        if element["tytul"] == "Zalecenia lekarza":
            nowe_wyniki = element["etykieta"].split()[0]

    podsumowanie_panelu = [
        {
            "ikona": "bi-calendar-check",
            "wartosc": len(nadchodzace_wizyty),
            "tytul": "Nadchodzące wizyty",
            "opis": "w tym miesiącu",
        },
        {
            "ikona": "bi-capsule",
            "wartosc": aktywne_recepty,
            "tytul": "Aktywne recepty",
            "opis": "do wykupienia",
        },
        {
            "ikona": "bi-clipboard2-pulse",
            "wartosc": nowe_wyniki,
            "tytul": "Nieprzeczytane wyniki",
            "opis": "badań",
        },
        {
            "ikona": "bi-shield-check",
            "wartosc": "PZU Zdrowie",
            "tytul": "Ubezpieczenie",
            "opis": "Aktywne",
        },
    ]

    return templates.TemplateResponse(
        request,
        "panel_pacjent.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "dashboard",
            "wizyty": moje_wizyty,
            "nadchodzace_wizyty": nadchodzace_wizyty,
            "najblizsza_wizyta": najblizsza_wizyta,
            "kolejna_wizyta": kolejna_wizyta,
            "plan_opieki": plan_opieki,
            "kalendarz_wizyt": kalendarz_wizyt,
            "podsumowanie_panelu": podsumowanie_panelu,
            "godziny_przyjec": godziny_przyjec,
            "dzisiejsza_data": date.today().isoformat(),
        },
    )


@router.get("/moje-wizyty")
def widok_moje_wizyty(
    request: Request,
    rok: int | None = None,
    miesiac: int | None = None,
    status: str | None = None,
    db: Session = Depends(get_db),
):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)
    godziny_przyjec = pobierz_godziny_przyjec(db)
    moje_wizyty = pobierz_wizyty_pacjenta(pacjent_id, db)
    nadchodzace_wizyty = pobierz_nadchodzace_wizyty(moje_wizyty)
    najblizsza_wizyta = znajdz_najblizsza_wizyte(nadchodzace_wizyty)
    kalendarz_wizyt = przygotuj_kalendarz_wizyt(
        moje_wizyty,
        najblizsza_wizyta,
        rok,
        miesiac,
    )
    komunikat_sukcesu = None
    komunikat_bledu = None
    status_info = STATUSY_WIZYT.get(status)

    if status_info:
        typ_statusu, komunikat = status_info

        if typ_statusu == "sukces":
            komunikat_sukcesu = komunikat
        else:
            komunikat_bledu = komunikat

    return templates.TemplateResponse(
        request,
        "moje_wizyty.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "wizyty",
            "nadchodzace_wizyty": nadchodzace_wizyty,
            "najblizsza_wizyta": najblizsza_wizyta,
            "kalendarz_wizyt": kalendarz_wizyt,
            "komunikat_sukcesu": komunikat_sukcesu,
            "komunikat_bledu": komunikat_bledu,
            "godziny_przyjec": godziny_przyjec,
            "dzisiejsza_data": date.today().isoformat(),
        },
    )


@router.get("/szybki-zapis")
def widok_szybki_zapis(
    request: Request,
    lekarz_id: int | None = None,
    db: Session = Depends(get_db),
):
    return templates.TemplateResponse(
        request,
        "szybki_zapis.html",
        przygotuj_kontekst_szybkiego_zapisu(lekarz_id=lekarz_id, db=db),
    )


@router.post("/szybki-zapis")
async def zapisz_szybki_zapis(request: Request, db: Session = Depends(get_db)):
    pacjent_id = 1
    dane_formularza = parse_qs((await request.body()).decode("utf-8"))

    try:
        lekarz_id = int(dane_formularza["lekarz_id"][0])
        data = dane_formularza["data"][0].strip()
        godzina = dane_formularza["godzina"][0].strip()
        tryb_wizyty = dane_formularza.get("tryb_wizyty", ["stacjonarnie"])[0].strip()
    except (KeyError, IndexError, ValueError):
        return templates.TemplateResponse(
            request,
            "szybki_zapis.html",
            przygotuj_kontekst_szybkiego_zapisu(
                "Nie udało się odczytać danych formularza.",
                db=db,
            ),
            status_code=400,
        )

    try:
        utworz_wizyte(
            pacjent_id=pacjent_id,
            lekarz_id=lekarz_id,
            data=data,
            godzina=godzina,
            notatka=f"Wizyta umówiona przez szybki zapis. Tryb wizyty: {tryb_wizyty}",
            db=db,
        )
    except PacjentNieIstnieje:
        blad = "Nie znaleziono pacjenta."
    except LekarzNieIstnieje:
        blad = "Wybrany lekarz nie istnieje."
    except NiepoprawnyTermin:
        blad = "Niepoprawny format daty lub godziny wizyty."
    except TerminWPrzeszlosci:
        blad = "Nie można umówić wizyty w przeszłości."
    except TerminZajety:
        blad = "Ten termin jest już zajęty. Wybierz inny termin."
    else:
        return przekieruj_do_wizyt("wizyta_dodana")

    return templates.TemplateResponse(
        request,
        "szybki_zapis.html",
        przygotuj_kontekst_szybkiego_zapisu(blad, db=db),
        status_code=400,
    )


@router.post("/moje-wizyty/{wizyta_id}/odwolaj")
async def odwolaj_wizyte_html(
    wizyta_id: int,
    db: Session = Depends(get_db),
):
    pacjent_id = 1

    try:
        odwolaj_wizyte(wizyta_id, pacjent_id, db)
    except (
        WizytaNieIstnieje,
        BrakDostepuDoWizyty,
        WizytaNieaktywna,
        TerminWPrzeszlosci,
    ) as blad:
        return przekieruj_do_wizyt(status_wizyty_z_wyjatku(blad))

    return przekieruj_do_wizyt("wizyta_odwolana")


@router.post("/moje-wizyty/{wizyta_id}/przesun")
async def przesun_wizyte_html(
    wizyta_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    pacjent_id = 1
    dane_formularza = parse_qs((await request.body()).decode("utf-8"))

    try:
        data = dane_formularza["data"][0].strip()
        godzina = dane_formularza["godzina"][0].strip()
    except (KeyError, IndexError):
        return przekieruj_do_wizyt("niepoprawny_termin")

    try:
        przesun_wizyte(
            wizyta_id=wizyta_id,
            pacjent_id=pacjent_id,
            data=data,
            godzina=godzina,
            db=db,
        )
    except (
        WizytaNieIstnieje,
        BrakDostepuDoWizyty,
        WizytaNieaktywna,
        NiepoprawnyTermin,
        TerminWPrzeszlosci,
        TerminZajety,
    ) as blad:
        return przekieruj_do_wizyt(status_wizyty_z_wyjatku(blad))

    return przekieruj_do_wizyt("wizyta_przesunieta")


@router.get("/recepty")
def widok_recepty(request: Request, db: Session = Depends(get_db)):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)
    recepty = pobierz_recepty_pacjenta(pacjent_id, db)
    apteki = pobierz_apteki(db)
    licznik_recept = {
        "aktywne": len([recepta for recepta in recepty if recepta["status"] == "aktywne"]),
        "wygasajace": len([recepta for recepta in recepty if recepta["status"] == "wygasajace"]),
        "archiwum": len([recepta for recepta in recepty if recepta["status"] == "archiwum"]),
    }

    return templates.TemplateResponse(
        request,
        "recepty.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "recepty",
            "recepty_pacjenta": recepty,
            "licznik_recept": licznik_recept,
            "apteki": apteki,
        },
    )


@router.get("/lekarze-widok")
def widok_lekarze(request: Request, objawy_status: str | None = None, db: Session = Depends(get_db)):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)
    komunikat_sukcesu = None
    komunikat_bledu = None

    if objawy_status == "zapisane":
        komunikat_sukcesu = "Opis objawów został zapisany. System podpowiedział specjalizację na podstawie zgłoszenia."
    elif objawy_status == "brak_danych":
        komunikat_bledu = "Zaznacz objaw albo wpisz krótki opis dolegliwości."
    elif objawy_status == "blad_mongo":
        komunikat_bledu = "Nie udało się zapisać objawów w MongoDB. Sprawdź, czy baza jest uruchomiona."

    return templates.TemplateResponse(
        request,
        "lekarze.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "lekarze",
            "lekarze": pobierz_wszystkich_lekarzy(db),
            "placowki": pobierz_placowki(db),
            "ostatnie_zgloszenie_objawow": pobierz_ostatnie_zgloszenie_objawow(pacjent_id),
            "komunikat_sukcesu": komunikat_sukcesu,
            "komunikat_bledu": komunikat_bledu,
        },
    )


@router.post("/lekarze-widok/objawy")
async def zapisz_objawy_pacjenta(request: Request):
    pacjent_id = 1
    dane_formularza = parse_qs((await request.body()).decode("utf-8"))
    objawy = dane_formularza.get("objawy", [])
    opis = dane_formularza.get("opis", [""])[0]
    pilnosc = dane_formularza.get("pilnosc", ["standardowa"])[0]

    try:
        zapisz_zgloszenie_objawow(
            pacjent_id=pacjent_id,
            objawy=objawy,
            opis=opis,
            pilnosc=pilnosc,
        )
    except ValueError:
        status = "brak_danych"
    except RuntimeError:
        status = "blad_mongo"
    else:
        status = "zapisane"

    return RedirectResponse(
        url=f"/lekarze-widok?objawy_status={status}",
        status_code=303,
    )


@router.get("/leki")
def widok_leki(request: Request, status: str | None = None, db: Session = Depends(get_db)):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)
    leki = pobierz_leki_pacjenta(pacjent_id, db)
    komunikat_sukcesu = None
    komunikat_bledu = None

    if status == "lek_dodany":
        komunikat_sukcesu = "Lek został dodany do listy pacjenta."
    elif status == "niepoprawny_lek":
        komunikat_bledu = "Uzupełnij nazwę leku i dawkowanie."

    return templates.TemplateResponse(
        request,
        "leki.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "leki",
            "leki_pacjenta": leki,
            "harmonogram_lekow": przygotuj_harmonogram_lekow(leki),
            "komunikat_sukcesu": komunikat_sukcesu,
            "komunikat_bledu": komunikat_bledu,
        },
    )


@router.post("/leki/dodaj")
async def dodaj_lek_html(request: Request, db: Session = Depends(get_db)):
    pacjent_id = 1
    dane_formularza = parse_qs((await request.body()).decode("utf-8"))
    nazwa = dane_formularza.get("nazwa", [""])[0].strip()
    dawkowanie = dane_formularza.get("dawkowanie", [""])[0].strip()
    zalecenie = dane_formularza.get("zalecenie", [""])[0].strip()

    if not nazwa or not dawkowanie:
        return RedirectResponse(url="/leki?status=niepoprawny_lek", status_code=303)

    dodaj_lek_pacjenta(
        pacjent_id=pacjent_id,
        nazwa=nazwa,
        dawkowanie=dawkowanie,
        zalecenie=zalecenie,
        db=db,
    )

    return RedirectResponse(url="/leki?status=lek_dodany", status_code=303)


@router.get("/apteki")
def widok_apteki(request: Request, db: Session = Depends(get_db)):
    return widok_leki(request, db)


@router.get("/historia")
def widok_historia(request: Request, db: Session = Depends(get_db)):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)
    wpisy_historii = pobierz_historie_medyczna_pacjenta(pacjent_id, db)[:3]

    return templates.TemplateResponse(
        request,
        "historia.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "historia",
            "historia_medyczna": wpisy_historii,
        },
    )


@router.get("/profil")
def widok_profil(request: Request, db: Session = Depends(get_db)):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)
    plan_opieki = pobierz_plan_opieki_pacjenta(pacjent_id, db)
    moje_wizyty = pobierz_wizyty_pacjenta(pacjent_id, db)
    nadchodzace_wizyty = pobierz_nadchodzace_wizyty(moje_wizyty)
    najblizsza_wizyta = znajdz_najblizsza_wizyte(nadchodzace_wizyty)
    ostatnie_wizyty = sorted(
        moje_wizyty,
        key=lambda wizyta: wizyta["data"],
        reverse=True,
    )[:3]

    return templates.TemplateResponse(
        request,
        "profil.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "profil",
            "najblizsza_wizyta": najblizsza_wizyta,
            "ostatnie_wizyty": ostatnie_wizyty,
            "plan_opieki": plan_opieki,
        },
    )


@router.get("/ustawienia")
def widok_ustawienia(request: Request, db: Session = Depends(get_db)):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id, db)

    return templates.TemplateResponse(
        request,
        "ustawienia.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "ustawienia",
        },
    )

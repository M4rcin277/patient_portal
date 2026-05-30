from datetime import date
from urllib.parse import parse_qs

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.dane import (
    apteki,
    godziny_przyjec,
    harmonogram_lekow,
    historia_medyczna,
    lekarze,
    leki_pacjenta,
    plan_opieki,
    recepty_pacjenta,
)
from app.pomocnicy import (
    pobierz_nadchodzace_wizyty,
    pobierz_wizyty_pacjenta,
    przygotuj_historie_medyczna,
    przygotuj_kalendarz_wizyt,
    znajdz_najblizsza_wizyte,
    znajdz_pacjenta,
)
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


@router.get("/panel-pacjenta")
def panel_pacjenta(
    request: Request,
    rok: int | None = None,
    miesiac: int | None = None,
):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)
    moje_wizyty = pobierz_wizyty_pacjenta(pacjent_id)
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
):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)
    moje_wizyty = pobierz_wizyty_pacjenta(pacjent_id)
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
def widok_szybki_zapis(request: Request, lekarz_id: int | None = None):
    return templates.TemplateResponse(
        request,
        "szybki_zapis.html",
        przygotuj_kontekst_szybkiego_zapisu(lekarz_id=lekarz_id),
    )


@router.post("/szybki-zapis")
async def zapisz_szybki_zapis(request: Request):
    pacjent_id = 1
    dane_formularza = parse_qs((await request.body()).decode("utf-8"))

    try:
        lekarz_id = int(dane_formularza["lekarz_id"][0])
        data = dane_formularza["data"][0].strip()
        godzina = dane_formularza["godzina"][0].strip()
    except (KeyError, IndexError, ValueError):
        return templates.TemplateResponse(
            request,
            "szybki_zapis.html",
            przygotuj_kontekst_szybkiego_zapisu(
                "Nie udało się odczytać danych formularza."
            ),
            status_code=400,
        )

    try:
        utworz_wizyte(
            pacjent_id=pacjent_id,
            lekarz_id=lekarz_id,
            data=data,
            godzina=godzina,
            notatka="Wizyta umówiona przez szybki zapis",
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
        przygotuj_kontekst_szybkiego_zapisu(blad),
        status_code=400,
    )


@router.post("/moje-wizyty/{wizyta_id}/odwolaj")
async def odwolaj_wizyte_html(wizyta_id: int):
    pacjent_id = 1

    try:
        odwolaj_wizyte(wizyta_id, pacjent_id)
    except (
        WizytaNieIstnieje,
        BrakDostepuDoWizyty,
        WizytaNieaktywna,
        TerminWPrzeszlosci,
    ) as blad:
        return przekieruj_do_wizyt(status_wizyty_z_wyjatku(blad))

    return przekieruj_do_wizyt("wizyta_odwolana")


@router.post("/moje-wizyty/{wizyta_id}/przesun")
async def przesun_wizyte_html(wizyta_id: int, request: Request):
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
def widok_recepty(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return templates.TemplateResponse(
        request,
        "recepty.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "recepty",
            "recepty_pacjenta": recepty_pacjenta,
            "apteki": apteki,
        },
    )


@router.get("/lekarze-widok")
def widok_lekarze(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return templates.TemplateResponse(
        request,
        "lekarze.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "lekarze",
            "lekarze": lekarze,
        },
    )


@router.get("/leki")
def widok_leki(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return templates.TemplateResponse(
        request,
        "leki.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "leki",
            "leki_pacjenta": leki_pacjenta,
            "harmonogram_lekow": harmonogram_lekow,
        },
    )


@router.get("/apteki")
def widok_apteki(request: Request):
    return widok_leki(request)


@router.get("/historia")
def widok_historia(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)
    wpisy_historii = przygotuj_historie_medyczna(historia_medyczna)[:3]

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
def widok_profil(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)
    moje_wizyty = pobierz_wizyty_pacjenta(pacjent_id)
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
def widok_ustawienia(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return templates.TemplateResponse(
        request,
        "ustawienia.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "ustawienia",
        },
    )

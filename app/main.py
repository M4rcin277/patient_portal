from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
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
    wizyty,
)

from app.pomocnicy import (
    pobierz_wolne_godziny,
    pobierz_nadchodzace_wizyty,
    pobierz_wizyty_pacjenta,
    przygotuj_historie_medyczna,
    przygotuj_kalendarz_wizyt,
    termin_jest_zajety,
    znajdz_najblizsza_wizyte,
    znajdz_lekarza,
    znajdz_pacjenta,
)
from app.schematy import NowaWizyta

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.get("/panel-pacjenta")
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
        },
    )


@app.get("/moje-wizyty")
def widok_moje_wizyty(
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
        moje_wizyty,
        najblizsza_wizyta,
        rok,
        miesiac,
    )

    return templates.TemplateResponse(
        request,
        "moje_wizyty.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "wizyty",
            "nadchodzace_wizyty": nadchodzace_wizyty,
            "najblizsza_wizyta": najblizsza_wizyta,
            "kalendarz_wizyt": kalendarz_wizyt,
        },
    )


@app.get("/szybki-zapis")
def widok_szybki_zapis(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return templates.TemplateResponse(
        request,
        "szybki_zapis.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "szybki_zapis",
            "lekarze": lekarze,
            "godziny_przyjec": godziny_przyjec,
        },
    )


@app.get("/recepty")
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


@app.get("/lekarze-widok")
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


@app.get("/leki")
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


@app.get("/apteki")
def widok_apteki(request: Request):
    return widok_leki(request)


@app.get("/historia")
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


@app.get("/profil")
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


@app.get("/ustawienia")
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


@app.get("/")
def strona_glowna():
    return {"wiadomosc": "Portal Pacjenta dziala"}


@app.get("/status")
def sprawdz_status():
    return {"status": "ok"}


@app.get("/lekarze")
def pobierz_lekarzy():
    return lekarze


@app.get("/lekarze/{lekarz_id}/wolne-terminy")
def pobierz_wolne_terminy(lekarz_id: int, data: str):
    lekarz = znajdz_lekarza(lekarz_id)

    if lekarz is None:
        raise HTTPException(
            status_code=404,
            detail="Lekarz o podanym id nie istnieje",
        )

    wolne_godziny = pobierz_wolne_godziny(lekarz_id, data)

    return {
        "lekarz_id": lekarz_id,
        "data": data,
        "wolne_godziny": wolne_godziny,
    }


@app.get("/wizyty")
def pobierz_wizyty():
    return wizyty


@app.post("/wizyty")
def dodaj_wizyte(nowa_wizyta: NowaWizyta):
    pacjent = znajdz_pacjenta(nowa_wizyta.pacjent_id)
    lekarz = znajdz_lekarza(nowa_wizyta.lekarz_id)

    if pacjent is None:
        raise HTTPException(
            status_code=404,
            detail="Pacjent o podanym id nie istnieje",
        )

    if lekarz is None:
        raise HTTPException(
            status_code=404,
            detail="Lekarz o podanym id nie istnieje",
        )

    if termin_jest_zajety(
        nowa_wizyta.lekarz_id,
        nowa_wizyta.data,
        nowa_wizyta.godzina,
    ):
        raise HTTPException(
            status_code=409,
            detail="Ten termin jest juz zajety",
        )

    wizyta = {
        "id": len(wizyty) + 1,
        "pacjent_id": nowa_wizyta.pacjent_id,
        "lekarz_id": nowa_wizyta.lekarz_id,
        "data": nowa_wizyta.data,
        "godzina": nowa_wizyta.godzina,
        "status": "zaplanowana",
        "notatka": nowa_wizyta.notatka,
    }

    wizyty.append(wizyta)

    return wizyta


@app.get("/pacjenci/ja")
def pobierz_moj_profil():
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return pacjent


@app.get("/pacjenci/ja/wizyty")
def pobierz_moje_wizyty():
    pacjent_id = 1
    return pobierz_wizyty_pacjenta(pacjent_id)

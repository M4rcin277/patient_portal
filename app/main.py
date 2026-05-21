from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.dane import (
    apteki,
    godziny_przyjec,
    historia_medyczna,
    lekarze,
    plan_opieki,
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
            "plan_opieki": plan_opieki,
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


@app.get("/apteki")
def widok_apteki(request: Request):
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return templates.TemplateResponse(
        request,
        "apteki.html",
        {
            "pacjent": pacjent,
            "aktywna_strona": "apteki",
            "apteki": apteki,
        },
    )


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

from fastapi import APIRouter, HTTPException

from app.dane import lekarze, wizyty
from app.pomocnicy import (
    pobierz_wizyty_pacjenta,
    pobierz_wolne_godziny,
    znajdz_lekarza,
    znajdz_pacjenta,
)
from app.schematy import NowaWizyta, PrzesuniecieWizyty
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


def blad_wizyty_http(wyjatek):
    if isinstance(wyjatek, PacjentNieIstnieje):
        return HTTPException(
            status_code=404,
            detail="Pacjent o podanym id nie istnieje",
        )
    if isinstance(wyjatek, LekarzNieIstnieje):
        return HTTPException(
            status_code=404,
            detail="Lekarz o podanym id nie istnieje",
        )
    if isinstance(wyjatek, WizytaNieIstnieje):
        return HTTPException(status_code=404, detail="Wizyta nie istnieje")
    if isinstance(wyjatek, BrakDostepuDoWizyty):
        return HTTPException(status_code=403, detail="Brak dostepu do wizyty")
    if isinstance(wyjatek, WizytaNieaktywna):
        return HTTPException(status_code=409, detail="Wizyta jest juz nieaktywna")
    if isinstance(wyjatek, NiepoprawnyTermin):
        return HTTPException(
            status_code=400,
            detail="Niepoprawny format daty lub godziny",
        )
    if isinstance(wyjatek, TerminWPrzeszlosci):
        return HTTPException(
            status_code=400,
            detail="Nie mozna wybrac terminu w przeszlosci",
        )
    if isinstance(wyjatek, TerminZajety):
        return HTTPException(status_code=409, detail="Ten termin jest juz zajety")

    return HTTPException(status_code=400, detail="Niepoprawne dane wizyty")


@router.get("/")
def strona_glowna():
    return {"wiadomosc": "Portal Pacjenta dziala"}


@router.get("/status")
def sprawdz_status():
    return {"status": "ok"}


@router.get("/lekarze")
def pobierz_lekarzy():
    return lekarze


@router.get("/lekarze/{lekarz_id}/wolne-terminy")
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


@router.get("/wizyty")
def pobierz_wizyty():
    return wizyty


@router.post("/wizyty")
def dodaj_wizyte(nowa_wizyta: NowaWizyta):
    try:
        return utworz_wizyte(
            pacjent_id=nowa_wizyta.pacjent_id,
            lekarz_id=nowa_wizyta.lekarz_id,
            data=nowa_wizyta.data,
            godzina=nowa_wizyta.godzina,
            notatka=nowa_wizyta.notatka,
        )
    except (
        PacjentNieIstnieje,
        LekarzNieIstnieje,
        NiepoprawnyTermin,
        TerminWPrzeszlosci,
        TerminZajety,
    ) as blad:
        raise blad_wizyty_http(blad)


@router.post("/wizyty/{wizyta_id}/odwolaj")
def odwolaj_moja_wizyte(wizyta_id: int):
    pacjent_id = 1

    try:
        return odwolaj_wizyte(wizyta_id, pacjent_id)
    except (
        WizytaNieIstnieje,
        BrakDostepuDoWizyty,
        WizytaNieaktywna,
        TerminWPrzeszlosci,
    ) as blad:
        raise blad_wizyty_http(blad)


@router.post("/wizyty/{wizyta_id}/przesun")
def przesun_moja_wizyte(wizyta_id: int, przesuniecie: PrzesuniecieWizyty):
    pacjent_id = 1

    try:
        return przesun_wizyte(
            wizyta_id=wizyta_id,
            pacjent_id=pacjent_id,
            data=przesuniecie.data,
            godzina=przesuniecie.godzina,
        )
    except (
        WizytaNieIstnieje,
        BrakDostepuDoWizyty,
        WizytaNieaktywna,
        NiepoprawnyTermin,
        TerminWPrzeszlosci,
        TerminZajety,
    ) as blad:
        raise blad_wizyty_http(blad)


@router.get("/pacjenci/ja")
def pobierz_moj_profil():
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return pacjent


@router.get("/pacjenci/ja/wizyty")
def pobierz_moje_wizyty():
    pacjent_id = 1
    return pobierz_wizyty_pacjenta(pacjent_id)

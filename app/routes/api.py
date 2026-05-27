from fastapi import APIRouter, HTTPException

from app.dane import lekarze, wizyty
from app.pomocnicy import (
    pobierz_wizyty_pacjenta,
    pobierz_wolne_godziny,
    termin_jest_zajety,
    znajdz_lekarza,
    znajdz_pacjenta,
)
from app.schematy import NowaWizyta

router = APIRouter()


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


@router.get("/pacjenci/ja")
def pobierz_moj_profil():
    pacjent_id = 1
    pacjent = znajdz_pacjenta(pacjent_id)

    return pacjent


@router.get("/pacjenci/ja/wizyty")
def pobierz_moje_wizyty():
    pacjent_id = 1
    return pobierz_wizyty_pacjenta(pacjent_id)

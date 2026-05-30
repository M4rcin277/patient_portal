from app.dane import lekarze


def pobierz_wszystkich_lekarzy():
    return lekarze


def znajdz_lekarza(lekarz_id: int):
    for lekarz in lekarze:
        if lekarz["id"] == lekarz_id:
            return lekarz

    return None

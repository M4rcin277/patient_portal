from app.dane import pacjenci


def znajdz_pacjenta(pacjent_id: int):
    for pacjent in pacjenci:
        if pacjent["id"] == pacjent_id:
            return pacjent

    return None

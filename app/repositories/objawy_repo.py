from datetime import datetime, timezone
from unicodedata import normalize

from app.mongo import pobierz_baze_mongo

try:
    from pymongo.errors import PyMongoError
except ImportError:
    PyMongoError = RuntimeError


SYMPTOM_REPORTS_COLLECTION = "symptom_reports"


def zasugeruj_specjalizacje(objawy: list[str], opis: str):
    tekst = normalize("NFKD", " ".join([*objawy, opis]).lower()).encode("ascii", "ignore").decode("ascii")
    punkty = {
        "Kardiolog": 0,
        "Dermatolog": 0,
        "Ortopeda": 0,
        "Internista": 0,
    }

    if any(slowo in tekst for slowo in ["serce", "klatka", "klatce", "cisnienie", "dusznosc", "duszno"]):
        punkty["Kardiolog"] += 1
    if any(slowo in tekst for slowo in ["skora", "skory", "wysypka", "swiad", "swedzenie", "znamie", "alergia"]):
        punkty["Dermatolog"] += 1
    if any(slowo in tekst for slowo in ["kolano", "plecy", "staw", "uraz", "zlamanie", "bol miesni"]):
        punkty["Ortopeda"] += 1
    if any(slowo in tekst for slowo in ["goraczka", "oslabienie", "kaszel", "bol glowy", "brzuch"]):
        punkty["Internista"] += 1

    dopasowania = [specjalizacja for specjalizacja, liczba_punktow in punkty.items() if liczba_punktow > 0]

    if len(dopasowania) > 1:
        return "Lekarz rodzinny"
    if len(dopasowania) == 1:
        return dopasowania[0]

    return "Lekarz rodzinny"


def zamien_zgloszenie_na_slownik(zgloszenie):
    if not zgloszenie:
        return None

    return {
        "id": str(zgloszenie["_id"]),
        "pacjent_id": zgloszenie["pacjent_id"],
        "objawy": zgloszenie.get("objawy", []),
        "opis": zgloszenie.get("opis", ""),
        "pilnosc": zgloszenie.get("pilnosc", "standardowa"),
        "sugerowana_specjalizacja": zgloszenie.get("sugerowana_specjalizacja", "Internista"),
        "utworzono": zgloszenie.get("utworzono"),
    }


def zapisz_zgloszenie_objawow(pacjent_id: int, objawy: list[str], opis: str, pilnosc: str):
    czyste_objawy = [objaw.strip() for objaw in objawy if objaw.strip()]
    czysty_opis = opis.strip()
    czysta_pilnosc = pilnosc.strip() or "standardowa"

    if not czyste_objawy and not czysty_opis:
        raise ValueError("Trzeba podać przynajmniej jeden objaw albo opis.")

    dokument = {
        "pacjent_id": pacjent_id,
        "objawy": czyste_objawy,
        "opis": czysty_opis,
        "pilnosc": czysta_pilnosc,
        "sugerowana_specjalizacja": zasugeruj_specjalizacje(czyste_objawy, czysty_opis),
        "status": "nowe",
        "utworzono": datetime.now(timezone.utc),
    }

    try:
        baza = pobierz_baze_mongo()
        wynik = baza[SYMPTOM_REPORTS_COLLECTION].insert_one(dokument)
    except PyMongoError as exc:
        raise RuntimeError("Nie udało się zapisać zgłoszenia objawów w MongoDB.") from exc

    dokument["_id"] = wynik.inserted_id

    return zamien_zgloszenie_na_slownik(dokument)


def pobierz_ostatnie_zgloszenie_objawow(pacjent_id: int):
    try:
        baza = pobierz_baze_mongo()
        zgloszenie = baza[SYMPTOM_REPORTS_COLLECTION].find_one(
            {"pacjent_id": pacjent_id},
            sort=[("utworzono", -1)],
        )
    except (RuntimeError, PyMongoError):
        return None

    return zamien_zgloszenie_na_slownik(zgloszenie)

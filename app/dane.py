pacjenci = [
    {
        "id": 1,
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "email": "jan.kowalski@example.com",
        "telefon": "123456789",
        "data_urodzenia": "1995-04-12",
        "adres": "ul. Zdrowa 10, Warszawa",
    },
    {
        "id": 2,
        "imie": "Maria",
        "nazwisko": "Nowak",
        "email": "maria.nowak@example.com",
        "telefon": "987654321",
        "data_urodzenia": "1988-09-20",
        "adres": "ul. Lekarska 5, Krakow",
    },
]


lekarze = [
    {
        "id": 1,
        "imie": "Anna",
        "nazwisko": "Kowalska",
        "specjalizacja": "Kardiolog",
        "miasto": "Warszawa",
        "lokalizacja": "Centrum Medyczne Zdrowie, Warszawa",
    },
    {
        "id": 2,
        "imie": "Piotr",
        "nazwisko": "Nowak",
        "specjalizacja": "Dermatolog",
        "miasto": "Krakow",
        "lokalizacja": "Przychodnia Derm-Med, Kraków",
    },
]


godziny_przyjec = [
    "09:00",
    "09:30",
    "10:00",
    "10:30",
    "11:00",
    "11:30",
    "12:00",
]


wizyty = [
    {
        "id": 1,
        "pacjent_id": 1,
        "lekarz_id": 1,
        "data": "2026-06-10",
        "godzina": "10:30",
        "status": "zaplanowana",
        "notatka": "Kontrola po badaniach",
    },
    {
        "id": 2,
        "pacjent_id": 1,
        "lekarz_id": 2,
        "data": "2026-07-02",
        "godzina": "14:00",
        "status": "zaplanowana",
        "notatka": "Konsultacja dermatologiczna",
    },
    {
        "id": 3,
        "pacjent_id": 2,
        "lekarz_id": 1,
        "data": "2026-07-05",
        "godzina": "09:00",
        "status": "zaplanowana",
        "notatka": "Wizyta kontrolna",
    },
]


plan_opieki = [
    {
        "ikona": "bi-clipboard-pulse",
        "data": "20.06.2026",
        "podpis": "ważna do",
        "tytul": "Aktywne recepty",
        "opis": "Polocard 75 mg, Metformina 500 mg",
        "etykieta": "2 aktywne",
    },
    {
        "ikona": "bi-capsule",
        "data": "codziennie",
        "podpis": "rano",
        "tytul": "Przypisane leki",
        "opis": "Polocard 75 mg, Metformina 500 mg",
        "etykieta": "2 leki",
    },
    {
        "ikona": "bi-journal-medical",
        "data": "przed wizytą",
        "podpis": "zalecenie",
        "tytul": "Zalecenia lekarza",
        "opis": "Wykonać morfologię krwi",
        "etykieta": "2 nowe",
    },
    {
        "ikona": "bi-activity",
        "data": "co tydzień",
        "podpis": "kontrola",
        "tytul": "Pomiar ciśnienia",
        "opis": "2 razy w tygodniu",
        "etykieta": "zadanie",
    },
]


apteki = [
    {
        "id": 1,
        "nazwa": "Apteka Zdrowie",
        "adres": "ul. Zdrowa 12, Warszawa",
        "godziny": "08:00-20:00",
    },
    {
        "id": 2,
        "nazwa": "Apteka Centrum",
        "adres": "ul. Prosta 4, Warszawa",
        "godziny": "07:00-22:00",
    },
    {
        "id": 3,
        "nazwa": "Apteka Dyżurna",
        "adres": "ul. Nocna 8, Warszawa",
        "godziny": "całodobowo",
    },
]


historia_medyczna = [
    {
        "data": "2026-03-12",
        "lekarz": "Anna Kowalska",
        "typ": "Badanie",
        "tytul": "Badanie kontrolne",
        "opis": "Omówienie wyników morfologii krwi.",
        "etykieta": "wyniki omówione",
        "ikona": "bi-clipboard2-pulse",
    },
    {
        "data": "2026-02-02",
        "lekarz": "Piotr Nowak",
        "typ": "Konsultacja",
        "tytul": "Konsultacja kardiologiczna",
        "opis": "Zalecenie regularnego pomiaru ciśnienia.",
        "etykieta": "zalecenia",
        "ikona": "bi-heart-pulse",
    },
    {
        "data": "2026-01-15",
        "lekarz": "Marta Wiśniewska",
        "typ": "Wizyta",
        "tytul": "Wizyta internistyczna",
        "opis": "Kontrola samopoczucia i aktualizacja planu leczenia.",
        "etykieta": "kontrola",
        "ikona": "bi-journal-medical",
    },
]

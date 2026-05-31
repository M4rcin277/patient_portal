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
        "tryb_wizyty": "Stacjonarna, Online",
    },
    {
        "id": 2,
        "imie": "Piotr",
        "nazwisko": "Nowak",
        "specjalizacja": "Dermatolog",
        "miasto": "Krakow",
        "lokalizacja": "Przychodnia Derm-Med, Kraków",
        "tryb_wizyty": "Stacjonarna",
    },
    {
        "id": 3,
        "imie": "Michał",
        "nazwisko": "Wiśniewski",
        "specjalizacja": "Ortopeda",
        "miasto": "Warszawa",
        "lokalizacja": "Centrum Ortopedyczne, Warszawa",
        "tryb_wizyty": "Stacjonarna",
    },
    {
        "id": 4,
        "imie": "Karolina",
        "nazwisko": "Maj",
        "specjalizacja": "Internista",
        "miasto": "Warszawa",
        "lokalizacja": "Centrum Medyczne Zdrowie, Warszawa",
        "tryb_wizyty": "Stacjonarna, Online",
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


recepty_pacjenta = [
    {
        "id": 1,
        "lekarz": "Anna Kowalska",
        "wystawiono": "10.05.2026",
        "wazna_do": "10.06.2026",
        "dni": "21 dni",
        "liczba_lekow": 2,
        "kolor": "purple",
        "ikona": "bi-capsule",
    },
    {
        "id": 2,
        "lekarz": "Piotr Nowak",
        "wystawiono": "12.05.2026",
        "wazna_do": "25.05.2026",
        "dni": "5 dni",
        "liczba_lekow": 1,
        "kolor": "green",
        "ikona": "bi-capsule",
    },
    {
        "id": 3,
        "lekarz": "Anna Kowalska",
        "wystawiono": "05.05.2026",
        "wazna_do": "07.06.2026",
        "dni": "18 dni",
        "liczba_lekow": 3,
        "kolor": "blue",
        "ikona": "bi-prescription2",
    },
    {
        "id": 4,
        "lekarz": "Michał Wiśniewski",
        "wystawiono": "02.05.2026",
        "wazna_do": "20.05.2026",
        "dni": "1 dzień",
        "liczba_lekow": 1,
        "kolor": "yellow",
        "ikona": "bi-file-earmark-medical",
    },
    {
        "id": 5,
        "lekarz": "Anna Kowalska",
        "wystawiono": "30.04.2026",
        "wazna_do": "15.06.2026",
        "dni": "26 dni",
        "liczba_lekow": 2,
        "kolor": "violet",
        "ikona": "bi-eyedropper",
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


leki_pacjenta = [
    {
        "id": 1,
        "nazwa": "Polocard 75 mg",
        "substancja": "kwas acetylosalicylowy",
        "dawkowanie": "1 tabletka rano",
        "zalecenie": "Przyjmować po śniadaniu, popić wodą.",
        "lekarz": "Anna Kowalska",
        "status": "Aktywny",
        "do_kiedy": "20.06.2026",
        "ikona": "bi-capsule",
        "kolor": "blue",
    },
    {
        "id": 2,
        "nazwa": "Metformina 500 mg",
        "substancja": "metformina",
        "dawkowanie": "1 tabletka wieczorem",
        "zalecenie": "Przyjmować w trakcie kolacji.",
        "lekarz": "Anna Kowalska",
        "status": "Aktywny",
        "do_kiedy": "bez terminu",
        "ikona": "bi-prescription2",
        "kolor": "green",
    },
    {
        "id": 3,
        "nazwa": "Witamina D3 2000 IU",
        "substancja": "cholekalcyferol",
        "dawkowanie": "1 kapsułka dziennie",
        "zalecenie": "Przyjmować razem z posiłkiem.",
        "lekarz": "Piotr Nowak",
        "status": "Aktywny",
        "do_kiedy": "30.07.2026",
        "ikona": "bi-droplet",
        "kolor": "yellow",
    },
]


harmonogram_lekow = [
    {
        "pora": "Rano",
        "godzina": "08:00",
        "leki": "Polocard 75 mg",
        "status": "Do przyjęcia",
    },
    {
        "pora": "Południe",
        "godzina": "13:00",
        "leki": "Witamina D3 2000 IU",
        "status": "Zaplanowane",
    },
    {
        "pora": "Wieczór",
        "godzina": "20:00",
        "leki": "Metformina 500 mg",
        "status": "Zaplanowane",
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

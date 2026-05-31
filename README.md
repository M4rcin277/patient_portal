# Portal Pacjenta

Aplikacja webowa tworzona jako projekt portfolio Junior Python Developer.

Celem projektu jest stworzenie prostego portalu pacjenta z widokami renderowanymi po stronie backendu. Aplikacja nie używa Reacta ani Node jako głównego frontendu. HTML jest generowany przez FastAPI i Jinja2.

---

## Technologie

- Python
- FastAPI
- Jinja2
- Bootstrap 5
- Bootstrap Icons
- SQLAlchemy
- SQLite lokalnie jako etap przygotowania bazy
- PostgreSQL w późniejszym etapie
- Docker w późniejszym etapie
- GitHub, branche i Pull Requesty

---

## Aktualny etap projektu

Projekt ma działający backend FastAPI, wspólny layout Jinja2 oraz widoki pacjenta renderowane po stronie serwera.

Aktualnie zrobione są między innymi:

- panel pacjenta z podsumowaniem wizyt i planem opieki,
- górna nawigacja wspólna dla widoków pacjenta,
- profil pacjenta,
- widok moich wizyt z kalendarzem i listami wizyt,
- szybki zapis z realnym formularzem zapisu wizyty,
- walidacja zapisu wizyty:
  - pacjent musi istnieć,
  - lekarz musi istnieć,
  - termin nie może być w przeszłości,
  - termin nie może być zajęty,
  - data i godzina muszą mieć poprawny format,
- przesuwanie wizyty,
- odwoływanie wizyty,
- komunikaty sukcesu i błędów po akcjach na wizytach,
- ukrywanie zajętych terminów w szybkim zapisie,
- endpoint wolnych godzin lekarza,
- widok lekarzy,
- widok recept,
- widok leków,
- widok historii medycznej,
- widok ustawień.

Na tym etapie aplikacja czyta dane przez repozytoria z lokalnej bazy SQLite zarządzanej przez SQLAlchemy. Plik `app/seed_data.py` zawiera dane demo używane tylko przez skrypt seedujący bazę. Kolejnym większym krokiem będzie podmiana SQLite na PostgreSQL.

---

## Architektura projektu

Najważniejsze pliki i katalogi:

```text
app/
  main.py
  database.py
  init_db.py
  seed_db.py
  seed_data.py
  pomocnicy.py
  schematy.py

  routes/
    api.py
    strony.py

  services/
    wizyty.py
    szybki_zapis.py
    statusy_wizyt.py

  repositories/
    apteki_repo.py
    godziny_przyjec_repo.py
    historia_repo.py
    leki_repo.py
    pacjenci_repo.py
    lekarze_repo.py
    plan_opieki_repo.py
    recepty_repo.py
    wizyty_repo.py

  models/
    uzytkownik.py
    apteka.py
    godzina_przyjec.py
    pacjent.py
    pacjent_lek.py
    lekarz.py
    wizyta.py
    specjalizacja.py
    placowka.py
    plan_opieki.py
    recepta.py
    lek.py
    recepta_lek.py
    historia_medyczna.py

  templates/
    base.html
    panel_pacjent.html
    moje_wizyty.html
    szybki_zapis.html
    recepty.html
    leki.html
    lekarze.html
    historia.html
    profil.html
    ustawienia.html

  static/
    css/
      app.css
    fonts/
    icons/
```

Podział odpowiedzialności:

- `main.py` tworzy aplikację FastAPI, podpina pliki statyczne i routery.
- `database.py` zawiera konfigurację SQLAlchemy: adres bazy, silnik połączenia, sesję i funkcję `get_db()`.
- `init_db.py` tworzy tabele w lokalnej bazie danych na podstawie modeli SQLAlchemy.
- `seed_db.py` dodaje do bazy dane startowe z `app/seed_data.py`.
- `seed_data.py` zawiera dane demo używane wyłącznie do wypełnienia pustej bazy.
- `routes/strony.py` obsługuje widoki HTML.
- `routes/api.py` obsługuje endpointy API zwracające JSON.
- `services/wizyty.py` zawiera logikę biznesową wizyt.
- `services/szybki_zapis.py` przygotowuje dane dla widoku szybkiego zapisu.
- `services/statusy_wizyt.py` mapuje błędy i statusy akcji na komunikaty dla widoków.
- `repositories/` zawiera funkcje dostępu do danych i komunikuje się z bazą przez SQLAlchemy.
- `models/` zawiera modele SQLAlchemy opisujące tabele bazy danych.
- `pomocnicy.py` zawiera funkcje pomocnicze do formatowania i przygotowywania danych pod widoki.
- `templates/` zawiera szablony Jinja2.
- `static/` zawiera CSS, fonty i grafiki.

---

## Endpointy HTML

```text
/panel-pacjenta
/moje-wizyty
/szybki-zapis
/recepty
/leki
/apteki
/lekarze-widok
/historia
/profil
/ustawienia
```

Akcje formularzy HTML:

```text
POST /szybki-zapis
POST /moje-wizyty/{wizyta_id}/odwolaj
POST /moje-wizyty/{wizyta_id}/przesun
```

---

## Endpointy API

```text
GET  /
GET  /status
GET  /lekarze
GET  /wizyty
POST /wizyty
POST /wizyty/{wizyta_id}/odwolaj
POST /wizyty/{wizyta_id}/przesun
GET  /pacjenci/ja
GET  /pacjenci/ja/wizyty
GET  /lekarze/{lekarz_id}/wolne-terminy?data=YYYY-MM-DD
```

Dokumentacja API jest dostępna pod:

```text
http://127.0.0.1:8000/docs
```

---

## Uruchomienie projektu lokalnie

### Aktywacja środowiska

```powershell
.\.venv\Scripts\activate
```

### Przygotowanie lokalnej bazy danych

```powershell
python -m app.init_db
python -m app.seed_db
```

`init_db` tworzy tabele w lokalnym pliku `patient_portal.db`, a `seed_db` wypełnia je danymi demonstracyjnymi z `app/seed_data.py`.

### Uruchomienie aplikacji

```powershell
uvicorn app.main:app --reload
```

### Adres lokalny

```text
http://127.0.0.1:8000
```

Najważniejsze widoki:

```text
http://127.0.0.1:8000/panel-pacjenta
http://127.0.0.1:8000/moje-wizyty
http://127.0.0.1:8000/szybki-zapis
http://127.0.0.1:8000/lekarze-widok
http://127.0.0.1:8000/recepty
http://127.0.0.1:8000/leki
http://127.0.0.1:8000/historia
http://127.0.0.1:8000/profil
```

---

## Planowane funkcjonalności

- podmiana lokalnego SQLite na PostgreSQL,
- migracje bazy danych, np. Alembic,
- logowanie użytkowników,
- odejście od tymczasowego `pacjent_id = 1`,
- panel lekarza,
- dalsza rozbudowa recept, leków i historii medycznej,
- wyszukiwarka i filtrowanie lekarzy,
- prawdziwe dane placówek i lokalizacji,
- Docker Compose,
- testy automatyczne,
- CI/CD GitHub Actions.

---

## Status projektu

Projekt jest rozwijany etapami. Obecny etap skupia się na działającym przepływie danych przez modele SQLAlchemy, repozytoria i lokalną bazę SQLite, aby później bezpiecznie przejść na PostgreSQL.

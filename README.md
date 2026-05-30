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

Na tym etapie dane są przechowywane tymczasowo w listach Pythonowych w `app/dane.py`. W kolejnych etapach zostaną przeniesione do PostgreSQL.

---

## Architektura projektu

Najważniejsze pliki i katalogi:

```text
app/
  main.py
  dane.py
  pomocnicy.py
  schematy.py

  routes/
    api.py
    strony.py

  services/
    wizyty.py
    szybki_zapis.py
    statusy_wizyt.py

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
- `routes/strony.py` obsługuje widoki HTML.
- `routes/api.py` obsługuje endpointy API zwracające JSON.
- `services/wizyty.py` zawiera logikę biznesową wizyt.
- `services/szybki_zapis.py` przygotowuje dane dla widoku szybkiego zapisu.
- `services/statusy_wizyt.py` mapuje błędy i statusy akcji na komunikaty dla widoków.
- `pomocnicy.py` zawiera funkcje pomocnicze do wyszukiwania i formatowania danych.
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

- dalsze porządkowanie struktury plików,
- przygotowanie danych pod przyszłe tabele w PostgreSQL,
- logowanie użytkowników,
- odejście od tymczasowego `pacjent_id = 1`,
- panel lekarza,
- rozbudowa recept i leków po zaprojektowaniu bazy danych,
- pełna historia medyczna pacjenta,
- wyszukiwarka i filtrowanie lekarzy,
- prawdziwe dane placówek i lokalizacji,
- PostgreSQL,
- Docker Compose,
- testy automatyczne,
- CI/CD GitHub Actions.

---

## Status projektu

Projekt jest rozwijany etapami. Obecny etap skupia się na dopracowaniu logiki wizyt, uporządkowaniu warstw aplikacji oraz przygotowaniu projektu do dalszego rozwoju backendu i bazy danych.

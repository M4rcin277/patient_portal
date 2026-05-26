# Portal Pacjenta

Aplikacja webowa tworzona jako projekt portfolio Junior Python Developer.

Celem projektu jest stworzenie systemu umożliwiającego:
- zarządzanie wizytami,
- podgląd profilu pacjenta,
- obsługę panelu pacjenta,
- wyszukiwanie lekarzy i aptek,
- obsługę historii medycznej i recept.

---

## Technologie

- Python
- FastAPI
- Jinja2
- Bootstrap 5
- Bootstrap Icons
- PostgreSQL w późniejszym etapie
- MongoDB w późniejszym etapie
- Docker w późniejszym etapie
- GitHub, branche i Pull Requesty

---

## Aktualny etap projektu

Projekt ma podstawowy backend FastAPI, wspólny layout Jinja2 oraz kilka widoków pacjenta renderowanych po stronie serwera.

Aktualnie dostępne są między innymi:
- endpoint statusu aplikacji,
- lista lekarzy,
- lista wizyt,
- dodawanie wizyty przez `POST /wizyty`,
- sprawdzanie, czy pacjent i lekarz istnieją,
- blokada dodania wizyty na zajęty termin,
- endpoint wolnych terminów lekarza,
- profil aktualnego pacjenta,
- wizyty aktualnego pacjenta,
- panel pacjenta z podsumowaniem wizyt,
- profil pacjenta dostępny z profilu w górnej nawigacji,
- wspólna górna nawigacja dla wszystkich widoków pacjenta,
- widok moich wizyt z kalendarzem,
- widok szybkiego zapisu z filtrowaniem po specjalizacji i mieście,
- widok historii medycznej jako stos 3 najnowszych wpisów,
- widoki recept, lekarzy, aptek i ustawień.

Na tym etapie dane są przechowywane tymczasowo w listach Pythonowych. W kolejnych etapach zostaną przeniesione do bazy danych.

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

---

## Adresy lokalne

Aplikacja:

```text
http://127.0.0.1:8000
```

Panel pacjenta:

```text
http://127.0.0.1:8000/panel-pacjenta
```

Najważniejsze widoki pacjenta:

```text
http://127.0.0.1:8000/moje-wizyty
http://127.0.0.1:8000/szybki-zapis
http://127.0.0.1:8000/historia
http://127.0.0.1:8000/profil
```

Dokumentacja API:

```text
http://127.0.0.1:8000/docs
```

---

## Planowane funkcjonalności

- Rejestracja i logowanie użytkowników
- Role: pacjent i lekarz
- Panel lekarza
- Umawianie wizyt z poziomu widoku HTML
- Pełna lista archiwalnych wpisów historii medycznej
- Podpięcie szybkiego zapisu pod backend
- Komunikaty sukcesu i błędów po zapisie wizyty
- Lepsza walidacja dat i godzin wizyt
- Rozbudowa recept
- Wyszukiwarka lekarzy
- Mapa aptek i placówek medycznych
- Integracja z PostgreSQL
- Integracja z MongoDB
- Docker Compose
- Testy automatyczne
- CI/CD GitHub Actions

---

## Status projektu

Projekt jest rozwijany etapami. Obecny etap skupia się na dopracowaniu widoków pacjenta, utrzymaniu prostego backendu, porządkowaniu logiki w helperach oraz dobrych praktykach pracy z Git i Pull Requestami.

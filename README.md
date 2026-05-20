# Portal Pacjenta

Aplikacja webowa tworzona jako projekt portfolio Junior Python Developer.

Celem projektu jest stworzenie systemu umożliwiającego:
- zarządzanie wizytami,
- podgląd profilu pacjenta,
- obsługę panelu pacjenta,
- wyszukiwanie lekarzy i aptek,
- późniejszą obsługę historii medycznej i recept.

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

Projekt ma już podstawowy backend FastAPI oraz pierwszy widok panelu pacjenta renderowany przez Jinja2.

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
- panel pacjenta pod adresem `/panel-pacjenta`.

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
- Historia medyczna
- Recepty
- Wyszukiwarka lekarzy
- Mapa aptek i placówek medycznych
- Integracja z PostgreSQL
- Integracja z MongoDB
- Docker Compose
- Testy automatyczne
- CI/CD GitHub Actions

---

## Status projektu

Projekt jest rozwijany etapami. Obecny etap skupia się na uporządkowaniu dashboardu pacjenta, podstawowej logice wizyt i dobrych praktykach pracy z Git oraz Pull Requestami.

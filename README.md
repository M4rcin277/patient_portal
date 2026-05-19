# Portal Pacjenta

Aplikacja webowa tworzona jako projekt portfolio Junior Python Developer.

Celem projektu jest stworzenie systemu umożliwiającego:
- zarządzanie wizytami,
- historią medyczną,
- receptami,
- wyszukiwaniem lekarzy i aptek.

---

## Technologie

- Python
- FastAPI
- PostgreSQL
- MongoDB
- Jinja2
- Bootstrap 5
- Docker
- GitHub Actions

---

## Aktualny etap projektu

- Utworzone środowisko wirtualne Python
- Zainstalowane FastAPI i Uvicorn
- Utworzona pierwsza aplikacja FastAPI
- Dodany plik `requirements.txt`
- Dodany plik `.gitignore`

---

## Uruchomienie projektu lokalnie

### Aktywacja środowiska

```powershell
.\venv\Scripts\activate
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

Dokumentacja API:

```text
http://127.0.0.1:8000/docs
```

---

## Planowane funkcjonalności

- Rejestracja i logowanie użytkowników
- Role: pacjent i lekarz
- Panel pacjenta
- Panel lekarza
- Umawianie wizyt
- Historia medyczna
- Recepty
- Wyszukiwarka lekarzy
- Mapa aptek i lekarzy

---

## Status projektu

Projekt jest obecnie rozwijany i będzie stopniowo rozszerzany o:
- autoryzację JWT,
- integrację PostgreSQL i MongoDB,
- Docker Compose,
- testy automatyczne,
- CI/CD GitHub Actions.
# Schemat bazy danych

Ten dokument opisuje aktualny schemat bazy danych projektu Portal Pacjenta.
Na tym etapie aplikacja używa lokalnej bazy SQLite przez SQLAlchemy, ale modele są projektowane tak, żeby później można było przejść na PostgreSQL.

## Aktualny etap

SQLite jest teraz bazą developerską. Służy do:

- sprawdzenia poprawności modeli SQLAlchemy,
- pracy aplikacji na realnej bazie zamiast list Pythonowych,
- przygotowania repozytoriów pod PostgreSQL,
- nauki przepływu `route -> service -> repository -> database`.

Docelowo SQLite zostanie zastąpione przez PostgreSQL. Dane demo znajdują się w `app/seed_data.py`, a do bazy trafiają przez `app/seed_db.py`.

## Główne tabele

### `uzytkownicy`

Tabela pod przyszłe logowanie.

Najważniejsze pola:

- `email`
- `haslo_hash`
- `rola`
- `pacjent_id`
- `lekarz_id`

Na razie jest przygotowana strukturalnie. Prawdziwe logowanie, haszowanie haseł i role użytkowników będą osobnym etapem.

### `pacjenci`

Tabela przechowuje dane pacjenta widoczne w profilu i używane w wizytach.

Najważniejsze pola:

- `imie`
- `nazwisko`
- `email`
- `telefon`
- `data_urodzenia`
- `adres`

Relacje:

- jeden pacjent może mieć wiele wizyt,
- jeden pacjent może mieć wiele recept,
- jeden pacjent może mieć wiele leków w planie leczenia,
- jeden pacjent może mieć wiele wpisów historii medycznej.

### `lekarze`

Tabela przechowuje lekarzy dostępnych w aplikacji.

Najważniejsze pola:

- `imie`
- `nazwisko`
- `specjalizacja`
- `miasto`
- `lokalizacja`
- `tryb_wizyty`

Uwaga: `specjalizacja` i `lokalizacja` są teraz tekstami. To świadome uproszczenie etapu SQLite, bo istniejące widoki i filtrowanie już na tym bazują. Mamy też tabele `specjalizacje` i `placowki`, które przygotowują projekt do późniejszej normalizacji.

### `wizyty`

Tabela przechowuje wizyty pacjentów.

Najważniejsze pola:

- `pacjent_id`
- `lekarz_id`
- `data`
- `godzina`
- `status`
- `notatka`

Relacje:

- wizyta należy do jednego pacjenta,
- wizyta należy do jednego lekarza.

Ta tabela obsługuje obecnie szybki zapis, kalendarz wizyt, przesuwanie wizyty, odwoływanie wizyty i sprawdzanie zajętych terminów.

## Tabele medyczne

### `recepty`

Tabela przechowuje nagłówki recept.

Najważniejsze pola:

- `pacjent_id`
- `lekarz_id`
- `kod`
- `wystawiono`
- `wazna_do`
- `status`

### `leki`

Katalog leków.

Najważniejsze pola:

- `nazwa`
- `substancja`
- `dawka`
- `postac`

### `recepta_leki`

Tabela łącząca recepty z lekami.

Dlaczego istnieje:

- jedna recepta może zawierać wiele leków,
- ten sam lek może pojawić się na wielu receptach.

Najważniejsze pola:

- `recepta_id`
- `lek_id`
- `dawkowanie`
- `ilosc`

### `pacjent_leki`

Tabela przechowuje leki przypisane do konkretnego pacjenta.

Nie trzymamy dawkowania bezpośrednio w tabeli `leki`, bo `leki` to katalog. Ten sam lek może mieć inne dawkowanie u różnych pacjentów.

Najważniejsze pola:

- `pacjent_id`
- `lek_id`
- `lekarz_id`
- `dawkowanie`
- `zalecenie`
- `status`
- `do_kiedy`

### `historia_medyczna`

Tabela przechowuje wpisy historii pacjenta, np. badanie, konsultację, wizytę lub zalecenie.

Najważniejsze pola:

- `pacjent_id`
- `lekarz_id`
- `wizyta_id`
- `data`
- `typ`
- `tytul`
- `opis`
- `etykieta`

`lekarz_id` i `wizyta_id` są opcjonalne, bo nie każdy wpis historii musi od razu pochodzić z konkretnej wizyty.

## Tabele pomocnicze

### `specjalizacje`

Tabela przygotowana pod późniejsze uporządkowanie specjalizacji lekarzy.

Na teraz lekarz nadal ma tekstowe pole `specjalizacja`. Docelowo można przejść na:

```text
lekarze.specjalizacja_id -> specjalizacje.id
```

### `placowki`

Tabela przygotowana pod późniejsze wydzielenie placówek medycznych.

Na teraz lekarz nadal ma tekstowe pole `lokalizacja`. Docelowo można przejść na:

```text
lekarze.placowka_id -> placowki.id
```

### `apteki`

Tabela przechowuje apteki pokazywane przy realizacji recept.

Najważniejsze pola:

- `nazwa`
- `adres`
- `godziny`

### `plan_opieki`

Tabela przechowuje elementy planu opieki pacjenta widoczne na dashboardzie i profilu.

Najważniejsze pola:

- `pacjent_id`
- `kolejnosc`
- `ikona`
- `data`
- `podpis`
- `tytul`
- `opis`
- `etykieta`

### `godziny_przyjec`

Prosta tabela z dostępnymi godzinami przyjęć.

Na teraz jest wspólna dla aplikacji. To wystarcza do obecnego szybkiego zapisu i walidacji zajętych terminów.

Docelowo może zostać zastąpiona przez bardziej precyzyjny grafik lekarza, np.:

```text
grafik_lekarza
  lekarz_id
  dzien_tygodnia
  godzina_od
  godzina_do
  slot_minuty
```

## Świadome uproszczenia

Aktualny schemat jest dobry jako etap przygotowania pod PostgreSQL, ale nie jest jeszcze finalnym schematem produkcyjnym.

Świadomie zostawiamy na później:

- migracje Alembic,
- pełne powiązanie lekarzy z `specjalizacje`,
- pełne powiązanie lekarzy z `placowki`,
- prawdziwy grafik lekarzy,
- logowanie i aktualny pacjent z sesji użytkownika,
- role użytkowników i autoryzację,
- MongoDB dla elastycznych zgłoszeń objawów.

## Decyzja na teraz

Na tym etapie zostawiamy SQLite jako lokalną bazę developerską i utrzymujemy obecny schemat jako fundament. Następne większe kroki to:

- konfiguracja bazy przez zmienną środowiskową,
- migracje Alembic,
- PostgreSQL,
- Docker Compose,
- logowanie użytkownika.

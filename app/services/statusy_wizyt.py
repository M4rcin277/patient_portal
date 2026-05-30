from fastapi.responses import RedirectResponse

from app.services.wizyty import (
    BrakDostepuDoWizyty,
    NiepoprawnyTermin,
    TerminWPrzeszlosci,
    TerminZajety,
    WizytaNieaktywna,
    WizytaNieIstnieje,
)


STATUSY_WIZYT = {
    "wizyta_dodana": ("sukces", "Wizyta została zapisana."),
    "wizyta_odwolana": ("sukces", "Wizyta została odwołana."),
    "wizyta_przesunieta": ("sukces", "Wizyta została przesunięta."),
    "wizyta_nie_istnieje": ("blad", "Nie znaleziono wybranej wizyty."),
    "brak_dostepu": ("blad", "Nie masz dostępu do tej wizyty."),
    "wizyta_nieaktywna": ("blad", "Ta wizyta jest już nieaktywna."),
    "termin_w_przeszlosci": ("blad", "Nie można wybrać terminu z przeszłości."),
    "termin_zajety": ("blad", "Ten termin jest już zajęty. Wybierz inny termin."),
    "niepoprawny_termin": ("blad", "Niepoprawny format daty lub godziny wizyty."),
}


def status_wizyty_z_wyjatku(wyjatek):
    if isinstance(wyjatek, WizytaNieIstnieje):
        return "wizyta_nie_istnieje"
    if isinstance(wyjatek, BrakDostepuDoWizyty):
        return "brak_dostepu"
    if isinstance(wyjatek, WizytaNieaktywna):
        return "wizyta_nieaktywna"
    if isinstance(wyjatek, NiepoprawnyTermin):
        return "niepoprawny_termin"
    if isinstance(wyjatek, TerminWPrzeszlosci):
        return "termin_w_przeszlosci"
    if isinstance(wyjatek, TerminZajety):
        return "termin_zajety"

    return "niepoprawny_termin"


def przekieruj_do_wizyt(status: str):
    return RedirectResponse(
        url=f"/moje-wizyty?status={status}",
        status_code=303,
    )

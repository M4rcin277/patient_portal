from pydantic import BaseModel


class NowaWizyta(BaseModel):
    pacjent_id: int
    lekarz_id: int
    data: str
    godzina: str
    notatka: str


class PrzesuniecieWizyty(BaseModel):
    data: str
    godzina: str

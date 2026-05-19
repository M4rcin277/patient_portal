from pydantic import BaseModel


class NowaWizyta(BaseModel):
    pacjent_id: int
    lekarz_id: int
    data: str
    godzina: str
    notatka: str

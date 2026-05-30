from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Lekarz(Base):
    __tablename__ = "lekarze"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    imie: Mapped[str] = mapped_column(String(100))
    nazwisko: Mapped[str] = mapped_column(String(100))
    specjalizacja: Mapped[str] = mapped_column(String(100), index=True)
    miasto: Mapped[str] = mapped_column(String(100), index=True)
    lokalizacja: Mapped[str] = mapped_column(String(255))
    tryb_wizyty: Mapped[str] = mapped_column(String(100))

    wizyty: Mapped[list["Wizyta"]] = relationship(back_populates="lekarz")

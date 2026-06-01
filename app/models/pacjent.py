from __future__ import annotations

from datetime import date

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Pacjent(Base):
    __tablename__ = "pacjenci"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    imie: Mapped[str] = mapped_column(String(100))
    nazwisko: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    telefon: Mapped[str] = mapped_column(String(30))
    data_urodzenia: Mapped[date | None] = mapped_column(Date, nullable=True)
    adres: Mapped[str | None] = mapped_column(String(255), nullable=True)
    grupa_krwi: Mapped[str | None] = mapped_column(String(10), nullable=True)

    wizyty: Mapped[list["Wizyta"]] = relationship(back_populates="pacjent")

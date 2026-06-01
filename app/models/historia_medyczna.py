from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class HistoriaMedyczna(Base):
    __tablename__ = "historia_medyczna"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pacjent_id: Mapped[int] = mapped_column(ForeignKey("pacjenci.id"), index=True)
    lekarz_id: Mapped[int | None] = mapped_column(
        ForeignKey("lekarze.id"),
        nullable=True,
        index=True,
    )
    wizyta_id: Mapped[int | None] = mapped_column(
        ForeignKey("wizyty.id"),
        nullable=True,
        index=True,
    )
    data: Mapped[date] = mapped_column(Date, index=True)
    typ: Mapped[str] = mapped_column(String(50), index=True)
    tytul: Mapped[str] = mapped_column(String(150))
    opis: Mapped[str] = mapped_column(String(1000))
    etykieta: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ikona: Mapped[str | None] = mapped_column(String(100), nullable=True)

    pacjent = relationship("Pacjent")
    lekarz = relationship("Lekarz")
    wizyta = relationship("Wizyta")

from __future__ import annotations

from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Recepta(Base):
    __tablename__ = "recepty"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pacjent_id: Mapped[int] = mapped_column(ForeignKey("pacjenci.id"), index=True)
    lekarz_id: Mapped[int | None] = mapped_column(
        ForeignKey("lekarze.id"),
        nullable=True,
        index=True,
    )
    kod: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    wystawiono: Mapped[date] = mapped_column(Date)
    wazna_do: Mapped[date] = mapped_column(Date, index=True)
    status: Mapped[str] = mapped_column(String(30), default="aktywna", index=True)

    pacjent = relationship("Pacjent")
    lekarz = relationship("Lekarz")
    pozycje = relationship("ReceptaLek", back_populates="recepta")

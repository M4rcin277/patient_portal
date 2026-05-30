from __future__ import annotations

from datetime import date, time

from sqlalchemy import Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Wizyta(Base):
    __tablename__ = "wizyty"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pacjent_id: Mapped[int] = mapped_column(ForeignKey("pacjenci.id"), index=True)
    lekarz_id: Mapped[int] = mapped_column(ForeignKey("lekarze.id"), index=True)
    data: Mapped[date] = mapped_column(Date, index=True)
    godzina: Mapped[time] = mapped_column(Time)
    status: Mapped[str] = mapped_column(String(30), default="zaplanowana")
    notatka: Mapped[str | None] = mapped_column(String(500), nullable=True)

    pacjent: Mapped["Pacjent"] = relationship(back_populates="wizyty")
    lekarz: Mapped["Lekarz"] = relationship(back_populates="wizyty")

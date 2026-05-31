from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PlanOpieki(Base):
    __tablename__ = "plan_opieki"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pacjent_id: Mapped[int] = mapped_column(ForeignKey("pacjenci.id"), index=True)
    kolejnosc: Mapped[int] = mapped_column(Integer, default=0)
    ikona: Mapped[str] = mapped_column(String(100))
    data: Mapped[str] = mapped_column(String(50))
    podpis: Mapped[str] = mapped_column(String(100))
    tytul: Mapped[str] = mapped_column(String(150))
    opis: Mapped[str] = mapped_column(String(255))
    etykieta: Mapped[str] = mapped_column(String(100))

    pacjent = relationship("Pacjent")

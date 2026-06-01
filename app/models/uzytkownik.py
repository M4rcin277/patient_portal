from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Uzytkownik(Base):
    __tablename__ = "uzytkownicy"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    haslo_hash: Mapped[str] = mapped_column(String(255))
    rola: Mapped[str] = mapped_column(String(30))
    pacjent_id: Mapped[int | None] = mapped_column(
        ForeignKey("pacjenci.id"),
        nullable=True,
        unique=True,
    )
    lekarz_id: Mapped[int | None] = mapped_column(
        ForeignKey("lekarze.id"),
        nullable=True,
        unique=True,
    )

    pacjent = relationship("Pacjent")
    lekarz = relationship("Lekarz")

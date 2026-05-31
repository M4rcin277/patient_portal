from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PacjentLek(Base):
    __tablename__ = "pacjent_leki"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    pacjent_id: Mapped[int] = mapped_column(ForeignKey("pacjenci.id"), index=True)
    lek_id: Mapped[int] = mapped_column(ForeignKey("leki.id"), index=True)
    lekarz_id: Mapped[int | None] = mapped_column(
        ForeignKey("lekarze.id"),
        nullable=True,
        index=True,
    )
    dawkowanie: Mapped[str] = mapped_column(String(255))
    zalecenie: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="Aktywny")
    do_kiedy: Mapped[str | None] = mapped_column(String(50), nullable=True)
    ikona: Mapped[str | None] = mapped_column(String(100), nullable=True)
    kolor: Mapped[str | None] = mapped_column(String(50), nullable=True)

    pacjent = relationship("Pacjent")
    lek = relationship("Lek")
    lekarz = relationship("Lekarz")

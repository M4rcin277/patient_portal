from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReceptaLek(Base):
    __tablename__ = "recepta_leki"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    recepta_id: Mapped[int] = mapped_column(ForeignKey("recepty.id"), index=True)
    lek_id: Mapped[int] = mapped_column(ForeignKey("leki.id"), index=True)
    dawkowanie: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ilosc: Mapped[str | None] = mapped_column(String(100), nullable=True)

    recepta = relationship("Recepta", back_populates="pozycje")
    lek = relationship("Lek")

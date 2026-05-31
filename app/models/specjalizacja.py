from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Specjalizacja(Base):
    __tablename__ = "specjalizacje"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nazwa: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    opis: Mapped[str | None] = mapped_column(String(500), nullable=True)

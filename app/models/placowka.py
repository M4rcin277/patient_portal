from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Placowka(Base):
    __tablename__ = "placowki"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nazwa: Mapped[str] = mapped_column(String(150), index=True)
    miasto: Mapped[str] = mapped_column(String(100), index=True)
    adres: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefon: Mapped[str | None] = mapped_column(String(30), nullable=True)

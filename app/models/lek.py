from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Lek(Base):
    __tablename__ = "leki"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nazwa: Mapped[str] = mapped_column(String(150), index=True)
    substancja: Mapped[str | None] = mapped_column(String(150), nullable=True)
    dawka: Mapped[str | None] = mapped_column(String(100), nullable=True)
    postac: Mapped[str | None] = mapped_column(String(100), nullable=True)

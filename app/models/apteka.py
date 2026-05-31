from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Apteka(Base):
    __tablename__ = "apteki"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nazwa: Mapped[str] = mapped_column(String(150), index=True)
    adres: Mapped[str] = mapped_column(String(255))
    godziny: Mapped[str] = mapped_column(String(100))

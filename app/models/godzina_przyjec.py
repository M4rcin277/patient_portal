from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class GodzinaPrzyjec(Base):
    __tablename__ = "godziny_przyjec"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    godzina: Mapped[str] = mapped_column(String(5), unique=True, index=True)

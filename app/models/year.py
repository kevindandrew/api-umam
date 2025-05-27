from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Year(Base):
    __tablename__ = "year"

    year_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relación con la tabla Gestion
    gestiones: Mapped[list["Gestion"]] = relationship(
        "Gestion", back_populates="year")

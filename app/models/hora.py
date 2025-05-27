from sqlalchemy import Time, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Hora(Base):
    __tablename__ = "hora"

    hora_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    hora_inicio: Mapped[str] = mapped_column(Time, nullable=False)
    hora_fin: Mapped[str] = mapped_column(Time, nullable=False)

    __table_args__ = (
        CheckConstraint("hora_fin > hora_inicio", name="check_hora_valida"),
    )

    # Relaciones
    dias_clase: Mapped[list["DiasClase"]] = relationship(back_populates="hora")

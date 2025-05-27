from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, TIMESTAMP, DECIMAL, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Matricula(Base):
    __tablename__ = "matriculas"
    __table_args__ = (
        UniqueConstraint("estudiante_id", "horario_id",
                         "gestion_id", name="uq_matricula"),
    )

    matricula_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    estudiante_id: Mapped[int] = mapped_column(
        ForeignKey("estudiantes.estudiante_id"), nullable=False)
    horario_id: Mapped[int] = mapped_column(
        ForeignKey("horarios.horario_id"), nullable=False)
    gestion_id: Mapped[int] = mapped_column(
        ForeignKey("gestion.gestion_id"), nullable=False)

    fecha_matricula: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow)
    nota_final: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=True)
    estado: Mapped[str] = mapped_column(String(20), default="activo")

    # Relaciones
    estudiante: Mapped["Estudiante"] = relationship(
        back_populates="matriculas")
    horario: Mapped["Horario"] = relationship(
        back_populates="matriculas")
    gestion: Mapped["Gestion"] = relationship(
        back_populates="matriculas")

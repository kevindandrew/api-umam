from sqlalchemy import String, Text, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class DatosFamiliar(Base):
    __tablename__ = "datos_familiares"

    familiar_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    estudiante_id: Mapped[int] = mapped_column(
        ForeignKey("estudiantes.estudiante_id"), nullable=False)

    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    ap_paterno: Mapped[str] = mapped_column(String(100), nullable=True)
    ap_materno: Mapped[str] = mapped_column(String(100), nullable=True)
    nombres: Mapped[str] = mapped_column(String(100), nullable=True)
    parentesco: Mapped[str] = mapped_column(String(50), nullable=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    direccion: Mapped[str] = mapped_column(Text, nullable=True)
    relacion: Mapped[str] = mapped_column(String(50), nullable=True)

    __table_args__ = (
        CheckConstraint("tipo IN ('referencia', 'convive')",
                        name="check_tipo_valido"),
    )

    # Relación inversa
    estudiante: Mapped["Estudiante"] = relationship(
        back_populates="datos_familiares")

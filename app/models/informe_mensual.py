from datetime import datetime
from sqlalchemy import String, Text, Integer, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class InformeMensual(Base):
    __tablename__ = "informes_mensuales"
    __table_args__ = (
        UniqueConstraint("usuario_id", "mes", "anio", name="uq_informe_usuario_mes_anio"),
    )

    informe_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.usuario_id"), nullable=False)
    carrera: Mapped[str] = mapped_column(String(200), nullable=False)
    universidad: Mapped[str] = mapped_column(String(200), nullable=False)
    mes: Mapped[int] = mapped_column(Integer, nullable=False)
    anio: Mapped[int] = mapped_column(Integer, nullable=False)
    actividades_realizadas: Mapped[str] = mapped_column(Text, nullable=False)
    como_se_realizaron: Mapped[str] = mapped_column(Text, nullable=False)
    resultados_obtenidos: Mapped[str] = mapped_column(Text, nullable=False)
    relacion_alcaldia: Mapped[str] = mapped_column(Text, nullable=False)
    medios_otorgados_alcaldia: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    fecha_actualizacion: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

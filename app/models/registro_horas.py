from datetime import datetime, date
from sqlalchemy import String, Integer, ForeignKey, DateTime, Date, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class RegistroHoras(Base):
    __tablename__ = "registro_horas"

    registro_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.usuario_id"), nullable=False)
    tipo_servicio: Mapped[str] = mapped_column(String(30), nullable=False)
    hora_entrada: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    hora_salida: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duracion_horas: Mapped[float | None] = mapped_column(Numeric(6, 2), nullable=True)
    fecha: Mapped[date] = mapped_column(Date, nullable=False)
    observaciones: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sucursal_id: Mapped[int | None] = mapped_column(ForeignKey("sucursales.sucursal_id"), nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="registro_horas")
    sucursal: Mapped["Sucursal"] = relationship(back_populates="registro_horas")

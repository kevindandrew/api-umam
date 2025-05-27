from typing import List
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    ap_paterno: Mapped[str] = mapped_column(String(100), nullable=False)
    ap_materno: Mapped[str] = mapped_column(String(100), nullable=False)
    ci: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)

    rol_id: Mapped[int] = mapped_column(
        ForeignKey("roles.rol_id"), nullable=False)
    sucursal_id: Mapped[int | None] = mapped_column(
        ForeignKey("sucursales.sucursal_id"), nullable=True)

    # Relaciones
    rol: Mapped["Rol"] = relationship(back_populates="usuarios")
    sucursal: Mapped["Sucursal"] = relationship(back_populates="usuarios")

    curso_docente: Mapped[List["CursoDocente"]] = relationship(
        back_populates="usuario"
    )
    horarios: Mapped[list["Horario"]] = relationship(back_populates="profesor")

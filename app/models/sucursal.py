from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Sucursal(Base):
    __tablename__ = "sucursales"

    sucursal_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    direccion: Mapped[str] = mapped_column(Text, nullable=False)

    # Relaciones con otras tablas
    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="sucursal")
    aulas: Mapped[list["Aula"]] = relationship(back_populates="sucursal")
    curso_sucursal: Mapped[list["CursoSucursal"]
                           ] = relationship(back_populates="sucursal")

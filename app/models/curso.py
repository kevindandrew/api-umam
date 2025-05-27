from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class Curso(Base):
    __tablename__ = "cursos"

    curso_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    gestoria: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Relaciones
    curso_docente: Mapped[list["CursoDocente"]
                          ] = relationship(back_populates="curso")
    curso_sucursal: Mapped[list["CursoSucursal"]
                           ] = relationship(back_populates="curso")
    horarios: Mapped[list["Horario"]] = relationship(back_populates="curso")

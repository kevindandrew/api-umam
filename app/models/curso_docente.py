from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class CursoDocente(Base):
    __tablename__ = "curso_docente"

    curso_docente_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.curso_id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.usuario_id"), nullable=False)
    gestion_id: Mapped[int] = mapped_column(
        ForeignKey("gestion.gestion_id"), nullable=False)

    __table_args__ = (UniqueConstraint("curso_id", "usuario_id",
                      "gestion_id", name="uq_curso_usuario_gestion"),)

    # Relaciones
    curso: Mapped["Curso"] = relationship(back_populates="curso_docente")
    usuario: Mapped["Usuario"] = relationship(back_populates="curso_docente")
    gestion: Mapped["Gestion"] = relationship(back_populates="curso_docente")

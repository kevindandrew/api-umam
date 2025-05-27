from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class CursoSucursal(Base):
    __tablename__ = "curso_sucursal"

    curso_sucursal_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)

    curso_id: Mapped[int] = mapped_column(
        ForeignKey("cursos.curso_id"), nullable=False)
    sucursal_id: Mapped[int] = mapped_column(
        ForeignKey("sucursales.sucursal_id"), nullable=False)
    gestion_id: Mapped[int] = mapped_column(
        ForeignKey("gestion.gestion_id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("curso_id", "sucursal_id", "gestion_id",
                         name="uq_curso_sucursal_gestion"),
    )

    # Relaciones
    curso: Mapped["Curso"] = relationship(back_populates="curso_sucursal")
    sucursal: Mapped["Sucursal"] = relationship(
        back_populates="curso_sucursal")
    gestion: Mapped["Gestion"] = relationship(
        back_populates="curso_sucursal")

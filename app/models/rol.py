from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base  # Asegúrate de que este archivo esté en app/models/base.py


class Rol(Base):
    __tablename__ = "roles"

    rol_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False)

    # Relación inversa con usuarios (si existe el modelo Usuario)
    usuarios: Mapped[list["Usuario"]] = relationship(
        "Usuario", back_populates="rol")

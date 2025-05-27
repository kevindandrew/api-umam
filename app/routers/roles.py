from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, text
from app.models.rol import Rol
from app.schemas.rol import RolRead
from app.database import get_session, verificar_conexion
import logging

router = APIRouter(prefix="/roles", tags=["roles"])
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[RolRead])
def obtener_roles(db: Session = Depends(get_session)):
    # Verificar conexión primero
    if not verificar_conexion():
        raise HTTPException(
            status_code=500, detail="Error de conexión a la base de datos")

    try:
        # Consulta con verificación explícita
        logger.info("Ejecutando consulta de roles...")

        # Opción 1: Consulta directa con SQL crudo
        roles_raw = db.exec(text("SELECT * FROM roles")).all()
        logger.info(f"Consulta cruda devolvió {len(roles_raw)} registros")

        # Opción 2: Consulta con SQLModel
        roles = db.exec(select(Rol)).all()
        logger.info(f"Consulta con SQLModel devolvió {len(roles)} registros")

        if not roles and roles_raw:
            logger.warning("¡Hay datos pero SQLModel no los está mapeando!")
            return [RolRead(rol_id=r[0], nombre=r[1]) for r in roles_raw]

        return roles

    except Exception as e:
        logger.error(f"Error en endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

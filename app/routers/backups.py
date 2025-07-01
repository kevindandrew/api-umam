import os
import subprocess
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app.models.usuario import Usuario
from app.database import get_session
from app.dependencies import require_admin, get_current_active_user
from app.schemas.backup import BackupOut  # Nuevo schema que definiremos

router = APIRouter(prefix="/backups", tags=["Backups"])

# Configuración
BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)


@router.get("/", response_model=List[BackupOut])
def list_backups(
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_active_user)
):
    """
    Lista todos los backups disponibles.
    Accesible para cualquier usuario autenticado.
    """
    backups = []
    for filename in os.listdir(BACKUP_DIR):
        if filename.endswith(".sql"):
            filepath = os.path.join(BACKUP_DIR, filename)
            backups.append({
                "filename": filename,
                "size_mb": round(os.path.getsize(filepath) / (1024 * 1024), 2),
                "created_at": datetime.fromtimestamp(
                    os.path.getctime(filepath)
                ).isoformat()
            })

    return sorted(backups, key=lambda x: x["created_at"], reverse=True)


@router.post("/create", response_model=BackupOut, status_code=201)
def create_backup(
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    """
    Crea un nuevo backup de la base de datos.
    Requiere privilegios de administrador.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"backup_{timestamp}.sql"
        filepath = os.path.join(BACKUP_DIR, filename)

        # Ejecutar pg_dump
        db_url = db.bind.url
        command = f"pg_dump -Fp -h {db_url.host} -p {db_url.port} -U {db_url.username} -d {db_url.database} > {filepath}"

        # Configurar variable de entorno para la contraseña
        env = os.environ.copy()
        env["PGPASSWORD"] = db_url.password or ""

        subprocess.run(command, shell=True, check=True, env=env)

        # Obtener información del backup creado
        backup_info = {
            "filename": filename,
            "size_mb": round(os.path.getsize(filepath) / (1024 * 1024), 2),
            "created_at": datetime.now().isoformat(),
            "status": "success"
        }

        return backup_info

    except subprocess.CalledProcessError as e:
        # Limpiar archivo si falló
        if os.path.exists(filepath):
            os.remove(filepath)
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear backup: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@router.get("/download/{filename}")
def download_backup(
    filename: str,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    """
    Descarga un archivo de backup específico.
    Accesible para cualquier usuario autenticado.
    """
    # Validar nombre de archivo por seguridad
    if not filename.endswith(".sql") or "/" in filename or ".." in filename:
        raise HTTPException(
            status_code=400,
            detail="Nombre de archivo inválido"
        )

    filepath = os.path.join(BACKUP_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Backup no encontrado"
        )

    return FileResponse(
        filepath,
        filename=filename,
        media_type="application/sql",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.delete("/{filename}", status_code=204)
def delete_backup(
    filename: str,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin)
):
    """
    Elimina un archivo de backup específico.
    Requiere privilegios de administrador.
    """
    # Validar nombre de archivo por seguridad
    if not filename.endswith(".sql") or "/" in filename or ".." in filename:
        raise HTTPException(
            status_code=400,
            detail="Nombre de archivo inválido"
        )

    filepath = os.path.join(BACKUP_DIR, filename)

    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=404,
            detail="Backup no encontrado"
        )

    os.remove(filepath)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models import Estudiante, DatosFamiliar, DatosAcademico, DatosMedico
from app.schemas.estudiante import EstudianteCreate, EstudianteOut, TipoFamiliar
from app.database import get_session
from sqlalchemy.orm import joinedload, session, selectinload
from app.dependencies import require_admin_or_encargado, get_current_active_user
from app.models.usuario import Usuario
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.post("/", response_model=EstudianteOut)
def crear_estudiante(
    estudiante: EstudianteCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin_or_encargado)
):
    try:
        # Iniciar transacción explícitamente
        if db.in_transaction():
            db.rollback()  # Limpiar cualquier transacción existente

        # Crear estudiante principal
        nuevo_estudiante = Estudiante(
            nombres=estudiante.nombres,
            ap_paterno=estudiante.ap_paterno,
            ap_materno=estudiante.ap_materno,
            ci=estudiante.ci,
            telefono=estudiante.telefono,
            fecha_nacimiento=estudiante.fecha_nacimiento,
            genero=estudiante.genero,
            lugar_nacimiento=estudiante.lugar_nacimiento,
            estado_civil=estudiante.estado_civil,
            direccion=estudiante.direccion,
            como_se_entero=estudiante.como_se_entero
        )
        db.add(nuevo_estudiante)
        db.flush()  # Para obtener el ID sin hacer commit

        # Registrar datos relacionados
        if estudiante.datos_familiares:
            for familiar in estudiante.datos_familiares:
                db.add(DatosFamiliar(
                    estudiante_id=nuevo_estudiante.estudiante_id,
                    **familiar.dict()
                ))

        if estudiante.datos_academicos:
            for academico in estudiante.datos_academicos:
                db.add(DatosAcademico(
                    estudiante_id=nuevo_estudiante.estudiante_id,
                    **academico.dict()
                ))

        if estudiante.datos_medicos:
            for medico in estudiante.datos_medicos:
                db.add(DatosMedico(
                    estudiante_id=nuevo_estudiante.estudiante_id,
                    **medico.dict()
                ))

        db.commit()

        # Recargar el estudiante con relaciones
        estudiante_con_todo = db.query(Estudiante).options(
            joinedload(Estudiante.datos_familiares),
            joinedload(Estudiante.datos_academicos),
            joinedload(Estudiante.datos_medicos)
        ).filter(
            Estudiante.estudiante_id == nuevo_estudiante.estudiante_id
        ).first()

        return estudiante_con_todo

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error al crear estudiante: {str(e)}"
        )


@router.get("/", response_model=List[EstudianteOut])
def obtener_estudiantes(db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_active_user)):
    return db.query(Estudiante).all()


@router.get("/{estudiante_id}", response_model=EstudianteOut)
def obtener_estudiante(estudiante_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(get_current_active_user)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.estudiante_id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.put("/{estudiante_id}", response_model=EstudianteOut)
def actualizar_estudiante(
    estudiante_id: int,
    estudiante_actualizado: EstudianteCreate,
    db: Session = Depends(get_session),
    current_user: Usuario = Depends(require_admin_or_encargado)
):
    try:
        # Verificar si hay transacción activa y limpiar si es necesario
        if db.in_transaction():
            db.rollback()

        # Iniciar nueva transacción
        db.begin()

        # Obtener estudiante existente
        estudiante = db.query(Estudiante).filter(
            Estudiante.estudiante_id == estudiante_id
        ).first()

        if not estudiante:
            db.rollback()
            raise HTTPException(
                status_code=404,
                detail="Estudiante no encontrado"
            )

        # Actualizar campos básicos
        datos_actualizados = estudiante_actualizado.dict(exclude_unset=True)
        for key, value in datos_actualizados.items():
            if key not in ['datos_familiares', 'datos_academicos', 'datos_medicos']:
                setattr(estudiante, key, value)

        # Manejar datos familiares
        if 'datos_familiares' in datos_actualizados:
            db.query(DatosFamiliar).filter(
                DatosFamiliar.estudiante_id == estudiante_id
            ).delete()

            for familiar in estudiante_actualizado.datos_familiares:
                try:
                    TipoFamiliar(familiar.tipo)  # Validación con Enum
                    db.add(DatosFamiliar(
                        estudiante_id=estudiante_id,
                        **familiar.dict()
                    ))
                except ValueError:
                    db.rollback()
                    raise HTTPException(
                        status_code=400,
                        detail=f"Tipo de familiar no válido: {familiar.tipo}"
                    )

        # Manejar datos académicos
        if 'datos_academicos' in datos_actualizados:
            db.query(DatosAcademico).filter(
                DatosAcademico.estudiante_id == estudiante_id
            ).delete()

            if estudiante_actualizado.datos_academicos:
                db.bulk_insert_mappings(
                    DatosAcademico,
                    [
                        {**a.dict(), 'estudiante_id': estudiante_id}
                        for a in estudiante_actualizado.datos_academicos
                    ]
                )

        # Manejar datos médicos
        if 'datos_medicos' in datos_actualizados:
            db.query(DatosMedico).filter(
                DatosMedico.estudiante_id == estudiante_id
            ).delete()

            if estudiante_actualizado.datos_medicos:
                db.bulk_insert_mappings(
                    DatosMedico,
                    [
                        {**m.dict(), 'estudiante_id': estudiante_id}
                        for m in estudiante_actualizado.datos_medicos
                    ]
                )

        db.commit()

        # Recargar el estudiante con relaciones
        estudiante_actualizado = db.query(Estudiante).options(
            selectinload(Estudiante.datos_familiares),
            selectinload(Estudiante.datos_academicos),
            selectinload(Estudiante.datos_medicos)
        ).filter(
            Estudiante.estudiante_id == estudiante_id
        ).first()

        return estudiante_actualizado

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error de integridad en la base de datos: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Error inesperado: {str(e)}"
        )


@router.delete("/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int, db: Session = Depends(get_session), current_user: Usuario = Depends(require_admin_or_encargado)):
    estudiante = db.query(Estudiante).filter(
        Estudiante.estudiante_id == estudiante_id).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db.delete(estudiante)
    db.commit()
    return {"mensaje": "Estudiante eliminado correctamente"}

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.schemas.curso import (
    CursoCreate, CursoOut,
    CursoDocenteCreate, CursoDocenteOut,
    CursoSucursalCreate, CursoSucursalOut,
    GestionCreate, GestionOut
)
from app.models import Curso, CursoDocente, CursoSucursal, Gestion
from app.database import get_session

router = APIRouter(prefix="/cursos", tags=["Cursos"])

# ---------------------------
# CRUD para Curso
# ---------------------------


@router.post("/", response_model=CursoOut)
def crear_curso(curso: CursoCreate, db: Session = Depends(get_session)):
    nuevo_curso = Curso(**curso.dict())
    db.add(nuevo_curso)
    db.commit()
    db.refresh(nuevo_curso)
    return nuevo_curso


@router.get("/", response_model=list[CursoOut])
def listar_cursos(db: Session = Depends(get_session)):
    return db.query(Curso).all()


@router.get("/{curso_id}", response_model=CursoOut)
def obtener_curso(curso_id: int, db: Session = Depends(get_session)):
    curso = db.query(Curso).get(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    return curso


@router.put("/{curso_id}", response_model=CursoOut)
def actualizar_curso(curso_id: int, datos: CursoCreate, db: Session = Depends(get_session)):
    curso = db.query(Curso).get(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    for campo, valor in datos.dict().items():
        setattr(curso, campo, valor)
    db.commit()
    db.refresh(curso)
    return curso


@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_curso(curso_id: int, db: Session = Depends(get_session)):
    curso = db.query(Curso).get(curso_id)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    db.delete(curso)
    db.commit()


# ---------------------------
# CRUD para CursoDocente
# ---------------------------
@router.post("/docente", response_model=CursoDocenteOut)
def asignar_docente(datos: CursoDocenteCreate, db: Session = Depends(get_session)):
    asignacion = CursoDocente(**datos.dict())
    db.add(asignacion)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Asignación duplicada")
    db.refresh(asignacion)
    return asignacion


@router.get("/docente/", response_model=List[CursoDocenteOut])
def listar_asignaciones_docentes(
    gestion_id: Optional[int] = Query(None),
    usuario_id: Optional[int] = Query(None),
    curso_id: Optional[int] = Query(None),
    db: Session = Depends(get_session)
):
    query = db.query(CursoDocente)

    if gestion_id:
        query = query.filter(CursoDocente.gestion_id == gestion_id)
    if usuario_id:
        query = query.filter(CursoDocente.usuario_id == usuario_id)
    if curso_id:
        query = query.filter(CursoDocente.curso_id == curso_id)

    return query.all()


# ---------------------------
# CRUD para CursoSucursal
# ---------------------------
@router.post("/sucursal", response_model=CursoSucursalOut)
def asignar_sucursal(datos: CursoSucursalCreate, db: Session = Depends(get_session)):
    asignacion = CursoSucursal(**datos.dict())
    db.add(asignacion)
    try:
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Asignación duplicada")
    db.refresh(asignacion)
    return asignacion


@router.get("/sucursal/", response_model=List[CursoSucursalOut])
def listar_asignaciones_sucursales(
    gestion_id: Optional[int] = Query(None),
    sucursal_id: Optional[int] = Query(None),
    curso_id: Optional[int] = Query(None),
    db: Session = Depends(get_session)
):
    query = db.query(CursoSucursal)

    if gestion_id:
        query = query.filter(CursoSucursal.gestion_id == gestion_id)
    if sucursal_id:
        query = query.filter(CursoSucursal.sucursal_id == sucursal_id)
    if curso_id:
        query = query.filter(CursoSucursal.curso_id == curso_id)

    return query.all()

# ---------------------------
# CRUD para Gestión
# ---------------------------


@router.post("/gestion", response_model=GestionOut)
def crear_gestion(gestion: GestionCreate, db: Session = Depends(get_session)):
    nueva = Gestion(**gestion.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@router.get("/gestiones", response_model=list[GestionOut])
def listar_gestiones(db: Session = Depends(get_session)):
    return db.query(Gestion).all()

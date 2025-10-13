from app import db, crud, models, schemas
from sqlmodel import Session
from typing import List, Optional
from fastapi import APIRouter, Depends, Query

router = APIRouter(prefix="/carreras", tags=["Carreras"])

#
# Endpoint: Devuelve todas las carrera (query)
#
@router.get("/", response_model=List[models.Carreras])
def carreras_query(query: Optional[str] = Query(default=None), session: Session = Depends(db.get_session)):
    carreras = crud.r_carreras.obtener_carreras(session, query)
    return carreras

#
# Endpoint: Devuelve las materias pertenecientes a una carrera (id)
#
@router.get("/{carrera_id}/materias", response_model=List[schemas.SubjectCareerDetail])
def carrera_materias_query(carrera_id: int, query: Optional[str] = Query(default=None), session: Session = Depends(db.get_session)):
    materias_carrera = crud.r_carreras.obtener_materias_carrera(session, carrera_id, query)
    return materias_carrera

#
# Endpoint: Devuelve los estudiantes pertenecientes a una carrera (id)
#
@router.get("/{carrera_id}/estudiantes", response_model=List[schemas.UserResponse])
def carrera_estudiantes_query(carrera_id: int, query: Optional[str] = Query(default=None), session: Session = Depends(db.get_session)):
    estudiantes = crud.r_carreras.estudiantes_por_carrera(session, carrera_id, query)
    return estudiantes

#
# Endpoint: Devuelve los profesores pertenecientes a una carrera (id)
#
@router.get("/{carrera_id}/profesores", response_model=List[schemas.UserResponse])
def carrera_profesores_query(carrera_id: int, query: Optional[str] = Query(default=None), session: Session = Depends(db.get_session)):
    profesores = crud.r_carreras.obtener_profesores(session, carrera_id, query)
    return profesores

#
# Endpoint: Devuelve las correlativas de una carrera (id)
#
@router.get("/{carrera_id}/correlativas", response_model=List[schemas.CorrelativesSubject])
def carrera_correlativas_id(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_carreras.correlativas_por_carrera(carrera_id, session)

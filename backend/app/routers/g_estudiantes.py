from app import db, crud, schemas
from sqlmodel import Session
from typing import List, Optional
from fastapi import APIRouter, Query, Depends

router = APIRouter(prefix="/estudiantes", tags=["Consulta de Estudiantes"])

#
# Endpoint: Devuelve un estudiante y toda su información (id)
#
@router.get("/{estudiante_id}", response_model=schemas.UserResponse)
def estudiante_id(estudiante_id: int, session: Session = Depends(db.get_session)):
    estudiante = crud.cr_estudiantes.estudiante_id(estudiante_id, session)
    return estudiante

#
# Endpoint: Devuelve las notas y las correlativas de un estudiante (id)
#
@router.get("/{estudiante_id}/notas_correlativas", response_model=List[schemas.CorreAverageNoteYear])
def estudiante_notas_y_correlativas(estudiante_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_estudiantes.notas_con_correlativas(estudiante_id, session)

#
# Endpoint: Devuelve las mesas de examen inscriptas de un estudiante (id)
#
@router.get("/{estudiante_id}/mesas_inscriptas", response_model=List[schemas.ExamRegistrationDetail])
def estudiante_mesas_inscriptas(estudiante_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_estudiantes.obtener_mesas_inscriptas(estudiante_id, session)

from app import db, crud, schemas
from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])

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
def estudiante_notas_y_correlativas_id(estudiante_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_estudiantes.notas_con_correlativas(estudiante_id, session)

#
# Endpoint: Devuelve las mesas de examen inscriptas de un estudiante (id)
#
@router.get("/{estudiante_id}/mesas_inscriptas", response_model=List[schemas.TablesRegisteredPerYear])
def estudiante_mesas_inscriptas_id(estudiante_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_estudiantes.obtener_mesas_inscriptas(estudiante_id, session)

#
# Endpoint: Modifica el estado de una inscripción (id)
#
@router.patch("/{inscripcion_id}/estado", response_model=schemas.ApiResponse, status_code=status.HTTP_200_OK)
def actualizar_estado_inscripcion_id(
    inscripcion_id: int,
    nuevo_estado: schemas.RegistrationExamUpdateStatus,
    session: Session = Depends(db.get_session)
):
    return crud.u_inscripcion.actualizar_estado_inscripcion(inscripcion_id, nuevo_estado, session)

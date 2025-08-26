from typing import List
from sqlmodel import Session
from app import db, crud, models, schemas
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/mesas", tags=["Gestión de Mesas de Examen"])

#
# Endpoint: Devuelve las mesas de examen por nota del estudiante (1 a 6)
#
@router.get("/{estudiante_id}/nota", response_model=List[schemas.TablesExamPerNote])
def mesas_examen_por_nota_estudiante(estudiante_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_mesas_examen.mesas_examen_por_nota(estudiante_id, session)

#
# Endpoint: Devuelve las mesas de examen por profesor (id)
#
@router.get("/{profesor_id}/profesor", response_model=List[schemas.ExamDetailWithStudents])
def mesas_examen_por_profesor(profesor_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_mesas_examen.mesas_examen_por_profesor(profesor_id, session)

#
# Endpoint: Crear una mesa de examen
#
@router.post("/crear/", response_model=models.Mesas_Examen)
def mesa_examen_crear(mesa: schemas.TableExamCreate, session: Session = Depends(db.get_session)):
    return crud.cr_mesas_examen.crear_mesa_examen(session, mesa)

#
# Endpoint: Inscribe a un estudiante en una mesa de examen
#
@router.post("/inscripciones/", response_model=schemas.ApiResponse, status_code=status.HTTP_200_OK)
def mesa_examen_inscripcion(inscripcion: schemas.RegistrationExamCreate, session: Session = Depends(db.get_session)):
    result = crud.cr_mesas_examen.inscribir_a_mesa_examen(session, inscripcion)
    return result

#
# Endpoint: Modifica el estado de una inscripción
#
@router.patch("/inscripciones/{inscripcion_id}/estado", response_model=schemas.ApiResponse, status_code=status.HTTP_200_OK)
def mesa_examen_estado(
    inscripcion_id: int,
    nuevo_estado: schemas.RegistrationExamUpdateStatus,
    session: Session = Depends(db.get_session)
):
    return crud.cr_mesas_examen.actualizar_estado_inscripcion(inscripcion_id, nuevo_estado, session)

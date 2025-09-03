from app import db, crud, schemas
from typing import List
from sqlmodel import Session
from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/notas", tags=["Gestión de Notas"])

#
# Endpoint: Agregar una nota a un estudiante
#
@router.post("/", response_model=schemas.NoteBase)
def agregar_notas(nota: schemas.NoteCreate, session: Session = Depends(db.get_session)):
    return crud.cr_notas.insertar_nota(session, nota)

#
# Endpoint: Califica una nota de examen a un estudiante
#
@router.post("/examen/calificar/", response_model=schemas.ApiResponse)
def calificar_nota_examen(data: schemas.NotesExamUpdate, session: Session = Depends(db.get_session)):
    try:
        crud.cr_notas.calificar_nota_examen(session, data.inscripcion_id, data.nota)
        return schemas.ApiResponse(success=True, message="Nota de examen calificada exitosamente.")
    except HTTPException as e:
        return schemas.ApiResponse(success=False, errors=[e.detail])
    except Exception as e:
        return schemas.ApiResponse(success=False, errors=[f"Error inesperado: {str(e)}"])

#
# Endpoint: Devuelve todas las notas de un estudiante (id)
#
@router.get("/{estudiante_id}", response_model=List[schemas.NotesDetail])
def notas_estudiante_id(estudiante_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_notas.notas_estudiante(session, estudiante_id)

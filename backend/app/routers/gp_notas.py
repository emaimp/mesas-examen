from app import db, crud, schemas
from typing import List
from sqlmodel import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/notas", tags=["Gestión de Notas"])

#
# Endpoint: Agregar una nota a un estudiante
#
@router.post("/", response_model=schemas.NoteBase)
def agregar_notas(nota: schemas.NoteCreate, session: Session = Depends(db.get_session)):
    return crud.cr_notas.insertar_nota(session, nota)

#
# Endpoint: Devuelve todas las notas de un estudiante (id)
#
@router.get("/{estudiante_id}", response_model=List[schemas.NotesDetail])
def notas_estudiante_id(estudiante_id: int, session: Session = Depends(db.get_session)):
    return crud.cr_notas.notas_estudiante(session, estudiante_id)

from app import db, crud, schemas
from sqlmodel import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/profesores", tags=["Consulta de Profesores"])

#
# Endpoint: Devuelve un profesor y toda su información (id)
#
@router.get("/{profesor_id}", response_model=schemas.TeacherInfoResponse)
def profesor_id(profesor_id: int, session: Session = Depends(db.get_session)):
    profesor = crud.cr_profesores.profesor_id(profesor_id, session)
    return profesor

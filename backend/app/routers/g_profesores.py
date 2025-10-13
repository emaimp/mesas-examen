from app import db, crud, models, schemas
from sqlmodel import Session
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query

router = APIRouter(prefix="/profesores", tags=["Profesores"])

#
# Endpoint: Obtiene todos los profesores (query)
#
@router.get("/", response_model=List[schemas.TeacherResponse])
def profesores_query(query: Optional[str] = Query(default=None), session: Session = Depends(db.get_session)):
    profesores = crud.cr_profesores.obtener_profesores(session, query)
    return profesores

#
# Endpoint: Obtiene un profesor (id)
#
@router.get("/{profesor_id}", response_model=models.Profesores)
def profesor_id(profesor_id: int, session: Session = Depends(db.get_session)):
    profesor = session.query(models.Profesores).filter(models.Profesores.id == profesor_id).first()
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

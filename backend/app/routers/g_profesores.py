from app import db, models, core
from typing import List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/profesores", tags=["Profesores"], responses={404: {"description": "Not found"}})

#
# Endpoint: Obtiene todos los profesores
#
@router.get("/", response_model=List[models.Profesores])
async def get_all_profesores(
    db: Session = Depends(db.get_session),
    current_user: models.Usuarios = Depends(core.get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden ver todos los profesores."
        )
    profesores = db.query(models.Profesores).all()
    return profesores

#
# Endpoint: Obtiene un profesor por su ID
#
@router.get("/{profesor_id}", response_model=models.Profesores)
async def get_profesor_by_id(
    profesor_id: int,
    db: Session = Depends(db.get_session),
    current_user: models.Usuarios = Depends(core.get_current_user)
):
    if current_user.role != "admin" and current_user.id != profesor_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para ver este profesor."
        )
    profesor = db.query(models.Profesores).filter(models.Profesores.id == profesor_id).first()
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor

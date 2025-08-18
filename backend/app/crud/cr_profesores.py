from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Crear un nuevo profesor en la tabla profesores
#
def create_profesor(session: Session, profesor_in: schemas.TeacherCreate) -> models.Profesores:
    # Valida los datos de entrada del profesor usando el modelo Profesores
    profesor = models.Profesores.model_validate(profesor_in)
    session.add(profesor)
    session.commit()
    session.refresh(profesor)
    return profesor

#
# Devuelve un profesor y toda su información
#
def profesor_id(profesor_id: int, session: Session) -> schemas.TeacherInfoResponse:
    # Obtiene el registro del profesor en la tabla Profesores
    profesor_record = session.exec(
        select(models.Profesores)
        .where(models.Profesores.profesor_id == profesor_id)
        .options(
            selectinload(models.Profesores.materia_carrera).selectinload(models.Materia_Carreras.materia),
            selectinload(models.Profesores.materia_carrera).selectinload(models.Materia_Carreras.carrera), # Add this line to load carrera
            selectinload(models.Profesores.usuario)
        )
    ).first()

    if not profesor_record:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    # Obtiene el usuario asociado al profesor
    user = profesor_record.usuario
    materia_nombre = profesor_record.materia_carrera.materia.nombre if profesor_record.materia_carrera and profesor_record.materia_carrera.materia else None
    carrera_nombre = profesor_record.materia_carrera.carrera.nombre if profesor_record.materia_carrera and profesor_record.materia_carrera.carrera else None

    if not user or user.role != "teacher":
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    return schemas.TeacherInfoResponse(
        id=user.id,
        username=user.username,
        nombre=user.nombre,
        dni=user.dni,
        email=user.email,
        legajo=user.legajo,
        libreta=user.libreta, # Use user.libreta instead of None
        role=user.role,
        carrera_id=None,
        materia_nombre=materia_nombre,
        carrera_nombre=carrera_nombre
    )

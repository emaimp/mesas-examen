from app import models, schemas
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, col

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
# Devuelve todos los profesores (query)
#
def obtener_profesores(session: Session, query: Optional[str] = None) -> List[schemas.TeacherResponse]:
    statement = select(models.Profesores).join(models.Usuarios)
    if query:
        statement = statement.where(col(models.Usuarios.nombre).ilike(f"{query}%"))
    profesores = session.exec(statement).all()

    # Construir la respuesta con el schema personalizado
    result = []
    for profesor in profesores:
        result.append(schemas.TeacherResponse(
            id=profesor.id,
            profesor_id=profesor.profesor_id,
            nombre=profesor.usuario.nombre,
            legajo=profesor.legajo,
            materia_carrera_id=profesor.materia_carrera_id,
            anio_asignado=profesor.anio_asignado
        ))
    return result

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
        role=user.role,
        carrera_id=None,
        materia_nombre=materia_nombre,
        carrera_nombre=carrera_nombre,
        legajo=profesor_record.legajo
    )

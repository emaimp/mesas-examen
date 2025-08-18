from app import models, schemas
from typing import List
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Devuelve todas las notas de un estudiante
#
def notas_estudiante(session: Session, estudiante_id: int) -> List[models.Notas]:
    #  Crea una consulta para seleccionar las notas del estudiante, incluyendo información de la materia y la carrera.
    statement = (
        select(models.Notas)
        .where(models.Notas.estudiante_id == estudiante_id)
        # Carga las relaciones de forma eficiente para evitar múltiples consultas a la base de datos.
        .options(
            selectinload(models.Notas.materia_carrera).selectinload(models.Materia_Carreras.materia)
        )
    )
    # Ejecuta la consulta y obtiene todas las notas.
    notas = session.exec(statement).all()
    
    if not notas:
        raise HTTPException(status_code=404, detail="No se encontraron notas para el estudiante.")
    return notas

#
# Agrega una nota a un estudiante
#
def insertar_nota(session: Session, data: schemas.NoteCreate) -> models.Notas:
    # Obtiene el estudiante para verificar su existencia y rol
    estudiante = session.get(models.Usuarios, data.estudiante_id)
    
    # Si el estudiante no existe o no tiene el rol de "student", lanza una excepción HTTP 404.
    if not estudiante or estudiante.role != "student":
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    
    # Obtiene la materia_carrera para verificar su existencia
    materia_carrera = session.get(models.Materia_Carreras, data.materia_carrera_id)
    
    # Si la materia_carrera no existe, lanza una excepción HTTP 404.
    if not materia_carrera:
        raise HTTPException(status_code=404, detail="Materia no encontrada.")
    
    # Verifica si la materia pertenece al plan de carrera del estudiante.
    if materia_carrera.carrera_id != estudiante.carrera_id:
        raise HTTPException(
            status_code=400,
            detail="La materia no pertenece al plan de carrera del estudiante."
        )
    
    #  Verifica si ya existe una nota para el estudiante en la materia.
    existing_nota_statement = select(models.Notas).where(
        models.Notas.estudiante_id == data.estudiante_id,
        models.Notas.materia_carrera_id == data.materia_carrera_id
    )
    existente = session.exec(existing_nota_statement).first()
    
    # Si ya existe una nota, lanza una excepción HTTP 400.
    if existente:
        raise HTTPException(status_code=400, detail="Nota ya registrada.")
    
    # Crea la nota
    nota = models.Notas.model_validate(data)
    session.add(nota)
    session.commit()
    session.refresh(nota)
    return nota

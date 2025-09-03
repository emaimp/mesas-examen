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

#
# Califica una nota de examen a un estudiante
#
def calificar_nota_examen(session: Session, inscripcion_id: int, nota: int) -> models.Notas_Examen:
    # 1. Busca la inscripción por ID
    inscripcion = session.get(models.Inscripciones_Examen, inscripcion_id)

    if not inscripcion:
        raise HTTPException(status_code=404, detail="Inscripción a examen no encontrada.")
    
    # 2. Verifica que la inscripción esté activa
    if inscripcion.estado != models.Inscripciones_Examen.EstadoInscripcion.activo.value:
        raise HTTPException(status_code=400, detail="La inscripción no está activa y no se puede calificar.")

    estudiante_id = inscripcion.estudiante_id
    materia_carrera_id = inscripcion.mesa_examen.materia_carrera_id
    examen_a_calificar = inscripcion.examen

    if not examen_a_calificar:
        raise HTTPException(status_code=400, detail="La inscripción no tiene un examen asignado para calificar.")

    # 3. Obtiene o crea el registro de Notas_Examen
    nota_examen = session.exec(
        select(models.Notas_Examen)
        .where(
            models.Notas_Examen.estudiante_id == estudiante_id,
            models.Notas_Examen.materia_carrera_id == materia_carrera_id
        )
    ).first()

    if not nota_examen:
        # Si no existe, crea un nuevo registro con los campos de examen en None
        nota_examen = models.Notas_Examen(
            estudiante_id=estudiante_id,
            materia_carrera_id=materia_carrera_id,
            primer_examen=None,
            segundo_examen=None,
            tercer_examen=None
        )
        session.add(nota_examen)
        session.commit()
        session.refresh(nota_examen)

    # 4. Califica el examen correspondiente y verifica que no se pueda actualizar
    if examen_a_calificar == "primer_examen":
        if nota_examen.primer_examen is not None: # Comprueba si ya tiene una nota
            raise HTTPException(status_code=400, detail="La nota para el primer examen ya ha sido registrada.")
        nota_examen.primer_examen = nota
    elif examen_a_calificar == "segundo_examen":
        if nota_examen.segundo_examen is not None: # Comprueba si ya tiene una nota
            raise HTTPException(status_code=400, detail="La nota para el segundo examen ya ha sido registrada.")
        nota_examen.segundo_examen = nota
    elif examen_a_calificar == "tercer_examen":
        if nota_examen.tercer_examen is not None: # Comprueba si ya tiene una nota
            raise HTTPException(status_code=400, detail="La nota para el tercer examen ya ha sido registrada.")
        nota_examen.tercer_examen = nota
    else:
        raise HTTPException(status_code=400, detail="Número de examen inválido en la inscripción.")

    session.add(nota_examen)
    session.commit()
    session.refresh(nota_examen)

    # 5. Registra la asistencia como "si"
    inscripcion.asistencia = models.Inscripciones_Examen.EstadoAsistencia.si.value
    session.add(inscripcion)
    session.commit()
    session.refresh(inscripcion)

    return nota_examen

from app import models, schemas
from datetime import timedelta
from fastapi import HTTPException
from sqlmodel import Session, select

#
# Crear una mesa de examen
#
def crear_mesa_examen(session: Session, data: schemas.TableExamCreate) -> models.Mesas_Examen:
    # Verifica si existe la relación entre materia y carrera
    materia_carrera = session.get(models.Materia_Carreras, data.materia_carrera_id)
    if not materia_carrera:
        raise HTTPException(status_code=404, detail="La relación entre la materia y la carrera no existe.")

    # Verifica que el profesor exista y tenga el rol de 'teacher'
    profesor_usuario = session.get(models.Usuarios, data.profesor_id)
    if not profesor_usuario or profesor_usuario.role != "teacher":
        raise HTTPException(status_code=404, detail="Profesor no encontrado o no es un usuario válido con rol de profesor.")

    # Obtiene la carrera_id de la mesa de examen
    carrera_id_mesa = materia_carrera.carrera_id

    # Verifica que el profesor esté asignado a alguna materia dentro de esta carrera
    profesor_en_carrera = session.exec(
        select(models.Profesores)
        .where(
            models.Profesores.profesor_id == profesor_usuario.id,
            models.Profesores.materia_carrera_id.in_(
                select(models.Materia_Carreras.id).where(models.Materia_Carreras.carrera_id == carrera_id_mesa)
            )
        )
    ).first()

    if not profesor_en_carrera:
        raise HTTPException(status_code=400, detail="El profesor seleccionado no está asignado a ninguna materia de esta carrera.")

    # Validar que al menos un llamado sea proporcionado
    if not data.primer_llamado and not data.segundo_llamado:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos la fecha para el primer o segundo llamado.")

    # Determinar la fecha del llamado que se está creando para las validaciones de mes
    fecha_llamado_a_validar = data.primer_llamado if data.primer_llamado else data.segundo_llamado

    # Extrae el año y el mes de la fecha del llamado a validar
    primer_dia_mes = fecha_llamado_a_validar.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Calcula el último día del mes
    if fecha_llamado_a_validar.month == 12:
        ultimo_dia_mes = fecha_llamado_a_validar.replace(year=fecha_llamado_a_validar.year + 1, month=1, day=1) - timedelta(microseconds=1)
    else:
        ultimo_dia_mes = fecha_llamado_a_validar.replace(month=fecha_llamado_a_validar.month + 1, day=1) - timedelta(microseconds=1)

    # Lógica para verificar si ya existe un llamado del mismo tipo en el mes
    if data.primer_llamado:
        existing_primer_llamado_statement = select(models.Mesas_Examen).where(
            models.Mesas_Examen.materia_carrera_id == data.materia_carrera_id,
            models.Mesas_Examen.primer_llamado >= primer_dia_mes,
            models.Mesas_Examen.primer_llamado <= ultimo_dia_mes,
            models.Mesas_Examen.primer_llamado.is_not(None) # Asegura que estamos buscando un primer llamado existente
        )
        existing_primer_llamado = session.exec(existing_primer_llamado_statement).first()
        if existing_primer_llamado:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un primer llamado para esta carrera/materia en el mes seleccionado."
            )

    if data.segundo_llamado:
        existing_segundo_llamado_statement = select(models.Mesas_Examen).where(
            models.Mesas_Examen.materia_carrera_id == data.materia_carrera_id,
            models.Mesas_Examen.segundo_llamado >= primer_dia_mes,
            models.Mesas_Examen.segundo_llamado <= ultimo_dia_mes,
            models.Mesas_Examen.segundo_llamado.is_not(None) # Asegura que estamos buscando un segundo llamado existente
        )
        existing_segundo_llamado = session.exec(existing_segundo_llamado_statement).first()
        if existing_segundo_llamado:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un segundo llamado para esta carrera/materia en el mes seleccionado."
            )

    # Crea la nueva mesa de examen
    nueva_mesa = models.Mesas_Examen(
        materia_carrera_id=data.materia_carrera_id,
        profesor_id=data.profesor_id,
        primer_llamado=data.primer_llamado,
        segundo_llamado=data.segundo_llamado
    )
    session.add(nueva_mesa)
    session.commit()
    session.refresh(nueva_mesa)
    return nueva_mesa

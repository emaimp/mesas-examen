from app import models, schemas
from typing import List, Dict
from fastapi import HTTPException
from datetime import date, timedelta
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Devuelve las mesas de examen por nota del estudiante (1 a 6)
#
def mesas_examen_por_nota(estudiante_id: int, session: Session) -> List[schemas.TablesExamPerNote]:
    # Define el rango de fechas para buscar mesas de examen
    hoy = date.today()
    tres_meses = hoy + timedelta(days=90)

    # Construye la consulta para obtener mesas de examen
    statement = (
        select(models.Mesas_Examen)
        # Une con Materia_Carreras y Materias para obtener información
        .join(models.Materia_Carreras)
        .join(models.Materias)
        # Une con Notas, filtrando por estudiante y rango de notas
        .join(models.Notas, and_(
            models.Notas.materia_carrera_id == models.Materia_Carreras.id,
            models.Notas.estudiante_id == estudiante_id,
            models.Notas.nota_prom >= 1,
            models.Notas.nota_prom < 7
        ))
        # Filtra las mesas de examen por fecha
        .where(
            models.Mesas_Examen.fecha >= hoy,
            models.Mesas_Examen.fecha <= tres_meses,
        )
        # Carga relaciones anidadas para optimizar el acceso a datos
        .options(
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.materia),
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.carrera),
            selectinload(models.Mesas_Examen.profesor_usuario)
        )
        # Ordena los resultados
        .order_by(models.Materia_Carreras.anio, models.Materias.nombre, models.Mesas_Examen.fecha)
    )

    # Ejecuta la consulta
    mesas = session.exec(statement).all()

    # Agrupa las mesas de examen por año de carrera
    agrupado: Dict[int, List[schemas.TableExamDetail]] = {}
    for mesa in mesas:
        anio = mesa.anio
        if anio not in agrupado:
            agrupado[anio] = []
        agrupado[anio].append(
            schemas.TableExamDetail(
                id=mesa.id,
                fecha=mesa.fecha,
                materia_nombre=mesa.materia_nombre,
                profesor_nombre=mesa.profesor_nombre,
                carrera_nombre=mesa.carrera_nombre
            )
        )

    # Convierte el diccionario agrupado en una lista de esquemas
    return [
        schemas.TablesExamPerNote(anio=anio, mesas=mesas)
        for anio, mesas in sorted(agrupado.items())
    ]

#
# Devuelve las mesas de examen por id de profesor
#
def mesas_examen_por_profesor(profesor_id: int, session: Session) -> List[schemas.ExamDetailWithStudents]:
    # Consulta mesas de examen, estudiantes inscritos y el estado de la inscripción
    statement = (
        select(models.Mesas_Examen, models.Usuarios, models.Inscripciones_Examen)
        .join(models.Inscripciones_Examen, models.Mesas_Examen.id == models.Inscripciones_Examen.mesa_examen_id)
        .join(models.Usuarios, models.Inscripciones_Examen.estudiante_id == models.Usuarios.id)
        .where(models.Mesas_Examen.profesor_id == profesor_id)
        .options(
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.materia),
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.carrera),
            selectinload(models.Mesas_Examen.profesor_usuario)
        )
    )
    results = session.exec(statement).all()
    # Mapea los resultados al esquema ExamDetailWithStudents
    return [
        schemas.ExamDetailWithStudents(
            id=mesa_examen.id,
            fecha=mesa_examen.fecha,
            profesor_id=mesa_examen.profesor_id,
            materia_nombre=mesa_examen.materia_nombre,
            profesor_nombre=mesa_examen.profesor_nombre,
            carrera_nombre=mesa_examen.carrera_nombre,
            estudiante_nombre=usuario_estudiante.nombre,
            dni=usuario_estudiante.dni,
            libreta=usuario_estudiante.libreta,
            estado=inscripcion.estado
        )
        for mesa_examen, usuario_estudiante, inscripcion in results
    ]

#
# Crear una mesa de examen
#
def crear_mesa_examen(session: Session, data: schemas.TableExamCreate) -> models.Mesas_Examen:
    # Verifica si existe la relación entre materia y carrera
    materia_carrera = session.get(models.Materia_Carreras, data.materia_carrera_id)
    if not materia_carrera:
        raise HTTPException(status_code=404, detail="La relación entre la materia y la carrera no existe")

    # Verifica que el profesor exista y tenga el rol de 'teacher'
    profesor_usuario = session.get(models.Usuarios, data.profesor_id)
    if not profesor_usuario or profesor_usuario.role != "teacher":
        raise HTTPException(status_code=404, detail="Profesor no encontrado o no es un usuario válido con rol de profesor")

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
        raise HTTPException(status_code=400, detail="El profesor seleccionado no está asignado a ninguna materia de esta carrera")

    # Extrae el año y el mes de la fecha proporcionada
    fecha_mesa = data.fecha
    primer_dia_mes = fecha_mesa.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Calcula el último día del mes
    if fecha_mesa.month == 12:
        ultimo_dia_mes = fecha_mesa.replace(year=fecha_mesa.year + 1, month=1, day=1) - timedelta(microseconds=1)
    else:
        ultimo_dia_mes = fecha_mesa.replace(month=fecha_mesa.month + 1, day=1) - timedelta(microseconds=1)

    # Extrae el año y el mes de la fecha proporcionada
    fecha_mesa = data.fecha
    primer_dia_mes = fecha_mesa.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Calcula el último día del mes
    if fecha_mesa.month == 12:
        ultimo_dia_mes = fecha_mesa.replace(year=fecha_mesa.year + 1, month=1, day=1) - timedelta(microseconds=1)
    else:
        ultimo_dia_mes = fecha_mesa.replace(month=fecha_mesa.month + 1, day=1) - timedelta(microseconds=1)

    # Verifica cuántas mesas de examen existen para la misma materia/carrera en el mismo mes
    existing_mesas_count_statement = select(models.Mesas_Examen).where(
        models.Mesas_Examen.materia_carrera_id == data.materia_carrera_id,
        models.Mesas_Examen.fecha >= primer_dia_mes,
        models.Mesas_Examen.fecha <= ultimo_dia_mes
    )
    existing_mesas = session.exec(existing_mesas_count_statement).all()

    # Si ya existen 2 o más mesas para esta materia/carrera en el mes, no permite crear más
    if len(existing_mesas) >= 2:
        raise HTTPException(
            status_code=400,
            detail="Ya existen dos mesas de examen para esta carrera/materia en el mes seleccionado."
        )

    # Crea la nueva mesa de examen
    nueva_mesa = models.Mesas_Examen.model_validate(data)
    session.add(nueva_mesa)
    session.commit()
    session.refresh(nueva_mesa)
    return nueva_mesa

#
# Inscribe a un estudiante en una mesa de examen
#
def inscribir_a_mesa_examen(session: Session, data: schemas.RegistrationExamCreate) -> schemas.ApiResponse:
    try:
        # 1. Verifica que el estudiante exista y sea un estudiante
        estudiante = session.get(models.Usuarios, data.estudiante_id)
        # Si el estudiante no existe o no tiene el rol de "student", retorna un error
        if not estudiante or estudiante.role != "student":
            return schemas.ApiResponse(success=False, errors=["Estudiante no encontrado o no es un estudiante válido"])
        
        # 2. Verifica que la mesa exista
        mesa = session.get(models.Mesas_Examen, data.mesa_examen_id)
        # Si la mesa de examen no existe, retorna un error
        if not mesa:
            return schemas.ApiResponse(success=False, errors=["Mesa de examen no encontrada"])
        
        # 3. Verifica que la materia de la mesa pertenezca al plan de carrera del estudiante
        estudiante_record = session.exec(
            select(models.Estudiantes)
            .where(models.Estudiantes.estudiante_id == data.estudiante_id)
            .options(selectinload(models.Estudiantes.carrera))
        ).first()
        
        mesa_con_materia_carrera = session.exec(
            select(models.Mesas_Examen)
            .where(models.Mesas_Examen.id == data.mesa_examen_id)
            .options(selectinload(models.Mesas_Examen.materia_carrera))
        ).first()

        # Si no se encuentra el registro del estudiante o la mesa con la materia/carrera, retorna un error
        if not estudiante_record or not mesa_con_materia_carrera:
            return schemas.ApiResponse(success=False, errors=["Error interno al verificar relaciones de estudiante o mesa"])

        # 4. Verifica que la materia de la mesa pertenezca al plan de carrera del estudiante
        materia_en_plan_statement = select(models.Materia_Carreras).where(
            models.Materia_Carreras.id == mesa_con_materia_carrera.materia_carrera_id,
            models.Materia_Carreras.carrera_id == estudiante_record.carrera_id
        )
        materia_en_plan = session.exec(materia_en_plan_statement).first()

        # Si la materia no pertenece al plan de carrera del estudiante, retorna un error
        if not materia_en_plan:
            return schemas.ApiResponse(success=False, errors=["La materia no pertenece al plan de carrera"])
        
        # 5. Verifica que no tenga más de 2 inscripciones activas y que no esté inscripto a la misma materia
        inscripciones_activas_statement = select(models.Inscripciones_Examen).where(
            models.Inscripciones_Examen.estudiante_id == estudiante.id
        )
        inscripciones_activas = session.exec(inscripciones_activas_statement).all()

        # Si el estudiante ya tiene 2 inscripciones activas, retorna un error
        if len(inscripciones_activas) >= 2:
            return schemas.ApiResponse(success=False, errors=["Solo se permiten hasta 2 inscripciones"])
        
        # Itera sobre las inscripciones activas para verificar duplicados
        for inscripcion_activa in inscripciones_activas:
            mesa_inscripta = session.get(models.Mesas_Examen, inscripcion_activa.mesa_examen_id)
            # Si el estudiante ya está inscripto en la misma materia, retorna un error
            if mesa_inscripta and mesa_inscripta.materia_carrera_id == mesa.materia_carrera_id:
                return schemas.ApiResponse(success=False, errors=["Ya estás inscripto en esta materia"])
        
        # 6. Verifica si ya promocionó la materia (nota >= 7)
        nota_actual_statement = select(models.Notas).where(
            models.Notas.estudiante_id == estudiante.id,
            models.Notas.materia_carrera_id == materia_en_plan.id
        )
        nota_actual = session.exec(nota_actual_statement).first()
        
        # Si el estudiante ya promocionó la materia, retorna un error
        if nota_actual and nota_actual.nota_prom >= 7.0:
            return schemas.ApiResponse(success=False, errors=["Ya promocionaste la materia"])
        
        # 7. Verifica las correlativas si la materia es de 2º año en adelante
        # Si la materia es de segundo año o superior, verifica las correlativas
        if materia_en_plan.anio and materia_en_plan.anio > 1:
            correlativas_statement = select(models.Correlativas).where(
                models.Correlativas.materia_carrera_id == materia_en_plan.id
            )
            correlativas = session.exec(correlativas_statement).all()
            
            # Itera sobre las correlativas para verificar si el estudiante las cumple
            for corr in correlativas:
                nota_corr_statement = select(models.Notas).where(
                    models.Notas.estudiante_id == estudiante.id,
                    models.Notas.materia_carrera_id == corr.correlativa_id
                )
                nota = session.exec(nota_corr_statement).first()
                
                # Si no tiene la nota de la correlativa o es menor a 4.0, retorna un error
                if not nota or nota.nota_prom < 4.0:
                    return schemas.ApiResponse(success=False, errors=["No cumple las correlativas"])
        
        # 8. Registra la inscripción si todas las validaciones son correctas
        nueva_inscripcion = models.Inscripciones_Examen.model_validate(data)
        
        session.add(nueva_inscripcion)
        session.commit()
        session.refresh(nueva_inscripcion)
        
        return schemas.ApiResponse(
            success=True,
            message="Inscripción realizada con éxito",
            data={
                "id": nueva_inscripcion.id,
                "estudiante_id": nueva_inscripcion.estudiante_id,
                "mesa_examen_id": nueva_inscripcion.mesa_examen_id,
                "fecha_inscripcion": nueva_inscripcion.fecha_inscripcion.isoformat()
            }
        )
    except HTTPException as e:
        return schemas.ApiResponse(success=False, errors=[e.detail])
    except Exception as e:
        return schemas.ApiResponse(success=False, errors=[f"Error inesperado: {str(e)}"])

#
# Actualiza el estado de una inscripción
#
def actualizar_estado_inscripcion(
    inscripcion_id: int,
    nuevo_estado: schemas.RegistrationExamUpdateStatus,
    session: Session
) -> schemas.ApiResponse:
    try:
        # 1. Busca la inscripción por ID
        inscripcion = session.get(models.Inscripciones_Examen, inscripcion_id)

        # Si la inscripción no existe, retorna un error
        if not inscripcion:
            return schemas.ApiResponse(success=False, errors=["Inscripción a examen no encontrada"])

        # 2. Actualiza el estado de la inscripción
        inscripcion.estado = nuevo_estado.estado
        session.add(inscripcion)
        session.commit()
        session.refresh(inscripcion)

        return schemas.ApiResponse(
            success=True,
            message=f"Estado de inscripción {inscripcion_id} actualizado a '{inscripcion.estado}'",
            data={
                "id": inscripcion.id,
                "estudiante_id": inscripcion.estudiante_id,
                "mesa_examen_id": inscripcion.mesa_examen_id,
                "estado": inscripcion.estado
            }
        )
    except Exception as e:
        return schemas.ApiResponse(success=False, errors=[f"Error inesperado al actualizar el estado de la inscripción: {str(e)}"])

from app import models, schemas
from typing import List, Dict
from fastapi import HTTPException
from datetime import date, timedelta
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

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

#
# Inscribe a un estudiante en una mesa de examen
#
def inscribir_mesa_examen(session: Session, data: schemas.RegistrationExamCreate) -> schemas.ApiResponse:
    try:
        # 1. Verifica que el estudiante exista y sea un estudiante
        estudiante = session.get(models.Usuarios, data.estudiante_id)
        # Si el estudiante no existe o no tiene el rol de "student", retorna un error
        if not estudiante or estudiante.role != "student":
            return schemas.ApiResponse(success=False, errors=["Estudiante no encontrado o no es un estudiante válido."])
        
        # 2. Verifica que la mesa exista
        mesa = session.get(models.Mesas_Examen, data.mesa_examen_id)
        # Si la mesa de examen no existe, retorna un error
        if not mesa:
            return schemas.ApiResponse(success=False, errors=["Mesa de examen no encontrada."])
        
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
            return schemas.ApiResponse(success=False, errors=["Error interno al verificar relaciones de estudiante o mesa."])

        # 4. Verifica que la materia de la mesa pertenezca al plan de carrera del estudiante
        materia_en_plan_statement = select(models.Materia_Carreras).where(
            models.Materia_Carreras.id == mesa_con_materia_carrera.materia_carrera_id,
            models.Materia_Carreras.carrera_id == estudiante_record.carrera_id
        )
        materia_en_plan = session.exec(materia_en_plan_statement).first()

        # Si la materia no pertenece al plan de carrera del estudiante, retorna un error
        if not materia_en_plan:
            return schemas.ApiResponse(success=False, errors=["La materia no pertenece al plan de carrera."])
        
        # 5. Verifica que no tenga más de 2 inscripciones activas y que no esté inscripto a la misma materia
        inscripciones_activas_statement = select(models.Inscripciones_Examen).where(
            models.Inscripciones_Examen.estudiante_id == estudiante.id
        )
        inscripciones_activas = session.exec(inscripciones_activas_statement).all()

        # Si el estudiante ya tiene 2 inscripciones activas, retorna un error
        if len(inscripciones_activas) >= 2:
            return schemas.ApiResponse(success=False, errors=["Solo se permiten hasta 2 inscripciones."])
        
        # Itera sobre las inscripciones activas para verificar duplicados
        for inscripcion_activa in inscripciones_activas:
            mesa_inscripta = session.get(models.Mesas_Examen, inscripcion_activa.mesa_examen_id)
            # Si el estudiante ya está inscripto en la misma materia, retorna un error
            if mesa_inscripta and mesa_inscripta.materia_carrera_id == mesa.materia_carrera_id:
                return schemas.ApiResponse(success=False, errors=["Ya estás inscripto en esta materia."])
        
        # 6. Verifica si ya promocionó la materia (nota >= 7)
        nota_actual_statement = select(models.Notas).where(
            models.Notas.estudiante_id == estudiante.id,
            models.Notas.materia_carrera_id == materia_en_plan.id
        )
        nota_actual = session.exec(nota_actual_statement).first()
        
        # Si el estudiante ya promocionó la materia, retorna un error
        if nota_actual and nota_actual.nota_prom >= 7.0:
            return schemas.ApiResponse(success=False, errors=["Ya promocionaste la materia."])
        
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
                    return schemas.ApiResponse(success=False, errors=["No cumple las correlativas."])
        
        # 8. Determina el tipo de inscripción (libre o regular)
        tipo_inscripcion = None
        if nota_actual:
            if nota_actual.nota_prom < 4.0:
                tipo_inscripcion = models.Inscripciones_Examen.TipoInscripcion.libre.value
            elif 4.0 <= nota_actual.nota_prom < 7.0:
                tipo_inscripcion = models.Inscripciones_Examen.TipoInscripcion.regular.value
        
        # 9. Registra la inscripción si todas las validaciones son correctas
        nueva_inscripcion = models.Inscripciones_Examen(
            estudiante_id=data.estudiante_id,
            mesa_examen_id=data.mesa_examen_id,
            llamado_inscrito=data.llamado_inscrito,
            tipo_inscripcion=tipo_inscripcion # Asigna el tipo de inscripción
        )
        
        session.add(nueva_inscripcion)
        session.commit()
        session.refresh(nueva_inscripcion)
        
        return schemas.ApiResponse(
            success=True,
            message=f"Inscripción a {mesa.materia_nombre} realizada con éxito.",
            data={
                "id": nueva_inscripcion.id,
                "estudiante_id": nueva_inscripcion.estudiante_id,
                "mesa_examen_id": nueva_inscripcion.mesa_examen_id,
                "fecha_inscripcion": nueva_inscripcion.fecha_inscripcion.isoformat(),
                "llamado_inscrito": nueva_inscripcion.llamado_inscrito,
                "tipo_inscripcion": nueva_inscripcion.tipo_inscripcion
            }
        )
    except HTTPException as e:
        return schemas.ApiResponse(success=False, errors=[e.detail])
    except Exception as e:
        return schemas.ApiResponse(success=False, errors=[f"Error inesperado: {str(e)}"])

#
# Devuelve todas las mesas de examen divididas por carrera
#
def mesas_examen_por_carrera(session: Session) -> List[schemas.TablesExamPerCareer]:
    # Consulta todas las mesas de examen
    statement = (
        select(models.Mesas_Examen)
        .join(models.Materia_Carreras)
        .join(models.Carreras)
        .options(
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.materia),
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.carrera),
            selectinload(models.Mesas_Examen.profesor_usuario)
        )
        .order_by(
            models.Carreras.nombre,
            models.Materia_Carreras.id, # Ordena las mesas según el nombre de la materia
            models.Mesas_Examen.primer_llamado.is_not(None).desc(), # Primero los primeros llamados no nulos
            models.Mesas_Examen.primer_llamado, # Luego por la fecha del primer llamado
            models.Mesas_Examen.segundo_llamado # Si no hay primer llamado, por la fecha del segundo llamado
        )
    )
    mesas = session.exec(statement).all()

    # Agrupa las mesas de examen por carrera
    agrupado: Dict[str, List[schemas.TableExamPerCareerDetail]] = {}
    for mesa in mesas:
        carrera_nombre = mesa.carrera_nombre
        if carrera_nombre not in agrupado:
            agrupado[carrera_nombre] = []
        agrupado[carrera_nombre].append(
            schemas.TableExamPerCareerDetail(
                id=mesa.id,
                primer_llamado=mesa.primer_llamado,
                segundo_llamado=mesa.segundo_llamado,
                materia_nombre=mesa.materia_nombre,
                profesor_nombre=mesa.profesor_nombre,
            )
        )

    # Convierte el diccionario agrupado en una lista de esquemas
    return [
        schemas.TablesExamPerCareer(carrera_nombre=carrera_nombre, mesas=mesas)
        for carrera_nombre, mesas in sorted(agrupado.items(), key=lambda item: item[0])
    ]

#
# Devuelve las mesas de examen por nota del estudiante
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
        # Filtra las mesas de examen por fecha, considerando ambos llamados
        .where(
            # El primer llamado está dentro del rango Y no es NULL
            ((models.Mesas_Examen.primer_llamado >= hoy) &
             (models.Mesas_Examen.primer_llamado <= tres_meses))
            |  # O
            # El segundo llamado está dentro del rango Y no es NULL
            ((models.Mesas_Examen.segundo_llamado >= hoy) &
             (models.Mesas_Examen.segundo_llamado <= tres_meses))
        )
        # Carga relaciones anidadas para optimizar el acceso a datos
        .options(
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.materia),
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.carrera),
            selectinload(models.Mesas_Examen.profesor_usuario)
        )
        # Ordena los resultados
        .order_by(
            models.Materia_Carreras.anio,
            models.Materias.nombre,
            models.Mesas_Examen.primer_llamado.is_not(None).desc(), # Primero los primeros llamados no nulos
            models.Mesas_Examen.primer_llamado, # Luego por la fecha del primer llamado
            models.Mesas_Examen.segundo_llamado # Si no hay primer llamado, por la fecha del segundo llamado
        )
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
                primer_llamado=mesa.primer_llamado,
                segundo_llamado=mesa.segundo_llamado,
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
# Devuelve las mesas de examen por profesor
#
def mesas_examen_por_profesor(profesor_id: int, session: Session) -> List[schemas.TablesExamPerCareerForTeacher]:
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

    # Agrupa los resultados por carrera
    agrupado: Dict[str, List[schemas.ExamWithStudentsDetail]] = {}
    for mesa_examen, usuario_estudiante, inscripcion in results:
        carrera_nombre = mesa_examen.carrera_nombre
        if carrera_nombre not in agrupado:
            agrupado[carrera_nombre] = []
        agrupado[carrera_nombre].append(
            schemas.ExamWithStudentsDetail(
                id=mesa_examen.id,
                llamado_inscrito=inscripcion.llamado_inscrito,
                tipo_inscripcion=inscripcion.tipo_inscripcion,
                fecha_llamado=mesa_examen.primer_llamado if inscripcion.llamado_inscrito == "primer_llamado" else mesa_examen.segundo_llamado,
                materia_nombre=mesa_examen.materia_nombre,
                carrera_nombre=mesa_examen.carrera_nombre,
                profesor_id=mesa_examen.profesor_id,
                profesor_nombre=mesa_examen.profesor_nombre,
                estudiante_nombre=usuario_estudiante.nombre,
                dni=usuario_estudiante.dni,
                libreta=usuario_estudiante.libreta,
                estado=inscripcion.estado
            )
        )

    # Convierte el diccionario agrupado en una lista de esquemas
    return [
        schemas.TablesExamPerCareerForTeacher(carrera_nombre=carrera_nombre, mesas=mesas)
        for carrera_nombre, mesas in sorted(agrupado.items(), key=lambda item: item[0])
    ]

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
            return schemas.ApiResponse(success=False, errors=["Inscripción a examen no encontrada."])

        # 2. Actualiza el estado de la inscripción
        inscripcion.estado = nuevo_estado.estado
        session.add(inscripcion)
        session.commit()
        session.refresh(inscripcion)

        return schemas.ApiResponse(
            success=True,
            message=f"Estado de inscripción {inscripcion_id} actualizado a '{inscripcion.estado}'.",
            data={
                "id": inscripcion.id,
                "estudiante_id": inscripcion.estudiante_id,
                "mesa_examen_id": inscripcion.mesa_examen_id,
                "estado": inscripcion.estado
            }
        )
    except Exception as e:
        return schemas.ApiResponse(success=False, errors=[f"Error inesperado al actualizar el estado de la inscripción: {str(e)}."])

#
# Elimina una mesa de examen
#
def eliminar_mesa_examen(mesa_examen_id: int, session: Session) -> schemas.ApiResponse:
    # Busca la mesa de examen por ID
    mesa = session.get(models.Mesas_Examen, mesa_examen_id)

    # Si la mesa no existe, retorna un error
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa de examen no encontrada.")

    # Elimina todas las inscripciones asociadas a esta mesa de examen
    statement = select(models.Inscripciones_Examen).where(models.Inscripciones_Examen.mesa_examen_id == mesa_examen_id)
    results = session.execute(statement)
    for inscripcion in results.scalars():
        session.delete(inscripcion)

    session.commit()

    # Elimina la mesa de examen
    session.delete(mesa)
    session.commit()
    return schemas.ApiResponse(success=True, message=f"Mesa de examen eliminada exitosamente.")

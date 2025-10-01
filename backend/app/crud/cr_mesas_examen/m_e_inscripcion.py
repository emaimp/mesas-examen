from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

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
        
        # 9. Determina el número de examen y registra la inscripción si todas las validaciones son correctas
        # Obtener el registro de Notas_Examen para el estudiante y la materia
        nota_examen_existente = session.exec(
            select(models.Notas_Examen)
            .where(
                models.Notas_Examen.estudiante_id == estudiante.id,
                models.Notas_Examen.materia_carrera_id == materia_en_plan.id
            )
        ).first()

        numero_examen_a_asignar = None
        if not nota_examen_existente:
            numero_examen_a_asignar = "primer_examen"
        else:
            if nota_examen_existente.primer_examen is None:
                numero_examen_a_asignar = "primer_examen"
            elif nota_examen_existente.segundo_examen is None and nota_examen_existente.primer_examen != 4:
                numero_examen_a_asignar = "segundo_examen"
            elif nota_examen_existente.tercer_examen is None and nota_examen_existente.primer_examen != 4 and nota_examen_existente.segundo_examen != 4:
                numero_examen_a_asignar = "tercer_examen"
            else:
                # Si ya tiene notas en todos los exámenes o ya aprobó con un 4, no debería poder inscribirse a otro examen.
                # Esto ya está cubierto por la lógica de mesas_examen_por_nota, pero se añade una validación explícita.
                return schemas.ApiResponse(success=False, errors=["Ya has rendido todos los exámenes disponibles o ya la aprobaste."])

        # Verifica si ya existe una inscripción activa para el mismo examen (primer_examen, segundo_examen, tercer_examen)
        existing_active_exam_inscription = session.exec(
            select(models.Inscripciones_Examen)
            .where(
                models.Inscripciones_Examen.estudiante_id == estudiante.id,
                models.Inscripciones_Examen.mesa_examen_id == data.mesa_examen_id,
                models.Inscripciones_Examen.examen == numero_examen_a_asignar,
                models.Inscripciones_Examen.estado == models.Inscripciones_Examen.EstadoInscripcion.activo.value
            )
        ).first()

        if existing_active_exam_inscription:
            return schemas.ApiResponse(success=False, errors=[f"Ya estás inscripto para el {numero_examen_a_asignar} de esta materia."])

        nueva_inscripcion = models.Inscripciones_Examen(
            estudiante_id=data.estudiante_id,
            mesa_examen_id=data.mesa_examen_id,
            llamado_inscrito=data.llamado_inscrito,
            tipo_inscripcion=tipo_inscripcion,
            examen=numero_examen_a_asignar
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
                "tipo_inscripcion": nueva_inscripcion.tipo_inscripcion,
                "examen": nueva_inscripcion.examen
            }
        )
    except HTTPException as e:
        return schemas.ApiResponse(success=False, errors=[e.detail])
    except Exception as e:
        return schemas.ApiResponse(success=False, errors=[f"Error inesperado: {str(e)}"])

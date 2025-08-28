from app import models, schemas
from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, col

#
# Crear un nuevo estudiante en la tabla estudiantes
#
def create_estudiante(session: Session, estudiante_in: schemas.StudentCreate) -> models.Estudiantes:
    # Valida los datos de entrada del estudiantes usando el modelo Estudiantes
    estudiante = models.Estudiantes.model_validate(estudiante_in)
    session.add(estudiante)
    session.commit()
    session.refresh(estudiante)
    return estudiante

#
# Devuelve el id y el nombre de todos los estudiantes
#
def obtener_estudiantes(session: Session, query: Optional[str] = None) -> List[models.Usuarios]:
    # Selecciona todos los usuarios con el rol de "student"
    statement = select(models.Usuarios).where(models.Usuarios.role == "student")
    # Si se proporciona un query, procede a filtrar por nombre (ilike para búsqueda insensible a mayúsculas)
    if query:
        statement = statement.where(col(models.Usuarios.nombre).ilike(f"{query}%"))
    return session.exec(statement).all()

#
# Devuelve un estudiante y toda su información
#
def estudiante_id(estudiante_id: int, session: Session):
    # Obtiene el registro del estudiante en la tabla Estudiantes
    estudiante_record = session.exec(
        select(models.Estudiantes)
        .where(models.Estudiantes.estudiante_id == estudiante_id)
        .options(selectinload(models.Estudiantes.carrera))
    ).first()

    if not estudiante_record:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    # Obtiene el usuario asociado al estudiante
    estudiante = session.exec(
        select(models.Usuarios)
        .where(
            models.Usuarios.id == estudiante_id,
            models.Usuarios.role == "student"
        )
    ).first()

    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante

#
# Devuelve las notas y las correlativas de un estudiante
#
def notas_con_correlativas(estudiante_id: int, session: Session) -> List[schemas.CorreAverageNoteYear]:
    # Obtener el estudiante para verificar su existencia y rol
    estudiante = session.get(models.Usuarios, estudiante_id)
    if not estudiante or estudiante.role != "student":
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Obtener el registro del estudiante en la tabla Estudiantes
    estudiante_record = session.exec(select(models.Estudiantes).where(models.Estudiantes.estudiante_id == estudiante_id)).first()
    if not estudiante_record:
        raise HTTPException(status_code=404, detail="Registro de estudiante no encontrado")

    # Traer todas las materias de la carrera del estudiante, ordenadas por año y nombre
    materias_carrera_statement = (
        select(models.Materia_Carreras)
        .join(models.Materias)
        .where(models.Materia_Carreras.carrera_id == estudiante_record.carrera_id)
        .order_by(models.Materia_Carreras.anio, models.Materias.nombre)
    )
    materias_carrera = session.exec(materias_carrera_statement).all()
    
    # Asignar un código numérico a cada materia
    codigo_por_id = {mc.id: i + 1 for i, mc in enumerate(materias_carrera)}
    
    # Traer todas las notas del estudiante en una sola consulta
    notas_estudiante_statement = select(models.Notas).where(
        models.Notas.estudiante_id == estudiante_id,
        col(models.Notas.materia_carrera_id).in_([mc.id for mc in materias_carrera])
    )
    notas_estudiante = session.exec(notas_estudiante_statement).all()
    
    # Mapea las notas por materia_carrera_id para acceso rápido
    notas_map = {nota.materia_carrera_id: nota for nota in notas_estudiante}
    
    # Traer todas las correlativas de las materias de la carrera en una sola consulta
    correlativas_statement = select(models.Correlativas).where(
        col(models.Correlativas.materia_carrera_id).in_(codigo_por_id.keys())
    )
    correlativas = session.exec(correlativas_statement).all()
    
    # Agrupar correlativas por materia_carrera_id, mapeando correlativa_id a código
    correlativas_por_materia = {}
    
    agrupado = {}

    # Itera sobre las correlativas para agruparlas por materia
    for c in correlativas:
        # Acceder a la relación cargada por el join
        if c.materia_correlativa and c.materia_correlativa.materia_nombre:
            correlativas_por_materia.setdefault(c.materia_carrera_id, []).append(
                schemas.CorrelativeDetail(
                    id=c.materia_correlativa.id,
                    correlativa=c.materia_correlativa.materia_nombre
                )
            )
        else:
            # Fallback si la relación no está cargada o la propiedad no existe
            pass

    # Itera sobre las materias de la carrera para construir la estructura de datos final
    for mc in materias_carrera:
        nota = notas_map.get(mc.id)
        detalle = schemas.CorreAverageNote(
            codigo=codigo_por_id[mc.id],
            materia=mc.materia_nombre,
            nota_prom=nota.nota_prom if nota else None,
            correlativas=[corr_detalle.id for corr_detalle in correlativas_por_materia.get(mc.id, [])]
        )
        agrupado.setdefault(mc.anio, []).append(detalle)

    # Retorna la lista de CorreAverageNoteYear, ordenada por año
    return [
        schemas.CorreAverageNoteYear(anio=anio, materias=materias)
        for anio, materias in sorted(agrupado.items())
    ]

#
# Devuelve las mesas de examen inscriptas de un estudiante
#
def obtener_mesas_inscriptas(estudiante_id: int, session: Session) -> List[schemas.ExamRegistrationDetail]:
    # Obtener el estudiante para verificar su existencia y rol
    estudiante = session.get(models.Usuarios, estudiante_id)
    if not estudiante or estudiante.role != "student":
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Obtener el registro del estudiante en la tabla Estudiantes
    estudiante_record = session.exec(select(models.Estudiantes).where(models.Estudiantes.estudiante_id == estudiante_id)).first()
    if not estudiante_record:
        raise HTTPException(status_code=404, detail="Registro de estudiante no encontrado")

    # Consulta para obtener las inscripciones del estudiante, cargando las mesas de examen y sus relaciones
    statement = (
        select(models.Inscripciones_Examen, models.Mesas_Examen, models.Usuarios)
        .join(models.Mesas_Examen, models.Inscripciones_Examen.mesa_examen_id == models.Mesas_Examen.id)
        .join(models.Usuarios, models.Inscripciones_Examen.estudiante_id == models.Usuarios.id)
        .where(models.Inscripciones_Examen.estudiante_id == estudiante_id)
        .options(
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.materia),
            selectinload(models.Mesas_Examen.profesor_usuario)
        )
    )
    results = session.exec(statement).all()

    # Mapea los resultados del esquema ExamRegistrationDetail para la respuesta
    return [
        schemas.ExamRegistrationDetail(
            id_inscripcion=inscripcion_obj.id,
            estado=inscripcion_obj.estado,
            id=mesa_obj.id,
            llamado_inscrito=inscripcion_obj.llamado_inscrito,
            tipo_inscripcion=inscripcion_obj.tipo_inscripcion,
            fecha_llamado=mesa_obj.primer_llamado if inscripcion_obj.llamado_inscrito == "primer_llamado" else mesa_obj.segundo_llamado,
            materia_nombre=mesa_obj.materia_nombre,
            profesor_nombre=mesa_obj.profesor_nombre,
            carrera_nombre=mesa_obj.carrera_nombre,
            nombre_estudiante=usuario_obj.nombre,
            dni=usuario_obj.dni,
            libreta=usuario_obj.libreta
        )
        for inscripcion_obj, mesa_obj, usuario_obj in results
    ]

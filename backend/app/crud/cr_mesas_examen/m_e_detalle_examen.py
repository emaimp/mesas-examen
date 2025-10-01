from app import models, schemas
from datetime import date
from typing import List, Dict
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Devuelve el detalle de todos los examenes por profesor
#
def mesas_examen_detalle_examen(profesor_id: int, limit: int, offset: int, session: Session) -> List[schemas.TablesStudentExamDetailPerCareer]:
    # Consulta mesas de examen, estudiantes inscritos, el estado de la inscripción y las notas de examen
    statement = (
        select(models.Mesas_Examen, models.Usuarios, models.Inscripciones_Examen, models.Notas_Examen)
        .join(models.Inscripciones_Examen, models.Mesas_Examen.id == models.Inscripciones_Examen.mesa_examen_id)
        .join(models.Usuarios, models.Inscripciones_Examen.estudiante_id == models.Usuarios.id)
        .outerjoin(models.Notas_Examen, and_(
            models.Notas_Examen.estudiante_id == models.Usuarios.id,
            models.Notas_Examen.materia_carrera_id == models.Mesas_Examen.materia_carrera_id
        ))
        .where(models.Mesas_Examen.profesor_id == profesor_id)
        .where(models.Inscripciones_Examen.estado == models.Inscripciones_Examen.EstadoInscripcion.activo.value)
        .where(
            (models.Mesas_Examen.primer_llamado >= date.today()) |
            (models.Mesas_Examen.segundo_llamado >= date.today())
        )
        .options(
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.materia),
            selectinload(models.Mesas_Examen.materia_carrera).selectinload(models.Materia_Carreras.carrera),
            selectinload(models.Mesas_Examen.profesor_usuario)
        )
        .limit(limit)
        .offset(offset)
    )
    results = session.exec(statement).all()

    # Agrupa los resultados por carrera
    agrupado: Dict[str, List[schemas.StudentExamDetailForTeacher]] = {}
    for mesa_examen, usuario_estudiante, inscripcion, nota_examen in results:
        carrera_nombre = mesa_examen.carrera_nombre
        if carrera_nombre not in agrupado:
            agrupado[carrera_nombre] = []

        # Determinar la nota según el llamado inscrito
        nota_final = None
        if nota_examen:
            if inscripcion.examen == "primer_examen":
                nota_final = nota_examen.primer_examen
            elif inscripcion.examen == "segundo_examen":
                nota_final = nota_examen.segundo_examen
            elif inscripcion.examen == "tercer_examen":
                nota_final = nota_examen.tercer_examen

        agrupado[carrera_nombre].append(
            schemas.StudentExamDetailForTeacher(
                id=mesa_examen.id,
                id_profesor=mesa_examen.profesor_id,
                id_inscripcion=inscripcion.id,
                materia_nombre=mesa_examen.materia_nombre,
                estudiante_nombre=usuario_estudiante.nombre,
                dni=usuario_estudiante.dni,
                libreta=usuario_estudiante.libreta,
                fecha_llamado=mesa_examen.primer_llamado if inscripcion.llamado_inscrito == "primer_llamado" else mesa_examen.segundo_llamado,
                llamado_inscrito=inscripcion.llamado_inscrito,
                tipo_inscripcion=inscripcion.tipo_inscripcion,
                asistencia=inscripcion.asistencia,
                nota=nota_final,
                estado=inscripcion.estado
            )
        )

    # Convierte el diccionario agrupado en una lista de esquemas
    return [
        schemas.TablesStudentExamDetailPerCareer(carrera_nombre=carrera_nombre, mesas=mesas)
        for carrera_nombre, mesas in sorted(agrupado.items(), key=lambda item: item[0])
    ]

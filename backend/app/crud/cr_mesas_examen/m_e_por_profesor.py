from app import models, schemas
from typing import List, Dict
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Devuelve las mesas de examen por profesor
#
def mesas_examen_por_profesor(profesor_id: int, session: Session) -> List[schemas.TablesExamPerCareerForTeacher]:
    # Consulta mesas de examen, estudiantes inscritos y el estado de la inscripción
    statement = (
        select(models.Mesas_Examen, models.Usuarios, models.Inscripciones_Examen, models.Estudiantes)
        .join(models.Inscripciones_Examen, models.Mesas_Examen.id == models.Inscripciones_Examen.mesa_examen_id)
        .join(models.Usuarios, models.Inscripciones_Examen.estudiante_id == models.Usuarios.id)
        .join(models.Estudiantes, models.Usuarios.id == models.Estudiantes.estudiante_id)
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
    for mesa_examen, usuario_estudiante, inscripcion, estudiante in results:
        carrera_nombre = mesa_examen.carrera_nombre
        if carrera_nombre not in agrupado:
            agrupado[carrera_nombre] = []
        agrupado[carrera_nombre].append(
            schemas.ExamWithStudentsDetail(
                id=mesa_examen.id,
                id_inscripcion=inscripcion.id,
                llamado_inscrito=inscripcion.llamado_inscrito,
                tipo_inscripcion=inscripcion.tipo_inscripcion,
                fecha_llamado=mesa_examen.primer_llamado if inscripcion.llamado_inscrito == "primer_llamado" else mesa_examen.segundo_llamado,
                materia_nombre=mesa_examen.materia_nombre,
                carrera_nombre=mesa_examen.carrera_nombre,
                id_profesor=mesa_examen.profesor_id,
                profesor_nombre=mesa_examen.profesor_nombre,
                estudiante_nombre=usuario_estudiante.nombre,
                dni=usuario_estudiante.dni,
                libreta=estudiante.libreta,
                estado=inscripcion.estado
            )
        )

    # Convierte el diccionario agrupado en una lista de esquemas
    return [
        schemas.TablesExamPerCareerForTeacher(carrera_nombre=carrera_nombre, mesas=mesas)
        for carrera_nombre, mesas in sorted(agrupado.items(), key=lambda item: item[0])
    ]

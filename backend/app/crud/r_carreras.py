from app import models, schemas
from typing import List, Optional, Dict
from sqlmodel import Session, select, col

#
# Devuelve todas las carreras
#
def obtener_carreras(session: Session, query: Optional[str] = None) -> List[models.Carreras]:
    statement = select(models.Carreras)
    if query:
        statement = statement.where(col(models.Carreras.nombre).ilike(f"{query}%"))
    return session.exec(statement).all()

#
# Devuelve las materias pertenecientes a una carrera
#
def obtener_materias_carrera(session: Session, carrera_id: int, query: Optional[str] = None) -> List[models.Materia_Carreras]:
    statement = select(models.Materia_Carreras).where(models.Materia_Carreras.carrera_id == carrera_id)
    if query:
        statement = statement.join(models.Materias).where(col(models.Materias.nombre).ilike(f"{query}%"))
    return session.exec(statement).all()

#
# Devuelve los estudiantes pertenecientes a una carrera
#
def estudiantes_por_carrera(session: Session, carrera_id: int, query: Optional[str] = None) -> List[models.Usuarios]:
    statement = select(models.Usuarios).join(models.Estudiantes).where(
        models.Estudiantes.carrera_id == carrera_id,
        models.Usuarios.role == "student"
    )
    if query:
        statement = statement.where(col(models.Usuarios.nombre).ilike(f"{query}%"))
    return session.exec(statement).all()

#
# Devuelve los profesores pertenecientes a una carrera
#
def obtener_profesores(session: Session, carrera_id: int, query: Optional[str] = None) -> List[models.Usuarios]:
    statement = select(models.Usuarios).join(models.Profesores).join(models.Materia_Carreras).where(
        models.Profesores.profesor_id == models.Usuarios.id,
        models.Materia_Carreras.carrera_id == carrera_id).where(
        models.Usuarios.role == "teacher")
    if query:
        statement = statement.where(col(models.Usuarios.nombre).ilike(f"{query}%"))
    return session.exec(statement).all()

#
# Devuelve las correlativas de una carrera
#
def correlativas_por_carrera(carrera_id: int, session: Session) -> List[schemas.CorrelativesSubject]:
    # Obtener todas las materias de la carrera con sus relaciones de materia
    materias_carrera_statement = (
        select(models.Materia_Carreras)
        .join(models.Materias)
        .where(models.Materia_Carreras.carrera_id == carrera_id)
    )
    materias_carrera = session.exec(materias_carrera_statement).all()

    # Obtener todas las correlativas relevantes con sus relaciones de materia_carrera y materia
    correlativas_statement = (
        select(models.Correlativas)
        .join(models.Materia_Carreras, models.Correlativas.correlativa_id == models.Materia_Carreras.id)
        .join(models.Materias, models.Materia_Carreras.materia_id == models.Materias.id)
        .where(col(models.Correlativas.materia_carrera_id).in_([mc.id for mc in materias_carrera]))
    )
    correlativas = session.exec(correlativas_statement).all()

    # Mapear correlativas por materia_carrera_id
    correlativas_map: Dict[int, List[schemas.CorrelativeDetail]] = {}
    for corr in correlativas:

        # Acceder a la relación cargada por el join
        if corr.materia_correlativa and corr.materia_correlativa.materia_nombre:
            correlativas_map.setdefault(corr.materia_carrera_id, []).append(
                schemas.CorrelativeDetail(
                    id=corr.materia_correlativa.id,
                    correlativa=corr.materia_correlativa.materia_nombre
                )
            )
        else:
            # Si la relación no está cargada o la propiedad no existe podría requerir un selectinload
            pass

    resultado: List[schemas.CorrelativesSubject] = []
    for mc in materias_carrera:
        resultado.append(
            schemas.CorrelativesSubject(
                id=mc.id,
                materia=mc.materia_nombre, # Usar la propiedad materia_nombre de MateriaCarrera
                correlativas=correlativas_map.get(mc.id, [])
            )
        )
    return resultado

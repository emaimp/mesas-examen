from app import models, schemas
from typing import List, Dict
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

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

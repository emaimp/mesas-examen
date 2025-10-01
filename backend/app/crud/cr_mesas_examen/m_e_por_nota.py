from app import models, schemas
from typing import List, Dict
from datetime import date, timedelta
from sqlalchemy import and_
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Devuelve las mesas de examen por nota del estudiante
#
def mesas_examen_por_nota(estudiante_id: int, session: Session) -> List[schemas.TablesExamPerNote]:
    # Define el rango de fechas para buscar mesas de examen
    hoy = date.today()
    tres_meses = hoy + timedelta(days=90)

    # Construye la consulta para obtener mesas de examen
    # Subconsulta para verificar si el estudiante ya aprobó la materia con un 4 en Notas_Examen
    subquery_aprobado_examen = (
        select(models.Notas_Examen.materia_carrera_id)
        .where(
            models.Notas_Examen.estudiante_id == estudiante_id,
            (models.Notas_Examen.primer_examen == 4) |
            (models.Notas_Examen.segundo_examen == 4) |
            (models.Notas_Examen.tercer_examen == 4)
        )
    ).subquery()

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
             (models.Mesas_Examen.segundo_llamado <= tres_meses)),
            # Excluye las mesas de examen si el estudiante ya aprobó con un 4 en Notas_Examen
            ~models.Mesas_Examen.materia_carrera_id.in_(subquery_aprobado_examen)
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

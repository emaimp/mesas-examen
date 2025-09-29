from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select

#
# Obtiene el porcentaje de inscripciones activas y canceladas en mesas de examen
#
def porcentaje_inscripciones_carrera(session: Session, carrera_id: int) -> schemas.EnrollmentCareer:
    # Busca la carrera por su ID
    carrera = session.get(models.Carreras, carrera_id)
    # Si la carrera no existe, lanza un error
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Consulta todas las mesas de examen de la carrera
    all_mesas_in_career_statement = (
        select(models.Mesas_Examen)
        .join(models.Materia_Carreras)
        .where(models.Materia_Carreras.carrera_id == carrera_id)
    )
    all_mesas_in_career = session.exec(all_mesas_in_career_statement).all()

    total_inscripciones = 0
    activos_count = 0
    cancelados_count = 0

    # Para cada mesa de examen, cuenta las inscripciones activas y canceladas
    for mesa in all_mesas_in_career:
        inscripciones_statement = select(models.Inscripciones_Examen).where(models.Inscripciones_Examen.mesa_examen_id == mesa.id)
        inscripciones = session.exec(inscripciones_statement).all()
        total_inscripciones += len(inscripciones)
        for inscripcion in inscripciones:
            if inscripcion.estado == "active":
                activos_count += 1
            elif inscripcion.estado == "canceled":
                cancelados_count += 1

    # Calcula los porcentajes de cada categoría
    activos_percentage = round((activos_count / total_inscripciones * 100), 2) \
        if total_inscripciones > 0 else 0.0
    cancelados_percentage = round((cancelados_count / total_inscripciones * 100), 2) \
        if total_inscripciones > 0 else 0.0

    # Retorna un objeto con los resultados de las inscripciones
    return schemas.EnrollmentCareer(
        carrera_id=carrera_id,
        carrera_nombre=carrera.nombre,  # Accede al nombre de la carrera
        activos_count=activos_count,
        activos_percentage=activos_percentage,
        cancelados_count=cancelados_count,
        cancelados_percentage=cancelados_percentage,
        total_inscripciones=total_inscripciones
    )

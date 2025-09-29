from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select

#
# Obtiene el rendimiento promedio de las notas en una carrera (promocionados, regulares y libres)
#
def rendimiento_promedio_carrera(session: Session, carrera_id: int) -> schemas.PerformanceCareer:
    # Busca la carrera por su ID
    carrera = session.get(models.Carreras, carrera_id)
    # Si la carrera no existe, lanza un error
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    
    # Consulta todas las notas de las materias de la carrera
    all_notas_in_career_statement = (
        select(models.Notas)
        .join(models.Materia_Carreras)
        .where(models.Materia_Carreras.carrera_id == carrera_id)
    )
    all_notas_in_career = session.exec(all_notas_in_career_statement).all()
    
    promocionados_count = 0
    regulares_count = 0
    libres_count = 0
    total_notas_evaluadas = len(all_notas_in_career)
    
    # Calcula el número de promocionados, regulares y libres
    if total_notas_evaluadas > 0:
        for nota in all_notas_in_career:
            if nota.nota_prom >= 7.0:
                promocionados_count += 1
            elif nota.nota_prom >= 4.0 and nota.nota_prom < 7.0:
                regulares_count += 1
            elif nota.nota_prom < 4.0:
                libres_count += 1
    
    # Calcula los porcentajes de cada categoría
    promocionados_percentage = round((promocionados_count / total_notas_evaluadas * 100), 2) \
        if total_notas_evaluadas > 0 else 0.0
    regulares_percentage = round((regulares_count / total_notas_evaluadas * 100), 2) \
        if total_notas_evaluadas > 0 else 0.0
    libres_percentage = round((libres_count / total_notas_evaluadas * 100), 2) \
        if total_notas_evaluadas > 0 else 0.0
    
    # Retorna un objeto con los resultados del rendimiento
    return schemas.PerformanceCareer(
        carrera_id=carrera_id,
        carrera_nombre=carrera.nombre, # Accede al nombre de la carrera
        promocionados_count=promocionados_count,
        promocionados_percentage=promocionados_percentage,
        regulares_count=regulares_count,
        regulares_percentage=regulares_percentage,
        libres_count=libres_count,
        libres_percentage=libres_percentage,
        total_notas_evaluadas=total_notas_evaluadas
    )

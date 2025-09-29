from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select

#
# Obtiene el porcentaje de aprobados y desaprobados en mesas de examen
#
def rendimiento_mesas_examen_carrera(session: Session, carrera_id: int) -> schemas.ExamApprovalCareer:
    # Busca la carrera por su ID
    carrera = session.get(models.Carreras, carrera_id)
    # Si la carrera no existe, lanza un error
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Consulta todas las notas de examen en la carrera
    all_exam_notes_in_career_statement = (
        select(models.Notas_Examen)
        .join(models.Materia_Carreras)
        .where(models.Materia_Carreras.carrera_id == carrera_id)
    )
    all_exam_notes_in_career = session.exec(all_exam_notes_in_career_statement).all()

    aprobados_count = 0
    desaprobados_count = 0
    total_examenes_evaluados = 0

    # Calcula el número de exámenes aprobados y desaprobados
    for nota_examen in all_exam_notes_in_career:
        # Chequear primer examen
        if nota_examen.primer_examen is not None:
            total_examenes_evaluados += 1
            if nota_examen.primer_examen >= 4:
                aprobados_count += 1
            else:
                desaprobados_count += 1
        # Chequear segundo examen
        if nota_examen.segundo_examen is not None:
            total_examenes_evaluados += 1
            if nota_examen.segundo_examen >= 4:
                aprobados_count += 1
            else:
                desaprobados_count += 1
        # Chequear tercer examen
        if nota_examen.tercer_examen is not None:
            total_examenes_evaluados += 1
            if nota_examen.tercer_examen >= 4:
                aprobados_count += 1
            else:
                desaprobados_count += 1

    # Calcula los porcentajes de cada categoría
    aprobados_percentage = round((aprobados_count / total_examenes_evaluados * 100), 2) \
        if total_examenes_evaluados > 0 else 0.0
    desaprobados_percentage = round((desaprobados_count / total_examenes_evaluados * 100), 2) \
        if total_examenes_evaluados > 0 else 0.0

    # Retorna un objeto con los resultados de la aprobación de exámenes
    return schemas.ExamApprovalCareer(
        carrera_id=carrera_id,
        carrera_nombre=carrera.nombre,
        aprobados_count=aprobados_count,
        aprobados_percentage=aprobados_percentage,
        desaprobados_count=desaprobados_count,
        desaprobados_percentage=desaprobados_percentage,
        total_examenes_evaluados=total_examenes_evaluados
    )

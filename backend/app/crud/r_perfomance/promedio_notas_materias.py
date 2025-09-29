from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select

#
# Obtiene el promedio de las notas por cada materia
#
def promedio_notas_materias_carrera(session: Session, carrera_id: int) -> schemas.GradesAverageCareer:
    # Busca la carrera por su ID
    carrera = session.get(models.Carreras, carrera_id)
    # Si la carrera no existe, lanza un error
    if not carrera:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")

    # Consulta todas las notas de la carrera con información de materia
    notas_statement = (
        select(models.Notas, models.Materia_Carreras, models.Materias)
        .join(models.Materia_Carreras, models.Notas.materia_carrera_id == models.Materia_Carreras.id)
        .join(models.Materias, models.Materia_Carreras.materia_id == models.Materias.id)
        .where(models.Materia_Carreras.carrera_id == carrera_id)
    )
    notas = session.exec(notas_statement).all()

    # Agrupar notas por materia
    from collections import defaultdict
    grades_by_subject = defaultdict(list)
    for nota, _, materia in notas:
        grades_by_subject[materia.nombre].append(nota.nota_prom)

    # Calcular el promedio y crear lista de asuntos
    subjects_list = []
    for materia_nombre, lista_notas in grades_by_subject.items():
        if lista_notas:
            average_grade = round(sum(lista_notas) / len(lista_notas), 2)
            total_students = len(lista_notas)
        else:
            average_grade = 0.0
            total_students = 0
        subjects_list.append(
            schemas.SubjectGradeAverage(
                materia_nombre=materia_nombre,
                materia_promedio=average_grade,
                total_students=total_students
            )
        )

    # Retorna el objeto con los resultados de los promedios por materia
    return schemas.GradesAverageCareer(
        carrera_id=carrera_id,
        carrera_nombre=carrera.nombre,
        materias=subjects_list
    )

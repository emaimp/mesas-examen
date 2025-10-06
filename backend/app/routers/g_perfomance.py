from app import db, crud, schemas
from sqlmodel import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/carreras", tags=["Estadísticas"])

#
# Endpoint: Devuelve el porcentaje de inscripciones activas y canceladas en mesas de examen (id)
#
@router.get("/{carrera_id}/porcentaje_inscripciones", response_model=schemas.EnrollmentCareer)
def porcentaje_inscripciones_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.porcentaje_inscripciones_carrera(session, carrera_id)

#
# Endpoint: Devuelve el rendimiento en mesas de examen: Porcentaje de aprobados y desaprobados (id)
#
@router.get("/{carrera_id}/rendimiento_examenes", response_model=schemas.ExamApprovalCareer)
def rendimiento_mesas_examen_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.rendimiento_mesas_examen_carrera(session, carrera_id)

#
# Endpoint: Devuelve el rendimiento promedio de las notas en una carrera: Promocionados, Regulares y Libres (id)
#
@router.get("/{carrera_id}/rendimiento_promedio", response_model=schemas.PerformanceCareer)
def rendimiento_promedio_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.rendimiento_promedio_carrera(session, carrera_id)

#
# Endpoint: Devuelve la predicción del rendimiento futuro de una carrera usando ML (id)
#
@router.get("/{carrera_id}/prediccion_rendimiento", response_model=schemas.PerformanceCareer)
def prediccion_rendimiento_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.prediccion_rendimiento_carrera(session, carrera_id)

#
# Endpoint: Devuelve el promedio de las notas por cada materia (id)
#
@router.get("/{carrera_id}/promedio_notas_materia", response_model=schemas.GradesAverageCareer)
def promedio_notas_materias_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.promedio_notas_materias_carrera(session, carrera_id)

#
# Endpoint: Devuelve el rendimiento demográfico de una carrera (id)
#
@router.get("/{carrera_id}/rendimiento_demografico", response_model=schemas.PerformanceDemographic)
def rendimiento_demografico_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.rendimiento_demografico_carrera(session, carrera_id)

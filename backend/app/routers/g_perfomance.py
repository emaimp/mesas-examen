from app import db, crud, schemas
from sqlmodel import Session
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/carreras", tags=["Desempeño Académico"])

#
# Endpoint: Devuelve el rendimiento global de una carrera, promocionados, regulares y libres (id)
#
@router.get("/{carrera_id}/notas_promedio", response_model=schemas.PerformanceCareer)
def notas_promedio_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.rendimiento_carrera(session, carrera_id)

#
# Endpoint: Devuelve la cantidad de inscripciones activas y canceladas en mesas de examen de una carrera (id)
#
@router.get("/{carrera_id}/cantidad_inscripciones", response_model=schemas.EnrollmentCareer)
def cantidad_inscripciones_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.cantidad_inscripciones_carrera(session, carrera_id)

#
# Endpoint: Devuelve la predicción del rendimiento futuro de una carrera usando ML (id)
#
@router.get("/{carrera_id}/prediccion_rendimiento", response_model=schemas.PerformanceCareer)
def prediccion_rendimiento_carrera(carrera_id: int, session: Session = Depends(db.get_session)):
    return crud.r_perfomance.predict_rendimiento_carrera(session, carrera_id)

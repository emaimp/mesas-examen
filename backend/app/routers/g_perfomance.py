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

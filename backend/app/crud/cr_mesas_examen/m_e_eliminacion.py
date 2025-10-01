from app import models, schemas
from fastapi import HTTPException
from sqlmodel import Session, select

#
# Elimina una mesa de examen
#
def eliminar_mesa_examen(mesa_examen_id: int, session: Session) -> schemas.ApiResponse:
    # Busca la mesa de examen por ID
    mesa = session.get(models.Mesas_Examen, mesa_examen_id)

    # Si la mesa no existe, retorna un error
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa de examen no encontrada.")

    # Elimina todas las inscripciones asociadas a esta mesa de examen
    statement = select(models.Inscripciones_Examen).where(models.Inscripciones_Examen.mesa_examen_id == mesa_examen_id)
    results = session.execute(statement)
    for inscripcion in results.scalars():
        session.delete(inscripcion)

    session.commit()

    # Elimina la mesa de examen
    session.delete(mesa)
    session.commit()
    return schemas.ApiResponse(success=True, message=f"Mesa de examen eliminada exitosamente.")

from app import models, schemas
from sqlmodel import Session

#
# Actualiza el estado de una inscripción
#
def actualizar_estado_inscripcion(
    inscripcion_id: int,
    nuevo_estado: schemas.RegistrationExamUpdateStatus,
    session: Session
) -> schemas.ApiResponse:
    try:
        # 1. Busca la inscripción por ID
        inscripcion = session.get(models.Inscripciones_Examen, inscripcion_id)

        # Si la inscripción no existe, retorna un error
        if not inscripcion:
            return schemas.ApiResponse(success=False, errors=["Inscripción a examen no encontrada."])

        # 2. Actualiza el estado de la inscripción
        inscripcion.estado = nuevo_estado.estado
        session.add(inscripcion)
        session.commit()
        session.refresh(inscripcion)

        return schemas.ApiResponse(
            success=True,
            message=f"Estado de inscripción {inscripcion_id} actualizado a '{inscripcion.estado}'.",
            data={
                "id": inscripcion.id,
                "estudiante_id": inscripcion.estudiante_id,
                "mesa_examen_id": inscripcion.mesa_examen_id,
                "estado": inscripcion.estado
            }
        )
    except Exception as e:
        return schemas.ApiResponse(success=False, errors=[f"Error inesperado al actualizar el estado de la inscripción: {str(e)}."])

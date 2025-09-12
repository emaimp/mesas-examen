from sqlmodel import select
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.models import Actas_Digitales, Usuarios

#
# Obtiene el registro de un acta de la base de datos utilizando el id
#
def pdf_record_id(db: Session, pdf_id: int) -> Optional[Actas_Digitales]:
    return db.get(Actas_Digitales, pdf_id)

#
# Obtiene una lista de todos los registros de actas por nombre de usuario
#
def pdf_records_uploader(db: Session, nombre: str) -> List[Actas_Digitales]:
    statement = (
        select(Actas_Digitales)
        .join(Usuarios, Actas_Digitales.uploaded_user_id == Usuarios.id)
        .where(Usuarios.nombre.ilike(nombre))
    )
    return db.exec(statement).all()

from sqlmodel import select
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.models import Actas_Digitales, Usuarios, Profesores

# Obtiene un registro de acta digital en formato PDF de la base de datos
def get_pdf_record_by_id(db: Session, pdf_id: int) -> Optional[Actas_Digitales]:
    return db.get(Actas_Digitales, pdf_id)

# Obtiene un registro de acta digital en formato PDF de la base de datos
def get_pdf_record_by_filename(db: Session, filename: str) -> Optional[Actas_Digitales]:
    statement = select(Actas_Digitales).where(Actas_Digitales.filename == filename)
    return db.exec(statement).first()

# Obtiene una lista de todos los registros de actas digitales
def get_pdf_records_by_user(db: Session, user_id: int) -> List[Actas_Digitales]:
    statement = select(Actas_Digitales).where(Actas_Digitales.uploaded_user_id == user_id)
    return db.exec(statement).all()

# Obtiene una lista de todos los registros de actas digitales por nombre de usuario
def get_pdf_records_by_uploader_name(db: Session, nombre: str) -> List[Actas_Digitales]:
    statement = (
        select(Actas_Digitales)
        .join(Usuarios, Actas_Digitales.uploaded_user_id == Usuarios.id)
        .where(Usuarios.nombre.ilike(nombre))
    )
    return db.exec(statement).all()

# Obtiene un registro de profesor de la base de datos utilizando su ID de usuario
def get_professor_by_user_id(db: Session, user_id: int) -> Optional[Profesores]:
    statement = select(Profesores).where(Profesores.profesor_id == user_id)
    return db.exec(statement).first()

from app import core, models, schemas
from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Crea un nuevo usuario en la base de datos
#
def create_user(session: Session, user_in: schemas.UserCreate):
    # Hashea la contraseña antes de guardarla
    hashed_password = core.security.get_password_hash(user_in.password)
    
    # Crea el objeto Usuarios con todos los campos, usando "getattr" para los opcionales
    user = models.Usuarios(
        username=user_in.username,
        password_hash=hashed_password,
        role=user_in.role,
        nombre=user_in.nombre,
        dni=user_in.dni,
        email=user_in.email
    )
    # Agrega el usuario a la sesión
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#
# Crea múltiples usuarios en la base de datos
#
def create_multiple_users(session: Session, users_in: List[schemas.UserCreate]) -> List[models.Usuarios]:
    users = []
    for user_in in users_in:
        hashed_password = core.security.get_password_hash(user_in.password)
        user = models.Usuarios(
            username=user_in.username,
            password_hash=hashed_password,
            role=user_in.role,
            nombre=user_in.nombre,
            dni=user_in.dni,
            email=user_in.email
        )
        users.append(user)
    
    session.add_all(users)
    session.commit()
    for user in users:
        session.refresh(user)
    return users

#
# Obtiene un usuario por sus campos únicos
#
def get_user_unique_fields(session: Session, user_in: schemas.UserCreate) -> Optional[models.Usuarios]:
    statement = select(models.Usuarios).where(
        (models.Usuarios.username == user_in.username) |
        (models.Usuarios.dni == user_in.dni)
    )
    if user_in.email:
        statement = statement.where(models.Usuarios.email == user_in.email)
    
    return session.exec(statement).first()

#
# Obtiene un usuario por su nombre de usuario
#
def get_username(session: Session, username: str):
    # Devuelve el usuario encontrado, o None si no existe
    return session.exec(select(models.Usuarios)
        .where(models.Usuarios.username == username)
        .options(selectinload(models.Usuarios.asignaciones_estudiante)
        .selectinload(models.Estudiantes.carrera))).first()

#
# Actualiza la contraseña de un usuario
#
def update_user_password(session: Session, user_id: int, current_password: str, new_password: str) -> models.Usuarios:
    user = session.get(models.Usuarios, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if not core.security.verify_password(current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Contraseña actual incorrecta")
    
    user.password_hash = core.security.get_password_hash(new_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

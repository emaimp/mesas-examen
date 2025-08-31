from app import core, models, schemas
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
        email=user_in.email,
        legajo=getattr(user_in, 'legajo', None),
        libreta=getattr(user_in, 'libreta', None)
    )
    # Agrega el usuario a la sesión
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

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

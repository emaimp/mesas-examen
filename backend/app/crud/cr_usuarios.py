from app import core, models, schemas
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

#
# Crea un nuevo usuario en la base de datos
#
def create_user(session: Session, user_in: schemas.UserCreate):
    # Hashea la contraseña antes de guardarla
    hashed_password = core.get_password_hash(user_in.password)
    
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

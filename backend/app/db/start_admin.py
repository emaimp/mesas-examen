from sqlmodel import Session
from app import db, crud, schemas
from pydantic_settings import BaseSettings, SettingsConfigDict

# Configuración de las variables de entorno para el usuario administrador
class AdminSettings(BaseSettings):
    INITIAL_ADMIN_USERNAME: str
    INITIAL_ADMIN_PASSWORD: str
    INITIAL_ADMIN_NOMBRE: str
    INITIAL_ADMIN_DNI: str
    INITIAL_ADMIN_EMAIL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

admin_settings = AdminSettings()

# Creación del usuario administrador inicial
def create_initial_admin_user():
    # Datos del usuario administrador inicial
    username = admin_settings.INITIAL_ADMIN_USERNAME
    password = admin_settings.INITIAL_ADMIN_PASSWORD
    nombre = admin_settings.INITIAL_ADMIN_NOMBRE
    dni = admin_settings.INITIAL_ADMIN_DNI
    email = admin_settings.INITIAL_ADMIN_EMAIL
    role = "admin"

    with Session(db.engine) as session:
        # Verificar si el usuario ya existe
        existing_user = crud.cr_usuarios.get_username(session, username=username)
        if existing_user:
            return

        # Crear el usuario con los campos específicos de rol como None para el admin
        user_in = schemas.UserCreate(
            username=username,
            password=password,
            nombre=nombre,
            dni=dni,
            email=email,
            role=role,
            libreta=None, # None para admin
            legajo=None # None para admin
        )
        try:
            new_admin = crud.cr_usuarios.create_user(session=session, user_in=user_in)
            print(f"✅ Usuario '{new_admin.username}' creado exitosamente.")
        except Exception as e:
            print(f"❎ Error al crear el usuario: {e}")

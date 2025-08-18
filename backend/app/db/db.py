import pymysql
from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# Configuración de la base de datos usando pydantic-settings
class Settings(BaseSettings):
    DB_USERNAME: str # Nombre de usuario para la conexión
    DB_PASSWORD: str # Contraseña para la conexión
    DB_HOST: str # Host de la base de datos
    DB_PORT: int # Puerto de la base de datos
    DB_NAME: str # Nombre de la base de datos

# Configuración para cargar variables de entorno desde el archivo .env
    model_config = SettingsConfigDict(
        env_file=".env", # Busca el archivo .env en el directorio raíz del proyecto
        env_file_encoding='utf-8', # Codificación del archivo .env
        extra='ignore' # Ignora variables de entorno adicionales
    )

settings = Settings()

# URL de la base de datos MySQL con PyMySQL, construida con las variables de entorno
DATABASE_URL = f"mysql+pymysql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL, echo=False, pool_recycle=3600) # pool_recycle sirve para conexiones MySQL de larga duración

# Función para crear la base de datos si no existe
def create_database():
    try:
        # Conectarse a MySQL sin especificar una base de datos
        connection = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USERNAME,
            password=settings.DB_PASSWORD
        )
        
        with connection:
            with connection.cursor() as cursor:
                # Crear la base de datos
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {settings.DB_NAME}")
                connection.commit()
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")
        raise

# Función para crear las tablas en la base de datos
def create_db_and_tables():
    # Primero crear la base de datos si no existe
    create_database()
    # Luego crear las tablas
    SQLModel.metadata.create_all(engine)

# Dependencia para obtener una sesión de base de datos
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

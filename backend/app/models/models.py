from enum import Enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, Relationship, SQLModel

"""
TABLA: USUARIOS
"""
# Representa a los usuarios del sistema, incluyendo estudiantes y profesores.
class Usuarios(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(max_length=50, unique=True, index=True) # Nickname del usuario
    password_hash: str = Field(max_length=100) # Contraseña hasheada
    role: str = Field(max_length=10) # Rol del usuario
    nombre: str = Field(max_length=50, index=True) # Nombre completo del usuario
    dni: str = Field(max_length=10, unique=True)
    email: Optional[str] = Field(default=None, max_length=50, unique=True) # Opcional
    legajo: Optional[str] = Field(default=None, max_length=10, unique=True) # Opcional
    libreta: Optional[str] = Field(default=None, max_length=10, unique=True) # Opcional

    # Relaciones con otras tablas
    # Un usuario (estudiante) puede tener muchas notas
    notas: List["Notas"] = Relationship(back_populates="estudiante_user")
    # Un usuario (estudiante) puede tener muchos prácticos
    practicos: List["Practicos"] = Relationship(back_populates="estudiante_user")
    # Un usuario (estudiante) puede tener muchas inscripciones a examen
    inscripciones: List["Inscripciones_Examen"] = Relationship(back_populates="estudiante_user")
    # Un usuario (estudiante) puede tener muchas asignaciones como estudiante
    asignaciones_estudiante: List["Estudiantes"] = Relationship(back_populates="usuario")
    # Un usuario (profesor) puede tener muchas asignaciones como profesor
    asignaciones_profesor: List["Profesores"] = Relationship(back_populates="usuario")
    # Un usuario (profesor) puede dictar muchas mesas de examen
    mesas_examen_dictadas: List["Mesas_Examen"] = Relationship(back_populates="profesor_usuario")
    # Un usuario (estudiante) puede tener muchas notas de examen
    notas_examen: List["Notas_Examen"] = Relationship(back_populates="estudiante_user_examen")
    # Un usuario puede haber subido muchas actas digitales
    actas_digitales_subidas: List["Actas_Digitales_PDF"] = Relationship(back_populates="uploaded_by_user")

"""
TABLA: PROFESORES
"""
# Define a los profesores en sus respectivas materia_carrera y año de asignación.
class Profesores(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('profesor_id', 'materia_carrera_id', 'anio_asignado', name='uq_profesor_materia_carrera_anio'),
    )
    id: int = Field(default=None, primary_key=True)
    profesor_id: int = Field(foreign_key="usuarios.id") # ID del profesor (FK a Usuarios)
    materia_carrera_id: int = Field(foreign_key="materia_carreras.id") # ID de materia_carrera (FK a Materia_Carreras)
    anio_asignado: int = None

    # Relaciones con otras tablas
    # Referencia al usuario con el rol de profesor
    usuario: "Usuarios" = Relationship(back_populates="asignaciones_profesor")
    # Referencia a la materia_carrera asignada
    materia_carrera: "Materia_Carreras" = Relationship(back_populates="profesores")

"""
TABLA: ESTUDIANTES
"""
# Define a los estudiantes en sus respectivas carreras y año de ingreso.
class Estudiantes(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('estudiante_id', 'carrera_id', 'anio_ingreso', name='uq_estudiante_carrera_anio_ingreso'),
    )
    id: int = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="usuarios.id") # ID del estudiante (FK a Usuarios)
    carrera_id: int = Field(foreign_key="carreras.id") # ID de la carrera (FK a Carreras)
    anio_ingreso: int = None

    # Relaciones
    # Referencia al usuario con el rol de estudiante
    usuario: "Usuarios" = Relationship(back_populates="asignaciones_estudiante")
    # Referencia a la carrera en la que se inscribió el estudiante
    carrera: "Carreras" = Relationship(back_populates="estudiantes_carrera")

    # Propiedades para obtener el nombre del estudiante y la carrera
    @property
    def estudiante_nombre(self):
        return self.usuario.nombre if self.usuario else None
    @property
    def carrera_nombre(self):
        return self.carrera.nombre if self.carrera else None

"""
TABLA: CARRERAS
"""
# Define las diferentes carreras.
class Carreras(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True)

    # Relaciones con otras tablas
    # Una carrera puede tener muchas materias asociadas
    materias_carrera: List["Materia_Carreras"] = Relationship(back_populates="carrera")
    # Una carrera puede tener muchos estudiantes
    estudiantes_carrera: List["Estudiantes"] = Relationship(back_populates="carrera")

"""
TABLA: MATERIAS
"""
# Define las diferentes materias.
class Materias(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, unique=True)

    # Relaciones con otras tablas
    # Una materia puede estar en varias carreras (a través de Materia_Carreras)
    materias_carrera: List["Materia_Carreras"] = Relationship(back_populates="materia")

"""
TABLA: MATERIA CARRERAS
"""
# Tabla intermedia que relaciona materias con carreras (establece las materias que se dictaran en cada carrera).
class Materia_Carreras(SQLModel, table=True):
    # Restricción de unicidad para asegurar que una materia solo se asocie una vez a una carrera
    __table_args__ = (
        UniqueConstraint("materia_id", "carrera_id", name="uq_materia_carrera"),
    )
    id: int = Field(default=None, primary_key=True)
    materia_id: int = Field(foreign_key="materias.id") # ID de la materia (FK a Materias)
    carrera_id: int = Field(foreign_key="carreras.id") # ID de la carrera (FK a Carreras)
    anio: int = None # Año al que pertenece la materia en esa carrera

    # Relaciones con otras tablas
    # Una asociación materia_carrera puede tener muchas notas asociadas
    notas: List["Notas"] = Relationship(back_populates="materia_carrera")
    # Referencia a la materia
    materia: Materias = Relationship(back_populates="materias_carrera")
    # Referencia a la carrera
    carrera: Carreras = Relationship(back_populates="materias_carrera")
    # Una asociación materia_carrera puede tener muchas mesas de examen
    mesas_examen: List["Mesas_Examen"] = Relationship(back_populates="materia_carrera")
    # Una asociación materia_carrera puede tener muchos profesores asignados
    profesores: List["Profesores"] = Relationship(back_populates="materia_carrera")
    # Una asociación materia_carrera puede tener muchas notas de examen
    notas_examen: List["Notas_Examen"] = Relationship(back_populates="materia_carrera")
    # Una asociación materia_carrera puede tener muchos prácticos
    practicos: List["Practicos"] = Relationship(back_populates="materia_carrera")

    # Propiedades para obtener nombres de carrera y materia
    @property
    def carrera_nombre(self):
        return self.carrera.nombre if self.carrera else None
    @property
    def materia_nombre(self):
        return self.materia.nombre if self.materia else None

"""
TABLA: NOTAS
"""
# Almacena las notas de los estudiantes para cada materia/carrera.
class Notas(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('estudiante_id', 'materia_carrera_id', name='uq_estudiante_materia'),
    )
    id: int = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="usuarios.id") # ID del estudiante (FK a Usuarios)
    materia_carrera_id: int = Field(foreign_key="materia_carreras.id") # ID de materia_carrera (FK a Materia_Carreras)
    eval_1: int = Field(..., ge=0, le=10)
    rec_1: int = Field(..., ge=0, le=10)
    eval_2: int = Field(..., ge=0, le=10)
    rec_2: int = Field(..., ge=0, le=10) # Notas de las Evaluaciones (hasta 10)
    eval_3: int = Field(..., ge=0, le=10)
    rec_3: int = Field(..., ge=0, le=10)
    nota_prom: float # Nota promedio final

    # Relaciones con otras tablas
    # Referencia al usuario estudiante
    estudiante_user: "Usuarios" = Relationship(back_populates="notas")
    # Referencia a la asociación materia_carrera
    materia_carrera: Materia_Carreras = Relationship(back_populates="notas")

    # Propiedad para obtener el nombre de la materia
    @property
    def materia(self):
        return self.materia_carrera.materia_nombre if self.materia_carrera else None

"""
TABLA: NOTAS_EXAMEN
"""
# Almacena las notas de los estudiantes para las mesas de examen de cada materia/carrera.
class Notas_Examen(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('estudiante_id', 'materia_carrera_id', name='uq_estudiante_materia_examen'),
    )
    id: int = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="usuarios.id") # ID del estudiante (FK a Usuarios)
    materia_carrera_id: int = Field(foreign_key="materia_carreras.id") # ID de materia_carrera (FK a Materia_Carreras)
    primer_examen: Optional[int] = Field(default=None, ge=0, le=4)
    segundo_examen: Optional[int] = Field(default=None, ge=0, le=4) # Notas de los Examenes (hasta 4, permitiendo None)
    tercer_examen: Optional[int] = Field(default=None, ge=0, le=4)

    # Relaciones con otras tablas
    # Referencia al usuario estudiante
    estudiante_user_examen: "Usuarios" = Relationship(back_populates="notas_examen")
    # Referencia a la asociación materia_carrera
    materia_carrera: Materia_Carreras = Relationship(back_populates="notas_examen")

    # Propiedad para obtener el nombre de la materia
    @property
    def materia(self):
        return self.materia_carrera.materia_nombre if self.materia_carrera else None

"""
TABLA: PRACTICOS
"""
# Almacena las notas de los trabajos prácticos de los estudiantes.
class Practicos(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint('estudiante_id', 'materia_carrera_id', name='uq_estudiante_materia_practico'),
    )
    id: int = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="usuarios.id") # ID del estudiante (FK a Usuarios)
    materia_carrera_id: int = Field(foreign_key="materia_carreras.id") # ID de materia_carrera (FK a Materia_Carreras)
    tp_1: int = Field(..., ge=0, le=10)
    tp_2: int = Field(..., ge=0, le=10)
    tp_3: int = Field(..., ge=0, le=10)
    tp_4: int = Field(..., ge=0, le=10)
    tp_5: int = Field(..., ge=0, le=10) # Nota de los Trabajos Prácticos (hasta 10)
    tp_6: int = Field(..., ge=0, le=10)
    tp_7: int = Field(..., ge=0, le=10)
    tp_8: int = Field(..., ge=0, le=10)
    tp_9: int = Field(..., ge=0, le=10)
    tp_10: int = Field(..., ge=0, le=10)

    # Relaciones con otras tablas
    # Referencia al usuario estudiante
    estudiante_user: "Usuarios" = Relationship(back_populates="practicos")
    # Referencia a la asociación materia_carrera
    materia_carrera: "Materia_Carreras" = Relationship(back_populates="practicos")

"""
TABLA: CORRELATIVAS
"""
# Define las materias correlativas para cursar o rendir otras materias.
class Correlativas(SQLModel, table=True):
    # Restricción de unicidad para asegurar que una correlativa solo se asocie una vez a una materia/carrera
    __table_args__ = (
        UniqueConstraint("materia_carrera_id", "correlativa_id", name="uq_materia_correlativa"),
    )
    id: int = Field(default=None, primary_key=True)
    materia_carrera_id: int = Field(foreign_key="materia_carreras.id") # ID de la materia/carrera que tiene la correlativa (FK a Materia_Carreras)
    correlativa_id: int = Field(foreign_key="materia_carreras.id") # ID de la materia/carrera que es la correlativa (FK a Materia_Carreras)

    # Relaciones con otras tablas
    # Referencia a la materia/carrera que es la correlativa

    # La función lambda hace una evaluación diferida de un FK para resolver ambigüedad, en este caso entre los FKs de "Correlativas" a "Materia_Carreras"
    # sa_relationship_kwargs: Pasa argumentos adicionales a SQLAlchemy `relationship`, como `foreign_keys`
    materia_correlativa: Materia_Carreras = Relationship(sa_relationship_kwargs={"foreign_keys": lambda: [Correlativas.correlativa_id]})

"""
TABLA: MESAS EXAMEN
"""
# Define las mesas de examen disponibles para rendir materias.
class Mesas_Examen(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    materia_carrera_id: int = Field(foreign_key="materia_carreras.id") # ID de materia_carrera (FK a Materia_Carreras)
    profesor_id: int = Field(foreign_key="usuarios.id") # ID del profesor (FK a Usuarios)
    primer_llamado: Optional[datetime] = None
    segundo_llamado: Optional[datetime] = None

    # Relaciones con otras tablas
    # Referencia al usuario con el rol de profesor
    profesor_usuario: "Usuarios" = Relationship(back_populates="mesas_examen_dictadas")
    # Referencia a la asociación materia_carrera
    materia_carrera: Materia_Carreras = Relationship(back_populates="mesas_examen")
    # Una mesa de examen puede tener muchas inscripciones de estudiantes
    inscripciones: List["Inscripciones_Examen"] = Relationship(back_populates="mesa_examen")

    # Propiedades para obtener el nombre del profesor, materia, carrera, y el año
    @property
    def profesor_nombre(self):
        return self.profesor_usuario.nombre if self.profesor_usuario else None
    @property
    def materia_nombre(self):
        return self.materia_carrera.materia_nombre if self.materia_carrera else None
    @property
    def carrera_nombre(self):
        return self.materia_carrera.carrera_nombre if self.materia_carrera else None
    @property
    def anio(self):
        return self.materia_carrera.anio if self.materia_carrera else 0

"""
TABLA: INSCRIPCIONES EXAMEN
"""
# Registra la inscripción de un estudiante a una mesa de examen específica.
class Inscripciones_Examen(SQLModel, table=True):
    # Restricción de unicidad para asegurar que un estudiante solo se inscriba una vez a una mesa de examen
    __table_args__ = (
        UniqueConstraint('estudiante_id', 'mesa_examen_id', name='uq_estudiante_mesa'),
    )
    id: int = Field(default=None, primary_key=True)
    estudiante_id: int = Field(foreign_key="usuarios.id") # ID del estudiante (FK a Usuarios)
    mesa_examen_id: int = Field(foreign_key="mesas_examen.id") # ID de la mesa de examen (FK a Mesas_Examen)
    fecha_inscripcion: datetime = Field(default_factory=datetime.utcnow) # Fecha y hora de la inscripción
    llamado_inscrito: str = Field(max_length=30) # "primer_llamado" o "segundo_llamado"
    examen: Optional[str] = Field(default=None, max_length=30) # "primer_examen", "segundo_examen" o "tercer_examen"

    # Enumeración para el tipo de inscripción
    class TipoInscripcion(str, Enum):
        libre = "libre"
        regular = "regular"

    # Enumeración para el estado de la inscripción
    class EstadoInscripcion(str, Enum):
        activo = "active" # La inscripción está activa
        cancelado = "canceled" # La inscripción ha sido cancelada

    # Enumeración para el estado de asistencia
    class EstadoAsistencia(str, Enum):
        si = "si"
        no = "no"

    tipo_inscripcion: Optional[str] = Field(default=None, max_length=10) # "libre" o "regular"
    estado: str = Field(default="active") # Estado actual de la inscripción, por defecto 'active'
    asistencia: str = Field(default=EstadoAsistencia.no) # Campo para registrar la asistencia, por defecto 'no'

    # Relaciones con otras tablas
    # Referencia al usuario con el rol de estudiante
    estudiante_user: "Usuarios" = Relationship(back_populates="inscripciones")
    # Referencia a la mesa de examen
    mesa_examen: Mesas_Examen = Relationship(back_populates="inscripciones")

"""
TABLA: ACTAS_DIGITALES_PDF
"""
# Almacena los metadatos de los archivos PDF de actas digitales subidos.
class Actas_Digitales_PDF(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    filename: str = Field(max_length=255, unique=True) # Nombre único del archivo
    filepath: str = Field(max_length=500) # Ruta completa del archivo en el servidor
    uploaded_by_user_id: int = Field(foreign_key="usuarios.id") # ID del usuario que subió el archivo (FK a Usuarios)
    upload_date: datetime = Field(default_factory=datetime.utcnow) # Fecha y hora de la subida

    # Relación con la tabla Usuarios
    uploaded_by_user: Usuarios = Relationship(back_populates="actas_digitales_subidas")

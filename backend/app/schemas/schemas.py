from sqlmodel import SQLModel
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

"""
SCHEMAS: API RESPONSE
"""
class ApiResponse(SQLModel):
    success: bool
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    data: Optional[Dict[str, Any]] = None

"""
SCHEMAS: USUARIOS
"""
# Base model "Users"
class UserBase(SQLModel):
    username: str
    nombre: str
    dni: str
    email: Optional[str] = None
    legajo: Optional[str] = None
    libreta: Optional[str] = None

# Crea un nuevo usuario
class UserCreate(UserBase):
    password: str
    role: str

# Inicio de sesión de un usuario
class UserLogin(SQLModel):
    username: str
    password: str

# Devuelve el token de acceso
class Token(BaseModel):
    access_token: str
    token_type: str
    id: int
    nombre: str

# Devuelve la información del token
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Devuelve la información del usuario
class UserResponse(UserBase):
    id: int
    role: str
    carrera_id: Optional[int] = None
    class Config:
        from_attributes = True

# Cambia la contraseña de un usuario
class UserPasswordChange(SQLModel):
    current_password: str
    new_password: str

"""
SCHEMAS: ESTUDIANTES
"""
# Base model "Estudiantes"
class StudentBase(SQLModel):
    estudiante_id: int
    carrera_id: int
    anio_ingreso: int
    class Config:
        from_attributes = True

# Crea un nuevo estudiante
class StudentCreate(StudentBase):
    pass

# Devuelve el id y nombre de un estudiante
class StudentIdName(SQLModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

"""
SCHEMAS: PROFESORES
"""
# Base model "Profesores"
class TeacherBase(SQLModel):
    profesor_id: int
    materia_carrera_id: int
    anio_asignado: int
    class Config:
        from_attributes = True

# Crea un nuevo profesor
class TeacherCreate(TeacherBase):
    pass

# Devuelve toda la información de un profesor 
class TeacherInfoResponse(UserResponse):
    materia_nombre: Optional[str] = None
    carrera_nombre: Optional[str] = None
    class Config:
        from_attributes = True

"""
SCHEMAS: CARRERAS
"""
# Base model "Carreras"
class CareerBase(SQLModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

"""
SCHEMAS: MATERIAS
"""
# Base model "Materias"
class SubjectBase(SQLModel):
    id: int
    nombre: str
    class Config:
        from_attributes = True

"""
SCHEMAS: MATERIA CARRERAS
"""
# Devuelve datos especificos de una materia en una carrera
class SubjectCareerDetail(SQLModel):
    id: int
    materia_nombre: str
    class Config:
        from_attributes = True

"""
SCHEMAS: CORRELATIVAS
"""
# Devuelve el nombre de una correlativa
class CorrelativeDetail(SQLModel):
    id: int
    correlativa: str # Nombre de la correlativa
    class Config:
        from_attributes = True

# Devuelve una materia con sus correlativas (en una carrera)
class CorrelativesSubject(SQLModel):
    id: int
    materia: str
    correlativas: List[CorrelativeDetail] = []
    class Config:
        from_attributes = True

"""
SCHEMAS: NOTAS
"""
# Base model "Notas"
class NoteBase(SQLModel):
    id: int
    estudiante_id: int
    materia_carrera_id: int
    eval_1: int
    rec_1: int
    eval_2: int
    rec_2: int
    eval_3: int
    rec_3: int
    nota_prom: float
    class Config:
        from_attributes = True

# Crea una nota
class NoteCreate(SQLModel):
    estudiante_id: int
    materia_carrera_id: int
    eval_1: int
    rec_1: int
    eval_2: int
    rec_2: int
    eval_3: int
    rec_3: int
    nota_prom: float

# Devuelve detalle específicos de las notas
class NotesDetail(SQLModel):
    materia: str
    eval_1: int
    rec_1: int
    eval_2: int
    rec_2: int
    eval_3: int
    rec_3: int
    nota_prom: float
    class Config:
        from_attributes = True

# Devuelve las notas promedio y las correlativas de un estudiante
class CorreAverageNote(SQLModel):
    codigo: int
    materia: str
    nota_prom: Optional[float] = None
    correlativas: List[int] = []
    class Config:
        from_attributes = True

# Separa las notas promedio y las correlativas por materias de un año
class CorreAverageNoteYear(SQLModel):
    anio: int
    materias: List[CorreAverageNote]
    class Config:
        from_attributes = True

"""
SCHEMAS: NOTAS EXAMEN
"""
# Crea una nota de examen
class NotesExamCreate(SQLModel):
    estudiante_id: int
    materia_carrera_id: int
    primer_examen: int
    segundo_examen: int
    tercer_examen: int

# Esquema para actualizar una nota de examen
class NotesExamUpdate(SQLModel):
    inscripcion_id: int
    nota: int

"""
SCHEMAS: MESAS EXAMEN
"""
# Crea una mesa de examen
class TableExamCreate(SQLModel):
    materia_carrera_id: int
    profesor_id: int
    primer_llamado: Optional[datetime] = None
    segundo_llamado: Optional[datetime] = None

# Devuelve datos especificos de una mesa de examen
class TableExamDetail(SQLModel):
    id: int
    primer_llamado: Optional[datetime] = None
    segundo_llamado: Optional[datetime] = None
    materia_nombre: str
    profesor_nombre: str
    carrera_nombre: str
    class Config:
        from_attributes = True

# Devuelve las mesas de examen agrupadas por añio
class TablesExamPerNote(SQLModel):
    anio: int
    mesas: List[TableExamDetail]
    class Config:
        from_attributes = True

# Devuelve datos especificos de una mesa de examen dentro de una carrera
class TableExamPerCareerDetail(SQLModel):
    id: int
    primer_llamado: Optional[datetime] = None
    segundo_llamado: Optional[datetime] = None
    materia_nombre: str
    profesor_nombre: str
    class Config:
        from_attributes = True

# Devuelve las mesas de examen agrupadas por carrera
class TablesExamPerCareer(SQLModel):
    carrera_nombre: str
    mesas: List[TableExamPerCareerDetail]
    class Config:
        from_attributes = True

"""
SCHEMAS: INSCRIPCIONES EXAMEN
"""
# Crea una inscripción en una mesa de examen
class RegistrationExamCreate(SQLModel):
    estudiante_id: int
    mesa_examen_id: int
    llamado_inscrito: str
    tipo_inscripcion: Optional[str] = None
    examen: Optional[str] = None

# Devuelve datos especificos de una inscripción
class ExamRegistrationDetail(SQLModel):
    id: int # id mesa de examen
    id_inscripcion: int
    llamado_inscrito: str
    tipo_inscripcion: Optional[str] = None
    fecha_llamado: Optional[datetime] = None
    materia_nombre: str
    carrera_nombre: str
    profesor_nombre: str
    estudiante_nombre: str
    dni: str
    libreta: Optional[str] = None
    estado: str
    asistencia: str

# Devuelve las mesas de examen inscriptas agrupadas por año
class TablesRegisteredPerYear(SQLModel):
    anio: int
    mesas: List[ExamRegistrationDetail]
    class Config:
        from_attributes = True

# Devuelve datos especificos de los estudiantes inscriptos
class ExamWithStudentsDetail(SQLModel):
    id: int # id mesa de examen
    id_inscripcion: int
    llamado_inscrito: str
    tipo_inscripcion: Optional[str] = None
    fecha_llamado: Optional[datetime] = None
    materia_nombre: str
    carrera_nombre: str
    profesor_id: int
    profesor_nombre: str
    estudiante_nombre: str
    dni: str
    libreta: Optional[str] = None
    estado: str
    class Config:
        from_attributes = True

# Devuelve las mesas de examen agrupadas por carrera del profesor
class TablesExamPerCareerForTeacher(SQLModel):
    carrera_nombre: str
    mesas: List[ExamWithStudentsDetail]
    class Config:
        from_attributes = True

# Devuelve el detalle de todos los examenes por profesor
class StudentExamDetailForTeacher(SQLModel):
    id: int # id de la mesa de examen
    id_profesor: int
    id_inscripcion: int
    materia_nombre: str
    estudiante_nombre: str
    dni: str
    libreta: Optional[str] = None
    fecha_llamado: Optional[datetime] = None
    llamado_inscrito: str
    tipo_inscripcion: Optional[str] = None
    asistencia: Optional[str] = None
    nota: Optional[int] = None
    estado: str
    class Config:
        from_attributes = True

# Devuelve las mesas de examen agrupadas por carrera con detalles de los examenes
class TablesStudentExamDetailPerCareer(SQLModel):
    carrera_nombre: str
    mesas: List[StudentExamDetailForTeacher]
    class Config:
        from_attributes = True

# Actualiza el estado de una inscripción
class RegistrationExamUpdateStatus(SQLModel):
    estado: str

"""
SCHEMAS: RENDIMIENTO DE UNA CARRERA
"""
# Calcula el rendimiento de una carrera
class PerformanceCareer(SQLModel):
    carrera_id: int
    carrera_nombre: str
    promocionados_count: int
    promocionados_percentage: float
    regulares_count: int
    regulares_percentage: float
    libres_count: int
    libres_percentage: float
    total_notas_evaluadas: int
    class Config:
        from_attributes = True

"""
SCHEMAS: OLLAMA CHAT
"""
# Crea un mensaje
class MessageRequest(SQLModel):
    message: str

# Devuelve un mensaje
class MessageResponse(SQLModel):
    response: str

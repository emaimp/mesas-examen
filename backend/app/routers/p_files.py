from sqlmodel import Session
from app import db, crud, schemas
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends, status

router = APIRouter(tags=["Subir Archivos"])

#
# Endpoint: Cargar archivo xlxs con los datos de los usuarios (admin, estudiantes, profesores) y sus asignaciones
#
@router.post("/usuarios/cargar_excel", response_model=schemas.ApiResponse)
def excel_usuarios(file: UploadFile = File(...), session: Session = Depends(db.get_session)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe tener extensión .xlsx")
    file_bytes = file.file.read()
    return crud.u_files.cargar_usuarios_excel(file_bytes, session)

#
# Endpoint: Cargar archivo xlsx con las notas de los estudiantes
#
@router.post("/notas/cargar_excel", response_model=schemas.ApiResponse)
def excel_notas(file: UploadFile = File(...), session: Session = Depends(db.get_session)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe tener extensión .xlsx")
    file_bytes = file.file.read()
    return crud.u_files.cargar_notas_excel(file_bytes, session)

#
# Endpoint: Cargar archivo xlsx con los datos de carreras, materias, materia_carreras y correlativas
#
@router.post("/carreras_materias_correlativas/cargar_excel", response_model=schemas.ApiResponse)
def excel_carreras_materias_correlativas(file: UploadFile = File(...), session: Session = Depends(db.get_session)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe tener extensión .xlsx")
    file_bytes = file.file.read()
    return crud.u_files.cargar_carreras_materias_correlativas_excel(file_bytes, session)

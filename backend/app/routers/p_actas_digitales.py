import uuid # Genera nombres de archivo únicos
from app import db, core, crud, models
from typing import List
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, FileResponse
from fastapi import APIRouter, UploadFile, HTTPException, Depends, Query, File, status

router = APIRouter(prefix="/actas", tags=["Actas Digitales"], responses={404: {"description": "Not found"}},)

UPLOAD_DIRECTORY = Path("uploads/pdfs") # Directorio donde se guardarán los PDFs
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True) # Crea el directorio si no existe

#
# Endpoint: Guarda los metadatos de un acta en la base de datos
#
@router.post("/upload_pdf/")
async def upload_actas_digitales(
    file: UploadFile = File(...),
    db: Session = Depends(db.get_session),
    current_user: models.Usuarios = Depends(core.get_current_user)
):
    if not file.content_type == "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo se permiten archivos PDF."
        )

    # Generar un nombre de archivo único para evitar colisiones
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = UPLOAD_DIRECTORY / unique_filename

    try:
        with open(file_path, "wb") as buffer:
            # Leer el archivo en bloques para manejar archivos grandes eficientemente
            while contents := await file.read(1024 * 1024): # Leer en bloques de 1MB
                buffer.write(contents)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al guardar el archivo: {e}"
        )

    # Guardar metadatos en la base de datos
    new_pdf_record = models.Actas_Digitales(
        filename=unique_filename,
        filepath=str(file_path),
        uploaded_user_id=current_user.id,
        upload_date=datetime.utcnow()
    )
    db.add(new_pdf_record)
    db.commit()
    db.refresh(new_pdf_record)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "PDF subido exitosamente", "filename": unique_filename, "filepath": str(file_path)}
    )

#
# Endpoint: Descarga un acta en formato PDF (id)
#
@router.get("/download_pdf/{pdf_id}")
async def actas_digitales_download(
    pdf_id: int,
    db: Session = Depends(db.get_session),
    current_user: models.Usuarios = Depends(core.get_current_user)
):
    pdf_record = crud.cr_actas_digitales.pdf_record_id(db, pdf_id)

    if not pdf_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="PDF no encontrado."
        )

    # Lógica de autorización: solo el usuario que lo subió o un administrador puede descargarlo
    if current_user.id != pdf_record.uploaded_user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para descargar este PDF."
        )

    file_path = Path(pdf_record.filepath)
    if not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El archivo PDF no se encuentra en el servidor."
        )

    return FileResponse(path=file_path, filename=pdf_record.filename, media_type="application/pdf")

#
# Endpoint: Lista los metadatos de las actas para filtrarlas por nombre del uploader
#
@router.get("/pdfs_por_uploader/", response_model=List[dict])
async def actas_digitales_por_uploader(
    nombre: str = Query(..., description="Nombre del usuario que subió el PDF"),
    db: Session = Depends(db.get_session),
    current_user: models.Usuarios = Depends(core.get_current_user)
):
    # Solo los administradores pueden usar este endpoint para listar PDFs de otros usuarios
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden listar PDFs por usuario."
        )

    pdf_records = crud.cr_actas_digitales.pdf_records_uploader(db, nombre)

    if not pdf_records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron PDFs subidos por el usuario '{nombre}'."
        )

    # Devolver una lista de metadatos relevantes para el administrador
    return [
        {
            "id": record.id,
            "filename": record.filename,
            "upload_date": record.upload_date,
            "uploaded_by_name": record.uploaded_user.nombre
        }
        for record in pdf_records
    ]

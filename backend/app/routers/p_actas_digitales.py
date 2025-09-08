import uuid # Genera nombres de archivo únicos
from app import db, core, models
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status

router = APIRouter(prefix="/actas", tags=["Actas Digitales"], responses={404: {"description": "Not found"}},)

UPLOAD_DIRECTORY = Path("uploads/pdfs") # Directorio donde se guardarán los PDFs
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True) # Crea el directorio si no existe

@router.post("/upload_pdf/")
async def upload_actas_digitales_pdf(
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
    new_pdf_record = models.Actas_Digitales_PDF(
        filename=unique_filename,
        filepath=str(file_path),
        uploaded_by_user_id=current_user.id,
        upload_date=datetime.utcnow()
    )
    db.add(new_pdf_record)
    db.commit()
    db.refresh(new_pdf_record)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "PDF subido exitosamente", "filename": unique_filename, "filepath": str(file_path)}
    )

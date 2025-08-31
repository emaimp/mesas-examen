from app import db, core, crud, models, schemas
from typing import Annotated
from sqlmodel import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status

router = APIRouter(prefix="/auth", tags=["Auth"])

#
# Endpoint: Registra un nuevo usuario
#
@router.post("/register", response_model=schemas.UserResponse)
def registra_usuario(user_in: schemas.UserCreate, session: Annotated[Session, Depends(db.get_session)]):
    db_user = crud.cr_usuarios.get_username(session, username=user_in.username) # Verifica si el nombre de usuario ya está registrado
    if db_user:
        raise HTTPException(status_code=400, detail="Nombre de usuario ya registrado.")
    user = crud.cr_usuarios.create_user(session=session, user_in=user_in) # Crea el nuevo usuario en la base de datos
    return user

#
# Endpoint: Obtiene el token de acceso
#
@router.post("/token", response_model=schemas.Token)
async def token_acceso(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Annotated[Session, Depends(db.get_session)]):
    return await core.security.login_for_access_token(form_data, session)

#
# Endpoint: Obtiene la información del usuario actual
#
@router.get("/users/me/", response_model=schemas.UserResponse)
async def usuario_actual(current_user: Annotated[models.Usuarios, Depends(core.get_current_user)]):
    user_response_data = current_user.model_dump()
    if current_user.role == "student" and current_user.asignaciones_estudiante: # Verificación para saber si el usuario es estudiante
        user_response_data["carrera_id"] = current_user.asignaciones_estudiante[0].carrera_id # Toma solo la primera carrera del estudiante
    else:
        user_response_data["carrera_id"] = None
    return schemas.UserResponse(**user_response_data)

#
# Endpoint: Cambia la contraseña del usuario actual
#
@router.put("/users/me/password", response_model=schemas.ApiResponse, status_code=status.HTTP_200_OK)
async def change_password(
    password_change: schemas.UserPasswordChange,
    current_user: Annotated[models.Usuarios, Depends(core.get_current_user)],
    session: Annotated[Session, Depends(db.get_session)]
):
    try:
        crud.cr_usuarios.update_user_password(
            session=session,
            user_id=current_user.id,
            current_password=password_change.current_password,
            new_password=password_change.new_password
        )
        return schemas.ApiResponse(success=True, message="Contraseña actualizada exitosamente.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor: {e}")

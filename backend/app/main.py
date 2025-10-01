from app import db, routers
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from sqlalchemy.exc import IntegrityError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Context manager para el ciclo de vida de la aplicación
@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    db.create_initial_admin_user()
    yield

app = FastAPI(lifespan=lifespan)

# Routers migrados
app.include_router(routers.gp_auth.router)
app.include_router(routers.g_carreras.router)
app.include_router(routers.g_profesores.router)
app.include_router(routers.gp_estudiantes.router)
app.include_router(routers.gp_notas.router)
app.include_router(routers.gp_mesas_examen.router)
app.include_router(routers.p_actas_digitales.router)
app.include_router(routers.p_files.router)
app.include_router(routers.g_perfomance.router)

#
# CORS: Middleware
#
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#
# Exception Handler: Manejo de errores
#
@app.exception_handler(IntegrityError)
async def handle_sqlalchemy_integrity_error(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "No se pudo procesar la solicitud por un error de integridad."}
    )

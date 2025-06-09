from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth  # Importa el router de autenticación
from app.routers import usuario  # Importa el router de usuarios
from app.routers import sucursales  # Importa el router de sucursales
from app.routers import curso  # Importa el router de cursos
from app.routers import horario  # Importa el router de horarios
from app.routers import estudiante  # Importa el router de estudiantes
from app.routers import listas  # Importa el router de listas
from app.routers import reportes  # Importa el router de reportes
from app.routers import inscripcion  # Importa el router de inscripciones
app = FastAPI()

# Agrega esta configuración justo después de crear la instancia de FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://tuapp.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Incluye el router de roles

app.include_router(auth.router)
app.include_router(usuario.router)
app.include_router(sucursales.router)
app.include_router(curso.router)
app.include_router(horario.router)
app.include_router(estudiante.router)
app.include_router(listas.router)
app.include_router(reportes.router)
app.include_router(inscripcion.router)

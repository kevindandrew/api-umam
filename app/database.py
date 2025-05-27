import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session, text
from typing import Generator

# Carga variables de entorno
load_dotenv()

# Configuración de la conexión (usa la misma URL que ya tienes)
DATABASE_URL = os.getenv("DATABASE_URL")

# Engine con configuración mejorada
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Muestra SQL en consola (útil para desarrollo)
    pool_pre_ping=True,  # Evita conexiones rotas
    pool_size=10,  # Conexiones mantenidas abiertas
    max_overflow=20  # Conexiones adicionales cuando se necesiten
)

# Función para crear tablas (se llamará al iniciar la app)


def crear_db_y_tablas():
    SQLModel.metadata.create_all(engine)

# Generador de sesiones (equivalente a tu get_db pero para SQLModel)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def verificar_conexion():
    """Función para diagnosticar problemas de conexión"""
    try:
        with Session(engine) as session:
            # 1. Verificar conexión básica
            db_name = session.exec(text("SELECT current_database()")).one()
            print(f"✅ Conectado a la base de datos: {db_name}")

            # 2. Verificar existencia de la tabla
            table_exists = session.exec(
                text(
                    "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'roles')")
            ).one()
            print(f"🔍 ¿Existe tabla 'roles'? {'Sí' if table_exists else 'No'}")

            # 3. Contar registros con SQL crudo
            count = session.exec(text("SELECT COUNT(*) FROM roles")).one()
            print(f"📊 Registros en 'roles': {count}")

            # 4. Ver esquema de la tabla
            columns = session.exec(
                text(
                    "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'roles'")
            ).all()
            print("🗂 Esquema de la tabla:")
            for col in columns:
                print(f"- {col[0]}: {col[1]}")

            return True
    except Exception as e:
        print(f"❌ Error de conexión: {str(e)}")
        return False

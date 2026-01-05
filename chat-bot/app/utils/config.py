import os                               # Acceso a variables de entorno (config externa)
from pathlib import Path                # Manejo de rutas de archivos de forma portable

ENV = os.getenv("ENV", "development")                                   # Entorno de ejecución (dev / prod)
API_HOST = os.getenv("API_HOST", "0.0.0.0")                             # Host donde escucha la API
API_PORT = int(os.getenv("API_PORT", 8000))                             # Puerto de la API
BASE_DIR = Path(__file__).resolve().parents[2]                          # Raíz del proyecto (path base)
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "chatbot.db"))   # Ruta a la base de datos SQLite
SCHEMA_PATH = os.getenv("SCHEMA_PATH", str(BASE_DIR / "app" / "db" / "schema.sql")) # Ruta de schema SQL

# Modelo de embeddings (vectorización semántica)
EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME",
    "nomic-ai/nomic-embed-text-v1.5"
)

MODEL_DIR = Path(os.getenv("MODEL_DIR", BASE_DIR / "models"))           # Carpeta donde viven los modelos locales
RAG_TOP_K = int(os.getenv("RAG_TOP_K", 5))                              # Cantidad de documentos más similares a recuperar (top-K)

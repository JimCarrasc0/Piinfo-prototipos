from fastapi import FastAPI                         # Framework backend (API REST async)
from fastapi.middleware.cors import CORSMiddleware  # Middleware CORS (permite llamadas desde frontend)
from dotenv import load_dotenv                      # Carga variables de entorno desde .env
load_dotenv()                                       # Inicializa las variables del .env en el proceso

from app.api.chat import router as chat_router      # Router con endpoints del chatbot
from app.api.health import router as health_router  # Router de health check
from app.utils.logger import get_logger             # Logger centralizado

from app.api import posts, metrics, comments

logger = get_logger("main")                         # Logger específico del módulo principal

# Instancia principal de la API
app = FastAPI(
    title="T-Radar Chatbot API",
    description="Backend del chatbot BandurrIA con RAG y embeddings",
    version="0.1.0",
)

# Configuración CORS (frontend libre en dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["health"])    # Endpoint de estado del sistema
app.include_router(chat_router, prefix="/chat", tags=["chat"])          # Endpoint principal del chatbot
app.include_router(posts.router)
app.include_router(metrics.router)
app.include_router(comments.router)

"""
DESCRIPCIÓN: Se ejecuta automáticamente al iniciar el backend
"""
@app.on_event("startup")
async def startup_event():
    logger.info("------- Backend T-Radar iniciado correctamente ------- ")

"""
DESCRIPCIÓN: Se ejecuta al detener el backend
"""
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("------- Backend T-Radar detenido -------")

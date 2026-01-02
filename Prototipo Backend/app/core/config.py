import logging
import sys

from app.core.logging import InterceptHandler
from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

API_PREFIX = "/api"
VERSION = "0.1.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
MEMOIZATION_FLAG: bool = config("MEMOIZATION_FLAG", cast=bool, default=True)

PROJECT_NAME: str = config("PROJECT_NAME", default="T-Radar")

# =========================================================================
# CONFIGURACIÓN DE SEGURIDAD (JWT)
# =========================================================================

# CLAVE SECRETA: Esencial para firmar (codificar) y verificar (decodificar) el token.
SECRET_KEY: Secret = config(
    "SECRET_KEY",
    cast=Secret,
    default="una_clave_secreta_fuerte"
)
# ALGORITMO: Usualmente HS256 para JWT.
ALGORITHM: str = config("ALGORITHM", default="HS256")

# EXPIRACIÓN: Tiempo de vida del token. (7 días)
ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60 * 24 * 7)

# CORS origins (comma separated). Default to local dev React.
_cors_origins = config(
    "CORS_ORIGINS",
    default=(
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://frontend:3000"
    ),
)
CORS_ORIGINS = [o.strip() for o in _cors_origins.split(",") if o.strip()]

# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])

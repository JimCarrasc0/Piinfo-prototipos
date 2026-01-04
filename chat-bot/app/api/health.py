from fastapi import APIRouter   # Router de FastAPI para definir endpoints HTTP

router = APIRouter()            # Crea el router del módulo health (chequeo de estado del backend)

"""
DESCRIPCIÓN: Endpoint de verificación de estado del backend. Permite comprobar que la API está levantada y respondiendo.

ENTRADAS:   - No recibe parámetros.

SALIDAS:    - JSON con estado OK.
"""
@router.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "bandurria-backend"
    }

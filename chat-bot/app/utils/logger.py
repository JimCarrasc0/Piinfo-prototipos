import logging              # Módulo estándar de logging (registro de eventos del sistema)
import sys                  # Acceso a stdout / stderr (consola)

LOG_LEVEL = logging.INFO    # Nivel de logs: INFO (ignora DEBUG, muestra info relevante)

"""
DESCRIPCIÓN: Crea y configura un logger reutilizable para el proyecto.

ENTRADAS:   - name (str): nombre del módulo que usa el logger

SALIDAS:    - logging.Logger: logger configurado
"""
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

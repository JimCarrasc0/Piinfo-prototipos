import sqlite3                                      # Driver de SQLite (motor de base de datos embebido en archivo)
from app.utils.config import DB_PATH, SCHEMA_PATH   # Ruta del SQLite y el schema SQL

print("DB_PATH real:", DB_PATH)
print("SCHEMA_PATH real:", SCHEMA_PATH)

_connection: sqlite3.Connection | None = None       # Conexión global (singleton simple)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    conn.commit()
    conn.close()

"""
DESCRIPCIÓN: Obtiene una conexión activa a la base de datos SQLite. Si la conexión no existe, la crea e inicializa el esquema.

ENTRADAS:   - No recibe parámetros.

SALIDAS:    - sqlite3.Connection: conexión activa a la base de datos.
"""
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

"""
DESCRIPCIÓN: Inicializa el esquema de la base de datos ejecutando el archivo schema.sql. Solo crea tablas si no existen.

ENTRADAS:   - conn (sqlite3.Connection): conexión activa a la base de datos.

SALIDAS:    - None
"""
def _init_schema(conn: sqlite3.Connection) -> None:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript

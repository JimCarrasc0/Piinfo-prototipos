from app.db.database import get_db  # Herramientas para uso y conexión de la base de datos
from datetime import datetime       #  Herramienta usada para setear fechas

'''
DESCRIPCIÓN: Función que permite crear un post en la base de datos

ENTRADA: Recibe un json con los datos necesarios para la creación de un post (ver README para mas detalles)

SALIDA: No retorna nada
'''
def create_post(post):
    db = get_db()
    db.execute(
        """
        INSERT INTO posts (id, platform, caption, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (
            post.post_id,
            post.platform,
            post.caption,
            post.created_at or datetime.utcnow().isoformat()
        )
    )
    db.commit()

'''
DESCRIPCIÓN: Función que permite obtener todos los post en la base de datos

ENTRADA: No recibe nada

SALIDA: No retorna nada
'''
def get_posts():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM posts"
    ).fetchall()
    return [dict(row) for row in rows]

'''
DESCRIPCIÓN: Función que permite actualizar un post en la base de datos

ENTRADA: Recibe un json con los datos necesarios para la actualización de un post (ver README para mas detalles)

SALIDA: No retorna nada
'''
def update_post(post_id, payload):
    db = get_db()
    cursor = db.execute(
        """
        UPDATE posts
        SET caption = COALESCE(?, caption)
        WHERE post_id = ?
        """,
        (payload.caption, post_id)
    )
    db.commit()
    return cursor.rowcount > 0

'''
DESCRIPCIÓN: Función que permite crear un post en la base de datos

ENTRADA: Recibe eun json con los datos necesarios para la creación de un post (ver README para mas detalles)

SALIDA: No retorna nada
'''
def delete_post(post_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM posts WHERE id = ?",
        (post_id,)
    )
    db.commit()
    return cursor.rowcount > 0

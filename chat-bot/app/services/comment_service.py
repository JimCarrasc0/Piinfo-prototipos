from app.db.database import get_db      # Herramientas para uso y conexión de la base de datos

'''
DESCRIPCIÓN: Función que permite crear un comentario en la base de datos

ENTRADA: Recibe un json con los datos necesarios para la creación de un comentario (ver README para mas detalles)

SALIDA: No retorna nada
'''
def create_comment(comment):
    db = get_db()
    db.execute(
        """
        INSERT INTO meta_comments (post_id, comment_id, text, sentiment, timestamp)
        VALUES (?, ?, ?, ?, ?)
        """,
        (comment.post_id, comment.comment_id, comment.text, comment.sentiment, comment.timestamp)
    )
    db.commit()

'''
DESCRIPCIÓN: Función creada para obtener todos los comentarios en la base de datos

ENTRADA: No recibe nada

SALIDA: No retorna nada
'''
def get_comments():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM meta_comments"
    ).fetchall()
    return [dict(row) for row in rows]

'''
DESCRIPCIÓN: Función que permite actualizar un comentario en la base de datos

ENTRADA: Recibe un json con los datos necesarios para la creación de un comentario (ver README para mas detalles)

SALIDA: No retorna nada
'''
def update_comment(comment_id, payload):
    db = get_db()
    cursor = db.execute(
        """
        UPDATE meta_comments
        SET
            text = COALESCE(?, text),
            sentiment = COALESCE(?, sentiment)
        WHERE id = ?
        """,
        (payload.text, payload.sentiment, comment_id)
    )
    db.commit()
    return cursor.rowcount > 0

'''
DESCRIPCIÓN: Función que permite eliminar un comentario en la base de datos

ENTRADA: Recibe el id del comentario a eliminar

SALIDA: No retorna nada
'''
def delete_comment(comment_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM meta_comments WHERE id = ?",
        (comment_id,)
    )
    db.commit()
    return cursor.rowcount > 0

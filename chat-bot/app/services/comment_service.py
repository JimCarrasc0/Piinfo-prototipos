from app.db.database import get_db

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

def get_comments():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM meta_comments"
    ).fetchall()
    return [dict(row) for row in rows]

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

def delete_comment(comment_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM meta_comments WHERE id = ?",
        (comment_id,)
    )
    db.commit()
    return cursor.rowcount > 0

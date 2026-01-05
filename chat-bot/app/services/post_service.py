from app.db.database import get_db
from datetime import datetime

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

def get_posts():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM posts"
    ).fetchall()
    return [dict(row) for row in rows]

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

def delete_post(post_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM posts WHERE id = ?",
        (post_id,)
    )
    db.commit()
    return cursor.rowcount > 0

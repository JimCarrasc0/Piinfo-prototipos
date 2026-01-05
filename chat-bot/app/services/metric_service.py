from app.db.database import get_db

def create_metric(metric):
    db = get_db()
    db.execute(
        """
        INSERT INTO meta_metrics (post_id, metric_name, period, value, end_time)
        VALUES (?, ?, ?, ?, ?)
        """,
        (metric.post_id, metric.metric_name, metric.period, metric.value, metric.end_time)
    )
    db.commit()

def get_metrics():
    db = get_db()
    rows = db.execute(
        "SELECT * FROM meta_metrics"
    ).fetchall()
    return [dict(row) for row in rows]

def update_metric(metric_id, payload):
    db = get_db()
    cursor = db.execute(
        """
        UPDATE meta_metrics
        SET value = ?
        WHERE id = ?
        """,
        (payload.value, metric_id)
    )
    db.commit()
    return cursor.rowcount > 0

def delete_metric(metric_id):
    db = get_db()
    cursor = db.execute(
        "DELETE FROM meta_metrics WHERE id = ?",
        (metric_id,)
    )
    db.commit()
    return cursor.rowcount > 0

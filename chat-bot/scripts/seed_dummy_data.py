from app.db.database import get_db, init_db
from app.services.embeddings import embed_text
import json
from datetime import datetime

init_db()
db = get_db()

# =========================
# POSTS
# =========================
posts = [
    ("post_1", "instagram", "Promoción de verano"),
    ("post_2", "instagram", "Lanzamiento nuevo producto"),
    ("post_3", "facebook", "Descuento por tiempo limitado"),
]

for post_id, platform, caption in posts:
    db.execute("""
    INSERT OR IGNORE INTO posts (id, platform, caption, created_at)
    VALUES (?, ?, ?, ?)
    """, (post_id, platform, caption, datetime.utcnow().isoformat()))

# =========================
# MÉTRICAS (muchas más)
# =========================
metrics = [
    # post_1 – engagement medio
    ("post_1", "likes", 120),
    ("post_1", "comments", 15),
    ("post_1", "shares", 8),
    ("post_1", "saves", 22),
    ("post_1", "reach", 980),

    # post_2 – bajo rendimiento
    ("post_2", "likes", 40),
    ("post_2", "comments", 3),
    ("post_2", "shares", 1),
    ("post_2", "saves", 4),
    ("post_2", "reach", 300),

    # post_3 – alto engagement
    ("post_3", "likes", 320),
    ("post_3", "comments", 62),
    ("post_3", "shares", 45),
    ("post_3", "saves", 90),
    ("post_3", "reach", 2500),
]

for post_id, name, value in metrics:
    db.execute("""
    INSERT OR IGNORE INTO meta_metrics
    (post_id, metric_name, period, value, end_time)
    VALUES (?, ?, 'day', ?, ?)
    """, (
        post_id,
        name,
        value,
        datetime.utcnow().isoformat(),
    ))

# =========================
# COMENTARIOS (muchos + variados)
# =========================
comments = [
    # post_1
    ("post_1", "c1", "Me gustó mucho la promo", "positive"),
    ("post_1", "c2", "Buen descuento, pero podría ser mejor", "neutral"),
    ("post_1", "c3", "Muy caro para lo que ofrecen", "negative"),
    ("post_1", "c4", "Siempre suben los precios antes de bajar", "negative"),
    ("post_1", "c5", "¿Hasta cuándo dura la oferta?", "neutral"),

    # post_2
    ("post_2", "c6", "No entendí bien el producto", "neutral"),
    ("post_2", "c7", "Esperaba algo mejor por ese precio", "negative"),
    ("post_2", "c8", "Demasiado básico", "negative"),

    # post_3
    ("post_3", "c9", "Excelente descuento", "positive"),
    ("post_3", "c10", "Esto sí vale la pena", "positive"),
    ("post_3", "c11", "Compré altiro", "positive"),
    ("post_3", "c12", "Muy buena oferta, recomendado", "positive"),
    ("post_3", "c13", "Demasiada publicidad, pero buen precio", "neutral"),
]

for post_id, cid, text, sentiment in comments:
    db.execute("""
    INSERT OR IGNORE INTO meta_comments
    (post_id, comment_id, text, sentiment, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (
        post_id,
        cid,
        text,
        sentiment,
        datetime.utcnow().isoformat(),
    ))

# =========================
# EMBEDDINGS (RAG real)
# =========================
embedding_texts = [
    # métricas interpretadas
    ("metric", "post_1_engagement", "El post tiene engagement medio con críticas al precio"),
    ("metric", "post_2_low_perf", "El post tiene bajo alcance y poca interacción"),
    ("metric", "post_3_high_perf", "El post muestra alto engagement y comentarios positivos"),

]

# embeddings por comentario
for post_id, cid, text, _ in comments:
    embedding_texts.append(("comment", cid, text))

for source_type, source_id, content in embedding_texts:
    vector = embed_text(content)
    db.execute("""
    INSERT OR IGNORE INTO embeddings
    (source_type, source_id, content, embedding)
    VALUES (?, ?, ?, ?)
    """, (
        source_type,
        source_id,
        content,
        json.dumps(vector),
    ))

db.commit()
print("🚀 Base de datos poblada con ALTA densidad semántica")

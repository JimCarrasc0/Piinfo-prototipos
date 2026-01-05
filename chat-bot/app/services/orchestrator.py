from app.db.database import get_db
from app.services.intent_detector import detect_intent
from app.services.rag import retrieve_relevant_context

"""
DESCRIPCIÓN:
Orquesta la consulta del usuario detectando intenciones,
resolviendo entidades y extrayendo datos relevantes desde la BD
y la capa RAG.

ENTRADAS:
- message (str): mensaje del usuario

SALIDAS:
- dict: contexto estructurado para el LLM
"""
def build_context(message: str, intent_data: dict) -> dict:
    db = get_db()

    intents = intent_data["intents"]
    entities = intent_data["entities"]

    context = {
        "intents": intents,
        "entities": entities,
        "posts": [],
        "metrics": [],
        "comments": [],
        "rag_context": []
    }

    post_ids = []

    post_scope = entities.get("post_scope")

    if post_scope == "last":
        row = db.execute(
            """
            SELECT id, caption
            FROM posts
            ORDER BY created_at DESC
            LIMIT 1
            """
        ).fetchone()

        if row:
            post_ids.append(row["id"])
            context["posts"].append(dict(row))

    elif post_scope == "first":
        row = db.execute(
            """
            SELECT id, caption
            FROM posts
            ORDER BY created_at ASC
            LIMIT 1
            """
        ).fetchone()

        if row:
            post_ids.append(row["id"])
            context["posts"].append(dict(row))

    elif post_scope == "all":
        rows = db.execute(
            "SELECT id, caption FROM posts"
        ).fetchall()

        for r in rows:
            post_ids.append(r["id"])
            context["posts"].append(dict(r))

    elif post_scope == "specific" and entities.get("post_query"):
        rows = db.execute(
            "SELECT id, caption FROM posts"
        ).fetchall()

        captions = [r["caption"] for r in rows]
        from app.services.embeddings import embed_text
        from sentence_transformers import util

        query_emb = embed_text(entities["post_query"])
        caption_embs = [embed_text(c) for c in captions]

        scores = [
            util.cos_sim(query_emb, emb).item()
            for emb in caption_embs
        ]

        best_idx = scores.index(max(scores))
        best_post = rows[best_idx]

        post_ids.append(best_post["id"])
        context["posts"].append(dict(best_post))

    if "consultar_metricas" in intents and post_ids:
        metric_scope = entities.get("metric_scope")

        if metric_scope == "engagement_only":
            rows = db.execute(
                """
                SELECT post_id, metric_name, value
                FROM meta_metrics
                WHERE post_id IN ({seq})
                AND metric_name = 'engagement'
                """.format(seq=",".join("?" * len(post_ids))),
                post_ids,
            ).fetchall()

        else:
            rows = db.execute(
                """
                SELECT post_id, metric_name, value
                FROM meta_metrics
                WHERE post_id IN ({seq})
                """.format(seq=",".join("?" * len(post_ids))),
                post_ids,
            ).fetchall()

        context["metrics"] = [dict(r) for r in rows]

    if "analizar_comentarios" in intents and post_ids:
        rows = db.execute(
            """
            SELECT post_id, text, sentiment
            FROM meta_comments
            WHERE post_id IN ({seq})
            ORDER BY timestamp DESC
            LIMIT 10
            """.format(seq=",".join("?" * len(post_ids))),
            post_ids,
        ).fetchall()

        context["comments"] = [dict(r) for r in rows]

    if any(i in intents for i in ["consultar_metricas", "analizar_comentarios"]):
        rag_chunks = retrieve_relevant_context(
            query=message,
            source_type="marketing",
            limit=5
        )
        context["rag_context"] = rag_chunks

    return context

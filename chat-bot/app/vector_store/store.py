import json                         # Serialización JSON (guardar / leer embeddings)
import math                         # Operaciones matemáticas (distancias, normalizaciones)
from typing import List, Dict       # Tipado estático para listas y diccionarios

from db.database import get_db      # Acceso a la base de datos (SQLite)
from utils.logger import get_logger # Logger centralizado del sistema

logger = get_logger(__name__)       # Logger asociado a este módulo (store.py)

"""
Calcula similitud coseno entre dos vectores.
(similitud coseno = métrica que mide qué tan parecidos son dos embeddings)
"""
def cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b + 1e-10)

"""
DESCRIPCIÓN: Guarda un embedding asociado a una fuente lógica del sistema (post, métrica, comentario, resumen).

ENTRADAS:   - source_type (str): tipo de fuente (post | metric | comment | summary)
            - source_id (str): identificador lógico de la fuente
            - content (str): texto original
            - embedding (list[float]): vector numérico

SALIDAS:    - None (persistencia en DB)
"""
def save_embedding(source_type: str, source_id: str, content: str, embedding: List[float],):
    db = get_db()

    db.execute(
        """
        INSERT INTO embeddings (source_type, source_id, content, embedding)
        VALUES (?, ?, ?, ?)
        """,
        (
            source_type,
            source_id,
            content,
            json.dumps(embedding),
        ),
    )
    db.commit()

    logger.info(f"Embedding guardado: {source_type}:{source_id}")

"""
DESCRIPCIÓN: Busca los textos más similares semánticamente a un embedding de consulta.

ENTRADAS:   - query_embedding (list[float]): embedding de la consulta
            - source_type (str): tipo de fuente a filtrar
            - top_k (int): cantidad de resultados

SALIDAS:    - Lista de dicts con contenido y score de similitud
"""
def search_similar(query_embedding: List[float], source_type: str, top_k: int = 5,) -> List[Dict]:
    db = get_db()

    rows = db.execute(
        """
        SELECT content, embedding
        FROM embeddings
        WHERE source_type = ?
        """,
        (source_type,),
    ).fetchall()

    scored = []

    for row in rows:
        emb = json.loads(row["embedding"])
        score = cosine_similarity(query_embedding, emb)

        scored.append({
            "content": row["content"],
            "score": score,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return scored[:top_k]

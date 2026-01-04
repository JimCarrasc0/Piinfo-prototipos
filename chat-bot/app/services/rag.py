import numpy as np                                  # Librería numérica para operaciones vectoriales (álgebra lineal)
from typing import List                             # Tipado estático para listas (type hints)
from app.db.database import get_db                  # Acceso a la base de datos (persistencia de contexto)
from app.services.embeddings import embed_text      # Generador de embeddings (vectores semánticos del texto)

# Función de similitud coseno
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

"""
DESCRIPCIÓN: Recupera contenido relevante usando búsqueda semántica.

ENTRADAS:   - query (str): pregunta del usuario
            - source_type (str): tipo de fuente (post, metric, comment)
            - limit (int): máximo de resultados

SALIDAS:    - List[str]: textos relevantes ordenados por similitud
"""
def retrieve_relevant_context(query: str, source_type: str, limit: int = 5) -> List[str]:
    db = get_db()
    cursor = db.execute(
        """
        SELECT content, embedding
        FROM embeddings
        WHERE source_type = ?
        """,
        (source_type,),
    )

    rows = cursor.fetchall()
    if not rows:
        return []

    query_vec = np.array(embed_text(query))
    scored = []

    for row in rows:
        emb = np.array(eval(row["embedding"]))
        score = cosine_similarity(query_vec, emb)
        scored.append((score, row["content"]))

    scored.sort(reverse=True, key=lambda x: x[0])
    return [content for _, content in scored[:limit]]

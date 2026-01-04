from sentence_transformers import SentenceTransformer, util

_model = SentenceTransformer("all-MiniLM-L6-v2")

INTENTS = {
    "listar_posts": [
        "qué publicaciones tengo",
        "cuáles son mis posts",
        "dime mis publicaciones",
        "qué he publicado",
        "muéstrame mis posts"
    ],
    "consultar_metricas": [
        "cómo me fue",
        "cómo va el engagement",
        "qué tal el rendimiento",
        "métricas del post",
        "alcance e interacciones"
    ],
    "analizar_comentarios": [
        "qué dicen los comentarios",
        "opinión de la gente",
        "comentarios negativos",
        "feedback de usuarios",
        "qué opinan"
    ],
    "recomendacion_general": [
        "qué me recomiendas",
        "cómo puedo mejorar",
        "qué debería hacer",
        "algún consejo",
        "sugerencias"
    ]
}

POST_SCOPES = {
    "last": [
        "última publicación",
        "post más reciente",
        "el último post",
        "la última que publiqué"
    ],
    "first": [
        "primera publicación",
        "mi primer post",
        "el primer post que publiqué"
    ],
    "all": [
        "todas las publicaciones",
        "todos mis posts",
        "mis publicaciones"
    ],
    "best": [
        "mejor publicación",
        "post con más likes",
        "el que mejor rindió",
        "el más exitoso"
    ],
    "worst": [
        "peor publicación",
        "post con menos engagement",
        "el que peor rindió"
    ],
    "specific": [
        "la publicación",
        "el post que dice",
        "el post sobre"
    ]
}

METRIC_SCOPES = {
    "engagement_only": [
        "engagement",
        "interacción",
        "nivel de interacción"
    ],
    "reach_only": [
        "alcance",
        "reach",
        "a cuánta gente llegó"
    ],
    "all_metrics": [
        "métricas",
        "rendimiento",
        "resultados"
    ],
    "aggregate": [
        "en general",
        "global",
        "total",
        "promedio"
    ]
}

"""
DESCRIPCIÓN: Analiza el texto del usuario para detectar múltiples intenciones y referencias implícitas a datos del sistema.

ENTRADAS:   - text (str): mensaje del usuario
            - threshold (float): umbral mínimo de similitud semántica

SALIDAS:    - dict con intents, entidades y nivel de confianza
"""
def detect_intent(text: str, threshold: float = 0.45) -> dict:
    text_emb = _model.encode(text, convert_to_tensor=True)

    intents_detected = []
    confidence = {}

    for intent, examples in INTENTS.items():
        examples_emb = _model.encode(examples, convert_to_tensor=True)
        score = util.cos_sim(text_emb, examples_emb).max().item()

        if score >= threshold:
            intents_detected.append(intent)
            confidence[intent] = round(score, 2)

    if not intents_detected:
        intents_detected.append("recomendacion_general")
        confidence["recomendacion_general"] = 0.5

    entities = {
        "post_scope": "unspecified",
        "metric_scope": "unspecified",
        "comment_scope": "unspecified",
        "post_query": None
    }

    for scope, examples in POST_SCOPES.items():
        scope_emb = _model.encode(examples, convert_to_tensor=True)
        score = util.cos_sim(text_emb, scope_emb).max().item()

        if score >= threshold:
            entities["post_scope"] = scope
            break

    for scope, examples in METRIC_SCOPES.items():
        scope_emb = _model.encode(examples, convert_to_tensor=True)
        score = util.cos_sim(text_emb, scope_emb).max().item()

        if score >= threshold:
            entities["metric_scope"] = scope
            break

    if '"' in text:
        entities["post_query"] = text.split('"')[1]

    return {
        "intents": intents_detected,
        "entities": entities,
        "confidence": confidence
    }
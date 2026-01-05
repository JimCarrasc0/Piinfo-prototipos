from sentence_transformers import SentenceTransformer   # Importa la clase que permite cargar y usar modelos de embeddings
from typing import List                                 # Tipado para indicar listas de valores (mejora legibilidad y documentación)
import warnings                                         # Módulo para manejar advertencias del sistema
warnings.filterwarnings("ignore")                       # Silencia warnings (TensorFlow, Keras, etc.) para limpiar la salida en consola

MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"           # Identificador del modelo de embeddings usado (descargado desde Hugging Face)

_model: SentenceTransformer | None = None               # Variable global para cachear el modelo y evitar recargarlo múltiples veces

"""
DESCRIPCIÓN: Carga (lazy-load) el modelo de embeddings local.

ENTRADAS:   - No recibe parámetros.

SALIDAS:    - SentenceTransformer: modelo listo para generar embeddings.
"""
def get_embedding_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(
            MODEL_NAME,
            trust_remote_code=True
        )
    return _model

"""
DESCRIPCIÓN: Convierte un texto en un embedding numérico.

ENTRADAS:   - text (str): texto a vectorizar.

SALIDAS:    - List[float]: embedding vectorial del texto.
"""
def embed_text(text: str) -> List[float]:
    model = get_embedding_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
from app.services.embeddings import embed_text
import warnings
warnings.filterwarnings("ignore")

print("Probando embeddings...")
vector = embed_text("Hola mundo, esto es una prueba")

print("Tipo:", type(vector))
print("Largo del vector:", len(vector))
print("Primeros 5 valores:", vector[:5])
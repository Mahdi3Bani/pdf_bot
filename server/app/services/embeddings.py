from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def create_chunks(self, text: str, chunk_size: int = 500, overlap: int = 50):
        words = text.split()
        self.chunks = [
            " ".join(words[i:i + chunk_size])
            for i in range(0, len(words), chunk_size - overlap)
        ]

    def build_index(self):
        embeddings = self.model.encode(self.chunks)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))

    def search_index(self, query: str, top_k: int = 3):
        if not self.index:
            raise ValueError("Index has not been built yet.")
        query_embedding = self.model.encode([query])[0]
        distances, indices = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        return [self.chunks[i] for i in indices[0]]

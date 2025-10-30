import os

# Default directory for ChromaDB persistence
# This can be overridden by setting the CHROMA_DB_PERSIST_DIRECTORY environment variable
CHROMA_DB_PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

PROVIDER = "google_genai"
MODEL = "gemini-2.5-flash-lite"
MODEL_URL = None

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


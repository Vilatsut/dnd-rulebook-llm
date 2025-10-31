import os
from dotenv import load_dotenv

load_dotenv(override=True)

CHROMA_DB_PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

# These come from DMR
MODEL = os.getenv("AI_RUNNER_MODEL", "ai/smollm2")
MODEL_URL = os.getenv("AI_RUNNER_URL", "http://localhost:12434/engines/v1/")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


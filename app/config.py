import os
from dotenv import load_dotenv

load_dotenv(override=True)

CHROMA_DB_PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

# These come from DMR
MODEL = os.getenv("AI_RUNNER_MODEL", "NOT SET")
MODEL_URL = os.getenv("AI_RUNNER_URL", "NOT SET")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


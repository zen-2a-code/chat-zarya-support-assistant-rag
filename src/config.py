import os

from dotenv import load_dotenv

load_dotenv()

PDF_DIR = "data/pdfs"
CHUNKS_PATH = "data/chunks.json"
COLLECTION = "zarya_docs"

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")  # only for Qdrant Cloud

EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

# Below this cosine similarity the question is treated as out of scope (tune with eval/refusal.py)
MIN_SIMILARITY = float(os.getenv("MIN_SIMILARITY", "0.35"))

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # "ollama" or "openai"
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
from pathlib import Path

#Project root directory
BASE_DIR = Path(__file__).resolve().parent

# Docuentation location
DATA_PATH = BASE_DIR/"data"

# Chroma database location
VECTORSTORE_PATH = BASE_DIR / "vectorstore"
VECTORSTORE_FILENAME = VECTORSTORE_PATH/"chroma_db"

#ollama models
#Chat model
OLLAMA_MODEL = "qwen3.5:9b"
#OLLAMA_MODEL = "llama3.2"


#Embedding model
EMBEDDING_MODEL = "nomic-embed-text"

# Text Splitting

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".md"]
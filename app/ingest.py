from pathlib import Path 

import chromadb
from sentence_transformers import SentenceTransformer

# Configuration
#----------------

DOCUMENT_DIR = Path("data/documents")
CHROMA_DIR = Path("chroma_db")

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Load Embedding model
#----------------------

print("Loading embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding model loaded.")

# Create ChromaDB
#-------------------

client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="engineering_docs"
)

# Simple text chunking
#------------------------

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    sections = text.split("\n\n")

    chunks = []

    for section in sections:
        section = section.strip()

        if section:
            chunks.append(section)

    return chunks

# Read documents
#-----------------

documents = []
metadatas = []
ids = []

document_files = list(DOCUMENT_DIR.glob("*.txt"))
print(f"Found {len(document_files)} document(s).")

for file_path in document_files:

    print(f"Processing: {file_path.name}")

    text = file_path.read_text(encoding="utf-8")

    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):

        print(f"\n---- CHUNK {index}-----")
        print(chunk)

        documents.append(chunk)

        metadatas.append({
            "source": file_path.name,
            "chunk": index
        })

        ids.append(
            f"{file_path.stem}-chunk-{index}"
        )


# Generate embeddings 
#----------------------

print(f"Creating embeddings for {len(documents)} chuncks...")

embeddings = model.encode(
    documents,
    normalize_embeddings=True
)

# Store in ChromaDB
#---------------------

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("\n Ingestion complete.")
print(f" Stored {len(documents)} chunks in ChromaDB. ")
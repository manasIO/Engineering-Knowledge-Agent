import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Load embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

# Connect to existing chromadb
client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

collection = client.get_collection(
    name="engineering_docs"
)

def retrieve(question: str, top_k: int = 3):

    query_embedding = model.encode(question).tolist()
    
    # query_embedding = model.encode(
    #     [query],
    #     normalize_embeddings=True
    # )[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results

#-----------------------
# Test Retrieval
#-----------------------

if __name__ == "__main__":

    question = input("\n Ask a question: ")

    results = retrieve(question)

    print("\n ---Retrieved Documents ---\n")

    for i, document in enumerate(results["documents"][0]):

        metadata = results["metadatas"][0][i]
        distance = results["distances"][0][i]

        print(f"Result {i + 1}")
        print(f"Source: {metadata['source']}")
        print(f"Chunk: {metadata['chunk']}")
        print(f"Distance: {distance:.4f}")
        print()
        print(document)
        print("\n" + "-" * 60)
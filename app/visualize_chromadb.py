import chromadb

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection("engineering_docs")
data = collection.get(include=["embeddings","metadatas"])

embeddings = data["embeddings"]
print("Embedding shape: ", embeddings.shape)
print("First vector: ", embeddings[0])

points = PCA(n_components=2).fit_transform(embeddings)
plt.scatter(points[:, 0], points[:, 1])

for i, metadata in enumerate(data["metadatas"]):
    plt.annotate(metadata.get("source", str(i)), points[i])

plt.title("Engineering document embeddings (PCA)")
plt.show()
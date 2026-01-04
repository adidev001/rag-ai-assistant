import chromadb
import uuid
import os

# Use persistent client so data actually exists
# Ensure the directory exists or let chroma create it
PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "chroma_db")
client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)

collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

def add_to_vector_store(chunks, embeddings):
    documents = []
    metadatas = []
    ids = []

    for i, chunk in enumerate(chunks):
        documents.append(chunk["text"])
        metadatas.append(chunk["metadata"])
        ids.append(str(uuid.uuid4()))

    # embeddings is already a list of lists from embeddings.py
    collection.add(
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
        ids=ids
    )

def search_vector_store(query_embedding, top_k=5):
    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # print("SEARCH RESULT:", result)
    return result


def reset_vector_store():
    global collection
    client.delete_collection("documents")
    collection = client.get_or_create_collection("documents")

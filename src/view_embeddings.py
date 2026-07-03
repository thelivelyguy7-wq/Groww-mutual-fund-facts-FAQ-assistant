import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

def view_embeddings():
    print("Initializing embedding model (BAAI/bge-small-en-v1.5)...")
    embed_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db")
    
    if not os.path.exists(db_path):
        print(f"Error: ChromaDB directory not found at {db_path}")
        return
        
    print(f"Loading ChromaDB from {db_path}...")
    db = Chroma(persist_directory=db_path, embedding_function=embed_model)
    
    # We fetch a few random chunks to examine their structure and embeddings
    print("Fetching 3 chunks...\n" + "-"*50)
    data = db.get(limit=3, include=["embeddings", "metadatas", "documents"])
    
    docs = data.get("documents", [])
    metadatas = data.get("metadatas", [])
    embeddings = data.get("embeddings", [])
    
    for i in range(len(docs)):
        print(f"--- CHUNK {i+1} ---")
        print(f"METADATA: {metadatas[i]}")
        print(f"TEXT PREVIEW: {docs[i][:200]}...")
        
        # Determine embedding dimension
        emb = embeddings[i]
        print(f"EMBEDDING VECTOR: Length = {len(emb)}")
        print(f"EMBEDDING SAMPLE: {emb[:5]} ... (truncated)")
        print("-" * 50)
        
    print(f"\nTotal chunks in database: {db._collection.count()}")

if __name__ == "__main__":
    view_embeddings()

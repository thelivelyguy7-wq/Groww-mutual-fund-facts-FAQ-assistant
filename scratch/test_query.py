import os
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db")

def main():
    print("Loading HuggingFace BGE Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    print("Connecting to ChromaDB...")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    query = "What is the exit load for HDFC Small Cap?"
    print(f"\nQuerying: {query}")
    results = vectorstore.similarity_search(query, k=2)
    
    for i, doc in enumerate(results):
        print(f"\nResult {i+1} (Source: {doc.metadata.get('fund_name')}):")
        print(doc.page_content[:200] + "...")

if __name__ == "__main__":
    main()

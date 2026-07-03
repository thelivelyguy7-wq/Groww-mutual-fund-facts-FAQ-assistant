import os
import json
import glob
import shutil
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

load_dotenv()

PROCESSED_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db")

def main():
    json_files = glob.glob(os.path.join(PROCESSED_DIR, "*.json"))
    if not json_files:
        print("No processed JSON files found. Run cleaner.py first.")
        return
        
    # Wipe ChromaDB directory to start fresh
    if os.path.exists(DB_DIR):
        try:
            shutil.rmtree(DB_DIR)
            print("Wiped old ChromaDB.")
        except Exception as e:
            print(f"Warning: Could not delete old ChromaDB: {e}")
            
    documents = []
    
    # We use RecursiveCharacterTextSplitter for generic HTML text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
    )
    
    for filepath in json_files:
        if os.path.basename(filepath) in ["manifest.json", "hashes.json", "all_funds.json"]:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        fund_name = data.get("fund_name", "Unknown Fund")
        url = data.get("url", "")
        text = data.get("content", "")
        
        if not text.strip():
            continue
            
        chunks = text_splitter.split_text(text)
        
        for chunk in chunks:
            # Inject fund name into the chunk so LLM/CrossEncoder has full context
            chunk_with_title = f"Fund Name: {fund_name}\n\n{chunk}"
            
            meta = {
                "fund_name": fund_name,
                "source_url": url,
                "filename": os.path.basename(filepath)
            }
            
            doc = Document(
                page_content=chunk_with_title,
                metadata=meta
            )
            documents.append(doc)
            
    import hashlib
    for idx, doc in enumerate(documents):
        id_str = f"{doc.metadata.get('filename', 'unknown')}_{idx}"
        doc_id = hashlib.sha256(id_str.encode('utf-8')).hexdigest()
        doc.metadata["id"] = doc_id
            
    print(f"Created {len(documents)} document chunks from HTML.")
    
    print("Initializing HuggingFace BGE Embeddings...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    print("Storing chunks in ChromaDB...")
    vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    doc_ids = [doc.metadata["id"] for doc in documents]
    vectorstore.add_documents(documents=documents, ids=doc_ids)
    
    print(f"Successfully upserted {len(documents)} chunks into {DB_DIR}")

if __name__ == "__main__":
    main()

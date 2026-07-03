import os
import re
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma_db")

REFUSAL_MESSAGE = (
    "I can only provide objective facts based on official mutual fund documents. "
    "I cannot provide investment advice, recommendations, or speculative opinions. "
    "For more information, please visit the [AMFI Investor Education portal](https://www.amfiindia.com/investor-corner)."
)

def is_advisory_query(query: str) -> bool:
    """
    Very basic heuristic query classifier.
    In a real prod system, this could be a zero-shot LLM pass or a trained classifier.
    """
    advisory_keywords = [
        "should i", "recommend", "better", "best", "versus", "vs", 
        "advice", "buy or sell", "predict", "future", "opinion", "worth"
    ]
    query_lower = query.lower()
    for kw in advisory_keywords:
        if kw in query_lower:
            return True
    return False

def format_date(iso_str):
    if not iso_str:
        return "Unknown date"
    return iso_str.split("T")[0]

import time
import sqlite3
from sentence_transformers import CrossEncoder

def log_telemetry(query, latency, chunks_retrieved, final_answer):
    """Phase 7: Basic Observability Logger"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "telemetry.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs
                 (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, query TEXT, latency REAL, chunks INTEGER, answer TEXT)''')
    c.execute("INSERT INTO logs (query, latency, chunks, answer) VALUES (?, ?, ?, ?)", 
              (query, latency, chunks_retrieved, final_answer))
    conn.commit()
    conn.close()

class RAGPipeline:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        self.vectorstore = Chroma(persist_directory=DB_DIR, embedding_function=self.embeddings)
        # Phase 6: Cast a wider net for the reranker
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 15})
        self.llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.0)
        self.reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=512)
        
        self.rewrite_prompt = PromptTemplate(
            input_variables=["query"],
            template="Rewrite this query to be clear and optimized for semantic search of mutual funds. Output ONLY the rewritten query.\nQuery: {query}\nRewritten:"
        )
        
        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an AI assistant designed to answer questions about mutual funds based ONLY on the provided context. 
Keep your answers under 3 sentences. Do NOT provide financial advice. 
Note: If the user asks for the 'price' or 'current price', you MUST look for the 'NAV' (Net Asset Value) in the context and provide that value as the answer.
If the context does not contain the answer, say 'I do not have this information.'

Context:
{context}

Question:
{question}

Answer:"""
        )

    def process_query(self, query: str) -> str:
        start_time = time.time()
        
        if is_advisory_query(query):
            latency = time.time() - start_time
            log_telemetry(query, latency, 0, REFUSAL_MESSAGE)
            return REFUSAL_MESSAGE
            
        # Phase 6: Query Rewriting
        rewrite_chain = self.rewrite_prompt | self.llm
        rewritten_query = rewrite_chain.invoke({"query": query}).content.strip()
            
        docs = self.retriever.invoke(rewritten_query)
        if not docs:
            return "I do not have this information in my knowledge base."
            
        # Phase 6: Cross-Encoder Reranking
        pairs = [[rewritten_query, doc.page_content] for doc in docs]
        scores = self.reranker.predict(pairs)
        
        # Sort docs by score (descending)
        scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        # Keep top 3
        top_docs = [doc for doc, score in scored_docs[:3]]
            
        # Combine contexts
        context = "\n\n".join([d.page_content for d in top_docs])
        
        chain = self.prompt | self.llm
        result = chain.invoke({"context": context, "question": query})
        
        raw_answer = result.content.strip()
        
        # Enforce 3 sentence rule (LLM usually follows, but this is a hard post-processing fallback)
        sentences = re.split(r'(?<=[.!?]) +', raw_answer)
        if len(sentences) > 3:
            raw_answer = " ".join(sentences[:3])
            
        # Extract best source
        best_doc = top_docs[0]
        source_url = best_doc.metadata.get("source_url", "Unknown source")
        fund_name = best_doc.metadata.get("fund_name", "Unknown Fund")
        
        # Build footer
        footer = f"\n\nSource: [{fund_name}]({source_url})\n> Last updated from sources: 2026-07-03"
        
        final_answer = raw_answer + footer
        
        # Phase 7: Logging
        latency = time.time() - start_time
        log_telemetry(query, latency, len(top_docs), final_answer)
        
        return final_answer

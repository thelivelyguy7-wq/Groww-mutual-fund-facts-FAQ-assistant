from src.rag_pipeline import RAGPipeline
import asyncio

def test():
    pipeline = RAGPipeline()
    query = "What is the exit load for HDFC Small Cap Fund?"
    print(f"Query: {query}")
    answer = pipeline.process_query(query)
    print(f"\nAnswer:\n{answer}")
    
if __name__ == "__main__":
    test()

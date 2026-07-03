import os
import sys

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag_pipeline import RAGPipeline
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

def run_evals():
    print("--- Running Automated RAG Evals ---")
    pipeline = RAGPipeline()
    judge_llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.0)
    
    # Golden queries
    test_queries = [
        "What is the exit load for HDFC Small Cap?",
        "What is the riskometer classification for HDFC ELSS Tax Saver?",
        "What is the expense ratio of HDFC Liquid Fund?"
    ]
    
    # Basic judge prompt to check for hallucination (Faithfulness)
    faithfulness_prompt = PromptTemplate(
        input_variables=["context", "answer"],
        template="""Given the context, is the answer perfectly faithful and supported by it? 
Answer 'Yes' if all claims in the answer can be directly verified by the context. Answer 'No' otherwise.
Context:
{context}

Answer:
{answer}

Output (Yes/No):"""
    )
    
    for i, q in enumerate(test_queries):
        print(f"\nQuery {i+1}: {q}")
        try:
            # 1. Run pipeline (returns formatted answer + footer)
            final_answer = pipeline.process_query(q)
            # The context that was actually used is logged in telemetry, or we can just fetch it again to evaluate
            rewritten = pipeline.rewrite_prompt.invoke({"query": q}).to_messages()
            # Simulate retrieval just for context evaluation
            rewritten_str = pipeline.llm.invoke(rewritten).content.strip()
            docs = pipeline.retriever.invoke(rewritten_str)
            pairs = [[rewritten_str, doc.page_content] for doc in docs]
            scores = pipeline.reranker.predict(pairs)
            scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
            top_docs = [doc for doc, score in scored_docs[:3]]
            context = "\n\n".join([d.page_content for d in top_docs])
            
            print(f"Generated Answer:\n{final_answer}\n")
            
            # 2. Evaluate Faithfulness
            judge_chain = faithfulness_prompt | judge_llm
            result = judge_chain.invoke({"context": context, "answer": final_answer})
            
            judge_verdict = result.content.strip().lower()
            if 'yes' in judge_verdict:
                print(">> Faithfulness: PASSED")
            else:
                print(">> Faithfulness: FAILED")
                print(f"Judge output: {judge_verdict}")
                
        except Exception as e:
            print(f"Error evaluating query '{q}': {e}")
            
    print("\n--- Evals Complete ---")

if __name__ == "__main__":
    run_evals()

from src.rag_pipeline import RAGPipeline

p = RAGPipeline()
q = "What is the current price of HDFC Small Cap?"

print("1. Original Query:", q)
rewritten = (p.rewrite_prompt | p.llm).invoke({"query": q}).content.strip()
print("2. Rewritten Query:", rewritten)

docs = p.retriever.invoke(rewritten)
print("3. Retriever Docs Found:", len(docs))

pairs = [[rewritten, doc.page_content] for doc in docs]
scores = p.reranker.predict(pairs)
scored_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
top_docs = [doc for doc, score in scored_docs[:3]]

context = "\n\n".join([d.page_content for d in top_docs])
print("4. Top 3 Contexts (Truncated):")
for d in top_docs:
    print("---")
    print(d.page_content[:150].encode('ascii', 'ignore').decode())

result = (p.prompt | p.llm).invoke({"context": context, "question": q}).content.strip()
print("5. LLM Answer:", result.encode('ascii', 'ignore').decode())

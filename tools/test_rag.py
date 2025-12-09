from agents.rag_search_agent import RAGSearchAgent

rag = RAGSearchAgent()

query = "headache fever muscle pain"

results = rag.search(query, top_k=5)

print("\n=== RESULTS ===\n")
for r in results:
    print(f"{r['name']}  | score={r['score']:.3f}")

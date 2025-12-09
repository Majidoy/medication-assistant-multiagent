from agents.recommandation_agent import RecommendationAgent

agent = RecommendationAgent("data/enriched/openfda_enriched_500.json")

symptoms = "I have fever"

results = agent.recommend(symptoms)

print("\n=== RECOMMENDATIONS ===\n")
for r in results:
    print(f"{r['name']} | score={r['score']:.3f} | category={r['category']}")
    print("Symptoms:", r["symptoms"])
    print("Indications:", r["clean_indications"])
    print("Raw:", r["clean_indications"])
    print("-----")

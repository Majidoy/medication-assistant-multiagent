import json
from agents.rag_search_agent import RAGSearchAgent

class RecommendationAgent:
    def __init__(self, dataset_path="data/enriched/openfda_enriched_500.json"):
        print("[Reco] Initializing Recommendation Agent...")
        self.dataset_path = dataset_path

        # Appel correct du RAGSearchAgent
        self.rag = RAGSearchAgent(dataset_path)

        # Charger dataset
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def recommend(self, symptoms, top_k=5):
        print(f"[Reco] Symptoms input: {symptoms}")

        results = self.rag.search(symptoms, top_k=top_k)

        recommendations = []

        for item in results:
            med_name = item["name"]
            score = item["score"]
            med_info = self.data[med_name]

            recommendations.append({
                "name": med_name,
                "score": score,
                "category": med_info.get("category", "unknown"),
                "symptoms": med_info.get("symptoms", []),
                "clean_indications": med_info.get("clean_indications", "")
            })

        return recommendations

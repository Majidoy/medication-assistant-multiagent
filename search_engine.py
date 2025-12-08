import json
import re

class MedicationSearchEngine:
    def __init__(self, json_path="data/raw/openfda_500.json"):
        with open(json_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def preprocess_text(self, text):
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r"[^a-z0-9 ]+", " ", text)
        return text

    def search(self, query, top_k=5):
        query = self.preprocess_text(query)
        results = []

        for name, drug in self.data.items():
            combined_text = " ".join([
                drug.get("name", ""),
                drug.get("generic_name", ""),
                drug.get("substance_name", ""),
                drug.get("purpose", ""),
                drug.get("indications_and_usage", ""),
                drug.get("warnings", "")
            ])

            combined_text = self.preprocess_text(combined_text)

            score = sum(combined_text.count(word) for word in query.split())
            if score > 0:
                results.append((name, score))

        results.sort(key=lambda x: x[1], reverse=True)
        return [name for name, _ in results[:top_k]]

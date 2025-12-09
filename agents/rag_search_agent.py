import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class RAGSearchAgent:
    def __init__(self, dataset_path="data/enriched/openfda_enriched_500.json"):
        self.dataset_path = dataset_path

        print("[RAG] Loading enriched dataset...")
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

        print(f"[RAG] {len(self.data)} medications loaded.")

        # Préparer les documents textuels pour TF-IDF
        self.drug_names = list(self.data.keys())
        self.corpus = []

        for name, entry in self.data.items():
            text = " ".join([
                entry.get("clean_indications", ""),
                " ".join(entry.get("symptoms", [])),
                " ".join(entry.get("tags", [])),
                entry.get("category", "")
            ])
            self.corpus.append(text)

        print("[RAG] Building TF-IDF index...")
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.corpus)

        print("[RAG] RAG Search Agent ready.")

    def search(self, user_query, top_k=5):
        """
        Recherche les médicaments les plus similaires à une requête de symptômes.
        """
        query_vec = self.vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]

        # Trier les scores
        top_indices = similarities.argsort()[::-1][:top_k]

        results = []
        for i in top_indices:
            name = self.drug_names[i]
            score = similarities[i]
            results.append({
                "name": name,
                "score": float(score),
                "data": self.data[name]
            })

        return results

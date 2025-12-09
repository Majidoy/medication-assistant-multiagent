import json
import time
import re
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


def extract_json(text):
    """Extracts the largest JSON object from a messy LLM output."""
    json_candidates = re.findall(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', text, flags=re.DOTALL)

    if not json_candidates:
        raise ValueError("No JSON object found in response.")

    # Try all JSON chunks, prefer the largest valid one
    for chunk in sorted(json_candidates, key=len, reverse=True):
        try:
            return json.loads(chunk)
        except Exception:
            continue

    raise ValueError("No valid JSON object found in response.")


class DatasetEnricher:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path

        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        print("[LLM] Groq Enricher initialized.")

    def enrich_medicine(self, entry):
        name = entry.get("name", "")
        indications = entry.get("indications_and_usage", "")

        prompt = f"""
You are a medical NLP expert. Extract structured information from the medication description.

MEDICATION NAME: {name}
INDICATIONS: {indications}

Return a JSON object with:
- symptoms: list of symptoms mentioned
- category: one medical category (pain relief, cold & flu, antibacterial, skin care, allergy, fever, stomach, etc.)
- tags: 5–10 relevant keywords
- clean_indications: a short normalized rewritten version (one sentence)

Return ONLY valid JSON, no explanation.
"""

        for attempt in range(3):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.2,
                    max_tokens=300
                )

                content = response.choices[0].message.content.strip()

                # remove code fencing if present
                if content.startswith("```"):
                    content = content.replace("```json", "").replace("```", "").strip()

                # extract clean JSON
                return extract_json(content)

            except Exception as e:
                print(f"[WARNING] {name} → Attempt {attempt+1} failed: {e}")
                time.sleep(1)

        # fallback if totally impossible
        print(f"[FAILED] {name} → Using fallback empty structure.")
        return {
            "symptoms": [],
            "category": "unknown",
            "tags": [],
            "clean_indications": ""
        }

    def run(self):
        print("[Enricher] Loading dataset...")
        with open(self.input_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        print(f"[Enricher] {len(data)} medications loaded.")
        enriched_data = {}

        for i, (name, entry) in enumerate(data.items()):
            print(f"[{i+1}/{len(data)}] Processing: {name}")

            enriched = self.enrich_medicine(entry)

            enriched_data[name] = {**entry, **enriched}

            time.sleep(0.1)

        print("[Enricher] Saving final enriched dataset...")
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(enriched_data, f, indent=4, ensure_ascii=False)

        print(f"[DONE] Saved enriched dataset to {self.output_path}")


if __name__ == "__main__":
    enricher = DatasetEnricher(
        input_path="data/raw/openfda_500.json",
        output_path="data/enriched/openfda_enriched_500.json"
    )
    enricher.run()

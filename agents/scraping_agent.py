import requests
import json
import os
from time import sleep

class ScrapingAgent:
    BASE_URL = "https://api.fda.gov/drug/label.json"

    def __init__(self, output_path="data/raw/"):
        self.output_path = output_path
        if not os.path.exists(output_path):
            os.makedirs(output_path)

    # ---------------------------------------------------------
    # Fetch drug data from OpenFDA API
    # ---------------------------------------------------------
    def fetch_drugs(self, limit=10):
        print("[OpenFDA] Fetching drug data...")

        params = {
            "limit": limit
        }

        resp = requests.get(self.BASE_URL, params=params)

        if resp.status_code != 200:
            print("[OpenFDA] API Error:", resp.status_code)
            return []

        data = resp.json()

        drugs = data.get("results", [])
        print(f"[OpenFDA] Retrieved {len(drugs)} drugs.")

        return drugs

    # ---------------------------------------------------------
    # Parse FDA JSON for a single drug
    # ---------------------------------------------------------
    def parse_drug(self, drug_json):
        # Extract fields, fallback to empty strings/lists
        openfda = drug_json.get("openfda", {})

        return {
            "brand_name": openfda.get("brand_name", ["Unknown"])[0],
            "generic_name": openfda.get("generic_name", ["Unknown"])[0],
            "substance_name": openfda.get("substance_name", ["Unknown"])[0],
            "purpose": drug_json.get("purpose", [""])[0] if "purpose" in drug_json else "",
            "indications_and_usage": drug_json.get("indications_and_usage", [""])[0],
            "warnings": drug_json.get("warnings", [""])[0],
            "adverse_reactions": drug_json.get("adverse_reactions", [""])[0],
            "dosage_and_administration": drug_json.get("dosage_and_administration", [""])[0],
        }

    # ---------------------------------------------------------
    # Full scraping pipeline
    # ---------------------------------------------------------
    def scrape_all(self, limit=10):
        drugs_json = self.fetch_drugs(limit)

        parsed_data = {}

        for idx, drug in enumerate(drugs_json):
            parsed = self.parse_drug(drug)
            name = parsed["brand_name"]
            print(f"[{idx+1}/{len(drugs_json)}] Processed {name}")
            parsed_data[name] = parsed
            sleep(0.1)

        return parsed_data

    # ---------------------------------------------------------
    # Save to JSON
    # ---------------------------------------------------------
    def save_results(self, results, filename="openfda_data.json"):
        path = os.path.join(self.output_path, filename)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print(f"[OpenFDA] Data saved to {path}")

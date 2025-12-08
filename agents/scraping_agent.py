import requests
import json
import time
from pathlib import Path


class ScrapingAgent:
    BASE_URL = "https://api.fda.gov/drug/label.json"

    def __init__(self):
        self.output_dir = Path("data/raw")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _request(self, url, retries=5):
        """Robust GET request with retry logic."""
        for attempt in range(1, retries + 1):
            try:
                resp = requests.get(url, timeout=10)
                print(f"[HTTP] Status: {resp.status_code}")

                if resp.status_code == 200:
                    return resp.json()

                time.sleep(attempt * 1.2)

            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(attempt * 1.2)

        print("[ERROR] Failed after retries.")
        return None

    def fetch_paginated(self, target_total=500, batch_size=100):
        """
        Fetch approx `target_total` drugs using pagination.
        """
        print(f"[ScrapingAgent] Fetching ≈{target_total} drugs…")

        final_data = {}
        skip = 0

        while len(final_data) < target_total:

            print(f"\n[Batch] skip={skip}, current={len(final_data)}")

            query = (
                "search=purpose:*"     # take all categories for maximum variety
            )
            url = (
                f"{self.BASE_URL}?{query}"
                f"&limit={batch_size}&skip={skip}"
            )

            data = self._request(url)

            if not data or "results" not in data or len(data["results"]) == 0:
                print("[INFO] End of available OpenFDA results.")
                break

            for entry in data["results"]:
                brand = entry.get("openfda", {}).get("brand_name", ["UNKNOWN"])[0]

                if brand == "UNKNOWN":
                    continue

                # add clean record
                final_data[brand] = {
                    "name": brand,
                    "generic_name": entry.get("openfda", {}).get("generic_name", [""])[0],
                    "substance_name": entry.get("openfda", {}).get("substance_name", [""])[0],
                    "purpose": entry.get("purpose", [""])[0],
                    "indications_and_usage": entry.get("indications_and_usage", [""])[0],
                    "warnings": entry.get("warnings", [""])[0],
                    "adverse_reactions": entry.get("adverse_reactions", [""])[0],
                    "dosage_and_administration": entry.get("dosage_and_administration", [""])[0],
                }

                if len(final_data) >= target_total:
                    break

            skip += batch_size
            time.sleep(1.3)      # avoid rate limiting

        print(f"\n[ScrapingAgent] FINAL CLEAN COUNT: {len(final_data)}")
        return final_data

    def save(self, data, filename="openfda_500.json"):
        path = self.output_dir / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"[Saved] {path}")

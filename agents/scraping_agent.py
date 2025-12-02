# agents/scraping_agent.py

import requests
from bs4 import BeautifulSoup
import json
import os


class ScrapingAgent:
    def __init__(self, output_path="data/raw/"):
        self.base_url = "https://www.nhs.uk/medicines/"
        self.output_path = output_path

        if not os.path.exists(output_path):
            os.makedirs(output_path)

    # ----------------------------------------------------------------------
    # MAIN SCRAPING LOGIC
    # ----------------------------------------------------------------------

    def scrape_all_medicines(self):
        """
        Scrapes the A-to-Z list of medicines from NHS.uk
        and returns a dictionary of all scraped data.
        """
        print("[ScrapingAgent] Fetching list of medicines...")

        index_url = self.base_url + "a-to-z/"
        response = requests.get(index_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find medicine links
        links = soup.select("ul.nhsuk-list li a")[:5]
        print(f"[ScrapingAgent] Found {len(links)} medicines.")

        all_data = {}

        for idx, link in enumerate(links):
            med_name = link.text.strip()
            med_url = "https://www.nhs.uk" + link.get("href")

            print(f"[{idx+1}/{len(links)}] Scraping {med_name}...")

            data = self.scrape_medicine_page(med_url)
            if data:
                all_data[med_name] = data

        return all_data

    # ----------------------------------------------------------------------
    # SCRAPING EACH MEDICINE PAGE
    # ----------------------------------------------------------------------

    def scrape_medicine_page(self, url):
        """
        Scrapes an individual NHS medicine page.
        Extracts symptoms treated, side effects, and advice.
        """
        try:
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            return self.parse_nhs_medicine(soup)

        except Exception as e:
            print(f"[ScrapingAgent] Error scraping page: {e}")
            return None

    # ----------------------------------------------------------------------
    # NHS PARSER
    # ----------------------------------------------------------------------

    def parse_nhs_medicine(self, soup):
        """
        Extracts clean structured information from an NHS medicine page.
        """

        data = {
            "description": "",
            "uses": [],
            "side_effects": [],
            "warnings": []
        }

        # DESCRIPTION
        desc = soup.select_one("p.nhsuk-lede-text")
        if desc:
            data["description"] = desc.text.strip()

        # EXTRACT ALL SECTIONS TITLES
        sections = soup.select("h2.nhsuk-heading-l")

        for sec in sections:
            title = sec.text.strip().lower()

            # USES / WHAT IS IT FOR?
            if "used" in title or "what" in title:
                data["uses"] = self._extract_bullet_list(sec)

            # SIDE EFFECTS
            if "side effect" in title:
                data["side_effects"] = self._extract_bullet_list(sec)

            # WARNINGS / WHO CAN TAKE
            if "who can" in title or "not suitable" in title:
                data["warnings"] = self._extract_bullet_list(sec)

        return data

    # ----------------------------------------------------------------------
    # HELPERS
    # ----------------------------------------------------------------------

    def _extract_bullet_list(self, section_title):
        """
        Finds the <ul> list immediately after an <h2> section title.
        Useful for extracting side effects, symptoms, etc.
        """
        ul = section_title.find_next("ul")
        if not ul:
            return []
        return [li.text.strip() for li in ul.find_all("li")]

    # ----------------------------------------------------------------------
    # SAVE RESULTS
    # ----------------------------------------------------------------------

    def save_results(self, results, filename="nhs_scraped_data.json"):
        """
        Save scraped results to JSON.
        """
        path = os.path.join(self.output_path, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        print(f"[ScrapingAgent] Data saved to {path}")


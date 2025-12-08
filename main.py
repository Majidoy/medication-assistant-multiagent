from agents.scraping_agent import ScrapingAgent

def main():
    agent = ScrapingAgent()
    data = agent.scrape_all(limit=10)
    agent.save_results(data, "openfda_sample_10.json")

if __name__ == "__main__":
    main()

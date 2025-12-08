from agents.scraping_agent import ScrapingAgent

def main():
    agent = ScrapingAgent()
    data = agent.fetch_paginated(target_total=500, batch_size=100)
    agent.save(data, filename="openfda_500.json")

if __name__ == "__main__":
    main()

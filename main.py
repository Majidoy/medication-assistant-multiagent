from agents.query_llm_agent import QueryLLMAgent

def main():
    agent = QueryLLMAgent()

    print("Medication Assistant — Type your symptoms. Type quit to exit.\n")

    while True:
        user = input("You: ")
        if user.lower() in ["quit", "exit"]:
            break

        response = agent.recommend(user)
        print("\nAssistant:", response, "\n")

if __name__ == "__main__":
    main()

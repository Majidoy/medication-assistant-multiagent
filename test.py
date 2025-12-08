from agents.query_llm_agent import QueryLLMAgent

agent = QueryLLMAgent()

text = """
Temporarily relieves minor aches and pains due to headache,
menstrual cramps, cold, flu, toothache or fever.
"""

result = agent.classify_indication(text)

print("\n=== RESULT ===")
print(result)

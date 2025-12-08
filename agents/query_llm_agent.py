import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class QueryLLMAgent:
    """
    Agent LLM utilisant Groq pour classifier les médicaments selon les symptômes.
    """

    def __init__(self, model="llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY manquant dans le fichier .env")

        self.client = Groq(api_key=api_key)
        self.model = model

        print("[LLM] Groq Agent initialized.")

    def classify_indication(self, text):
        """
        Retourne une liste JSON de symptômes normalisés.
        """

        prompt = f"""
You are a medical text classifier.

Extract ONLY the symptoms, indications, or conditions mentioned
in the following drug description. Return a JSON list.

Text:
{text}

Output format example:
["pain", "fever", "headache"]
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content

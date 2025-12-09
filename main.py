import json
from agents.rag_search_agent import RAGSearchAgent
from agents.recommandation_agent import RecommendationAgent
from agents.vision_agent import VisionAgent
from tkinter import Tk, filedialog

def symptom_flow():
    print("\n=== SYMPTOM → RECOMMENDATION ===")
    symptoms = input("Enter your symptoms: ")

    agent = RecommendationAgent("data/enriched/openfda_enriched_500.json")
    results = agent.recommend(symptoms)

    print("\n=== TOP RECOMMENDATIONS ===")
    for r in results:
        print(f"- {r['name']} (score={r['score']:.3f}) | category={r['category']}")
    print()


def vision_flow():
    print("\n=== MEDICATION IMAGE VERIFICATION ===")

    Tk().withdraw()
    image_path = filedialog.askopenfilename(
        title="Select medication picture",
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )

    if not image_path:
        print("No image selected.")
        return

    print(f"[Vision] Image selected: {image_path}")

    agent = VisionAgent(model_path="data/models/yolo_best.pt", device="cpu")
    result = agent.detect(image_path)

    print("\n=== RESULT ===")
    if result is None:
        print("No medication detected.")
    else:
        print(f"Detected object: {result['detected_name']}")
        print(f"Confidence: {result['confidence']:.3f}")


def main():
    print("====================================")
    print(" Medication Assistant — Multi-Agent ")
    print("====================================")
    print("Choose an action:")
    print("1) Recommend medication from symptoms")
    print("2) Verify medication using image")
    print("3) Exit")

    choice = input("\nYour choice: ")

    if choice == "1":
        symptom_flow()
    elif choice == "2":
        vision_flow()
    else:
        print("Goodbye!")


if __name__ == "__main__":
    main()

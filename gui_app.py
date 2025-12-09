import json
import tkinter as tk
from tkinter import messagebox, filedialog
from agents.rag_search_agent import RAGSearchAgent
from agents.recommandation_agent import RecommendationAgent
from agents.vision_agent import VisionAgent

# -------------------------
# GUI APPLICATION
# -------------------------

class MedicationApp:
    def __init__(self, root):
        self.root = root
        root.title("Medication Assistant")
        root.geometry("650x500")

        title = tk.Label(root, text="Medication Assistant", font=("Arial", 20, "bold"))
        title.pack(pady=20)

        # ===================== SYMPTOM INPUT =====================
        symptom_frame = tk.LabelFrame(root, text="1. Enter Symptoms", padx=10, pady=10)
        symptom_frame.pack(fill="both", padx=20, pady=10)

        self.symptom_entry = tk.Entry(symptom_frame, width=60)
        self.symptom_entry.pack(side="left", padx=10)

        btn_symptom = tk.Button(
            symptom_frame, text="Recommend",
            command=self.recommend_from_symptoms
        )
        btn_symptom.pack(side="left", padx=10)

        # ===================== IMAGE VERIFICATION =====================
        image_frame = tk.LabelFrame(root, text="2. Verify Medication by Image", padx=10, pady=10)
        image_frame.pack(fill="both", padx=20, pady=10)

        btn_image = tk.Button(
            image_frame, text="Select Image",
            command=self.verify_med_image
        )
        btn_image.pack(pady=10)

        # ===================== OUTPUT BOX =====================
        self.output_box = tk.Text(root, height=12, width=70)
        self.output_box.pack(padx=20, pady=20)

    # ----------------------------------------------------
    # SYMPTOM → RAG RECOMMENDATION
    # ----------------------------------------------------
    def recommend_from_symptoms(self):
        symptoms = self.symptom_entry.get().strip()
        if not symptoms:
            messagebox.showwarning("Error", "Please enter symptoms.")
            return

        agent = RecommendationAgent("data/enriched/openfda_enriched_500.json")
        results = agent.recommend(symptoms)

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "=== RECOMMENDATIONS ===\n\n")

        for r in results:
            self.output_box.insert(
                tk.END,
                f"{r['name']} | score={r['score']:.3f}\n"
                f"Category: {r['category']}\n"
                f"Symptoms: {r['symptoms']}\n\n"
            )

    # ----------------------------------------------------
    # IMAGE → YOLO DETECTION
    # ----------------------------------------------------
    def verify_med_image(self):
        path = filedialog.askopenfilename(
            title="Select medication image",
            filetypes=[("Image", "*.jpg *.jpeg *.png")]
        )

        if not path:
            return

        agent = VisionAgent("data/models/yolo_best.pt", device="cpu")
        result = agent.detect(path)

        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, "=== MEDICATION CHECK ===\n\n")

        if result is None:
            self.output_box.insert(tk.END, "No medication detected.\n")
        else:
            self.output_box.insert(
                tk.END,
                f"Detected: {result['detected_name']}\n"
                f"Confidence: {result['confidence']:.3f}\n"
            )


# -------------------------
# RUN GUI
# -------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicationApp(root)
    root.mainloop()

import os
from ultralytics import YOLO

def main():
    print("=== YOLO Training Script ===")

    # Path vers ton data.yaml (adapter si besoin)
    DATA_YAML = "data/yolo/data.yaml"

    if not os.path.exists(DATA_YAML):
        raise FileNotFoundError(f"data.yaml introuvable : {DATA_YAML}")

    # Choisir le modèle YOLO de départ (pré-entraînement)
    MODEL_NAME = "yolov8s.pt"  # petit, rapide et très bon pour commencer

    print(f"[INFO] Loading YOLO model: {MODEL_NAME}")
    model = YOLO(MODEL_NAME)

    print(f"[INFO] Starting training with dataset: {DATA_YAML}")

    model.train(
        data=DATA_YAML,
        epochs=50,
        imgsz=640,
        batch=8,
        patience=10,
        workers=4,
        device="cpu",   # mettre "cuda" si tu as une carte NVIDIA
        project="runs_yolo",
        name="drug_detector_v1"
    )

    print("=== TRAINING COMPLETED ===")
    print("Les modèles entraînés sont dans: runs_yolo/drug_detector_v1/")

if __name__ == "__main__":
    main()

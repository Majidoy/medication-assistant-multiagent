import os
from ultralytics import YOLO

class VisionAgent:
    """
    Vision Agent for medication name detection using YOLOv8.
    """

    def __init__(self, model_path="models/yolo_best.pt", device="cpu"):
        """
        Initialize the vision agent with a YOLO model.

        Args:
            model_path (str): Path to best.pt trained model
            device (str): "cpu" or "cuda"
        """
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"[VisionAgent] Model not found: {model_path}")

        print(f"[VisionAgent] Loading YOLO model from {model_path} on {device}...")

        self.model = YOLO(model_path)
        self.device = device

    def predict(self, image_path):
        """
        Predict the medication name from an input image.

        Args:
            image_path (str): path to the image file

        Returns:
            dict containing:
                - detected_name
                - confidence
                - raw results
        """

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"[VisionAgent] Image not found: {image_path}")

        print(f"[VisionAgent] Running detection on {image_path}...")

        results = self.model.predict(source=image_path, device=self.device, verbose=False)

        if len(results) == 0:
            return {"detected_name": None, "confidence": 0.0, "raw": results}

        result = results[0]

        if len(result.boxes) == 0:
            return {"detected_name": None, "confidence": 0.0, "raw": results}

        # Since your dataset has only ONE class, the predicted class is always index 0 ("drug-name")
        box = result.boxes[0]
        conf = float(box.conf[0])

        return {
            "detected_name": "drug-name",
            "confidence": conf,
            "raw": results
        }

    def save_prediction(self, image_path, out_path="vision_output.jpg"):
        """
        Saves an image with YOLO predictions drawn on it.
        """
        results = self.model.predict(source=image_path, device=self.device, save=True, save_txt=False)
        print(f"[VisionAgent] Saved annotated result to {results[0].save_dir}")
        return results
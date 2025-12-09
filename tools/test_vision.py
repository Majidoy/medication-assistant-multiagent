from agents.vision_agent import VisionAgent

agent = VisionAgent("data/models/yolo_best.pt")

result = agent.predict("DJ.jpg")
print("DETECTED:", result)
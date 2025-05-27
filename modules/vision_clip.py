
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch
import cv2
from datetime import datetime
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

def capture_and_describe():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Camera error.")
        return

    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    image_input = processor(images=image, return_tensors="pt").to(device)

    labels = ["a person", "a phone", "a ball", "a cat", "a chair", "a laptop", "a window", "a cup", "a desk", "a light"]
    text_inputs = processor(text=labels, return_tensors="pt", padding=True).to(device)

    with torch.no_grad():
        outputs = model(**image_input, text_inputs=text_inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)[0].cpu().tolist()

    label_probs = dict(zip(labels, probs))
    best_label = max(label_probs, key=label_probs.get)
    confidence = label_probs[best_label]

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"data/images/{timestamp}.jpg"
    cv2.imwrite(image_path, frame)
    with open(f"data/vision_log/{timestamp}.txt", "w") as f:
        f.write(f"{best_label} ({confidence:.2f})")
    print(f"AI sees: {best_label} with confidence {confidence:.2f}")

if __name__ == "__main__":
    capture_and_describe()

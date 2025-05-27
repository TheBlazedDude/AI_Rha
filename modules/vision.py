
import cv2
import torch
import torchvision.transforms as transforms
from PIL import Image
from datetime import datetime
import os

def capture_and_log_image(label=None):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/images/{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        if label:
            with open(f"data/vision_log/{timestamp}.txt", "w") as f:
                f.write(label)
        print(f"Captured and labeled: {label}")
    cap.release()

if __name__ == "__main__":
    capture_and_log_image("example label")

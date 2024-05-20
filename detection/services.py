import base64
from io import BytesIO
from PIL import Image
from .model import YoloV8Model

# Inicializa el modelo una vez para todo el proyecto
yolo_model = YoloV8Model('../model/yolov8l.pt')

def decode_image(image_data):
    image_data = base64.b64decode(image_data)
    return Image.open(BytesIO(image_data))

def detect_objects(image_data):
    image = decode_image(image_data)
    print("Image decoded successfully.")
    results = yolo_model.predict(image)
    print("Prediction results:", results)
    detected_products = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = box.conf[0].item()
            cls = box.cls[0].item()
            label = yolo_model.model.names[int(cls)]
            detected_products.append({
                'name': label,
                'confidence': float(conf),
                'coordinates': {'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2}
            })
            print(f"Detected: {label} (Confidence: {conf}) at coordinates: {x1}, {y1}, {x2}, {y2}")

    return detected_products
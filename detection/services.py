import base64
from io import BytesIO
from PIL import Image
from .model import YoloV8Model

# Inicializa el modelo una vez para todo el proyecto
yolo_model = YoloV8Model('../model/yolov8n.pt')

HUMAN_CLASS_IDS = [0]
DINING_TABLE = [60]
HOT_DOG = [52]
DONUT = [54]
# Diccionario de traducción de labels
LABEL_TRANSLATIONS = {
    "carrot": "Zanahoria",
    "apple": "Manzana",
    "car": "Coche",
    "orange": "Naranja",
    "banana": "Plátano"
    # Agrega aquí más traducciones según tus necesidades
}

def decode_image(image_data):
    image_data = base64.b64decode(image_data)
    return Image.open(BytesIO(image_data))

def translate_label(label):
    return LABEL_TRANSLATIONS.get(label, label)

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
            if int(cls) not in HUMAN_CLASS_IDS and int(cls) not in DINING_TABLE and int(cls) not in DONUT and int(cls) not in HOT_DOG:  # Filtrar detecciones de humanos
                translated_label = translate_label(label)
                width = x2 - x1
                height = y2 - y1
                centerX = (x1 + x2) / 2
                centerY = (y1 + y2) / 2
                radius = max(width, height) / 2

                detected_products.append({
                    'name': translated_label,
                    'confidence': float(conf),
                    'coordinates': {
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2,
                        'width': width,
                        'height': height,
                        'centerX': (x1 + x2) / 2,
                        'centerY': (y1 + y2) / 2,
                        'radius': max(width, height) / 2
                    }
                })
                print(f"Detected: {translated_label} (Confidence: {conf}) at coordinates: {x1}, {y1}, {x2}, {y2}, with center at {centerX}, {centerY} and radius {radius}")

    return detected_products
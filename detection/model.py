from ultralytics import YOLO

class YoloV8Model:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    def predict(self, image):
        results = self.model(image)
        return results

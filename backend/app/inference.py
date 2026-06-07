import time
import numpy as np
from ultralytics import YOLO

from app.config import MODEL_PATH, CONF_THRESHOLD, IOU_THRESHOLD, IMAGE_SIZE


class DefectSegmenter:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model weights not found at {MODEL_PATH}. "
                "Please place trained YOLO segmentation weights as weights/best.pt"
            )

        self.model = YOLO(str(MODEL_PATH))

    def predict(self, image: np.ndarray):
        start_time = time.time()

        results = self.model.predict(
            source=image,
            imgsz=IMAGE_SIZE,
            conf=CONF_THRESHOLD,
            iou=IOU_THRESHOLD,
            verbose=False
        )

        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        return results[0], elapsed_ms
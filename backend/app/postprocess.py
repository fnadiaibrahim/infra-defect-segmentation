import base64
import cv2
import numpy as np


MASK_COLORS = {
    0: np.array([255, 0, 0], dtype=np.uint8),      # crack - blue in BGR
    1: np.array([0, 255, 255], dtype=np.uint8),    # spalling - yellow in BGR
}


def image_to_base64(image: np.ndarray) -> str:
    success, buffer = cv2.imencode(".jpg", image)

    if not success:
        raise ValueError("Failed to encode image.")

    return base64.b64encode(buffer).decode("utf-8")


def create_overlay(image: np.ndarray, result):
    overlay = image.copy()
    detections = []

    if result.masks is None or result.boxes is None:
        return overlay, detections

    masks = result.masks.data.cpu().numpy()
    boxes = result.boxes

    for idx, mask in enumerate(masks):
        class_id = int(boxes.cls[idx].item())
        confidence = float(boxes.conf[idx].item())

        resized_mask = cv2.resize(
            mask,
            (image.shape[1], image.shape[0]),
            interpolation=cv2.INTER_NEAREST
        )

        binary_mask = resized_mask > 0.5
        color = MASK_COLORS.get(class_id, np.array([255, 255, 255], dtype=np.uint8))

        overlay[binary_mask] = (
            overlay[binary_mask] * 0.55 + color * 0.45
        )

        area_percentage = round(
            binary_mask.sum() / (image.shape[0] * image.shape[1]) * 100,
            2
        )

        detections.append({
            "class_id": class_id,
            "confidence": round(confidence, 4),
            "area_percentage": area_percentage
        })

    return overlay.astype(np.uint8), detections
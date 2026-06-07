import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.config import CLASS_NAMES
from app.inference import DefectSegmenter
from app.postprocess import create_overlay, image_to_base64


app = FastAPI(
    title="Infrastructure Defect Segmentation API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


segmenter = None


@app.on_event("startup")
def load_model():
    global segmenter

    try:
        segmenter = DefectSegmenter()
        print("Model loaded successfully.")
    except FileNotFoundError as error:
        segmenter = None
        print(f"Model loading skipped: {error}")


@app.get("/")
def root():
    frontend_index = Path(__file__).resolve().parents[2] / "frontend" / "dist" / "index.html"

    if frontend_index.exists():
        return FileResponse(frontend_index)

    return {
        "message": "Welcome to the Infrastructure Defect Segmentation API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": segmenter is not None
    }


@app.get("/classes")
def get_classes():
    return CLASS_NAMES


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if segmenter is None:
        return {
            "error": "Model is not loaded. Please add trained weights at weights/best.pt"
        }

    if file.content_type not in ["image/jpeg", "image/png"]:
        return {
            "error": "Invalid file type. Please upload JPEG or PNG image."
        }

    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if image is None:
        return {
            "error": "Invalid image file."
        }

    result, elapsed_ms = segmenter.predict(image)
    overlay, detections = create_overlay(image, result)

    for detection in detections:
        detection["class_name"] = CLASS_NAMES.get(
            detection["class_id"],
            "unknown"
        )

    return {
        "filename": file.filename,
        "processing_time_ms": elapsed_ms,
        "detections": detections,
        "original_image": image_to_base64(image),
        "overlay_image": image_to_base64(overlay)
    }

FRONTEND_DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"

if FRONTEND_DIST.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="assets"
    )

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        index_file = FRONTEND_DIST / "index.html"
        return FileResponse(index_file)
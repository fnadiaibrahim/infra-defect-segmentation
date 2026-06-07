---
title: Infrastructure Defect Segmentation
emoji: 🏗️
colorFrom: blue
colorTo: yellow
sdk: docker
app_port: 7860
pinned: false
---

# Infrastructure Defect Segmentation

An end-to-end computer vision prototype for detecting and segmenting visible infrastructure surface defects from uploaded images.

This project uses a fine-tuned YOLOv8 instance segmentation model with a FastAPI backend and React frontend. The system detects concrete surface defects, generates segmentation overlays, and returns prediction metadata such as class label, confidence score, affected area percentage, and processing time.

## Live Demo

The deployed application is available at:

https://huggingface.co/spaces/fnadiaibrahim/infra-defect-segmentation

## Demo Overview

The current prototype supports two defect classes:

* Crack
* Spalling

The application workflow is:

```text
Upload image → Run segmentation → View overlay → Review prediction summary
```

## Demo Screenshots

### API Documentation

The FastAPI backend provides interactive Swagger documentation for all available endpoints.

![API Documentation](docs/screenshots/api_docs.png)

### Model Health Check

The `/health` endpoint confirms that the backend is running and the trained model is loaded successfully.

![Model Loaded Health Check](docs/screenshots/health_model_loaded.png)

### Spalling Prediction

Example prediction showing spalling segmentation overlay and prediction metadata.

![Spalling Prediction Demo](docs/screenshots/spalling_prediction_demo.png)

### Crack Prediction

Example prediction showing crack segmentation overlay and prediction metadata.

![Crack Prediction Demo](docs/screenshots/crack_prediction_demo.png)

## Key Features

* Fine-tuned YOLOv8 segmentation model
* Pixel-level defect mask overlay
* React-based image upload interface
* FastAPI inference backend
* Class label and confidence score output
* Affected area percentage estimation
* Processing time reporting
* API documentation through FastAPI Swagger UI

## Project Structure

```text
infra-defect-segmentation/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── inference.py
│   │   └── postprocess.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   └── package.json
├── training/
│   ├── dataset.yaml
│   ├── train.py
│   └── evaluate.py
├── docs/
│   ├── MODEL_CARD.md
│   ├── ARCHITECTURE.md
│   └── DECISIONS.md
├── weights/
│   └── best.pt
└── README.md
```

## Model Summary

The model is based on YOLOv8n-seg and was fine-tuned for infrastructure defect segmentation.

| Item         | Description           |
| ------------ | --------------------- |
| Base model   | YOLOv8n-seg           |
| Task         | Instance segmentation |
| Classes      | Crack, Spalling       |
| Input size   | 640 x 640             |
| Framework    | Ultralytics YOLO      |
| Final weight | `weights/best.pt`     |

## Dataset

The model was trained using a public Concrete Crack & Spalling segmentation dataset from Roboflow Universe.

Dataset classes:

```text
0: crack
1: spalling
```

The dataset was selected because it provides segmentation masks for two relevant infrastructure defect classes and can be exported directly in YOLOv8 segmentation format.

## Training

Training was performed using Google Colab with GPU acceleration.

Training configuration:

| Parameter    |            Value |
| ------------ | ---------------: |
| Epochs       |               50 |
| Image size   |              640 |
| Batch size   |                8 |
| Patience     |               10 |
| Base weights | `yolov8n-seg.pt` |
| Final model  |        `best.pt` |

## Validation Results

Validation was performed on 300 images containing 361 defect instances.

| Class    | Images | Instances | Box P | Box R | Box mAP50 | Box mAP50-95 | Mask P | Mask R | Mask mAP50 | Mask mAP50-95 |
| -------- | -----: | --------: | ----: | ----: | --------: | -----------: | -----: | -----: | ---------: | ------------: |
| All      |    300 |       361 | 0.936 | 0.894 |     0.895 |        0.769 |  0.936 |  0.894 |      0.891 |         0.601 |
| Crack    |    223 |       255 | 0.935 | 0.863 |     0.865 |        0.733 |  0.935 |  0.863 |      0.857 |         0.422 |
| Spalling |     78 |       106 | 0.937 | 0.925 |     0.925 |        0.805 |  0.937 |  0.925 |      0.925 |         0.779 |

## Result Interpretation

The model achieved strong overall segmentation performance with an overall mask mAP50 of 0.891.

Spalling achieved stronger mask mAP50-95 than crack because spalling defects are usually larger and have clearer visual boundaries.

Crack segmentation is more challenging because cracks are often thin, irregular, and sensitive to small pixel-level boundary errors. This explains the lower crack mask mAP50-95 score.

## Backend API

The backend is implemented using FastAPI.

### Endpoints

| Endpoint   | Method | Description                       |
| ---------- | ------ | --------------------------------- |
| `/`        | GET    | Root API information              |
| `/health`  | GET    | Backend and model loading status  |
| `/classes` | GET    | Supported class labels            |
| `/predict` | POST   | Upload image and run segmentation |

### Example Prediction Response

```json
{
  "filename": "sample.jpg",
  "processing_time_ms": 340.05,
  "detections": [
    {
      "class_id": 1,
      "confidence": 0.9432,
      "area_percentage": 11.07,
      "class_name": "spalling"
    }
  ],
  "original_image": "base64 encoded image",
  "overlay_image": "base64 encoded image"
}
```

## Running the Backend

From the project root:

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Check backend health:

```text
http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Running the Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev -- --host 0.0.0.0
```

Frontend will run on:

```text
http://localhost:5173
```

## Frontend Environment Variable

Create a `.env` file inside the `frontend/` directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

For GitHub Codespaces, use the forwarded backend URL instead:

```env
VITE_API_BASE_URL=https://your-codespace-8000.app.github.dev
```

When running in GitHub Codespaces, make sure both ports are set to Public visibility:

| Port | Purpose         |
| ---- | --------------- |
| 8000 | FastAPI backend |
| 5173 | React frontend  |

## Training Script

Training files are located in:

```text
training/
```

Example training command:

```bash
python training/train.py
```

The training script uses YOLOv8n-seg as the base model and fine-tunes it using the configured dataset YAML.

## Technical Decisions

Detailed engineering decisions and trade-offs are documented in:

```text
docs/DECISIONS.md
```

Architecture documentation is available in:

```text
docs/ARCHITECTURE.md
```

Model details are available in:

```text
docs/MODEL_CARD.md
```

## Known Limitations

* The current model supports only crack and spalling.
* Corrosion and structural deformation are not included in the current training data.
* Very thin cracks may be under-segmented.
* Shadows, stains, concrete joints, or surface texture may cause false positives.
* The validation set comes from the dataset split and is not a fully independent field inspection dataset.
* The prototype is not intended for safety-critical structural assessment without expert review.

## Future Improvements

* Add corrosion and structural deformation classes.
* Collect and annotate more diverse field inspection images.
* Evaluate using external real-world inspection images.
* Train larger segmentation models such as YOLOv8s-seg or YOLOv8m-seg.
* Export the model to ONNX or TensorRT for faster inference.
* Add confidence threshold control in the frontend.
* Add downloadable PDF/CSV inspection reports.
* Add Docker deployment.
* Add model versioning, logging, and monitoring.

## Safety Note

This project is a technical prototype for computer vision assessment purposes. It should not be used as the sole basis for real-world structural safety decisions. Any detected defects should be reviewed by qualified inspection or engineering professionals.

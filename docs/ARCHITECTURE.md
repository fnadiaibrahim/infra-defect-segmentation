# System Architecture

## Overview

This project is an end-to-end infrastructure defect segmentation prototype. It allows a user to upload an image through a React frontend, sends the image to a FastAPI backend, runs inference using a fine-tuned YOLOv8 segmentation model, and returns the detected defect masks as an overlay image with prediction metadata.

The current implementation supports two defect classes:

- Crack
- Spalling

## High-Level Architecture

```text
User
 │
 ▼
React Frontend
 │
 │  Upload image as multipart/form-data
 ▼
FastAPI Backend
 │
 │  Decode image
 │  Run YOLOv8 segmentation inference
 │  Generate mask overlay
 │  Calculate affected area percentage
 ▼
JSON Response
 │
 │  class label
 │  confidence score
 │  affected area %
 │  processing time
 │  original image base64
 │  overlay image base64
 ▼
Frontend Result View
```

## Component Design

### Frontend
The frontend is built using React. It handles image upload, preview, API request submission, and result visualization. The interface is intentionally simple so the reviewer can test the model quickly without needing technical setup.

### Backend
The backend is built using FastAPI. It exposes REST endpoints for health check, class metadata, and prediction. The backend receives the uploaded image, validates the file type, converts it into an image array, runs YOLOv8 segmentation inference, and returns the result as JSON.

### Model Layer
The model layer uses a fine-tuned YOLOv8 segmentation model. YOLOv8 was selected because it supports instance segmentation, has fast inference speed, and is lightweight enough for deployment on free-tier infrastructure.

## Data Pipeline

The dataset contains infrastructure defect images focused on crack and spalling classes. Images were prepared in YOLO segmentation format with polygon mask annotations. The dataset was split into training, validation, and testing sets to avoid evaluating on images seen during training.

Preprocessing steps include:
- resizing images to the model input size
- normalizing image values
- converting annotations into YOLO segmentation format
- applying augmentation during training

Augmentation helps improve robustness against different lighting conditions, surface textures, camera angles, and defect sizes.

## Training Pipeline

The training pipeline fine-tunes a pretrained YOLOv8 segmentation model on the defect dataset. Transfer learning was used because the dataset is relatively small and training from scratch would require more data and compute.

Training steps:
1. Load pretrained YOLOv8 segmentation weights.
2. Prepare dataset configuration file.
3. Train on crack and spalling segmentation classes.
4. Validate using a held-out validation set.
5. Save the best-performing checkpoint.
6. Evaluate the final model on a test set.

The selected checkpoint is used by the FastAPI inference service.

## Model Selection

YOLOv8 segmentation was selected over U-Net and Mask R-CNN.

| Model | Strength | Limitation |
|---|---|---|
| YOLOv8 Segmentation | Fast inference, easy deployment, supports masks and labels | May produce less refined masks for very thin cracks |
| U-Net | Strong pixel-level segmentation baseline | Requires more custom post-processing for class labels and deployment |
| Mask R-CNN | Strong instance segmentation framework | Heavier and slower for free-tier deployment |

YOLOv8 was chosen because the assessment values an end-to-end working prototype, deployment, inference speed, and explainable trade-offs.

## Post-processing

After inference, the backend converts model predictions into visual outputs. Segmentation masks are overlaid on the original image. The system also calculates affected area percentage by comparing predicted mask pixels against the full image area.

Returned metadata includes:
- defect class
- confidence score
- affected area percentage
- processing time
- original image
- overlay image

## Scalability and Production Readiness

The current system is suitable for prototype evaluation and small-scale testing. For production use, several improvements would be needed:

| Concern | Current Prototype | Production Improvement |
|---|---|---|
| Inference speed | Single image request | Batch processing or GPU-backed inference |
| Deployment | Free-tier public app | Containerized deployment with autoscaling |
| Storage | No permanent image storage | Object storage such as S3/GCS |
| Monitoring | Manual testing | Logging, latency tracking, error monitoring |
| Model updates | Manual checkpoint replacement | Model registry and versioning |
| Security | Basic upload handling | File scanning, size limits, authentication |

## Bottlenecks

The main bottlenecks are model inference latency, free-tier resource limits, and image processing overhead. Large images may increase processing time because resizing, decoding, inference, and base64 conversion all happen during request time.

For higher throughput, the backend can be optimized by:
- running inference on GPU
- resizing images before inference
- using asynchronous job queues
- caching repeated requests
- serving the model using TorchScript or ONNX Runtime
- separating frontend and backend deployments

## Limitations

The current model supports only crack and spalling classes. It may struggle with:
- very thin cracks
- poor lighting
- blurry images
- unseen defect types
- surfaces that visually resemble cracks or spalling

Future work would include adding more defect classes such as corrosion and deformation, increasing dataset diversity, improving annotation quality, and benchmarking against other segmentation architectures.
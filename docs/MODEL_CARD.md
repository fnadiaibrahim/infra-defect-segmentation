# Model Card: Infrastructure Defect Segmentation

## Model Overview

This prototype uses a fine-tuned YOLOv8n-seg instance segmentation model to detect and segment visible infrastructure surface defects from uploaded images.

The implemented defect classes are:

- Crack
- Spalling

The model produces:

- defect class label
- confidence score
- pixel-level segmentation mask
- affected area percentage
- overlay image for visual inspection

## Base Model

- Architecture: YOLOv8n-seg
- Task: Instance segmentation
- Input size: 640 x 640
- Framework: Ultralytics YOLO
- Model size: approximately 3.26M parameters

## Dataset

Dataset used:

- Concrete Crack & Spalling dataset from Roboflow Universe
- Export format: YOLOv8 segmentation
- Classes:
  - `0: crack`
  - `1: spalling`

The dataset was selected because it provides segmentation annotations for two relevant infrastructure defect classes and is practical for fast fine-tuning within the assessment time constraint.

## Training Setup

Training was performed using Google Colab with GPU acceleration.

Training configuration:

- Epochs: 50
- Image size: 640
- Batch size: 8
- Early stopping patience: 10
- Base weights: `yolov8n-seg.pt`
- Final model: `weights/best.pt`

## Validation Results

Validation was performed on the validation split.

| Class | Images | Instances | Box P | Box R | Box mAP50 | Box mAP50-95 | Mask P | Mask R | Mask mAP50 | Mask mAP50-95 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| All | 300 | 361 | 0.936 | 0.894 | 0.895 | 0.769 | 0.936 | 0.894 | 0.891 | 0.601 |
| Crack | 223 | 255 | 0.935 | 0.863 | 0.865 | 0.733 | 0.935 | 0.863 | 0.857 | 0.422 |
| Spalling | 78 | 106 | 0.937 | 0.925 | 0.925 | 0.805 | 0.937 | 0.925 | 0.925 | 0.779 |

## Interpretation

The model achieved strong overall segmentation performance with an overall mask mAP50 of 0.891.

Spalling achieved better mask mAP50-95 than crack. This is expected because spalling regions are usually larger, more visually distinct, and have clearer boundaries.

Crack segmentation is more challenging because cracks are often thin, irregular, discontinuous, and sensitive to small pixel-level boundary errors. This explains the lower crack mask mAP50-95 score.

## Inference Output

The API returns:

```json
{
  "filename": "sample.jpg",
  "processing_time_ms": 340.05,
  "detections": [
    {
      "class_id": 1,
      "class_name": "spalling",
      "confidence": 0.9432,
      "area_percentage": 11.07
    }
  ],
  "original_image": "base64 encoded image",
  "overlay_image": "base64 encoded image"
}
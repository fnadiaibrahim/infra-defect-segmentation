# Engineering Decisions and Trade-offs

## 1. Project Scope

The assessment asks for an infrastructure defect segmentation prototype with a deployed frontend and backend. Given the limited assessment timeline, I focused on building a complete end-to-end system instead of attempting to support many defect categories with weak or inconsistent data.

The implemented prototype supports:

- Crack segmentation
- Spalling segmentation

Corrosion and structural deformation are treated as future extensions.

## 2. Dataset Selection

I selected a public Roboflow Universe dataset for concrete crack and spalling segmentation.

Reasons:

- It provides segmentation annotations, not only bounding boxes.
- It supports two relevant infrastructure defect classes.
- It is available in YOLOv8 segmentation format.
- It is suitable for rapid fine-tuning and validation within the assessment timeline.
- It allows a working end-to-end prototype to be completed with measurable results.

Alternative considered:

- Crack-only datasets with larger image counts.

I did not choose a crack-only dataset as the main dataset because the assessment benefits from demonstrating multi-class segmentation. A two-class crack and spalling model is more representative of infrastructure defect inspection than a crack-only model.

## 3. Model Selection

I selected `YOLOv8n-seg` as the base model.

Reasons:

- It supports instance segmentation.
- It is lightweight and fast.
- It can be fine-tuned quickly using Google Colab.
- The trained weight file is small enough to include in the repository.
- It is suitable for a prototype backend API.

Larger models such as YOLOv8s-seg or YOLOv8m-seg may improve mask quality but require more compute and increase inference cost.

## 4. Training Strategy

The model was fine-tuned for 50 epochs using the Roboflow concrete crack and spalling dataset.

Key training choices:

- Image size: 640
- Batch size: 8
- Epochs: 50
- Patience: 10
- Base model: `yolov8n-seg.pt`

I used a quick training test first to confirm that the dataset format was valid before running the full 50-epoch training.

This reduced the risk of wasting GPU time on dataset path or label format errors.

## 5. Evaluation Strategy

The model was evaluated using the validation split from the dataset.

Main metrics recorded:

- Box precision
- Box recall
- Box mAP50
- Box mAP50-95
- Mask precision
- Mask recall
- Mask mAP50
- Mask mAP50-95

The most important metric for this task is mask performance because the assessment focuses on pixel-level defect segmentation.

The final model achieved:

- Overall mask precision: 0.936
- Overall mask recall: 0.894
- Overall mask mAP50: 0.891
- Overall mask mAP50-95: 0.601

## 6. Result Interpretation

Spalling achieved stronger mask mAP50-95 than crack.

This is expected because spalling regions are usually larger, more visible, and have clearer boundaries.

Crack segmentation is more difficult because cracks are:

- thin
- irregular
- discontinuous
- sensitive to small boundary errors
- sometimes visually similar to shadows or surface joints

Therefore, the lower crack mask mAP50-95 is acceptable for a first prototype and highlights an important area for future improvement.

## 7. Backend Design

FastAPI was selected for the backend.

Reasons:

- Simple and fast API development.
- Automatic Swagger documentation.
- Good support for file uploads.
- Easy integration with Python ML inference.
- Suitable for prototype deployment.

The backend exposes:

- `/health`
- `/classes`
- `/predict`

The `/predict` endpoint accepts an uploaded image and returns detection metadata and base64-encoded images.

## 8. Frontend Design

React with Vite was selected for the frontend.

Reasons:

- The assessment requires a JavaScript frontend.
- Vite provides a fast setup.
- React makes it easy to manage upload state, loading state, errors, and result display.
- The frontend provides a simple user workflow suitable for demo and evaluation.

The frontend shows:

- original uploaded image
- segmentation overlay
- class name
- confidence score
- affected area percentage
- processing time

## 9. Post-processing Design

The model output is post-processed by:

- resizing masks to the original image size
- applying class-specific colors
- blending masks with the original image
- calculating affected area percentage
- encoding images as base64 strings

Affected area percentage is calculated as:

```text
defect mask pixels / total image pixels * 100
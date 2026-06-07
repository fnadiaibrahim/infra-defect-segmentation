# Submission Summary

## Project Title

Infrastructure Defect Segmentation

## Overview

This project is an end-to-end computer vision prototype for detecting and segmenting visible infrastructure surface defects from uploaded images.

The system uses a fine-tuned YOLOv8 instance segmentation model with a FastAPI backend and React frontend. It returns pixel-level segmentation overlays, class labels, confidence scores, affected area percentage, and processing time.

## Repository

GitHub Repository:

```text
https://github.com/fnadiaibrahim/infra-defect-segmentation
```

## Deployed Application

Deployed Application URL:

```text
To be added after deployment.
```

## Walkthrough Video

Screen Recording Link:

```text
To be added after recording.
```

## Implemented Features

* React frontend for image upload and result display
* FastAPI backend for model inference
* Fine-tuned YOLOv8n-seg segmentation model
* Pixel-level defect segmentation overlay
* Defect class prediction
* Confidence score output
* Affected area percentage calculation
* Processing time reporting
* FastAPI Swagger documentation

## Supported Defect Classes

* Crack
* Spalling

## Model Training

The model was fine-tuned for 50 epochs using YOLOv8n-seg on a concrete crack and spalling segmentation dataset exported in YOLOv8 segmentation format.

Training configuration:

| Parameter   |             Value |
| ----------- | ----------------: |
| Base model  |       YOLOv8n-seg |
| Epochs      |                50 |
| Image size  |               640 |
| Batch size  |                 8 |
| Patience    |                10 |
| Final model | `weights/best.pt` |

## Validation Result Summary

Validation was performed on 300 images containing 361 defect instances.

| Metric                 | Value |
| ---------------------- | ----: |
| Overall mask precision | 0.936 |
| Overall mask recall    | 0.894 |
| Overall mask mAP50     | 0.891 |
| Overall mask mAP50-95  | 0.601 |

Class-level summary:

| Class    | Mask Precision | Mask Recall | Mask mAP50 | Mask mAP50-95 |
| -------- | -------------: | ----------: | ---------: | ------------: |
| Crack    |          0.935 |       0.863 |      0.857 |         0.422 |
| Spalling |          0.937 |       0.925 |      0.925 |         0.779 |

## Demo Evidence

Screenshots are available in:

```text
docs/screenshots/
```

Included screenshots:

* API documentation
* Health check showing model loaded
* Crack prediction demo
* Spalling prediction demo

## Main Documentation

* `README.md`
* `docs/ARCHITECTURE.md`
* `docs/DECISIONS.md`
* `docs/MODEL_CARD.md`

## Known Limitations

* The current model supports only crack and spalling.
* Corrosion and structural deformation are not included in the current training data.
* Very thin cracks may be under-segmented.
* Shadows, stains, surface joints, and concrete texture may cause false positives.
* The validation set comes from the dataset split and is not a fully independent field inspection dataset.
* The prototype is not intended for safety-critical structural assessment without expert review.

## Future Improvements

* Add corrosion and structural deformation classes.
* Collect and annotate more diverse field inspection data.
* Evaluate on external real-world inspection images.
* Train larger segmentation models such as YOLOv8s-seg or YOLOv8m-seg.
* Export model to ONNX or TensorRT for faster inference.
* Add confidence threshold control in the frontend.
* Add downloadable inspection reports.
* Add Docker deployment.
* Add logging, monitoring, and model versioning.

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
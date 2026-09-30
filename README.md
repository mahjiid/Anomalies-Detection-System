# Road Anomaly Detection System

Computer vision project for detecting road-surface anomalies using a custom YOLOv3 object-detection workflow.

## Project Overview

This project was developed as part of my Computer Engineering work on road anomaly detection. The workflow combines dataset preparation, image annotation, YOLO-based model training, evaluation, and deployment-oriented experimentation for road-scene monitoring.

The repository currently contains the original Google Colab notebooks used to configure and train the model with the Darknet YOLOv3 framework.

## What This Project Demonstrates

- Computer vision dataset preparation
- Object-detection training workflow
- Ground-truth annotation for road-scene imagery
- Bounding-box based labeling for supervised learning
- YOLOv3 / Darknet model training
- Google Colab GPU training
- OpenCV-enabled Darknet build
- CUDA and cuDNN acceleration
- Model-training configuration and experimentation
- Understanding of the relationship between annotation quality and detection performance

## Training Stack

| Area | Tools / Technologies |
| --- | --- |
| Object Detection | YOLOv3 |
| Framework | Darknet |
| Notebook Environment | Google Colab |
| GPU | NVIDIA Tesla T4 |
| Acceleration | CUDA, cuDNN |
| Computer Vision | OpenCV |
| Development | Python / Jupyter Notebook |
| Dataset Storage | Google Drive |

## Repository Files

### `Train_YoloV3_.ipynb`

Main model-training notebook. It includes:

1. GPU availability verification
2. Google Drive mounting
3. Darknet repository setup
4. Darknet compilation
5. GPU, OpenCV, and cuDNN enablement
6. Custom YOLO training workflow

### `Setup.ipynb`

Supporting environment and project setup notebook.

## Annotation Experience

The road-anomaly dataset used for this project required labeled image data suitable for supervised object detection.

This work provides practical experience relevant to AI data annotation roles, including:

- identifying target objects/anomalies in images
- creating ground-truth labels
- bounding-box annotation
- maintaining consistent class definitions
- preparing labels for YOLO training
- reviewing training data for labeling errors
- understanding how label quality affects false positives, false negatives, and model performance

> The original annotation platform, class definitions, sample annotations, and exported label examples will be added to this repository as the historical project materials are consolidated.

## Computer Vision Annotation Portfolio Relevance

This project supports work in:

- Computer Vision Data Annotation
- Image Annotation
- Video Annotation
- Object Detection
- Dataset Quality Assurance
- AI Data Training
- Annotation Review
- Human-in-the-loop AI workflows

## Planned Documentation Improvements

The repository is being expanded into a complete project case study. Upcoming additions include:

- [ ] Original annotation-tool documentation
- [ ] Annotation screenshots
- [ ] Dataset class list
- [ ] Sample YOLO label files
- [ ] Dataset structure
- [ ] Train/validation split documentation
- [ ] Example detections
- [ ] Evaluation metrics
- [ ] Model architecture/workflow diagram
- [ ] Embedded-system deployment notes
- [ ] Annotation QA guidelines

## Current Portfolio Expansion

I am extending this work into a dedicated computer-vision annotation portfolio covering:

- CVAT
- Bounding boxes
- Polygon annotation
- Semantic / instance segmentation
- Video object tracking
- Dataset QA and annotation review
- YOLO-format dataset export

## Author

**Abdulmajeed Olasunkanmi Abdulrasheed**  
Computer Engineer | Computer Vision | AI Data Annotation | Embedded Systems

GitHub: [@mahjiid](https://github.com/mahjiid)

---

If you are reviewing this repository for an AI-data or computer-vision role, the project demonstrates experience beyond basic labeling: the annotated data was used as part of an end-to-end object-detection training workflow.

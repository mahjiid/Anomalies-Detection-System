# Road Anomaly Detection System

Computer vision project for detecting road-surface anomalies using a custom annotation and object-detection workflow.

## Project Overview

This project was developed as part of my Computer Engineering work on road anomaly detection. It combines road-image dataset preparation, manual object annotation, model training, evaluation, and deployment-oriented experimentation.

The original dataset was managed and annotated in **Edge Impulse**, while the repository also contains the original Google Colab notebooks used to configure and train a **YOLOv3 / Darknet** object-detection workflow.


## Annotation Portfolio

For recruiter-facing evidence of annotation methodology and QA, see:

- [Annotation Portfolio](ANNOTATION_PORTFOLIO.md)
- [Video Annotation Method](docs/video_annotation_method.md)
- [Annotation QA Checklist](docs/annotation_qa_checklist.md)
- [Practice Video Action Annotation Sample](samples/video_action_annotation_practice.csv)

## Verified Edge Impulse Dataset

The original Edge Impulse export for **Pothole and Bumps** contains:

| Dataset detail | Verified value |
| --- | ---: |
| Total exported images | 711 |
| Training images | 575 |
| Testing images | 136 |
| Images with bounding boxes | 711 |
| Total bounding boxes | 795 |
| Pothole boxes | 337 |
| Bumps boxes | 456 |
| Person boxes | 1 |
| Car boxes | 1 |
| Maximum boxes in one image | 4 |

The exported metadata is stored in Edge Impulse's `info.labels` format and contains per-image bounding-box coordinates and class labels.

> Note: the Edge Impulse generated block-output view showed 572 training windows and 133 testing windows for the configured impulse. The raw project export contains 575 training files and 136 testing files; these represent different stages of the Edge Impulse pipeline.

## What This Project Demonstrates

- Computer vision dataset preparation
- Manual bounding-box annotation
- Ground-truth label creation
- Multi-object annotation in road imagery
- Annotation class consistency
- Training/test dataset management
- Object-detection model training
- Edge Impulse workflow experience
- YOLOv3 / Darknet training
- Google Colab GPU training
- OpenCV-enabled Darknet build
- CUDA and cuDNN acceleration
- Understanding of how annotation quality affects model performance

## Annotation Classes

The exported dataset primarily targets two road-anomaly classes:

- **Pothole**
- **Bumps**

The export also contains isolated annotations for `person` and `car`, which are retained in the source metadata and should be reviewed as part of dataset QA.

## Training & Annotation Stack

| Area | Tools / Technologies |
| --- | --- |
| Annotation / Dataset Management | Edge Impulse |
| Annotation Type | Bounding boxes |
| Main Classes | Pothole, Bumps |
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

## Annotation Workflow

The original Edge Impulse workflow involved:

1. Collecting and importing road-scene images
2. Separating data into training and testing categories
3. Identifying road anomalies in each image
4. Drawing object-detection bounding boxes
5. Assigning class labels such as `Pothole` and `Bumps`
6. Reviewing images containing multiple anomalies
7. Exporting labeled data for model development
8. Using labeled data in object-detection training and testing

This demonstrates practical experience relevant to professional AI annotation work, including:

- image annotation
- bounding-box placement
- object/class identification
- dataset QA
- label consistency
- train/test dataset preparation
- annotation metadata handling
- understanding false positives and false negatives
- connecting annotation quality to downstream model behavior

## Edge Impulse Model Artifacts

The Edge Impulse project produced downloadable object-detection artifacts including:

- TensorFlow Lite (float32)
- TensorFlow Lite (int8 quantized)
- TensorFlow SavedModel
- Keras H5 model

This makes the project an end-to-end embedded/computer-vision workflow rather than annotation-only work.

## LabelImg → Label Studio utility

I added a small, validated migration utility for converting **LabelImg Pascal VOC XML** bounding boxes into Label Studio JSON tasks.

- [Converter](tools/labelimg_voc_to_labelstudio.py)
- [Workflow documentation](docs/labelimg_to_labelstudio.md)
- [Sample LabelImg XML](samples/labelimg_example.xml)

This reflects hands-on LabelImg experience and demonstrates annotation-format conversion, bounding-box validation, and dataset migration.

## Computer Vision Annotation Portfolio Relevance

This project provides evidence for roles involving:

- Computer Vision Data Annotation
- Image Annotation
- Object Detection Annotation
- Dataset Quality Assurance
- AI Data Training
- Annotation Review
- Human-in-the-loop AI workflows
- Embedded AI dataset preparation

## Portfolio Expansion

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

If you are reviewing this repository for an AI-data or computer-vision role, this project demonstrates experience beyond basic labeling: annotated data was used as part of an end-to-end computer-vision model training workflow.

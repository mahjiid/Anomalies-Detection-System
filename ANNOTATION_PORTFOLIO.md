# Annotation Portfolio

This repository contains evidence of my computer-vision annotation, dataset-quality, and model-training work, plus a transparent practice framework for video annotation.

## 1. Real project evidence: Road Anomaly Detection

My final-year computer-engineering project used a labeled road-image dataset managed in Edge Impulse and an object-detection workflow using YOLOv3/Darknet.

Verified exported dataset summary:

- 711 labeled images
- 795 bounding boxes
- 337 pothole boxes
- 456 bump boxes
- Training/test split management
- Multi-object image review
- Annotation metadata review and class-consistency checks

This work required identifying visual events/objects, applying consistent labels, reviewing edge cases, and understanding how annotation quality affects model training.

## 2. Transferable video-annotation skills

The same quality principles apply to action-based video annotation:

- identify the exact observable action
- mark precise start/end boundaries
- distinguish action from outcome
- identify objects and interactions
- compare two clips against the same instruction
- flag ambiguity rather than guessing
- apply the same rubric consistently
- document decisions clearly
- perform a second-pass QA review

## 3. Practice video-annotation schema

The files in `samples/` are clearly labeled portfolio/practice artifacts. They demonstrate the structure I use for timeline-based human/robot action annotation and are not presented as paid client work.

Recommended fields:

- clip_id
- start_time
- end_time
- actor
- action
- object
- interaction
- end_state
- instruction_alignment
- confidence
- reviewer_note

## 4. Quality-control approach

My QA process is documented in `docs/annotation_qa_checklist.md`. It focuses on boundary accuracy, label consistency, evidence-based descriptions, and repeatable decisions.

## 5. Relevant domain background

I also work in semiconductor manufacturing/process engineering, where precision, inspection, defect identification, process compliance, and repeatable QA decisions are part of day-to-day work. This gives me a strong foundation for robotics and human-activity evaluation tasks.

## Annotation tools used

- **LabelImg** — bounding-box image annotation
- **Edge Impulse** — dataset management and object-detection labeling

## Tools and technologies

Edge Impulse · YOLOv3 · Darknet · OpenCV · Python · Jupyter · Computer Vision · Bounding Boxes · Dataset QA · AI Training Data

## Integrity note

This portfolio separates verified project work from practice examples. I do not claim commercial video-annotation experience that I have not completed.

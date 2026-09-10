---
title: LabelSetu CV Service
emoji: 🏷️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# LabelSetu CV Service

FastAPI microservice that runs PaddleOCR on uploaded product-label images and
returns bounding-box regions with extracted text.

**Entry point:** `cv_service.app:app`  
**Port:** 7860 (Hugging Face Spaces default)

## API

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check — does NOT load OCR model |
| POST | `/ocr` | Upload an image (`multipart/form-data`, field `file`); returns JSON with `image_width`, `image_height`, `regions[]` |

# LabelSetu Computer Vision + OCR Service

This is the standalone Part 2 service. It performs only:

```text
image -> OCR -> independent text regions
```

It does **not** identify MRP, net quantity, manufacturer, country of origin,
consumer care, or any other legal field. It does **not** run Legal Metrology
rules or compliance checks. Part 3 can consume the region output and decide
what each text region means.

## API contract

### `GET /health`

Returns:

```json
{
  "status": "ok",
  "service": "cv_service"
}
```

### `POST /ocr`

Send an image as multipart form data using the field name `file`:

```bash
curl -X POST http://localhost:8000/ocr \
  -F "file=@./label-photo.jpg"
```

The response always reports the dimensions of the **original uploaded image**.
Every bounding box also uses the original image's pixel coordinates, even
when the service internally upscales a small image before OCR.

```json
{
  "image_width": 1600,
  "image_height": 1200,
  "regions": [
    {
      "text": "Example text",
      "bounding_box": [112, 84, 410, 126],
      "confidence": 0.98,
      "pixel_height": 42
    }
  ]
}
```

`bounding_box` is `[x1, y1, x2, y2]`, and `pixel_height` is exactly
`y2 - y1`. Regions remain separate and are sorted top-to-bottom, then
left-to-right within a visual line. OCR confidence is passed through from
PaddleOCR.

Invalid images return HTTP 400. Oversized uploads return HTTP 413. If the OCR
provider fails, the service returns HTTP 502 with a useful error message.

## Install and run

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r cv_service/requirements.txt
uvicorn cv_service.app:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/docs` for the interactive API documentation.

## Configuration

Optional environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `OCR_LANGUAGE` | `en` | PaddleOCR language model |
| `OCR_USE_ANGLE_CLASSIFIER` | `true` | Enable orientation handling where supported |
| `OCR_MIN_CONFIDENCE` | `0.0` | Drop regions below this confidence |
| `OCR_UPSCALE_SMALL_IMAGES` | `true` | Upscale small images before OCR |
| `OCR_MIN_IMAGE_SIDE` | `1200` | Target shortest side for upscaling |
| `MAX_UPLOAD_BYTES` | `10485760` | Maximum accepted upload size |

The existing Node backend OCR placeholder is intentionally not modified by
this service. Integration can be added later as a separate adapter once the
Part 2 response contract is accepted by the team.

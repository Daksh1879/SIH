"""HTTP API for standalone image OCR."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field

from .config import MAX_UPLOAD_BYTES
from .ocr_engine import OCRProcessingError, get_default_engine
from .postprocessing import normalize_regions
from .preprocessing import InvalidImageError, decode_and_prepare


class OCRRegionResponse(BaseModel):
    text: str
    bounding_box: list[int] = Field(min_length=4, max_length=4)
    confidence: float
    pixel_height: int


class OCRResponse(BaseModel):
    image_width: int
    image_height: int
    regions: list[OCRRegionResponse]


app = FastAPI(
    title="LabelSetu Computer Vision Service",
    description="Image-to-text regions only; no field extraction or compliance rules.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health without forcing the OCR model to load."""

    return {"status": "ok", "service": "cv_service"}


@app.post("/ocr", response_model=OCRResponse)
async def ocr(file: UploadFile = File(...)) -> dict[str, Any]:
    """Run OCR and return independent regions in original-image coordinates."""

    image_bytes = await file.read()
    if len(image_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"Image exceeds the {MAX_UPLOAD_BYTES}-byte upload limit.",
        )

    try:
        prepared = decode_and_prepare(image_bytes)
    except InvalidImageError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    try:
        raw_results = get_default_engine().run(prepared.image)
        regions = normalize_regions(
            raw_results,
            scale_x=prepared.scale_x,
            scale_y=prepared.scale_y,
            original_width=prepared.original_width,
            original_height=prepared.original_height,
        )
    except OCRProcessingError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    return {
        "image_width": prepared.original_width,
        "image_height": prepared.original_height,
        "regions": [region.as_dict() for region in regions],
    }

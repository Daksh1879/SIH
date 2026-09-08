"""Configuration for the OCR service.

All settings are environment-variable driven so the OCR implementation can be
changed without changing the HTTP API.
"""

from __future__ import annotations

import os


def _as_bool(value: str, default: bool) -> bool:
    """Parse a human-friendly boolean environment variable."""

    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


OCR_LANGUAGE = os.getenv("OCR_LANGUAGE", "en")
OCR_USE_ANGLE_CLASSIFIER = _as_bool(
    os.getenv("OCR_USE_ANGLE_CLASSIFIER", "true"),
    default=True,
)
OCR_MIN_CONFIDENCE = float(os.getenv("OCR_MIN_CONFIDENCE", "0.0"))
OCR_UPSCALE_SMALL_IMAGES = _as_bool(
    os.getenv("OCR_UPSCALE_SMALL_IMAGES", "true"),
    default=True,
)
OCR_MIN_IMAGE_SIDE = int(os.getenv("OCR_MIN_IMAGE_SIDE", "1200"))
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))

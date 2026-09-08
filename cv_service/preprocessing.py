"""Image decoding and optional preprocessing for OCR.

The OCR engine may receive an upscaled image for improved recognition.  The
returned scale factors let postprocessing map every OCR box back to the
original uploaded image.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from .config import OCR_MIN_IMAGE_SIDE, OCR_UPSCALE_SMALL_IMAGES


class InvalidImageError(ValueError):
    """Raised when uploaded bytes are not a readable image."""


@dataclass(frozen=True)
class PreparedImage:
    """An OCR-ready image and its relationship to the original image."""

    image: np.ndarray
    original_width: int
    original_height: int
    scale_x: float
    scale_y: float


def decode_and_prepare(image_bytes: bytes) -> PreparedImage:
    """Decode uploaded bytes and optionally upscale small images.

    No cropping or content filtering is performed: OCR sees the complete
    image, including text that may not be relevant to later rule checks.
    """

    if not image_bytes:
        raise InvalidImageError("The uploaded file is empty.")

    encoded = np.frombuffer(image_bytes, dtype=np.uint8)
    decoded = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if decoded is None or decoded.size == 0:
        raise InvalidImageError("The uploaded file is not a readable image.")

    original_height, original_width = decoded.shape[:2]
    processed = decoded

    if OCR_UPSCALE_SMALL_IMAGES:
        shortest_side = min(original_width, original_height)
        if shortest_side < OCR_MIN_IMAGE_SIDE:
            scale = OCR_MIN_IMAGE_SIDE / shortest_side
            processed = cv2.resize(
                decoded,
                dsize=None,
                fx=scale,
                fy=scale,
                interpolation=cv2.INTER_CUBIC,
            )

    processed_height, processed_width = processed.shape[:2]
    return PreparedImage(
        image=processed,
        original_width=original_width,
        original_height=original_height,
        scale_x=original_width / processed_width,
        scale_y=original_height / processed_height,
    )

"""Replaceable PaddleOCR adapter.

The FastAPI layer depends only on ``OCREngine.run``.  Keeping PaddleOCR
construction and version-specific invocation here allows the OCR provider to
be replaced later without changing the HTTP contract.
"""

from __future__ import annotations

from threading import Lock
from typing import Any

import numpy as np

from .config import OCR_LANGUAGE, OCR_USE_ANGLE_CLASSIFIER


class OCRProcessingError(RuntimeError):
    """Raised when the OCR provider cannot process an image."""


class OCREngine:
    """Small provider-neutral interface used by the API layer."""

    def run(self, image: np.ndarray) -> Any:
        raise NotImplementedError


class PaddleOCREngine(OCREngine):
    """Adapter supporting PaddleOCR 2.x and 3.x invocation styles."""

    def __init__(self) -> None:
        self._engine: Any | None = None
        self._modern_api = False
        self._lock = Lock()

    def _create_engine(self) -> None:
        try:
            from paddleocr import PaddleOCR
        except ImportError as exc:
            raise OCRProcessingError(
                "PaddleOCR is not installed. Install cv_service/requirements.txt."
            ) from exc

        # PaddleOCR 3.x uses the new predict API and accepts these options.
        # Fall back to the 2.x constructor when running an older installation.
        try:
            self._engine = PaddleOCR(
                lang=OCR_LANGUAGE,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
                use_textline_orientation=OCR_USE_ANGLE_CLASSIFIER,
            )
            self._modern_api = hasattr(self._engine, "predict")
        except (TypeError, ValueError):
            try:
                self._engine = PaddleOCR(
                    lang=OCR_LANGUAGE,
                    use_angle_cls=OCR_USE_ANGLE_CLASSIFIER,
                )
                self._modern_api = False
            except Exception as exc:
                raise OCRProcessingError(
                    f"Could not initialize PaddleOCR: {exc}"
                ) from exc
        except Exception as exc:
            raise OCRProcessingError(
                f"Could not initialize PaddleOCR: {exc}"
            ) from exc

    def _get_engine(self) -> Any:
        if self._engine is None:
            with self._lock:
                if self._engine is None:
                    self._create_engine()
        return self._engine

    def run(self, image: np.ndarray) -> Any:
        engine = self._get_engine()
        try:
            if self._modern_api:
                return list(engine.predict(image))
            return engine.ocr(image, cls=OCR_USE_ANGLE_CLASSIFIER)
        except Exception as exc:
            raise OCRProcessingError(f"PaddleOCR failed to process image: {exc}") from exc


_default_engine: PaddleOCREngine | None = None
_default_engine_lock = Lock()


def get_default_engine() -> PaddleOCREngine:
    """Return the process-wide lazy OCR engine instance."""

    global _default_engine
    if _default_engine is None:
        with _default_engine_lock:
            if _default_engine is None:
                _default_engine = PaddleOCREngine()
    return _default_engine

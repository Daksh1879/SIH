"""Normalize OCR engine output into the public API contract."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Any, Iterable, Mapping, Sequence

from .config import OCR_MIN_CONFIDENCE


@dataclass(frozen=True)
class OCRRegion:
    """A single independent text region in original-image coordinates."""

    text: str
    bounding_box: list[int]
    confidence: float
    pixel_height: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "bounding_box": self.bounding_box,
            "confidence": self.confidence,
            "pixel_height": self.pixel_height,
        }


def _coordinates(points: Any) -> list[tuple[float, float]]:
    """Convert a Paddle polygon/box representation into x/y pairs."""

    if points is None:
        return []

    # Paddle may return numpy arrays; converting through tolist keeps this
    # module independent from numpy's concrete scalar types.
    if hasattr(points, "tolist"):
        points = points.tolist()

    if isinstance(points, Mapping):
        if {"x", "y"}.issubset(points):
            return [(float(points["x"]), float(points["y"]))]
        return []

    if not isinstance(points, Sequence) or isinstance(points, (str, bytes)):
        return []

    # A flat [x1, y1, x2, y2] box.
    if len(points) >= 4 and all(
        isinstance(value, (int, float)) for value in points[:4]
    ):
        values = [float(value) for value in points]
        return list(zip(values[::2], values[1::2]))

    result: list[tuple[float, float]] = []
    for point in points:
        if hasattr(point, "tolist"):
            point = point.tolist()
        if (
            isinstance(point, Sequence)
            and not isinstance(point, (str, bytes))
            and len(point) >= 2
        ):
            try:
                result.append((float(point[0]), float(point[1])))
            except (TypeError, ValueError):
                continue
    return result


def _box_from_points(points: Any) -> tuple[float, float, float, float] | None:
    coords = _coordinates(points)
    if not coords:
        return None
    xs = [point[0] for point in coords]
    ys = [point[1] for point in coords]
    return min(xs), min(ys), max(xs), max(ys)


def _read_value(value: Any, key: str, default: Any = None) -> Any:
    if isinstance(value, Mapping):
        return value.get(key, default)
    attribute = getattr(value, key, None)
    if attribute is not None:
        return attribute
    try:
        return value[key]
    except (KeyError, IndexError, TypeError):
        return default


def _as_float(value: Any, default: float = 0.0) -> float:
    try:
        converted = float(value)
    except (TypeError, ValueError):
        return default
    return converted if isfinite(converted) else default


def _modern_regions(result: Any) -> list[tuple[str, Any, float]]:
    """Parse PaddleOCR 3.x result objects/dicts."""

    texts = _read_value(result, "rec_texts", [])
    scores = _read_value(result, "rec_scores", [])
    boxes = _read_value(result, "rec_boxes", None)
    if boxes is None:
        boxes = _read_value(result, "rec_polys", [])

    if hasattr(texts, "tolist"):
        texts = texts.tolist()
    if hasattr(scores, "tolist"):
        scores = scores.tolist()
    if hasattr(boxes, "tolist"):
        boxes = boxes.tolist()

    if not isinstance(texts, Sequence) or isinstance(texts, (str, bytes)):
        return []
    if not isinstance(scores, Sequence) or isinstance(scores, (str, bytes)):
        scores = []
    if not isinstance(boxes, Sequence) or isinstance(boxes, (str, bytes)):
        return []

    parsed: list[tuple[str, Any, float]] = []
    for index, text in enumerate(texts):
        if index >= len(boxes):
            break
        parsed.append(
            (
                str(text),
                boxes[index],
                _as_float(scores[index]) if index < len(scores) else 0.0,
            )
        )
    return parsed


def _legacy_regions(result: Any) -> list[tuple[str, Any, float]]:
    """Parse PaddleOCR 2.x output: [box, (text, confidence)]."""

    if hasattr(result, "tolist"):
        result = result.tolist()
    if not isinstance(result, Sequence) or isinstance(result, (str, bytes)):
        return []

    parsed: list[tuple[str, Any, float]] = []
    for line in result:
        if not isinstance(line, Sequence) or len(line) < 2:
            continue
        box = line[0]
        recognition = line[1]
        if (
            not isinstance(recognition, Sequence)
            or isinstance(recognition, (str, bytes))
            or len(recognition) < 2
            or not isinstance(recognition[0], str)
        ):
            continue
        parsed.append(
            (str(recognition[0]), box, _as_float(recognition[1]))
        )
    return parsed


def _raw_regions(raw_result: Any) -> Iterable[tuple[str, Any, float]]:
    """Yield raw regions from either PaddleOCR major API shape."""

    modern = _modern_regions(raw_result)
    if modern:
        yield from modern
        return
    yield from _legacy_regions(raw_result)


def normalize_regions(
    raw_results: Any,
    *,
    scale_x: float = 1.0,
    scale_y: float = 1.0,
    original_width: int | None = None,
    original_height: int | None = None,
) -> list[OCRRegion]:
    """Map raw OCR regions to original coordinates and sort them naturally."""

    # Legacy PaddleOCR wraps one image's lines in an outer list. Modern
    # predict() returns an iterable of result objects. Try the direct shape
    # first, then unwrap the common one-image legacy shape.
    candidates = list(_raw_regions(raw_results))
    if not candidates and isinstance(raw_results, Sequence):
        for item in raw_results:
            candidates.extend(_raw_regions(item))

    regions: list[OCRRegion] = []
    for text, raw_box, confidence in candidates:
        box = _box_from_points(raw_box)
        if box is None or not str(text).strip():
            continue

        x1, y1, x2, y2 = box
        x1 = round(x1 * scale_x)
        y1 = round(y1 * scale_y)
        x2 = round(x2 * scale_x)
        y2 = round(y2 * scale_y)

        if original_width is not None:
            x1 = min(max(x1, 0), original_width)
            x2 = min(max(x2, 0), original_width)
        if original_height is not None:
            y1 = min(max(y1, 0), original_height)
            y2 = min(max(y2, 0), original_height)

        if x2 <= x1 or y2 <= y1 or confidence < OCR_MIN_CONFIDENCE:
            continue

        regions.append(
            OCRRegion(
                text=str(text),
                bounding_box=[x1, y1, x2, y2],
                confidence=confidence,
                pixel_height=y2 - y1,
            )
        )

    return _sort_reading_order(regions)


def _sort_reading_order(regions: list[OCRRegion]) -> list[OCRRegion]:
    """Sort lines top-to-bottom while keeping regions left-to-right per line."""

    if len(regions) < 2:
        return regions

    # A region belongs to the same visual line when its vertical center is
    # within half of the larger text height. This handles different font
    # sizes without changing or merging any region.
    remaining = sorted(
        regions,
        key=lambda item: (item.bounding_box[1], item.bounding_box[0]),
    )
    ordered: list[OCRRegion] = []
    lines: list[dict[str, Any]] = []

    for region in remaining:
        x1, y1, x2, y2 = region.bounding_box
        center_y = (y1 + y2) / 2
        best_line: dict[str, Any] | None = None
        best_distance = float("inf")
        for line in lines:
            distance = abs(center_y - line["center_y"])
            tolerance = max(region.pixel_height, line["height"]) * 0.5
            if distance <= tolerance and distance < best_distance:
                best_line = line
                best_distance = distance

        if best_line is None:
            best_line = {
                "center_y": center_y,
                "height": region.pixel_height,
                "regions": [],
            }
            lines.append(best_line)
        best_line["regions"].append(region)
        count = len(best_line["regions"])
        best_line["center_y"] = (
            (best_line["center_y"] * (count - 1)) + center_y
        ) / count
        best_line["height"] = max(best_line["height"], region.pixel_height)

    lines.sort(key=lambda line: line["center_y"])
    for line in lines:
        ordered.extend(
            sorted(line["regions"], key=lambda item: item.bounding_box[0])
        )
    return ordered

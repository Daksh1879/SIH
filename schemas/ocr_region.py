# schemas/ocr_region.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class BoundingBox:
    x: float
    y: float
    width: float
    height: float

@dataclass
class OCRRegion:
    region_id: str
    raw_text: str
    confidence: float
    bounding_box: BoundingBox
    estimated_font_size_pt: Optional[float] = None
    language: Optional[str] = None
    page: int = 0
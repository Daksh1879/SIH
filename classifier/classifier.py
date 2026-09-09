# classifier/classifier.py
from schemas.ocr_region import OCRRegion
from schemas.declaration import ExtractedDeclaration, DeclarationField
from classifier.patterns import FIELD_PATTERNS
from classifier.keyword_heuristic import keyword_classify
from typing import List

def classify_regions(regions: List[OCRRegion]) -> List[ExtractedDeclaration]:
    declarations = []
    for region in regions:
        field, confidence = _classify_one(region.raw_text)
        declarations.append(ExtractedDeclaration(
            field=DeclarationField(field),
            raw_text=region.raw_text,
            normalized_value=_normalize(field, region.raw_text),
            source_region_ids=[region.region_id],
            classifier_confidence=confidence,
            font_size_pt=region.estimated_font_size_pt,
            bounding_box=region.bounding_box,
            language=region.language,
        ))
    return declarations

def _classify_one(text: str) -> tuple:
    # Stage 1: Regex
    for field, patterns in FIELD_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(text):
                return field, 0.95

    # Stage 2: Keyword heuristic
    field, score = keyword_classify(text)
    if field and score >= 0.3:
        return field, score

    # Stage 3: Fallback to unknown
    return "unknown", 0.0

def _normalize(field: str, text: str) -> str:
    import re
    text = text.strip()
    if field == "mrp":
        match = re.search(r"[\d,]+(\.\d{1,2})?", text)
        return match.group(0).replace(",", "") if match else text
    if field == "net_quantity":
        match = re.search(r"([\d.]+)\s*(g|kg|ml|l|nos?|cm|m)\b", text, re.IGNORECASE)
        return f"{match.group(1)} {match.group(2).lower()}" if match else text
    return text
# schemas/violation.py
from dataclasses import dataclass, field
from typing import Optional, List
from enum import Enum
from schemas.declaration import ExtractedDeclaration

class ViolationType(str, Enum):
    MISSING_FIELD    = "missing_field"
    FORMAT_MISMATCH  = "format_mismatch"
    FONT_TOO_SMALL   = "font_too_small"
    WRONG_UNIT       = "wrong_unit"
    WRONG_VALUE      = "wrong_value"
    PLACEMENT_ISSUE  = "placement_issue"
    LANGUAGE_MISSING = "language_missing"

class PenaltyClass(str, Enum):
    A = "A"
    B = "B"

@dataclass
class Violation:
    violation_id: str
    rule_id: str
    violation_type: ViolationType
    field: str
    description: str
    evidence_text: Optional[str]
    evidence_region_ids: List[str]
    penalty_class: PenaltyClass
    suggested_correction: str
    confidence: float

@dataclass
class ComplianceReport:
    scan_id: str
    product_id: Optional[str]
    scanned_at: str
    rule_set_version: str
    declarations: List[ExtractedDeclaration]
    violations: List[Violation]
    is_compliant: bool
    compliance_score: float
    summary: str
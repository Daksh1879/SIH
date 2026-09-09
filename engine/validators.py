# engine/validators.py
import re, uuid
from schemas.declaration import ExtractedDeclaration
from schemas.violation import Violation, ViolationType, PenaltyClass

def check_presence(rule, declarations):
    field = rule["field"]
    found = any(d.field.value == field for d in declarations)
    if not found:
        return [Violation(
            violation_id=str(uuid.uuid4()),
            rule_id=rule["id"],
            violation_type=ViolationType.MISSING_FIELD,
            field=field,
            description=rule["description"],
            evidence_text=None,
            evidence_region_ids=[],
            penalty_class=PenaltyClass(rule["penalty_class"]),
            suggested_correction=f"Add '{field.replace('_',' ')}' declaration to label.",
            confidence=1.0,
        )]
    return []

def check_format(rule, declarations):
    violations = []
    pattern = rule.get("format_regex")
    if not pattern:
        return violations
    regex = re.compile(pattern)
    for decl in declarations:
        if decl.field.value != rule["field"]:
            continue
        if not regex.search(decl.raw_text):
            violations.append(Violation(
                violation_id=str(uuid.uuid4()),
                rule_id=rule["id"],
                violation_type=ViolationType.FORMAT_MISMATCH,
                field=decl.field.value,
                description=f"{rule['description']} — found: '{decl.raw_text[:60]}'",
                evidence_text=decl.raw_text,
                evidence_region_ids=decl.source_region_ids,
                penalty_class=PenaltyClass(rule["penalty_class"]),
                suggested_correction=f"Reformat to include MRP prefix and ₹ symbol.",
                confidence=decl.classifier_confidence * 0.9,
            ))
    return violations

def check_font_size(rule, declarations):
    violations = []
    min_size = rule.get("min_font_size_pt", 2.8)
    for decl in declarations:
        if rule["field"] not in ("*", decl.field.value):
            continue
        if decl.font_size_pt is None:
            continue
        if decl.font_size_pt < min_size:
            violations.append(Violation(
                violation_id=str(uuid.uuid4()),
                rule_id=rule["id"],
                violation_type=ViolationType.FONT_TOO_SMALL,
                field=decl.field.value,
                description=f"Font {decl.font_size_pt:.1f}pt < minimum {min_size}pt",
                evidence_text=decl.raw_text[:60],
                evidence_region_ids=decl.source_region_ids,
                penalty_class=PenaltyClass(rule["penalty_class"]),
                suggested_correction=f"Increase font size to at least {min_size}pt (1mm).",
                confidence=0.85,
            ))
    return violations

def check_net_quantity_unit(rule, declarations):
    violations = []
    allowed = {u.lower() for u in rule.get("allowed_units", [])}
    for decl in declarations:
        if decl.field.value != "net_quantity":
            continue
        match = re.search(
            r"\b(g|kg|ml|l|cm|m|nos?\.?|pieces?|lbs?|oz|pounds?)\b",
            decl.raw_text, re.IGNORECASE
        )
        if not match or match.group(1).lower().rstrip(".") not in allowed:
            violations.append(Violation(
                violation_id=str(uuid.uuid4()),
                rule_id=rule["id"],
                violation_type=ViolationType.WRONG_UNIT,
                field="net_quantity",
                description=f"Non-standard unit in: '{decl.raw_text[:60]}'",
                evidence_text=decl.raw_text,
                evidence_region_ids=decl.source_region_ids,
                penalty_class=PenaltyClass(rule["penalty_class"]),
                suggested_correction="Use SI units: g, kg, ml, l, cm, m, or number.",
                confidence=0.90,
            ))
    return violations
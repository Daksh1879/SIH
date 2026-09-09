# engine/rule_engine.py
import uuid, datetime
from datetime import timezone
from datetime import date
from pathlib import Path
from engine.rule_loader import load_rules
from engine.validators import check_presence, check_format, check_font_size, check_net_quantity_unit
from engine.exemption_checker import is_exempted
from schemas.violation import ComplianceReport

VALIDATOR_MAP = {
    "presence":  check_presence,
    "format":    check_format,
    "font_size": check_font_size,
    "value":     check_net_quantity_unit,
}

def run_rule_engine(declarations, product_context, rule_set_version=None, category="general"):
    if rule_set_version is None:
        rule_set_version = date.today()

    rules = load_rules(Path("rules"), as_of_date=rule_set_version, category=category)
    all_violations = []

    for rule in rules:
        if is_exempted(rule, product_context):
            continue
        validator = VALIDATOR_MAP.get(rule["rule_type"])
        if validator:
            violations = validator(rule, declarations)
            all_violations.extend(violations)

    major = sum(1 for v in all_violations if v.penalty_class.value == "A")
    minor = len(all_violations) - major
    score = max(0, 100 - (major * 20) - (minor * 5))

    return ComplianceReport(
        scan_id=str(uuid.uuid4()),
        product_id=product_context.get("product_id"),
        scanned_at=datetime.datetime.now(timezone.utc).isoformat(),
        rule_set_version=rule_set_version.isoformat(),
        declarations=declarations,
        violations=all_violations,
        is_compliant=len(all_violations) == 0,
        compliance_score=score,
        summary=_summary(all_violations, score),
    )

def _summary(violations, score):
    if not violations:
        return "COMPLIANT — All mandatory declarations present and correctly formatted."
    lines = [f"NON-COMPLIANT — {len(violations)} violation(s). Score: {score}/100"]
    for v in violations[:5]:
        lines.append(f"  [{v.penalty_class.value}] {v.field}: {v.description[:80]}")
    if len(violations) > 5:
        lines.append(f"  ... and {len(violations)-5} more.")
    return "\n".join(lines)
# tests/test_rule_engine.py
import json
import pytest
from pathlib import Path
from schemas.ocr_region import OCRRegion, BoundingBox
from classifier.classifier import classify_regions
from engine.rule_engine import run_rule_engine

FIXTURES = Path("tests/fixtures")

def load_fixture(name):
    data = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    return [
        OCRRegion(
            region_id=r["region_id"],
            raw_text=r["raw_text"],
            confidence=r["confidence"],
            bounding_box=BoundingBox(**r["bounding_box"]),
            estimated_font_size_pt=r.get("estimated_font_size_pt"),
            language=r.get("language"),
        )
        for r in data["regions"]
    ]

class TestCompliantLabel:
    def setup_method(self):
        regions = load_fixture("sample_compliant.json")
        declarations = classify_regions(regions)
        self.report = run_rule_engine(
            declarations,
            product_context={"net_weight_g": 500, "product_id": "test-001"}
        )

    def test_mrp_field_found(self):
        fields = [d.field.value for d in self.report.declarations]
        assert "mrp" in fields

    def test_net_quantity_found(self):
        fields = [d.field.value for d in self.report.declarations]
        assert "net_quantity" in fields

    def test_score_is_high(self):
        assert self.report.compliance_score >= 40

class TestViolationLabel:
    def setup_method(self):
        regions = load_fixture("sample_violations.json")
        declarations = classify_regions(regions)
        self.report = run_rule_engine(
            declarations,
            product_context={"net_weight_g": 454, "product_id": "test-002"}
        )

    def test_not_compliant(self):
        assert not self.report.is_compliant

    def test_has_violations(self):
        assert len(self.report.violations) > 0

    def test_mrp_violation(self):
        rule_ids = [v.rule_id for v in self.report.violations]
        # Fixture has NO MRP region at all → presence rule fires (R9-0)
        # Format rule (R9-1) only fires when MRP text exists but is wrongly formatted
        assert "LM-PC-R9-0" in rule_ids

    def test_mrp_violation_type(self):
        vtypes = {v.violation_type for v in self.report.violations if v.rule_id == "LM-PC-R9-0"}
        assert "missing_field" in vtypes

    def test_wrong_unit_violation(self):
        vtypes = [v.violation_type for v in self.report.violations]
        assert "wrong_unit" in vtypes

    def test_font_violation(self):
        vtypes = [v.violation_type for v in self.report.violations]
        assert "font_too_small" in vtypes

    def test_score_below_50(self):
        assert self.report.compliance_score < 50

class TestRuleLoader:
    def test_rules_load(self):
        from engine.rule_loader import load_rules
        rules = load_rules()
        assert len(rules) > 0

    def test_historic_date_filters_rules(self):
        from engine.rule_loader import load_rules
        from datetime import date
        rules = load_rules(as_of_date=date(2010, 1, 1))
        assert len(rules) == 0

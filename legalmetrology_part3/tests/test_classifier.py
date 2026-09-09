# tests/test_classifier.py
import pytest
from schemas.ocr_region import OCRRegion, BoundingBox
from classifier.classifier import classify_regions

def make_region(rid, text, font_size=5.0):
    return OCRRegion(rid, text, 0.99, BoundingBox(0, 0, 0.5, 0.05),
                     estimated_font_size_pt=font_size, language="en")

def test_mrp_detected():
    d = classify_regions([make_region("r1", "MRP Rs. 99.00")])
    assert d[0].field.value == "mrp"

def test_mrp_rupee_symbol():
    d = classify_regions([make_region("r1", "MRP ₹45.50")])
    assert d[0].field.value == "mrp"

def test_net_quantity_grams():
    d = classify_regions([make_region("r1", "Net Weight: 250g")])
    assert d[0].field.value == "net_quantity"

def test_net_quantity_kg():
    d = classify_regions([make_region("r1", "Net Wt. 1.5 kg")])
    assert d[0].field.value == "net_quantity"

def test_manufacture_date():
    d = classify_regions([make_region("r1", "Mfg. Date: 08/2026")])
    assert d[0].field.value == "manufacture_date"

def test_expiry_date():
    d = classify_regions([make_region("r1", "Best Before: 08/2027")])
    assert d[0].field.value in ("expiry_date", "best_before")

def test_consumer_care():
    d = classify_regions([make_region("r1", "Consumer Care: 1800-123-4567")])
    assert d[0].field.value == "consumer_care"

def test_manufacturer_address_keyword():
    d = classify_regions([make_region("r1", "Manufactured by: ABC Ltd., Mumbai 400001")])
    assert d[0].field.value in ("manufacturer_name", "manufacturer_address")

def test_unknown_text():
    d = classify_regions([make_region("r1", "XYZABC RANDOM JUNK 12345")])
    assert d[0].field.value == "unknown"
# classifier/patterns.py
import re

FIELD_PATTERNS = {
    "mrp": [
        re.compile(r"(?i)(M\.?R\.?P\.?)\s*[₹Rs\.]+\s*[\d,]+(\.\d{1,2})?"),
        re.compile(r"(?i)maximum\s+retail\s+price\s*[₹Rs\.]+\s*[\d,]+"),
        re.compile(r"(?i)(price|rate)\s*[₹Rs\.]+\s*[\d,]+"),
    ],
    "net_quantity": [
        re.compile(r"(?i)(net\s*(weight|wt\.?|contents?|qty\.?|quantity))\s*:?\s*[\d.]+\s*(g|kg|ml|l|nos?\.?|cm|m)\b"),
        re.compile(r"(?i)[\d.]+\s*(grams?|kilograms?|millilitres?|litres?|pieces?)\b"),
        re.compile(r"(?i)net\s+wt\.?\s*[\d.]+"),
    ],
    "manufacture_date": [
        re.compile(r"(?i)(mfg\.?\s*date|mfd\.?|manufactured\s+on|packed\s+on|date\s+of\s+mfg\.?)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{4}|\w+\s+\d{4})"),
        re.compile(r"(?i)(mfg|mfd)\s*[:\-]?\s*\d{2}[\/\-]\d{4}"),
    ],
    "expiry_date": [
        re.compile(r"(?i)(exp\.?\s*date|best\s+before|use\s+by|expiry|exp\.?)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{4}|\w+\s+\d{4})"),
    ],
    "batch_number": [
        re.compile(r"(?i)(batch\s*(no\.?|number)?|lot\s*no\.?)\s*[:\-]?\s*([A-Z0-9\-/]+)"),
    ],
    "consumer_care": [
        re.compile(r"(?i)(consumer\s+care|helpline|toll[\s-]?free|customer\s+(care|service))\s*[:\-]?\s*(\+?[\d\s\-()]{7,})"),
        re.compile(r"(?i)1800[\s-]?\d{3}[\s-]?\d{4}"),
    ],
    "license_number": [
        re.compile(r"(?i)(fssai\s*(lic\.?\s*no\.?|license|licence)?\s*[:\-]?\s*(\d{14}))"),
        re.compile(r"(?i)(bis|isi|agmark|fpo)\s*(no\.?|cert\.?)?\s*[:\-]?\s*[A-Z0-9\-]+"),
    ],
    "manufacturer_address": [
        re.compile(r"(?i)(manufactured|mfg\.?|packed)\s+by\s*[:\-]?"),
        re.compile(r"\b\d{6}\b"),
    ],
    "country_of_origin": [
        re.compile(r"(?i)(country\s+of\s+origin|product\s+of|made\s+in)\s*[:\-]?\s*\w+"),
    ],
}
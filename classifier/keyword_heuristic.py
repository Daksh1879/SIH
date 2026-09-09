# classifier/keyword_heuristic.py

KEYWORD_SIGNALS = {
    "manufacturer_name":    ["manufactured by", "mfg. by", "mfr.", "producer", "marketed by"],
    "packer_name":          ["packed by", "packaged by", "packer"],
    "importer_name":        ["imported by", "importer", "sole importer"],
    "country_of_origin":    ["country of origin", "product of", "made in"],
    "ingredients":          ["ingredients", "contains", "composition", "made from"],
    "nutritional_info":     ["nutrition facts", "nutritional information", "energy", "protein", "carbohydrate", "fat"],
    "generic_name":         ["generic name", "common name"],
    "license_number":       ["lic. no.", "license no.", "fssai", "bis", "agmark", "fpo"],
    "consumer_care":        ["consumer care", "customer care", "helpline", "toll free", "1800"],
    "best_before":          ["best before", "use by", "consume before"],
    "manufacture_date":     ["mfg date", "mfd", "manufactured on", "packed on", "date of mfg"],
}

def keyword_classify(text: str) -> tuple:
    text_lower = text.lower()
    best_field, best_score = None, 0.0
    for field, keywords in KEYWORD_SIGNALS.items():
        for kw in keywords:
            if kw in text_lower:
                score = min(len(kw) / max(len(text_lower), 1) * 5, 0.80)
                if score > best_score:
                    best_field, best_score = field, score
    return best_field, best_score
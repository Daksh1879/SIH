# engine/exemption_checker.py

def is_exempted(rule: dict, product_context: dict) -> bool:
    for exemption in rule.get("exemptions", []):
        condition = exemption.get("condition", "")
        if not condition:
            continue
        try:
            if eval(condition, {"__builtins__": {}}, product_context):
                return True
        except Exception:
            pass
    return False
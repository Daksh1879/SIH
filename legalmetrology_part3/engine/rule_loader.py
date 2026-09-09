# engine/rule_loader.py
import yaml
from pathlib import Path
from datetime import date

def load_rules(
    rules_path: Path = Path("rules"),
    as_of_date: date = date.today(),
    category: str = "general"
) -> list:
    rules = []
    for f in rules_path.glob("*.yaml"):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        for rule in data.get("rules", []):
            added = date.fromisoformat(rule["added_date"])
            superseded = rule.get("superseded_date")
            if added > as_of_date:
                continue
            if superseded and date.fromisoformat(superseded) <= as_of_date:
                continue
            applies = rule.get("applies_to", ["*"])
            if category not in applies and "*" not in applies:
                continue
            rules.append(rule)
    return rules
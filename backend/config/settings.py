import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_json(name: str):
    with open(BASE_DIR / name) as f:
        return json.load(f)

ROOT_CAUSE_RULES = load_json("root_cause_rules.json")
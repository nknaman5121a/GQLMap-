import json

def load_payloads():
    with open("config/payloads.json", "r", encoding="utf-8") as f:
        return json.load(f)

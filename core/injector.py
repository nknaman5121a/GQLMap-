import json
import time
import httpx
from core.schema_enum import introspect_schema
from config.payloads import load_payloads

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

LOG_FILE = "output/logs/injection_log.txt"


def fuzz_field(field_name, payload):
    """Returns GraphQL string with payload injected into a field"""
    return f"""query {{
        __typename
        {field_name}(input: "{payload}") {{
            __typename
        }}
    }}"""


def send_payload(endpoint, query):
    try:
        start = time.time()
        res = httpx.post(endpoint, headers=HEADERS, json={"query": query}, timeout=10)
        delay = time.time() - start

        return {
            "status_code": res.status_code,
            "text": res.text,
            "delay": round(delay, 2)
        }

    except Exception as e:
        return {"status_code": 0, "text": str(e), "delay": -1}


def inject(endpoint):
    print(f"[*] Loading payloads and performing introspection on {endpoint} ...")
    
    schema = introspect_schema(endpoint)
    success = bool(schema)
    
    if not success:
        print("[-] Introspection failed. Cannot inject without schema.")
        return

    payloads = load_payloads()
    injections = payloads.get("injections", [])

    print(f"[+] Loaded {len(injections)} payloads. Starting injection tests...\n")
    log_entries = []

    # Extract field names from introspection schema
    tested_fields = [t['name'] for t in schema.get('data', {}).get('__schema', {}).get('queryType', {}).get('fields', [])]

    for field in tested_fields:
        print(f"[>] Testing field: {field}")
        for payload in injections:
            gql = fuzz_field(field, payload)
            result = send_payload(endpoint, gql)

            # Simple heuristic detection
            is_vuln = (
                "error" in result['text'].lower()
                or result['status_code'] >= 500
                or result['delay'] > 3
            )

            status = "[VULNERABLE]" if is_vuln else "[OK]"
            print(f"  - Payload: {payload[:30]}... | Status: {status}")

            entry = {
                "field": field,
                "payload": payload,
                "status_code": result["status_code"],
                "response_time": result["delay"],
                "response_snippet": result["text"][:100],
                "vulnerable": is_vuln
            }
            log_entries.append(entry)

    # Save log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        for entry in log_entries:
            f.write(json.dumps(entry, indent=2) + "\n")

    print(f"\n[+] Injection testing complete. Results saved to {LOG_FILE}")

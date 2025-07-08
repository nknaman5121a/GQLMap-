import argparse
from core.endpoint_finder import detect_graphql_endpoint
from core.js_scraper import find_graphql_from_js
from core.schema_enum import introspect_schema
from core.injector import inject
from core.utils import generate_html_report
from core.auth_tester import test_auth_bypass
from core.mutation_engine import run_mutation_engine


def main():
    parser = argparse.ArgumentParser(description="GQLMap - Automated GraphQL Pentest Tool")
    parser.add_argument("url", help="Target base URL (e.g. https://example.com)")
    parser.add_argument("--endpoint", help="Specify GraphQL endpoint manually")
    parser.add_argument("--crawl", action="store_true", help="Crawl JS files to detect hidden GraphQL endpoints")
    parser.add_argument("--introspect", action="store_true", help="Perform introspection query")
    parser.add_argument("--inject", action="store_true", help="Perform GraphQL injection testing")
    parser.add_argument("--token", help="JWT or bearer token to test authentication bypass")
    parser.add_argument("--test-roles", action="store_true", help="Check role-based access control issues")
    parser.add_argument("--header-fuzz", action="store_true", help="Fuzz headers for bypassing auth")
    parser.add_argument("--mutate", action="store_true", help="Run GraphQL mutation engine for logic bypass")
    parser.add_argument("--threads", type=int, default=5, help="Number of threads for mutation fuzzing")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    parser.add_argument("--retries", type=int, default=2, help="Retry count for failed requests")
    parser.add_argument("--verbose", action="store_true", help="Verbose output (debug level)")
    parser.add_argument("--report", help="Custom report file path")
    parser.add_argument("--output", choices=["html", "json", "markdown"], default="html", help="Output report format")

    args = parser.parse_args()

    base_url = args.url
    target_endpoint = args.endpoint

    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if args.token:
        headers["Authorization"] = f"Bearer {args.token}"

    # Step 1: Auto-detect endpoint if not specified
    if not target_endpoint:
        print("[*] No endpoint provided. Trying to auto-detect...")
        endpoints = detect_graphql_endpoint(base_url)
        if endpoints:
            print(f"[+] GraphQL endpoint(s) found: {endpoints}")
            target_endpoint = endpoints[0]
        elif args.crawl:
            print("[*] Crawling JavaScript files to find hidden GraphQL endpoints...")
            js_endpoints = find_graphql_from_js(base_url)
            if js_endpoints:
                print(f"[+] Found GraphQL endpoint(s) in JS: {js_endpoints}")
                target_endpoint = js_endpoints[0]
            else:
                print("[-] No GraphQL endpoints found in JS files.")
        else:
            print("[-] No common GraphQL endpoints found.")

    if not target_endpoint:
        print("[-] Could not detect any GraphQL endpoint. Exiting.")
        return

    print(f"[+] Using endpoint: {target_endpoint}")

    # Step 2: Introspection
    if args.introspect:
        print("[*] Performing introspection...")
        schema = introspect_schema(target_endpoint)
        if schema:
            print("[+] Introspection schema fetched.")
        else:
            print("[-] Introspection failed or disabled.")

    # Step 3: Injection engine
    if args.inject:
        print("[*] Starting GraphQL injection testing...")
        inject(target_endpoint)

    # Step 4: Mutation engine
    if args.mutate:
        print("[*] Running mutation fuzzer for logic bypass...")
        run_mutation_engine(
            base_url,
            target_endpoint,
            headers,
            threads=args.threads,
            timeout=args.timeout,
            retries=args.retries,
            verbose=args.verbose
        )

    # Step 5: Report generation
    if args.introspect or args.inject or args.mutate:
        generate_html_report(
            base_url,
            target_endpoint or "N/A",
            output_format=args.output,
            report_path=args.report
        )

    # Step 6: Auth Bypass
    if args.token or args.test_roles or args.header_fuzz:
        test_auth_bypass(base_url, target_endpoint, args)


if __name__ == "__main__":
    main()

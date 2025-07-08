import argparse
from core.endpoint_finder import detect_graphql_endpoint
from core.js_scraper import find_graphql_from_js
from core.schema_enum import introspect_schema
from core.injector import inject
from core.utils import generate_report
from core.auth_tester import test_auth_bypass
from core.mutation_engine import run_mutation_engine
from urllib.parse import urlparse
from datetime import datetime



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
    parser.add_argument("--output", choices=["html", "json", "markdown", "txt"], default="txt", help="Output report format")

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
        report_data = {
            "url": base_url,
            "endpoint": target_endpoint or "N/A",
            "introspected": bool(args.introspect),
            "injection_tested": bool(args.inject),
            "mutation_tested": bool(args.mutate)
        }

        # Always print to stdout
       #print("\nGraphQL Map Report")
        print("=" * 40)
        print(f"URL:                {report_data['url']}")
        print(f"GraphQL Endpoint:   {report_data['endpoint']}")
        print(f"Introspection:      {'✅' if report_data['introspected'] else '❌'}")
        print(f"Injection Tested:   {'✅' if report_data['injection_tested'] else '❌'}")
        print(f"Mutation Tested:    {'✅' if report_data['mutation_tested'] else '❌'}")
       #print(f"Generated On:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Only save report if output flag is given
        if args.output:
        domain = urlparse(base_url).netloc.replace('.', '_')
        report_path = args.report or f"output/{domain}_report.{args.output}"

        report_data = {
            "url": base_url,
            "endpoint": target_endpoint or "N/A",
            "introspected": bool(args.introspect),
            "injection_tested": bool(args.inject),
            "mutation_tested": bool(args.mutate)
        }

        generate_report(
            data=report_data,
            output_file=report_path,
            output_format=args.output
        )
        print(f"[+] Report saved to {report_path}") 
        
if __name__ == "__main__":
    main()

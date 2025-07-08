# core/endpoint_finder.py
import httpx

COMMON_ENDPOINTS = [
    "/graphql", "/api/graphql", "/graphiql", "/playground", "/gql", "/query", "/v1/graphql"
]

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def detect_graphql_endpoint(base_url):
    found_endpoints = []
    for path in COMMON_ENDPOINTS:
        full_url = base_url.rstrip("/") + path
        try:
            res = httpx.post(full_url, json={"query": "{}"}, headers=HEADERS, timeout=5)
            if "errors" in res.text or "Must provide query string" in res.text:
                found_endpoints.append(full_url)
        except Exception:
            continue
    return found_endpoints

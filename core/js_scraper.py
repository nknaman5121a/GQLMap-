# core/js_scraper.py

import httpx
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

GRAPHQL_REGEX = re.compile(r'["\'](\/[a-zA-Z0-9\/\-_]*graphql[a-zA-Z0-9\/\-_]*)["\']')

def extract_js_links(base_url):
    try:
        res = httpx.get(base_url, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        scripts = soup.find_all("script", src=True)
        js_links = [urljoin(base_url, script['src']) for script in scripts]
        return js_links
    except Exception as e:
        print(f"[!] Failed to extract JS links: {e}")
        return []

def find_graphql_in_js(js_links):
    graphql_endpoints = []
    for js_url in js_links:
        try:
            res = httpx.get(js_url, timeout=10)
            matches = GRAPHQL_REGEX.findall(res.text)
            for m in matches:
                if m not in graphql_endpoints:
                    graphql_endpoints.append(m)
        except:
            continue
    return graphql_endpoints

def find_graphql_from_js(base_url):
    js_links = extract_js_links(base_url)
    return find_graphql_in_js(js_links)

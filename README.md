# GQLMap - GraphQL Pentesting Automation

🔍 Auto-discover GraphQL endpoints  
⚙️ Perform introspection, injection, mutation fuzzing  
🛡️ Bypass authentication, test roles, and headers  
🧪 Injection payloads: SQLi, XSS, RCE, prototype pollution

---
## 🚀 Features

- Auto endpoint detection
- JavaScript crawling for hidden endpoints
- Full GraphQL introspection
- Injection engine with customizable payloads
- Mutation engine to break business logic
- Auth bypass and token/header fuzzing
- HTML, JSON, and Markdown reports

---
## 📦 Installation

```bash
git clone https://github.com/nknaman5121a/GQLMap.git
cd GQLMap
pip install -r requirements.txt
```
---
## 🔧 CLI Flags & Usage  
| Flag | Description |
|------|-------------|
| `url` | **(Required)** Target base URL (e.g. `https://example.com`) |
| `--endpoint` | Manually specify GraphQL endpoint |
| `--crawl` | Crawl JS files to find hidden GraphQL endpoints |
| `--introspect` | Run GraphQL introspection query |
| `--inject` | Perform injection fuzzing using `payloads.json` |
| `--mutate` | Run mutation-based fuzzing engine |
| `--token <token>` | JWT/Bearer token to use for auth |
| `--test-roles` | Check for role-based access control flaws |
| `--header-fuzz` | Fuzz headers to bypass authorization |
| `--threads <n>` | Run fuzzing using n threads (default: 5) |
| `--output <format>` | Export report to `json`, `html`, or `markdown` |
| `--report <file>` | Custom report output path |
| `--verbose` | Enable verbose logging |
| `--debug` | Enable debug logs |
| `--timeout <sec>` | Timeout for each request (default: 10) |
| `--retries <n>` | Number of retries on failure (default: 2) |

---
##Examples
# Auto-detect endpoint and run full recon
python gqlmap.py https://target.com --crawl --introspect

# Authenticated injection test
python gqlmap.py https://target.com --token abc.def.ghi --inject

# Full auth & mutation logic bypass fuzzing
python gqlmap.py https://target.com --token abc --test-roles --mutate

# Custom report path and format
python gqlmap.py https://target.com --inject --output html --report output/reports/target.html

🔓 Header fuzzing + token-based auth bypass
python gqlmap.py https://target.com --token xyz --header-fuzz

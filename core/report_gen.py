import os
import json
from datetime import datetime

REPORT_PATH = "output/reports/report.html"
LOG_PATH = "output/logs/injection_log.txt"
SCHEMA_PATH = "output/schema.json"

def generate_html_report(base_url, endpoint):
    print("[*] Generating HTML report...")

    # Load data
    schema_text = ""
    if os.path.exists(SCHEMA_PATH):
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_text = f.read()

    injection_results = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    injection_results.append(json.loads(line))
                except:
                    continue

    # Build HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>GQLmap Report</title>
    <style>
        body {{ font-family: Arial; background: #f5f5f5; padding: 20px; }}
        h1 {{ color: #333; }}
        .section {{ margin-bottom: 30px; }}
        .vuln {{ color: red; font-weight: bold; }}
        .ok {{ color: green; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; }}
        th {{ background-color: #f0f0f0; }}
        tr:hover {{ background-color: #f1f1f1; }}
    </style>
</head>
<body>
    <h1>GQLmap Report</h1>

    <div class="section">
        <h2>Target Info</h2>
        <p><strong>Base URL:</strong> {base_url}</p>
        <p><strong>Endpoint:</strong> {endpoint}</p>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <div class="section">
        <h2>Injection Test Results</h2>
        <table>
            <tr>
                <th>Field</th>
                <th>Payload</th>
                <th>Status Code</th>
                <th>Response Time (s)</th>
                <th>Status</th>
            </tr>"""

    for entry in injection_results:
        status = '<span class="vuln">VULNERABLE</span>' if entry["vulnerable"] else '<span class="ok">OK</span>'
        html += f"""
            <tr>
                <td>{entry["field"]}</td>
                <td>{entry["payload"]}</td>
                <td>{entry["status_code"]}</td>
                <td>{entry["response_time"]}</td>
                <td>{status}</td>
            </tr>"""

    html += """
        </table>
    </div>

    <div class="section">
        <h2>Introspected Schema (Raw)</h2>
        <pre style="white-space: pre-wrap; background: #fff; padding: 10px; border: 1px solid #ccc; max-height: 400px; overflow: auto;">"""
    
    html += schema_text[:5000] + ("..." if len(schema_text) > 5000 else "")
    
    html += """</pre>
    </div>

</body>
</html>
"""

    # Save HTML
    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] Report saved to {REPORT_PATH}")

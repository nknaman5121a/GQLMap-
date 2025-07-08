# core/utils.py

import os
import json

def generate_html_report(data, output_file="output/report.html"):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            f.write("<html><body><h1>GraphQL Map Report</h1><pre>")
            f.write(str(data))
            f.write("</pre></body></html>")
        print(f"[+] HTML Report saved to {output_file}")
    except Exception as e:
        print(f"[!] Failed to generate HTML report: {e}")

def save_to_report(data, filename="output/report.json"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] JSON Report saved to {filename}")
    except Exception as e:
        print(f"[!] Failed to save JSON report: {e}")

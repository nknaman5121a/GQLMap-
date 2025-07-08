# core/utils.py

import os
import json
import html

def generate_html_report(data, output_file="output/report.html", output_format="html"):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        if output_format == "html":
            with open(output_file, "w") as f:
                f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GQLMap Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        .container {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        pre {
            background: #f0f0f0;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>GraphQL Map Report</h1>
        <pre>""" + html.escape(json.dumps(data, indent=4)) + """</pre>
    </div>
</body>
</html>
""")
        elif output_format == "json":
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)
        elif output_format == "markdown":
            with open(output_file, "w") as f:
                f.write("# GraphQL Map Report\n\n```json\n")
                f.write(json.dumps(data, indent=4))
                f.write("\n```")
        print(f"[+] Report saved to {output_file}")
    except Exception as e:
        print(f"[!] Failed to generate report: {e}")


def save_to_report(data, filename="output/report.json"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[+] JSON Report saved to {filename}")
    except Exception as e:
        print(f"[!] Failed to save JSON report: {e}")

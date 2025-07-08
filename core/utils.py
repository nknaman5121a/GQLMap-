# core/utils.py
import os
import json
from datetime import datetime

def generate_report(data, output_file=None, output_format="txt"):
    try:
        # Set default file name based on URL
        domain = data.get("url", "report").replace("https://", "").replace("http://", "").replace("/", "_").strip("_")

        # Auto-select file path if not provided
        if output_file is None:
            output_file = f"output/{domain}_report.{output_format}"

        # Force correct extension if file extension does not match format
        ext = os.path.splitext(output_file)[1][1:]
        if ext != output_format:
            output_file = os.path.splitext(output_file)[0] + f".{output_format}"

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        if output_format == "html":
            with open(output_file, "w") as f:
                f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>GQLMap Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
        }}
        .summary {{
            font-size: 16px;
            line-height: 1.6;
        }}
        .status-true {{
            color: green;
            font-weight: bold;
        }}
        .status-false {{
            color: red;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>GraphQL Map Report</h1>
        <div class="summary">
            <p><strong>URL:</strong> {data.get("url", "N/A")}</p>
            <p><strong>GraphQL Endpoint:</strong> {data.get("endpoint", "N/A")}</p>
            <p><strong>Introspection:</strong> {'✅' if data.get("introspected") else '❌'}</p>
            <p><strong>Injection Tested:</strong> {'✅' if data.get("injection_tested") else '❌'}</p>
            <p><strong>Mutation Tested:</strong> {'✅' if data.get("mutation_tested") else '❌'}</p>
            <p><strong>Generated On:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </div>
</body>
</html>""")

        elif output_format == "json":
            with open(output_file, "w") as f:
                json.dump(data, f, indent=2)

        elif output_format == "markdown":
            with open(output_file, "w") as f:
                f.write("# GraphQL Map Report\n\n```json\n")
                f.write(json.dumps(data, indent=4))
                f.write("\n```")

        elif output_format == "txt":
            with open(output_file, "w") as f:
                f.write("GraphQL Map Report\n")
                f.write("=" * 40 + "\n")
                f.write(f"URL:                {data.get('url', 'N/A')}\n")
                f.write(f"GraphQL Endpoint:   {data.get('endpoint', 'N/A')}\n")
                f.write(f"Introspection:      {'✅' if data.get('introspected') else '❌'}\n")
                f.write(f"Injection Tested:   {'✅' if data.get('injection_tested') else '❌'}\n")
                f.write(f"Mutation Tested:    {'✅' if data.get('mutation_tested') else '❌'}\n")
                f.write(f"Generated On:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

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

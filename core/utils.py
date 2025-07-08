# core/utils.py

def generate_html_report(data, output_file="output/report.html"):
    try:
        with open(output_file, "w") as f:
            f.write("<html><body><h1>GraphQL Map Report</h1><pre>")
            f.write(str(data))
            f.write("</pre></body></html>")
        print(f"[+] Report saved to {output_file}")
    except Exception as e:
        print(f"[!] Failed to generate report: {e}")

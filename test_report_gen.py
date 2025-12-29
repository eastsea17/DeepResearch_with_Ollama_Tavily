import os
from report_generator import generate_html_report

# Mock data simulating the issue
mock_data_json = {
    "query": "Test JSON Parsing",
    "search_results": [{"results": [{"title": "Test Source", "url": "http://example.com", "content": "Test content"}]}],
    "final_answer": """
    Here is the result:
    ```json
    {
        "analysis": {
            "key_point": "**Bold Text** in JSON",
            "details": ["Item 1 with *Italic*", "Item 2"]
        },
        "conclusion": "Success"
    }
    ```
    """
}

# Mock data with plain markdown
mock_data_md = {
    "query": "Test Markdown",
    "search_results": [],
    "final_answer": "**This is bold text** and should be rendered as Markdown."
}

# Generate reports
import time
print("Generating JSON report...")
json_report_path = generate_html_report(mock_data_json)
print(f"JSON Report generated at: {json_report_path}")

time.sleep(2)

print("Generating Markdown report...")
md_report_path = generate_html_report(mock_data_md)
print(f"Markdown Report generated at: {md_report_path}")

# Read the generated files to verify content
with open(json_report_path, 'r') as f:
    content = f.read()
    if '<table' in content and '<strong>Bold Text</strong>' in content:
        print("PASS: JSON content rendered as HTML table AND markdown inside JSON is rendered.")
    else:
        print("FAIL: JSON content NOT rendered correctly.")
        if '<table' not in content:
            print("- Reason: Table not found")
        if '<strong>Bold Text</strong>' not in content:
            print("- Reason: Markdown inside JSON not rendered (expected <strong>Bold Text</strong>)")

with open(md_report_path, 'r') as f:
    content = f.read()
    if '<strong>This is bold text</strong>' in content:
        print("PASS: Markdown content rendered correctly.")
    else:
        print("FAIL: Markdown content NOT rendered correctly.")

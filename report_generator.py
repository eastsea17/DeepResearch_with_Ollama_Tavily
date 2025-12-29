import os
import datetime
import markdown
import json
import re
from config import ReportConfig

def _json_to_html(data):
    """
    Recursively converts a JSON object (dict or list) into an HTML structure.
    And renders markdown for string values.
    """
    if isinstance(data, dict):
        html = '<table style="width: 100%; border-collapse: collapse; margin-top: 10px;">'
        for key, value in data.items():
            html += f'<tr><th style="width: 30%; background-color: #f2f2f2; border: 1px solid #ddd; padding: 8px; vertical-align: top;">{key}</th>'
            html += f'<td style="border: 1px solid #ddd; padding: 8px;">{_json_to_html(value)}</td></tr>'
        html += '</table>'
        return html
    elif isinstance(data, list):
        html = '<ul>'
        for item in data:
            html += f'<li>{_json_to_html(item)}</li>'
        html += '</ul>'
        return html
    elif isinstance(data, str):
        # Render markdown content
        # Check if it's a simple string to avoid excessive <p> tags for short values?
        # Markdown usually wraps in <p>. 
        # For tables, <p> is fine.
        return markdown.markdown(data)
    else:
        return str(data)

def generate_html_report(data):
    """
    Generates an HTML report from the research data.
    
    Args:
        data (dict): Contains 'query', 'search_results', and 'final_answer'.
    
    Returns:
        str: The path to the generated HTML file.
    """
    query = data.get("query", "Unknown Query")
    search_results = data.get("search_results", [])
    final_answer = data.get("final_answer", "")
    
    # Create results directory if it doesn't exist
    results_dir = ReportConfig.RESULTS_DIR
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"research_report_{timestamp}.html"
    filepath = os.path.join(results_dir, filename)
    
    # Try to parse final_answer as JSON
    final_answer_html = ""
    json_parsed = False
    
    # Clean up <think> blocks if present
    cleaned_answer = re.sub(r"<think>.*?</think>", "", final_answer, flags=re.DOTALL).strip()
    
    # Attempt to find JSON block
    # Look for content between ```json and ``` or just start/end braces
    json_match = re.search(r"```json\s*(.*?)\s*```", cleaned_answer, re.DOTALL)
    if not json_match:
        json_match = re.search(r"(\{.*\})", cleaned_answer, re.DOTALL)
        
    if json_match:
        json_str = json_match.group(1) if json_match.lastindex else json_match.group(0)
        try:
            parsed_json = json.loads(json_str)
            final_answer_html = _json_to_html(parsed_json)
            json_parsed = True
        except json.JSONDecodeError:
            pass
            
    if not json_parsed:
        # Convert Markdown answer to HTML
        final_answer_html = markdown.markdown(final_answer)
    
    # Build HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Research Report: {query}</title>
        <style>
            body {{ font-family: sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; border-bottom: 2px solid #ecf0f1; padding-bottom: 10px; }}
            .section {{ margin-bottom: 30px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; vertical-align: top; }}
            th {{ background-color: #f2f2f2; }}
            .source-url {{ font-size: 0.9em; color: #7f8c8d; }}
            .answer {{ background-color: #f9f9f9; padding: 20px; border-radius: 5px; border: 1px solid #e0e0e0; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 5px; }}
        </style>
    </head>
    <body>
        <h1>Deep Research Report</h1>
        
        <div class="section">
            <h2>Research Topic</h2>
            <p><strong>{query}</strong></p>
        </div>
        
        <div class="section">
            <h2>Final Answer</h2>
            <div class="answer">
                {final_answer_html}
            </div>
        </div>
        
        <div class="section">
            <h2>Raw Search Results</h2>
            <table>
                <thead>
                    <tr>
                        <th>Source</th>
                        <th>Content Snippet</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for res in search_results:
        if "results" in res:
            for item in res["results"]:
                title = item.get("title", "No Title")
                url = item.get("url", "#")
                content = item.get("content", "No Content")
                
                html_content += f"""
                    <tr>
                        <td>
                            <strong>{title}</strong><br>
                            <a href="{url}" class="source-url" target="_blank">{url}</a>
                        </td>
                        <td>{content}</td>
                    </tr>
                """
    
    html_content += """
                </tbody>
            </table>
        </div>
        
        <div class="footer">
            <p>Generated by Deep Research Agent on """ + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        </div>
    </body>
    </html>
    """
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    return filepath

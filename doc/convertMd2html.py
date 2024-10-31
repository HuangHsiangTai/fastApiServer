import markdown2
import re
import yaml
import json
import sys

def find_openapi_snippets(md_text):
    """
    Finds all OpenAPI code snippets in the Markdown text.
    Returns the modified Markdown text and a list of OpenAPI specs with their placeholders.
    """
    pattern = re.compile(r'```(yaml|json)\n(.*?)```', re.DOTALL)
    openapi_snippets = []
    def replacer(match):
        language = match.group(1)
        code = match.group(2)
        try:
            # Parse the code block as YAML or JSON
            spec = yaml.safe_load(code) if language == 'yaml' else json.loads(code)
            if 'openapi' in spec:
                placeholder_id = len(openapi_snippets)
                placeholder = f'<div id="swagger-ui-{placeholder_id}"></div>'
                openapi_snippets.append((placeholder_id, spec))
                return placeholder
            else:
                return match.group(0)  # Keep the original code block
        except Exception:
            return match.group(0)  # Keep the original code block if parsing fails
    modified_md = pattern.sub(replacer, md_text)
    return modified_md, openapi_snippets

def markdown_to_html(md_text):
    """Converts Markdown text to HTML."""
    html = markdown2.markdown(md_text)
    return html

def generate_swagger_ui_scripts(openapi_snippets):
    """
    Generates JavaScript code to initialize Swagger UI instances for each OpenAPI spec.
    """
    scripts = ""
    for placeholder_id, spec in openapi_snippets:
        spec_json = json.dumps(spec)
        script = f"""
        <script>
        SwaggerUIBundle({{
            spec: {spec_json},
            dom_id: '#swagger-ui-{placeholder_id}',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
            ],
            layout: "BaseLayout"
        }});
        </script>
        """
        scripts += script
    return scripts

def generate_full_html(html_body, scripts):
    """
    Generates the complete HTML page with necessary CSS and JavaScript.
    """
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Markdown with OpenAPI</title>
        <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">
    </head>
    <body>
        {html_body}
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js"></script>
        {scripts}
    </body>
    </html>
    """
    return full_html

def convert_md_to_html(md_file_path, output_html_path):
    """Main function to convert Markdown to HTML with embedded OpenAPI UIs."""
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        md_text = md_file.read()
    
    # Find OpenAPI snippets and replace them with placeholders
    modified_md, openapi_snippets = find_openapi_snippets(md_text)
    
    # Convert the modified Markdown to HTML
    html_body = markdown_to_html(modified_md)
    
    # Generate scripts to initialize Swagger UI
    scripts = generate_swagger_ui_scripts(openapi_snippets)
    
    # Generate the full HTML with embedded Swagger UI
    full_html = generate_full_html(html_body, scripts)
    
    # Write the HTML to the output file
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(full_html)

# Usage example:
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python script.py input.md output.html")
    else:
        md_file_path = sys.argv[1]
        output_html_path = sys.argv[2]
        convert_md_to_html(md_file_path, output_html_path)

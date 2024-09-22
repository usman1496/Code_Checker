import subprocess
import json
import os
import re
from bs4 import BeautifulSoup
import importlib.util

def load_rules_from_python(file_path):
    spec = importlib.util.spec_from_file_location("validation_rule", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validation_rules

def lint_code(code: str, file_type: str) -> dict:
    file_name = f"temp.{file_type}"
    results = {
        "Html_errors": [],
        "custom_errors": [],
        "css_errors": [],
        "js_errors": [],
        "passes": []
    }

    try:
        # Write code to the temporary file
        with open(file_name, 'w') as file:
            file.write(code)

        # HTML Linting
        if file_type == "html":
            lint_command = r'"C:\\Users\\musma\\Desktop\\tidy\\tidy2_x64\\tidy.exe" -q -e ' + file_name
            try:
                result = subprocess.run(lint_command, shell=True, capture_output=True, text=True, check=True)
                output = result.stderr
                if output:
                    results["Html_errors"] = output.splitlines()
                else:
                    results["Html_errors"].append("No HTML Structural Errors Found.")
            except subprocess.CalledProcessError as e:
                results["Html_errors"].extend(e.stderr.splitlines() if e.stderr else ["Unknown error"])

            # Apply custom rules
            soup = BeautifulSoup(code, 'lxml', store_line_numbers=True)
            html_rules = load_rules_from_python('validation_rules.py')

            for rule_name, rule in html_rules.items():
                if "query_str" not in rule:
                    error_message = f"Rule '{rule_name}' is missing 'query_str'."
                    results["custom_errors"].append(error_message)
                    continue

                elements = soup.select(rule["query_str"])
                if len(elements) != rule.get("num_elems", 0):
                    if not elements:
                        potential_line_number = find_potential_error_line(rule["query_str"], code, file_type)
                        error_message = f"Line {potential_line_number}: No elements found: {rule_name} - {rule.get('error_msg', 'Error message not provided')}"
                        results["custom_errors"].append(error_message)
                    else:
                        for elem in elements:
                            line_number = getattr(elem, 'sourceline', find_element_line_number(elem, code))
                            error_message = f"Line {line_number}: {rule_name} - {rule.get('error_msg', 'Error message not provided')}"
                            results["custom_errors"].append(error_message)
                else:
                    pass_message = f"{rule_name} - Passed: {rule.get('pass_msg', 'Passed')}"
                    results["passes"].append(pass_message)

        # CSS Linting
        elif file_type == 'css':
            lint_command = r'"C:\\Users\\musma\\AppData\\Roaming\\npm\\stylelint.cmd" ' + file_name + ' --formatter json'
           
            try:
                result = subprocess.run(lint_command, shell=True, capture_output=True, text=True, encoding='utf-8', check=True)
                output = result.stdout
                lint_result = json.loads(output)

                # Process Prettier errors
                if lint_result and isinstance(lint_result, list):
                    for issue in lint_result[0].get("warnings", []):
                        line = issue.get("line", "Unknown")
                        column = issue.get("column", "Unknown")
                        text = issue.get("text", "Unknown error")
                        results["css_errors"].append(f"Prettier Error: {text} (line {line}, column {column})")
                else:
                    results["css_errors"].append("No Prettier linting errors found.")
            
            except subprocess.CalledProcessError as e:
                error_message = e.stderr.strip() if e.stderr else "No error message provided"
                results["css_errors"].append(f"Command failed with error: {error_message}")
            except json.JSONDecodeError:
                results["css_errors"].append("Error parsing Stylelint output.")
            except UnicodeDecodeError as e:
                results["css_errors"].append(f"Encoding error: {e}")
            except Exception as e:
                results["css_errors"].append(f"Unexpected error: {str(e)}")

            # Apply custom rules for CSS
            css_parsed = parse_css(code)
            css_rules = load_rules_from_python('rules.py')
            
            for rule_name, rule in css_rules.items():
                if "selector" in rule and "properties" in rule:
                    errors = validate_css_properties(css_parsed, rule)
                    if errors:
                        results["custom_errors"].extend(errors)
                    else:
                        pass_message = f"{rule_name} - Passed: {rule.get('pass_msg', '')}"
                        results["passes"].append(pass_message)

                if "selector" in rule and "max_specificity" in rule:
                    errors = validate_css_specificity(code, rule)
                    if errors:
                        results["custom_errors"].extend(errors)
                    else:
                        pass_message = f"{rule_name} - Passed: {rule.get('pass_msg', '')}"
                        results["passes"].append(pass_message)

                if "media_query" in rule and "selectors" in rule:
                    errors = validate_media_queries(code, rule)
                    if errors:
                        results["custom_errors"].extend(errors)
                    else:
                        pass_message = f"{rule_name} - Passed: {rule.get('pass_msg', '')}"
                        results["passes"].append(pass_message)
        # JavaScript Linting
        elif file_type == "js":
            lint_command = r'"C:\\Users\\musma\\AppData\\Roaming\\npm\\jshint.cmd" ' + file_name
            try:
                result = subprocess.run(lint_command, shell=True, capture_output=True, text=True)
                if result.returncode != 0:
                    if result.stderr.strip():
                        errors = result.stderr.splitlines()
                        results["js_errors"].extend([f'Error: {line}' for line in errors if line.strip()])
                    else:
                        results["js_errors"].append(result.stdout)
                else:
                    output = result.stdout.strip()
                    if output:
                        try:
                            lint_result = json.loads(output)
                            results["js_errors"].extend([f'{item["reason"]} (line {item["line"]}, column {item["character"]})' for item in lint_result])
                        except json.JSONDecodeError:
                            results["js_errors"].append(f"Error parsing linter output: {output}")
                    else:
                        results["js_errors"].append("No linting output produced.")

                # Apply custom JavaScript validation
                js_rules = load_rules_from_python('validation_rule.py')
                for rule_name, rule in js_rules.items():
                    if "query_str" in rule:
                        if rule["query_str"] in code:
                            results["custom_errors"].append(f"{rule_name} - {rule['error_msg']}")
                        else:
                            results["passes"].append(f"{rule_name} - Passed: {rule.get('pass_msg', 'P')}")

            except Exception as e:
                results["js_errors"].append(f"Unexpected error: {e}")

    finally:
        # Clean up temporary file
        if os.path.exists(file_name):
            os.remove(file_name)

    return results

def find_potential_error_line(query_str, code, file_type):
   
    if file_type == "html":
        tag_name = re.search(r'^[\w-]+', query_str)
        if tag_name:
            tag_pattern = rf'<{tag_name.group(0)}[^>]*>'
            match = re.search(tag_pattern, code)
            if match:
                start_pos = match.start()
                line_number = code.count('\n', 0, start_pos) + 1
                return str(line_number)
    elif file_type == "css":
        selector = re.search(r'^[^{\s]+', query_str)
        if selector:
            selector_pattern = rf'{re.escape(selector.group(0))}\s*{{'
            match = re.search(selector_pattern, code)
            if match:
                start_pos = match.start()
                line_number = code.count('\n', 0, start_pos) + 1
                return str(line_number)
    elif file_type == "js":
        match = re.search(re.escape(query_str), code)
        if match:
            start_pos = match.start()
            line_number = code.count('\n', 0, start_pos) + 1
            return str(line_number)

    # If no related tag is found, return 'Unknown'
    return "Unknown"

def find_element_line_number(element, html_code: str) -> str:
    pattern = re.escape(str(element))
    match = re.search(pattern, html_code)
    if match:
        start_pos = match.start()
        line_number = html_code.count('\n', 0, start_pos) + 1
        return str(line_number)
    else:
        return "Unknown"

def parse_css(css_code):
    parsed = {}
    selector = None
    line_number = 0
    
    for index, line in enumerate(css_code.splitlines(), start=1):
        line = line.strip()
        if line.endswith('{'):
            selector = line[:-1].strip()
            parsed[selector] = {"properties": [], "line": index}
        elif line.endswith('}'):
            selector = None
        elif selector:
            property_name = line.split(':')[0].strip()
            if property_name:
                parsed[selector]["properties"].append(property_name)
    return parsed

def validate_css_properties(css_parsed, rule):
    errors = []
    selector = rule["selector"]
    required_properties = rule["properties"]
    
    if selector not in css_parsed:
        errors.append(f"Missing selector: {selector}")
    else:
        properties = css_parsed[selector]["properties"]
        missing_properties = [prop for prop in required_properties if prop not in properties]
        if missing_properties:
            line_number = css_parsed[selector]["line"]
            errors.append(f"Line {line_number}: {rule['error_msg']} Missing properties: {', '.join(missing_properties)}")
    
    return errors

def validate_css_specificity(css_code, rule):
    errors = []
    selector = rule["selector"]
    max_specificity = list(map(int, rule["max_specificity"].split(',')))
    
    def calculate_specificity(selector):
        id_count = selector.count('#')
        class_count = selector.count('.') + selector.count('[') + selector.count(':')
        element_count = selector.count(' ') + selector.count('>') + selector.count('+') + selector.count('~') + 1
        return (0, id_count, class_count + element_count)

    css_parsed = parse_css(css_code)
    specificity = calculate_specificity(selector)
    
    if selector in css_parsed:
        line_number = css_parsed[selector]["line"]
    else:
        line_number = "Unknown"

    if specificity > tuple(max_specificity):
        errors.append(f"Line {line_number}: {rule['error_msg']}")

    return errors

def validate_media_queries(css_code, rule):
    errors = []
    media_query = rule["media_query"]
    required_selectors = rule["selectors"]

    if media_query not in css_code:
        errors.append(rule["error_msg"])
    else:
        media_query_block = re.search(rf'{re.escape(media_query)}\s*{{(.*?)}}', css_code, re.DOTALL)
        if media_query_block:
            media_query_css = media_query_block.group(1)
            parsed = parse_css(media_query_css)
            for selector in required_selectors:
                if selector not in parsed:
                    errors.append(rule["error_msg"])
        else:
            errors.append(rule["error_msg"])

    return errors

def format_lint_results(results: dict, file_type: str) -> str:
    output = []

    output.append("<b style='font-size: 20px;'>Results Summary</b>")
    output.append("<hr>")

    def sort_by_line_number(message):
        match = re.search(r'line (\d+)', message, re.IGNORECASE)
        return int(match.group(1)) if match else float('inf')

    # Sorting HTML Errors
    if file_type == "html":
        if results.get("Html_errors"):
            output.append("<b style='color: red; font-size: 16px;'>HTML Structural Errors:</b><br>")
            # Filter out empty errors before sorting
            sorted_html_errors = sorted(
                (error for error in results["Html_errors"] if error.strip()), 
                key=sort_by_line_number, 
                reverse=True
            )
            for error in sorted_html_errors:
                output.append(f"<span style='color: red; margin-left: 20px;'>- {error}</span><br>")
        else:
            output.append("<b style='color: green; font-size: 16px;'>No HTML Structural Errors Found</b><br>")

        # Sorting Custom Errors
        if results.get("custom_errors"):
            output.append("<b style='color: red; font-size: 16px;'>Custom Errors:</b><br>")
            # Reverse the sorted_custom_errors list to show latest errors first
            sorted_custom_errors = sorted(results["custom_errors"], key=sort_by_line_number, reverse=False)
            for error in sorted_custom_errors:
                output.append(f"<span style='color: red; margin-left: 20px;'>- {error}</span><br>")
        else:
            output.append("<b style='color: green; font-size: 16px;'>No Custom Errors Found</b><br>")

        # Reversing the order of passes to show the latest passes first
        if results.get("passes"):
            output.append("<b style='color: green; font-size: 16px;'>Passes:</b><br>")
            for message in reversed(results["passes"]):
                output.append(f"<span style='color: green; margin-left: 20px;'>- {message}</span><br>")
        else:
            output.append("<b style='color: red; font-size: 16px;'>No Passes</b><br>")

    # Sorting CSS Errors
    elif file_type == "css":
        if results.get("css_errors"):
            output.append("<b style='color: red; font-size: 16px;'>Structural CSS Errors:</b><br>")
            # Reverse the sorted_css_errors list to show latest errors first
            sorted_css_errors = sorted(results["css_errors"], key=sort_by_line_number, reverse=False)
            for error in sorted_css_errors:
                output.append(f"<span style='color: red; margin-left: 20px;'>- {error}</span><br>")
        else:
            output.append("<b style='color: green; font-size: 16px;'>No CSS Errors Found</b><br>")

        if results.get("custom_errors"):
            output.append("<b style='color: red; font-size: 16px;'>Custom CSS Errors:</b><br>")
            # Reverse the sorted_custom_css_errors list to show latest errors first
            sorted_custom_css_errors = sorted(results["custom_errors"], key=sort_by_line_number, reverse=False)
            for error in sorted_custom_css_errors:
                output.append(f"<span style='color: red; margin-left: 20px;'>- {error}</span><br>")
        else:
            output.append("<b style='color: green; font-size: 16px;'>No Custom CSS Errors Found</b><br>")

        # Reversing the order of passes to show the latest passes first
        if results.get("passes"):
            output.append("<b style='color: green; font-size: 16px;'>CSS Passes:</b><br>")
            for message in reversed(results["passes"]):
                output.append(f"<span style='color: green; margin-left: 20px;'>- {message}</span><br>")
        else:
            output.append("<b style='color: red; font-size: 16px;'>No CSS Passes</b><br>")

    # Sorting JS Errors
    elif file_type == "js":
        if results.get("js_errors"):
            output.append("<b style='color: red; font-size: 16px;'>Structural JS Errors:</b><br>")
            # Reverse the sorted_js_errors list to show latest errors first
            sorted_js_errors = sorted(results["js_errors"], key=sort_by_line_number, reverse=False)
            for error in sorted_js_errors:
                output.append(f"<span style='color: red; margin-left: 20px;'>- {error}</span><br>")
        else:
            output.append("<b style='color: green; font-size: 16px;'>No JS Errors Found</b><br>")

        if results.get("custom_errors"):
            output.append("<b style='color: red; font-size: 16px;'>Custom JS Errors:</b><br>")
            # Reverse the sorted_custom_js_errors list to show latest errors first
            sorted_custom_js_errors = sorted(results["custom_errors"], key=sort_by_line_number, reverse=False)
            for error in sorted_custom_js_errors:
                output.append(f"<span style='color: red; margin-left: 20px;'>- {error}</span><br>")
        else:
            output.append("<b style='color: green; font-size: 16px;'>No Custom JS Errors Found</b><br>")

        # Reversing the order of passes to show the latest passes first
        if results.get("passes"):
            output.append("<b style='color: green; font-size: 16px;'>JS Passes:</b><br>")
            for message in reversed(results["passes"]):
                output.append(f"<span style='color: green; margin-left: 20px;'>- {message}</span><br>")
        else:
            output.append("<b style='color: red; font-size: 16px;'>No JS Passes</b><br>")

    # Join the output without extra blank lines
    return "".join(output)

# Example usage
if __name__ == "__main__":
    code = '''${code}'''
    file_type = '${fileType}'

    result = lint_code(code, file_type)
    print(format_lint_results(result, file_type))

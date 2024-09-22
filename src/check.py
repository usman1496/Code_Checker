import subprocess
import json
import os
from bs4 import BeautifulSoup
import importlib.util

def load_rules_from_python(file_path):
    spec = importlib.util.spec_from_file_location("validation_rules", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validation_rules

def lint_code(code: str, file_type: str) -> dict:
    file_name = f"temp.{file_type}"
    results = {
        "tidy_errors": [],
        "custom_errors": [],
        "css_errors": [],
        "js_errors": [],
        "passes": []
    }

    try:
        with open(file_name, 'w') as file:
            file.write(code)

        if file_type == "html":
            lint_command = f'"C:\\Users\\musma\\Desktop\\tidy\\tidy2_x64\\tidy.exe" -q -e {file_name}'
            try:
                result = subprocess.run(lint_command, shell=True, capture_output=True, text=True, check=True)
                output = result.stderr
                results["tidy_errors"].extend(parse_tidy_output(output))
            except subprocess.CalledProcessError as e:
                results["tidy_errors"].extend(parse_tidy_output(e.stderr))

            soup = BeautifulSoup(code, 'html.parser')
            lines = code.splitlines()
            validation_rules = load_rules_from_python('validation_rules.py')

            for rule_name, rule in validation_rules.items():
                elements = soup.select(rule["query_str"])
                if len(elements) != rule["num_elems"]:
                    if not elements:
                        error_message = f"Line Unknown: No elements found: {rule_name} - {rule['error_msg']}"
                        results["custom_errors"].append(error_message)
                    else:
                        for elem in elements:
                            line_number = find_element_line_number(elem, lines)
                            error_message = f"Line {line_number}: {rule_name} - {rule['error_msg']}"
                            results["custom_errors"].append(error_message)
                else:
                    pass_message = f"{rule_name} - Passed"
                    results["passes"].append(pass_message)

        elif file_type == "css":
            lint_command = f'"C:\\Users\\musma\\AppData\\Roaming\\npm\\stylelint.cmd" {file_name} --formatter json'
            try:
                result = subprocess.run(lint_command, shell=True, capture_output=True, text=True, check=True)
                output = result.stdout
                lint_result = json.loads(output)
                results["css_errors"] = [f'{item["text"]} (line {item["line"]}, column {item["column"]})' for item in lint_result[0]["warnings"]]
            except subprocess.CalledProcessError as e:
                results["css_errors"].append(e.stderr.strip())
            except json.JSONDecodeError:
                results["css_errors"].append("Error parsing Stylelint output.")

        elif file_type == "js":
            lint_command = f'"C:\\Users\\musma\\AppData\\Roaming\\npm\\jshint.cmd" {file_name} --reporter json'
            try:
                result = subprocess.run(lint_command, shell=True, capture_output=True, text=True, check=True)
                output = result.stdout
                lint_result = json.loads(output)
                results["js_errors"] = [f'{item["reason"]} (line {item["line"]}, column {item["column"]})' for item in lint_result[0]["errors"]]
            except subprocess.CalledProcessError as e:
                results["js_errors"].append(e.stderr.strip())
            except json.JSONDecodeError:
                results["js_errors"].append("Error parsing JSHint output.")

    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

    return results

def parse_tidy_output(output: str) -> list:
    errors = []
    for line in output.splitlines():
        if line.strip():
            errors.append(line)
    return errors

def find_element_line_number(element, lines):
    if element is None:
        return "Unknown"

    tag_str = str(element)
    for i, line in enumerate(lines, start=1):
        if tag_str.strip() in line.strip():
            return i
    return "Unknown"

def format_lint_results(results: dict, file_type: str) -> str:
    output = []
    
    # Summary
    output.append("Linting Results Summary")
    output.append("=======================")

    # Tidy Errors
    if file_type == "html" and results["tidy_errors"]:
        output.append("\nTidy Errors:")
        for error in results["tidy_errors"]:
            output.append(f"  - {error}")
    elif file_type != "html" and results["tidy_errors"]:
        output.append("\nTidy Errors:")
        for error in results["tidy_errors"]:
            output.append(f"  - {error}")

    # Custom Errors
    if results["custom_errors"]:
        output.append("\nCustom Errors:")
        for error in results["custom_errors"]:
            output.append(f"  - {error}")
    else:
        output.append("\nNo Custom Errors")

    # CSS Errors
    if file_type == "css" and results["css_errors"]:
        output.append("\nCSS Errors:")
        for error in results["css_errors"]:
            output.append(f"  - {error}")
    elif file_type != "css" and results["css_errors"]:
        output.append("\nCSS Errors:")
        for error in results["css_errors"]:
            output.append(f"  - {error}")

    # JS Errors
    if file_type == "js" and results["js_errors"]:
        output.append("\nJS Errors:")
        for error in results["js_errors"]:
            output.append(f"  - {error}")
    elif file_type != "js" and results["js_errors"]:
        output.append("\nJS Errors:")
        for error in results["js_errors"]:
            output.append(f"  - {error}")

    # Passes
    if results["passes"]:
        output.append("\nPasses:")
        for pass_message in results["passes"]:
            output.append(f"  - {pass_message}")
    else:
        output.append("\nNo Passes")

    return "\n".join(output)

# Test code
if __name__ == "__main__":
    test_code = """<!DOCTYPE html>
<head>  
   
</head>
<body>
   
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li class="dropdown">
                <a href="#">Services</a>
                <ul class="dropdown-menu">
                    <li><a href="#">Consulting</a></li>
                    <li><a href="#">Development</a></li>
                    <li><a href="#">Support</a></li>
                </ul>
            </li>
            <li><a href="#">Contact</a></li>
        </ul>
    </nav>
    <main>
        <section class="card">
            <div class="card-header">Card Header</div>
            <div class="card-body">Card Body</div>
          
        </section>
    </main>
    <aside>
        <p>Additional information</p>
    </aside>
    <footer>
        <p>Footer Content</p>
    </footer>
</body>
</html>"""

    file_type = "html"
    results = lint_code(test_code, file_type)
    print(format_lint_results(results, file_type))


if __name__ == "__main__":
    js_code = '''
// Example HTML elements that the JS interacts with (you can imagine these being part of an HTML file):
// <img class="switch-image" src="image1.jpg" alt="Image" />

// Custom JS functions and interactions

document.querySelectorAll('.switch-image').forEach(function(imageElement) {
    // Event listener registration
    imageElement.addEventListener('click', function() {
        // Image switching on click
        imageElement.src = 'image2.jpg';
    });

    imageElement.addEventListener('dblclick', function() {
        // Image revert on double-click
        imageElement.src = 'image1.jpg';
    });
});

// Trigger a console error to test error handling rules
console.error('This is a test error');


    '''
    file_type = 'js'

    result = lint_code(js_code, file_type)
    print(format_lint_results(result, file_type))



    if __name__ == "__main__":
    js_code = '''
document.querySelectorAll('.switch-image').forEach(function(imageElement) {
    imageElement.addEventListener('click', function() {
        imageElement.src = 'image2.jpg';
    });

    imageElement.addEventListener('dblclick', function() {
        imageElement.src = 'image1.jpg';
    });
});

// Trigger a console error to test error handling rules
console.error('This is a test error');


    '''
    file_type = 'js'

    result = lint_code(js_code, file_type)
    print(format_lint_results(result, file_type))

    if __name__ == "__main__":
    css_code = '''
    body {
    background-color: #fff
    font-family: Arial, sans-serif;
 }

 .header {
    padding: 10px;
    background-color: #333;
    color: white;
 }

 .card {
    border: 1px solid #ccc;
    padding: 15px;
    margin: 10px;
 }

 .card-title {
    font-size: 18px;
    font-weight: bold
 }

 .card-footer {
    text-align: right;
    padding-top: 10px;
 }
 .important {
    /* Styles for .important */
 }
    '''
    file_type = 'css'

    result = lint_code(css_code, file_type)
    print(format_lint_results(result, file_type))
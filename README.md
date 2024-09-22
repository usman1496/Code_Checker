Assignment Checker is a JupyterLab extension designed to help students check their HTML, CSS, and JavaScript code. The extension provides immediate feedback by evaluating code against custom-defined rules and uses tools such as Stylelint, JSHint, and Tidy to catch common errors and enforce best practices. The extension integrates a Python backend with custom linting logic, making it easy for students to write clean, valid code.

Features
HTML, CSS, and JavaScript Validation: Automatically checks code quality and syntax issues in HTML, CSS, and JavaScript files.
Custom Rule Enforcement: The extension comes with task-related rules defined by instructors, ensuring students follow the specific guidelines for their assignments.
Integrated Tools:
Tidy: Used for validating HTML files and cleaning up the structure.
Stylelint: Ensures adherence to CSS coding standards and checks for common errors.
JSHint: Evaluates JavaScript code, flagging potential bugs and issues.
User-Friendly Interface: Adds a Check Code button to the notebook toolbar for quick code validation.
Requirements
Before running the extension, ensure you have the following tools installed locally:

Tidy: To validate HTML files.
Stylelint: For CSS validation.
JSHint: For JavaScript linting.
Install these tools locally by running:

bash
Copy code
# Install tidy (HTML Linter)
sudo apt-get install tidy  # For Linux
brew install tidy-html5    # For macOS
# For Windows, download the executable from https://github.com/htacg/tidy-html5

# Install Stylelint (CSS Linter)
npm install -g stylelint

# Install JSHint (JavaScript Linter)
npm install -g jshint
Installation
Step 1: Clone the Repository
First, clone the repository to your local machine:

bash
Copy code
git clone https://github.com/usman1496/Code_Checker.git
cd Code_Checker/src
Step 2: Build the Extension
Inside the src folder, run the following commands to build the extension:

bash
Copy code
jlpm install
jlpm build
Step 3: Install the Extension in JupyterLab
Once the extension is built, install it in JupyterLab by running:

bash
Copy code
jupyter lab extension install .
Step 4: Run JupyterLab
Now that the extension is installed, start JupyterLab:

bash
Copy code
jupyter lab
Usage
Once inside JupyterLab, follow these steps to check your code:

Open a notebook and create a code cell.
Write your HTML, CSS, or JavaScript code in the cell.
Click the Check Code button in the toolbar.
The extension will run your code through the linting process and display feedback in the notebook’s output section.
Custom Rule Checking
This extension goes beyond general linting by checking your code against custom-defined rules, which are tailored to specific tasks or assignments. These rules ensure that your code not only adheres to general best practices but also meets the requirements set by the instructor for the task at hand.

Example Output
After clicking Check Code, you will see the linting results in the output, which may include:

Warnings or errors for non-compliant code.
Suggestions to improve the structure or fix bugs.
Feedback about missing or incorrect implementations based on custom rules.
Development
If you'd like to contribute to this extension or make changes:

Ensure you have Node.js and npm installed.
Clone the repository and make your changes in the src folder.
Build the project using jlpm build and install it using jupyter lab extension install ..
Important Notes
Custom linting rules for HTML, CSS, and JavaScript are defined in the backend Python code. This ensures consistency in checking assignment-related requirements.
The backend Python code integrates with the linter tools to process and format the results, making the feedback user-friendly.

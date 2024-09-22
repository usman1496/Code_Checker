MYExtension is a JupyterLab extension designed for checking HTML, CSS, and JavaScript code directly within computational notebooks. It provides students with feedback on their code, using popular linting tools to analyze and suggest improvements. The backend is powered by Python, integrating Stylelint, JSHint, and Tidy to perform the code checks, while the frontend uses TypeScript to create a user-friendly interface and toolbar button.

// Features
HTML, CSS, and JavaScript code validation and feedback.
Displays results directly in the notebook's output area.
Python backend integrating:
1) Stylelint for CSS validation.
2) JSHint for JavaScript validation.
3) Tidy for HTML validation.
4) Easy-to-use "Check Code" button in the JupyterLab notebook toolbar.
//Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/usman1496/Code_Checker.git
2. Navigate to the src Folder
Go to the src folder where the extension files are located:

bash
Copy code
cd Code_Checker/src
3. Install Required Linting Tools
To run the code checks, you must install the following tools locally on your system:

Tidy (for HTML validation)
Stylelint (for CSS validation)
JSHint (for JavaScript validation)
Install Tidy:
On Linux:

bash
Copy code
sudo apt-get install tidy
On macOS:

bash
Copy code
brew install tidy-html5
On Windows, download the executable from Tidy's official website.

Install Stylelint:
bash
Copy code
npm install -g stylelint
Install JSHint:
bash
Copy code
npm install -g jshint
4. Build and Install the Extension
Rebuild the extension using the following command:

bash
Copy code
jlpm build
Install the extension in JupyterLab:

bash
Copy code
jupyter lab extension install .
5. Run JupyterLab
Once the tools are installed, you can run JupyterLab from the src folder:

bash
Copy code
jupyter lab
This will start JupyterLab, and the "Check Code" button will be available in the notebook toolbar.

How It Works
Open a JupyterLab notebook and write some HTML, CSS, or JavaScript code in a code cell.
Click the "Check Code" button in the notebook toolbar.
The extension will automatically detect the type of code (HTML, CSS, or JS) and run the appropriate linter (Tidy for HTML, Stylelint for CSS, and JSHint for JS).
The linting results will appear in the output area below the code cell, providing feedback and suggestions for improvement.
Development
The frontend of this extension is developed in TypeScript, which creates a button in the JupyterLab notebook toolbar.
The backend is implemented in Python and interacts with the linting tools to validate code and return feedback.
Contributing
Feel free to contribute by opening issues or submitting pull requests!

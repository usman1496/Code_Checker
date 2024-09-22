import nbformat as nbf

# Create a new notebook object
nb = nbf.v4.new_notebook()

# Assignment introduction
intro_text = """\
# HTML,CSS and JS Assignment

Welcome to your HTML, CSS and JS assignment! Please complete the following tasks:

1. Create a simple HTML page with a heading, paragraph, and a link.
2. Style the page using CSS to change the background color, text color, and font.

Once you're done, run the linter to check for errors or suggestions.
"""

# Add the introductory markdown cell
intro_cell = nbf.v4.new_markdown_cell(intro_text)
nb.cells.append(intro_cell)

# HTML task description
html_task = """\
## Task 1: Create HTML Structure

Write the HTML code for a simple webpage. It should include the following elements:

- A heading (e.g., `<h1>Welcome to My Page</h1>`)
- A paragraph (e.g., `<p>This is a paragraph of text on my webpage.</p>`)
- A link (e.g., `<a href="https://example.com">Click here</a>`)

You can write your HTML code in the cell below.
"""

# Add the HTML task markdown cell
html_task_cell = nbf.v4.new_markdown_cell(html_task)
nb.cells.append(html_task_cell)

# Add an empty code cell for HTML
html_code_cell = nbf.v4.new_code_cell("<!-- Write your HTML code here -->\n")
nb.cells.append(html_code_cell)

# CSS task description
css_task = """\
## Task 2: Add CSS Styling

Write the CSS code to style your HTML page. Your CSS should do the following:

- Change the background color of the page.
- Change the text color of the heading.
- Apply a different font to the paragraph.

You can write your CSS code in the cell below.
"""

# Add the CSS task markdown cell
css_task_cell = nbf.v4.new_markdown_cell(css_task)
nb.cells.append(css_task_cell)

# Add an empty code cell for CSS
css_code_cell = nbf.v4.new_code_cell("/* Write your CSS code here */\n")
nb.cells.append(css_code_cell)

# Save the notebook
with open("assignment.ipynb", "w") as f:
    nbf.write(nb, f)

print("Assignment notebook created: assignment.ipynb")

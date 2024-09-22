import unittest
from code_linter import lint_code, format_lint_results

class TestCSSLinting(unittest.TestCase):
    css_code = '''
    body {
        display: grid;
        grid-template-areas: "header" "content";
        grid-template-rows: 1fr 2fr;
        min-height: 100vh;
    }
    header {
        grid-area: header;
        display: flex;
        flex-flow: row wrap;
        border-radius: 5px;
        padding: 10px;
        background-color: #333;
    }
    nav ul {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        gap: 10px;
        padding: 0;
    }
    @media all and (min-width: 40em) {
        body { font-size: 18px; }
    }
    @media all and (min-width: 70em) {
        main > section > * { margin: 20px; }
    }
    '''

    def test_css_linting(self):
        result = lint_code(self.css_code, "css")
        print(format_lint_results(result, "css"))
        self.assertTrue(result["css_errors"], f"CSS Errors: {result['css_errors']}")

if __name__ == '__main__':
    unittest.main()

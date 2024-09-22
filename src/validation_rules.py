validation_rules = {
    "test_records_requirement_02_header": {
        "query_str": "body > header",
        "num_elems": 1,
        "error_msg": "Position 1 should contain an element that describes a header. Use the <header> element in HTML5."
    },
    "test_records_requirement_02_nav": {
        "query_str": "body > nav",
        "num_elems": 1,
        "error_msg": "Position 2 should contain an element that describes a navigation area. Use the <nav> element in HTML5."
    },
    "test_records_requirement_02_main": {
        "query_str": "body > main",
        "num_elems": 1,
        "error_msg": "Position 3 should contain an element that describes the main content area. Use the <main> element in HTML5."
    },
    "test_records_requirement_02_aside": {
        "query_str": "body > aside",
        "num_elems": 1,
        "error_msg": "Position 4 should contain an element that describes a complementary content area. Use the <aside> element in HTML5."
    },
    "test_records_requirement_02_footer": {
        "query_str": "body > footer",
        "num_elems": 1,
        "error_msg": "Position 5 should contain an element that describes a footer. Use the <footer> element in HTML5."
    },
    "test_records_requirement_03": {
        "query_str": "nav > ul",
        "num_elems": 1,
        "error_msg": "The navigation area should contain exactly one list. This can be an unordered or ordered list."
    },
    "nav_li_has_link": {
        "query_str": "nav > ul > li > a",
        "num_elems": 4,
        "error_msg": "Each <li> within <nav> should contain an <a> link."
    },
    "dropdown_has_links": {
        "query_str": ".dropdown-menu li > a",
        "num_elems": 3,
        "error_msg": "Each dropdown menu item should contain a link."
    },
    "nav_list_contains_li_only": {
        "query_str": "nav ul > *",
        "valid_elems": ["li"],
        "num_elems": 7,
        "error_msg": "Lists in the navigation area should only contain list items. Ensure that the list in the navigation contains exactly 7 list items."
    },
    "nav_contains_dropdown": {
        "query_str": "nav .dropdown",
        "num_elems": 1,
        "error_msg": "The navigation area should contain exactly one dropdown item with the class 'dropdown'."
    },
    "dropdown_contains_menu": {
        "query_str": "nav .dropdown > .dropdown-menu",
        "num_elems": 1,
        "error_msg": "The dropdown item should contain exactly one dropdown menu with the class 'dropdown-menu'."
    },
    "test_records_requirement_04": {
        "query_str": "main > section.card",
        "num_elems": 1,
        "error_msg": "The section acting as a card must have the appropriate class attribute value. It should not be a Header, Nav, Main, Aside, or Footer."
    },
    "card_has_footer": {
        "query_str": "section.card .card-footer",
        "num_elems": 1,
        "error_msg": "The card section must contain a footer."
    },
    "card_has_header": {
        "query_str": "section.card .card-header",
        "valid_elems": ["h1", "h2", "h3", "h4", "h5", "h6", "hgroup", "header"],
        "num_elems": 1,
        "error_msg": "The card section must contain a header. Consider using a heading element or a header element."
    },
    "card_has_body": {
        "query_str": "section.card .card-body",
        "valid_elems": ["p", "div"],
        "num_elems": 1,
        "error_msg": "The card section must contain a body. Use a paragraph or div element."
    },
    "card_has_image": {
        "query_str": "section.card .card-image",
        "valid_elems": ["img", "figure"],
        "num_elems": 1,
        "error_msg": "The card section should contain an image. Use the <img> element or a <figure> element containing the image."
    }
}

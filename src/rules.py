validation_rules = {
    "ensure_important_class": {
        "selector": ".important",
        "properties": ["color"],
        "error_msg": "The '.important' class must have a 'color' property."
    },
    "max_specificity": {
        "selector": "body .important",
        "max_specificity": "0,1,1",
        "error_msg": "Selector exceeds maximum specificity."
    },
    "media_query_check": {
        "media_query": "@media screen and (min-width: 600px)",
        "selectors": [".important"],
        "error_msg": "Media query '@media screen and (min-width: 600px)' must contain '.important' selector."
    },
    "ensure_common_selectors_properties": {
        "selectors": {
            "h1": ["font-size", "color"],
            "p": ["font-size", "line-height"],
            "a": ["text-decoration", "color"]
        },
        "error_msg": "Common selector '{selector}' must have the following properties: {properties}."
    },
    "validate_color_contrast": {
        "selector": ".important",
        "text_color_property": "color",
        "background_color_property": "background-color",
        "min_contrast_ratio": 4.5,
        "error_msg": "The contrast ratio between text color and background color in '.important' should be at least 4.5:1."
    },
    "avoid_important": {
        "selector": "*",
        "prohibited_usage": "!important",
        "error_msg": "Avoid using '!important' as it can lead to specificity issues."
    },
    "enforce_bem_naming": {
        "selector": "class",
        "regex_pattern": r"^([a-z]+(-[a-z]+)*)?(__[a-z]+(-[a-z]+)*)?(--[a-z]+(-[a-z]+)*)?$",
        "error_msg": "Class name '{class_name}' does not follow the BEM naming convention."
    },
    "consistent_units": {
        "selector": "*",
        "properties": ["margin", "padding", "width", "height"],
        "allowed_units": ["px", "em", "%"],
        "error_msg": "Properties within a selector should use consistent units. Found multiple units in '{selector}'."
    },
    "disallow_deprecated_properties": {
        "deprecated_properties": ["float", "text-shadow"],
        "error_msg": "The property '{property}' is deprecated and should not be used."
    },
    "check_vendor_prefixes": {
        "properties": {
            "transform": ["-webkit-transform", "-ms-transform", "transform"],
            "box-shadow": ["-webkit-box-shadow", "-moz-box-shadow", "box-shadow"]
        },
        "error_msg": "The property '{property}' requires vendor prefixes for cross-browser compatibility."
    },
    "validate_grid_layout": {
        "selector": ".grid-container",
        "required_properties": ["display: grid", "grid-template-columns", "grid-template-rows"],
        "error_msg": "The '.grid-container' selector should define a proper grid layout with 'grid-template-columns' and 'grid-template-rows'."
    }
}

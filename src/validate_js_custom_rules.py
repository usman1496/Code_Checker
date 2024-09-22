# validate_js_custom_rules.py

def validate_js_custom_rules(code, rules):
    errors = []

    # Check for event listeners
    if "event_listener_registration" in rules:
        event_listener_rule = rules["event_listener_registration"]
        event_listener_check = re.search(r"\.switch-image\s*\.\s*addEventListener\s*\(\s*'click'\s*,\s*switchImage\s*\)", code)
        if not event_listener_check:
            errors.append(event_listener_rule.get("error_msg", "Event listener registration error."))

    # Check for correct image switching on click
    if "image_switch_on_click" in rules:
        image_switch_check = re.search(r"switchImage\s*\(\s*\)\s*\{\s*document\.getElementById\('bulb1'\)\.setAttribute\s*\('src'\s*,\s*'http://localhost:8080/img/Dialog-information_on\.svg'\s*\)", code)
        if not image_switch_check:
            errors.append(rules["image_switch_on_click"].get("error_msg", "Image switching function error."))

    # Check for image revert on double-click
    if "image_revert_on_double_click" in rules:
        image_revert_check = re.search(r"switchImage\s*\(\s*\)\s*\{\s*document\.getElementById\('bulb2'\)\.setAttribute\s*\('src'\s*,\s*'http://localhost:8080/img/Dialog-information\.svg'\s*\)", code)
        if not image_revert_check:
            errors.append(rules["image_revert_on_double_click"].get("error_msg", "Image revert function error."))

    # Check for no console errors on page load
    if "no_console_errors_on_load" in rules:
        if "console.error" in code:
            errors.append(rules["no_console_errors_on_load"].get("error_msg", "Console errors found on page load."))

    # Check for no console errors after interaction
    if "no_console_errors_after_interaction" in rules:
        if "console.error" in code and ".switch-image" in code:
            errors.append(rules["no_console_errors_after_interaction"].get("error_msg", "Console errors found after interaction."))

    return errors

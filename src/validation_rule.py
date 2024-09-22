validation_rules = {
    "event_listener_registration": {
        "query_str": "script",
        "error_msg": "Event listener registration error."
    },
    "image_switch_on_click": {
        "query_str": "document.querySelector('.switch-image').addEventListener",
        "error_msg": "Image switching function error."
    },
    "image_revert_on_double_click": {
        "query_str": "document.querySelector('.switch-image').addEventListener",
        "error_msg": "Image revert function error."
    },
    "no_console_errors_on_load": {
        "query_str": "console.error",
        "error_msg": "Console errors found on page load."
    },
    "no_console_errors_after_interaction": {
        "query_str": "console.error",
        "error_msg": "Console errors found after interaction."
    }
}

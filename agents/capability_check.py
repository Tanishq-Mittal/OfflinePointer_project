import re


# Reject requests involving capabilities that the current fixture
# does not support. Check these BEFORE matching supported actions.
UNSUPPORTED_PATTERNS = [
    r"\bsearch\b",
    r"\bfind\b",
    r"\bprinter\b",
    r"\bprinting\b",
    r"\bprint settings\b",
    r"\b(text|font) colou?r\b",
    r"\bcolou?r\b",
    r"\bhighlight\b",
    r"\bunderline\b",
    r"\bdelete\b",
    r"\bundo\b",
    r"\bredo\b",
]


# Supported actions and their English/Hinglish variations.
ACTION_PATTERNS = {
    "bold": [
        r"\bbold\b",
        r"\bboldface\b",
        r"\bbold kar\b",
        r"\bbold karo\b",
        r"\bbold kar do\b",
    ],
    "italic": [
        r"\bitalic\b",
        r"\bitalics\b",
        r"\bitalicize\b",
        r"\bitalic kar\b",
        r"\bitalic karo\b",
        r"\bitalic kar do\b",
    ],
    "font_size": [
        r"\bbigger\b",
        r"\blarger\b",
        r"\bincrease font size\b",
        r"\bincrease the font size\b",
        r"\bfont size\b",
        r"\btext size\b",
        r"\bsize badha\b",
        r"\bsize badhao\b",
        r"\bfont badha\b",
        r"\bfont bada\b",
        r"\btext bada\b",
        r"\btext badi\b",
    ],
    "save": [
        r"\bsave\b",
        r"\bsave document\b",
        r"\bsave file\b",
        r"\bdocument save\b",
        r"\bfile save\b",
    ],
    "align_center": [
        r"\bcenter align\b",
        r"\bcentre align\b",
        r"\balign center\b",
        r"\balign centre\b",
        r"\bcenter\b",
        r"\bcentre\b",
        r"\bcenter mein\b",
        r"\bcentre mein\b",
        r"\bbeech mein align\b",
    ],
}


def check_capability(request: str, controls: list) -> tuple[bool, str]:
    """
    Check whether a request matches a supported action available
    in the supplied controls.

    Supports a limited set of English and Hinglish variations.
    This is a rule-based check, not a general language-understanding model.
    """

    text = request.lower().strip()

    if not text:
        return False, "The request is empty."

    # Support both Pydantic Control objects and dictionaries.
    available_ids = {
        control.id if hasattr(control, "id") else control.get("id")
        for control in controls
    }

    # Safety first: reject explicitly unsupported actions.
    for pattern in UNSUPPORTED_PATTERNS:
        if re.search(pattern, text):
            return False, (
                "The request involves an action that is not "
                "supported by the available controls."
            )

    # Live controls use generated ids, so the fixture whitelist cannot apply.
    # Defer to the model and the verifier in that case.
    if not any(cid in available_ids for cid in ACTION_PATTERNS):
        return True, "Live controls: model decides, verifier checks."

    # Match supported actions.
    matched_actions = []

    for control_id, patterns in ACTION_PATTERNS.items():
        if control_id not in available_ids:
            continue

        if any(re.search(pattern, text) for pattern in patterns):
            matched_actions.append(control_id)

    # Do not guess if the request matches multiple actions.
    if len(matched_actions) > 1:
        return False, (
            "The request appears to contain multiple actions. "
            "Please specify one action at a time."
        )

    if len(matched_actions) == 1:
        action = matched_actions[0]
        return True, f"Recognized supported action: {action}."

    return False, (
        "The request does not match a recognized supported action."
    )
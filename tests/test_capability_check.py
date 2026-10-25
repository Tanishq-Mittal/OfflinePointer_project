import pytest

from core.types import Control
from agents.capability_check import check_capability


CONTROLS = [
    Control(
        id="bold",
        name="Format > Font > Bold",
        role="menu item",
        x=230,
        y=45,
        w=60,
        h=22,
        enabled=True,
    ),
    Control(
        id="italic",
        name="Format > Font > Italic",
        role="menu item",
        x=230,
        y=70,
        w=60,
        h=22,
        enabled=True,
    ),
    Control(
        id="font_size",
        name="Format > Font > Bigger",
        role="menu item",
        x=230,
        y=95,
        w=90,
        h=22,
        enabled=True,
    ),
    Control(
        id="save",
        name="File > Save",
        role="menu item",
        x=45,
        y=20,
        w=60,
        h=22,
        enabled=True,
    ),
    Control(
        id="align_center",
        name="Format > Text > Center",
        role="menu item",
        x=260,
        y=125,
        w=90,
        h=22,
        enabled=True,
    ),
]


@pytest.mark.parametrize(
    "user_input",
    [
        "Bold",
        "Make this text bold",
        "Is text ko bold kar do",
    ],
)
def test_bold_variations_are_supported(user_input):
    supported, _ = check_capability(user_input, CONTROLS)
    assert supported is True


@pytest.mark.parametrize(
    "user_input",
    [
        "Make the text italic",
        "Italic kar do",
    ],
)
def test_italic_variations_are_supported(user_input):
    supported, _ = check_capability(user_input, CONTROLS)
    assert supported is True


@pytest.mark.parametrize(
    "user_input",
    [
        "Make the text bigger",
        "Font size badha do",
    ],
)
def test_font_size_variations_are_supported(user_input):
    supported, _ = check_capability(user_input, CONTROLS)
    assert supported is True


@pytest.mark.parametrize(
    "user_input",
    [
        "Save this document",
        "Document save kar do",
    ],
)
def test_save_variations_are_supported(user_input):
    supported, _ = check_capability(user_input, CONTROLS)
    assert supported is True


@pytest.mark.parametrize(
    "user_input",
    [
        "Center align the text",
        "Text ko center align karo",
    ],
)
def test_center_alignment_variations_are_supported(user_input):
    supported, _ = check_capability(user_input, CONTROLS)
    assert supported is True


@pytest.mark.parametrize(
    "user_input",
    [
        "Search",
        "Open printer settings",
        "Change the text color to blue",
        "Make the text bold and change its color to blue",
        "Delete this text",
        "Do something completely different",
    ],
)
def test_unsupported_requests_are_rejected(user_input):
    supported, _ = check_capability(user_input, CONTROLS)
    assert supported is False
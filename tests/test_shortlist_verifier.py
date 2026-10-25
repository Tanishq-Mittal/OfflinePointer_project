from core.types import Control, Result
from shortlist.fuzzy import make_shortlist
from verify.verifier import verify

def test_shortlist_keeps_all_when_small():
    controls = [{"id":"a","name":"Format > Font > Bold","role":"menu item",
                 "x":1,"y":1,"w":10,"h":10,"enabled":True}]
    assert len(make_shortlist("bold text", controls)) == 1

def test_verifier_rejects_unknown_id():
    controls = [Control(id="a", name="Save", x=1, y=1, w=10, h=10)]
    result = Result(status="ok", control_id="made-up", confidence=.99)
    control, caption = verify(result, controls)
    assert control is None
    assert "verified" in caption.lower()

def test_disabled_control_caption():
    controls = [Control(id="a", name="Format > Font > Bold", x=1, y=1,
                        w=10, h=10, enabled=False)]
    result = Result(status="ok", control_id="a", confidence=.99)
    control, caption = verify(result, controls)
    assert control is not None
    assert "greyed out" in caption

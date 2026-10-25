import json
from pathlib import Path
from core.types import Control

FIXTURE = Path(__file__).parent / "fixtures" / "textedit.json"

def read_fixture() -> list[Control]:
    data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return [Control.model_validate(item) for item in data]

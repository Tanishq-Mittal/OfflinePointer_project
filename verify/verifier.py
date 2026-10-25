from core.types import Control, Result

def verify(result: Result, controls: list[Control]) -> tuple[Control | None, str]:
    if result.status != "ok" or not result.control_id:
        return None, "I'm not sure. Here are the closest candidates: " + ", ".join(result.candidates)
    control = next((c for c in controls if c.id == result.control_id), None)
    if control is None or not control.name.strip() or control.w <= 0 or control.h <= 0:
        return None, "The selected control could not be verified."
    caption = control.name
    if not control.enabled:
        caption += " — it is here but greyed out"
    return control, caption

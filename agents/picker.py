import json
import time

from rapidfuzz import fuzz

from core.types import Control, PickerOutput, Result
from agents.ollama_client import chat
from agents.capability_check import check_capability
from config import (
    PICKER_MODEL,
    ESCALATION_MODEL,
    CONFIDENCE_THRESHOLD,
)


MIN_MATCH_SCORE = 35


def _rank_controls(
    request: str,
    controls: list[Control]
) -> list[tuple[Control, float]]:

    ranked = []

    for control in controls:
        if not control.name.strip():
            continue

        searchable_text = f"{control.name} {control.role}"

        score = max(
            fuzz.WRatio(request, control.name),
            fuzz.WRatio(request, searchable_text),
        )

        ranked.append((control, score))

    ranked.sort(key=lambda item: item[1], reverse=True)

    return ranked


def _ask(
    model: str,
    request: str,
    controls: list[Control]
):
    items = [
        {
            "id": c.id,
            "name": c.name,
            "role": c.role,
            "enabled": c.enabled,
        }
        for c in controls
    ]

    prompt = (
        "You select one existing UI control for the user's request. "
        "Only choose an ID from the supplied list. "
        "If none is suitable, return control_id null and confidence 0. "
        "Return JSON only with keys control_id, confidence, reason. "
        "Never invent IDs. Do not select unrelated controls.\n"
        f"User request: {request}\n"
        f"Controls: {json.dumps(items, ensure_ascii=False)}"
    )

    raw, tps, latency = chat(model, prompt)

    start = raw.find("{")
    end = raw.rfind("}")

    if start < 0 or end < start:
        raise ValueError("Model did not return valid JSON.")

    picked = PickerOutput.model_validate_json(raw[start:end + 1])

    return picked, tps, latency


def find_control(
    request: str,
    controls: list[Control]
) -> Result:

    started = time.perf_counter()

    request = request.strip()

    if not request:
        return Result(
            status="not_found",
            reason="The request is empty.",
        )

    if not controls:
        return Result(
            status="not_found",
            reason="No controls were available.",
        )

        # Reject requests that do not match an available capability.
    supported, capability_reason = check_capability(request, controls)

    if not supported:
        return Result(
            status="not_found",
            confidence=0.0,
            candidates=[],
            reason=capability_reason,
        )

    # Rank controls before asking the AI.
    ranked = _rank_controls(request, controls)

    if not ranked:
        return Result(
            status="not_found",
            reason="No named controls were available.",
        )

    # Preserve the best candidates for a possible fallback.
    top_candidates = [
        control.id
        for control, score in ranked[:3]
    ]

    best_score = ranked[0][1]

    # Reject requests that do not resemble any available control.
    # This prevents Search from matching unrelated formatting controls.
    if best_score < MIN_MATCH_SCORE:
        return Result(
            status="not_found",
            confidence=0.0,
            candidates=top_candidates,
            reason=(
                "No suitable control was found. "
                f"The best text-matching score was {best_score:.1f}."
            ),
        )

    # Give the AI the best-matching controls first.
    shortlist = [
        control
        for control, score in ranked[:35]
        if score >= MIN_MATCH_SCORE
    ]

    valid_ids = {control.id for control in controls}
    model_used = PICKER_MODEL
    total_latency = 0.0
    tps = None
    picked = None

    # First attempt, then one retry with the same model.
    for attempt in range(2):
        try:
            picked, tps, latency = _ask(
                model_used,
                request,
                shortlist,
            )

            total_latency += latency

            if (
                picked.control_id is not None
                and picked.control_id not in valid_ids
            ):
                raise ValueError("The model returned an unknown control ID.")

            if (
                picked.control_id is not None
                and picked.control_id not in {
                    control.id for control in shortlist
                }
            ):
                raise ValueError(
                    "The model selected a control outside the shortlist."
                )

            if (
                picked.control_id is not None
                and picked.confidence >= CONFIDENCE_THRESHOLD
            ):
                return Result(
                    status="ok",
                    control_id=picked.control_id,
                    confidence=picked.confidence,
                    candidates=top_candidates,
                    model_used=model_used,
                    latency_ms=total_latency,
                    tokens_per_sec=tps,
                    reason=picked.reason,
                )

        except Exception:
            if attempt == 1:
                picked = None

    # Escalate once if the primary model did not produce a valid,
    # sufficiently confident selection.
    model_used = ESCALATION_MODEL

    try:
        picked, tps, latency = _ask(
            model_used,
            request,
            shortlist,
        )

        total_latency += latency

        shortlist_ids = {
            control.id for control in shortlist
        }

        if (
            picked.control_id is not None
            and picked.control_id not in valid_ids
        ):
            raise ValueError("The escalation model returned an unknown ID.")

        if (
            picked.control_id is not None
            and picked.control_id not in shortlist_ids
        ):
            raise ValueError(
                "The escalation model selected a control outside the shortlist."
            )

        if (
            picked.control_id is not None
            and picked.confidence >= CONFIDENCE_THRESHOLD
        ):
            return Result(
                status="ok",
                control_id=picked.control_id,
                confidence=picked.confidence,
                candidates=top_candidates,
                model_used=model_used,
                latency_ms=total_latency,
                tokens_per_sec=tps,
                reason=picked.reason,
            )

        reason = (
            picked.reason
            if picked is not None
            else "The model did not return a reliable selection."
        )

    except Exception as exc:
        reason = f"Selection failed safely: {exc}"

    # Never report an uncertain selection as a successful one.
    return Result(
        status="low_confidence",
        confidence=(
            picked.confidence
            if picked is not None
            and picked.control_id is not None
            else 0.0
        ),
        candidates=top_candidates,
        model_used=model_used,
        latency_ms=(
            total_latency
            if total_latency > 0
            else (time.perf_counter() - started) * 1000
        ),
        tokens_per_sec=tps,
        reason=reason,
    )
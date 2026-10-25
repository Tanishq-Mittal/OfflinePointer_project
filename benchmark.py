import csv
import json
import time
from pathlib import Path

from agents.ollama_client import chat
from config import PICKER_MODEL, ESCALATION_MODEL

FIXTURE_PATH = Path("controls/fixtures/textedit.json")
OUTPUT_PATH = Path("benchmark_results.csv")

# Each request has a known expected result.
TEST_CASES = [
    ("Bold", "bold"),
    ("Make the text italic", "italic"),
    ("Make the text bigger", "font_size"),
    ("Save this document", "save"),
    ("Center align the text", "align_center"),
    ("Search", None),
    ("Open printer settings", None),
    ("Change the text color to blue", None),
]


def load_controls():
    with FIXTURE_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def select_control(model, request, controls):
    prompt = f"""
You are selecting a user interface control.

Choose a control only when it clearly matches the user's request.
If no suitable control exists, return null.
Never invent a control ID.

Return JSON only in this format:
{{"control_id": "bold", "confidence": 0.95, "reason": "..." }}

For no suitable control, return:
{{"control_id": null, "confidence": 0.0, "reason": "No matching control"}}

User request:
{request}

Available controls:
{json.dumps(controls, ensure_ascii=False)}
"""

    started = time.perf_counter()
    raw, tokens_per_sec, reported_latency = chat(model, prompt)
    elapsed_ms = (time.perf_counter() - started) * 1000

    # Find the JSON object, even if the model adds surrounding text.
    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end < start:
        raise ValueError("Model did not return a JSON object.")

    result = json.loads(raw[start:end + 1])

    selected_id = result.get("control_id")
    confidence = float(result.get("confidence", 0.0))

    valid_ids = {control["id"] for control in controls}

    if selected_id is not None and selected_id not in valid_ids:
        selected_id = "__INVALID_ID__"

    return {
        "selected_id": selected_id,
        "confidence": confidence,
        "latency_ms": round(elapsed_ms, 2),
        "reported_latency_ms": reported_latency,
        "tokens_per_sec": tokens_per_sec,
        "reason": result.get("reason", ""),
    }


def main():
    controls = load_controls()
    models = [PICKER_MODEL, ESCALATION_MODEL]
    results = []

    print("\nOFFLINEPOINTER MODEL BENCHMARK")
    print("=" * 55)
    print(f"Controls loaded: {len(controls)}")
    print(f"Test cases: {len(TEST_CASES)}")

    for model in models:
        print(f"\nTesting model: {model}")
        correct = 0
        errors = 0

        for request, expected_id in TEST_CASES:
            try:
                output = select_control(model, request, controls)
                selected_id = output["selected_id"]

                is_correct = selected_id == expected_id
                correct += int(is_correct)

                if selected_id == "__INVALID_ID__":
                    errors += 1

                row = {
                    "model": model,
                    "request": request,
                    "expected_id": expected_id or "NONE",
                    "selected_id": (
                        "INVALID_ID"
                        if selected_id == "__INVALID_ID__"
                        else selected_id or "NONE"
                    ),
                    "correct": is_correct,
                    "confidence": output["confidence"],
                    "latency_ms": output["latency_ms"],
                    "tokens_per_sec": output["tokens_per_sec"],
                    "reason": output["reason"],
                    "error": "",
                }

                print(
                    f"  Request: {request}\n"
                    f"  Expected: {expected_id or 'NONE'} | "
                    f"Selected: {row['selected_id']} | "
                    f"{'PASS' if is_correct else 'FAIL'} | "
                    f"{output['latency_ms']:.0f} ms\n"
                )

            except Exception as exc:
                errors += 1
                row = {
                    "model": model,
                    "request": request,
                    "expected_id": expected_id or "NONE",
                    "selected_id": "ERROR",
                    "correct": False,
                    "confidence": 0,
                    "latency_ms": "",
                    "tokens_per_sec": "",
                    "reason": "",
                    "error": str(exc),
                }
                print(f"  Request: {request} | ERROR: {exc}")

            results.append(row)

        accuracy = correct / len(TEST_CASES) * 100
        print(f"Results for {model}:")
        print(f"  Correct: {correct}/{len(TEST_CASES)}")
        print(f"  Accuracy: {accuracy:.1f}%")
        print(f"  Errors/invalid IDs: {errors}")

    if results:
        with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    print(f"\nDetailed results saved to: {OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
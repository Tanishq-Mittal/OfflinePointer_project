import argparse
import json
import subprocess
import sys
from pathlib import Path

from controls.reader import read_fixture
from core.types import Control
from shortlist.fuzzy import make_shortlist
from agents.picker import find_control
from verify.verifier import verify

ROOT = Path(__file__).resolve().parent


def read_live(app):
    """Read the real menus of `app` through the bash/AppleScript reader."""
    proc = subprocess.run(
        [str(ROOT / "controls" / "read_controls.sh"), app],
        capture_output=True, text=True,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        sys.exit("live reader failed: " + proc.stderr.strip())
    return [Control.model_validate(c) for c in json.loads(proc.stdout)]


def point(control, caption):
    """Glide the cursor to the control. Point only, never clicks."""
    subprocess.run([
        str(ROOT / "overlay" / "point_at.sh"),
        str(control.x), str(control.y),
        str(getattr(control, "w", 0) or 0), str(getattr(control, "h", 0) or 0),
        caption or control.name,
    ])


def main():
    parser = argparse.ArgumentParser(description="OfflinePointer local-model prototype")
    parser.add_argument("request", nargs="?", help="What control are you looking for?")
    parser.add_argument("--live", action="store_true", help="read the real app menus (macOS)")
    parser.add_argument("--app", default="TextEdit", help="app to read with --live")
    parser.add_argument("--point", action="store_true", help="move the cursor to the result")
    args = parser.parse_args()
    request = args.request or input("What do you want to find? ")
    controls = read_live(args.app) if args.live else read_fixture()
    print(f"controls: {len(controls)} ({'live' if args.live else 'fixture'})")
    short = make_shortlist(request, [c.model_dump() for c in controls])
    shortlist_controls = [Control.model_validate(c) for c in short]
    result = find_control(request, shortlist_controls)
    control, caption = verify(result, shortlist_controls)
    print("\nResult:", result.model_dump_json(indent=2))
    if control:
        print(f"\nTARGET: {control.name} at ({control.x}, {control.y})")
        print("Caption:", caption)
        if args.point:
            point(control, caption)
    else:
        print("\nFALLBACK:", caption)


if __name__ == "__main__":
    main()

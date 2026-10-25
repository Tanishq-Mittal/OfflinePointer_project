import argparse
from controls.reader import read_fixture
from core.types import Control
from shortlist.fuzzy import make_shortlist
from agents.picker import find_control
from verify.verifier import verify

def main():
    parser = argparse.ArgumentParser(description="OfflinePointer local-model prototype")
    parser.add_argument("request", nargs="?", help="What control are you looking for?")
    args = parser.parse_args()
    request = args.request or input("What do you want to find? ")
    controls = read_fixture()
    short = make_shortlist(request, [c.model_dump() for c in controls])
    shortlist_controls = [Control.model_validate(c) for c in short]
    result = find_control(request, shortlist_controls)
    control, caption = verify(result, shortlist_controls)
    print("\nResult:", result.model_dump_json(indent=2))
    if control:
        print(f"\nTARGET: {control.name} at ({control.x}, {control.y})")
        print("NOTE: this Windows prototype identifies the target; it does not move a macOS cursor.")
        print("Caption:", caption)
    else:
        print("\nFALLBACK:", caption)

if __name__ == "__main__":
    main()

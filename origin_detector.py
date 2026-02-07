import argparse
import json


def main() -> int:
    ap = argparse.ArgumentParser(description="Prompt Injection Origin Detector (MVP)")
    ap.add_argument("--trace", required=True, help="Path to JSONL trace file")
    args = ap.parse_args()

    events = []

    with open(args.trace, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict):
                    events.append(obj)
            except json.JSONDecodeError:
                continue

    print("")
    print("Prompt Injection Origin Detector (MVP)")
    print(f"Events loaded: {len(events)}")
    print("")

    for e in events:
        trace_id = e.get("trace_id")
        step = e.get("step")
        source = e.get("source")
        component = e.get("component")
        preview = e.get("preview", "")
        print(f"- trace={trace_id} step={step} source={source} component={component}")
        print(f"  preview: {preview[:120]}")

    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

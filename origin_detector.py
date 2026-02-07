import argparse
import json


INJECTION_PATTERNS = [
    "ignore previous instructions",
    "disregard previous instructions",
    "reveal the system prompt",
    "you are now the system",
    "act as the system",
    "bypass safety",
    "override the system",
]


def contains_injection(text: str) -> list[str]:
    text_l = text.lower()
    hits = []
    for p in INJECTION_PATTERNS:
        if p in text_l:
            hits.append(p)
    return hits


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

    # Sort by step just in case the file is out of order
    events.sort(key=lambda e: e.get("step", 0))

    print("")
    print("Prompt Injection Origin Detector (MVP)")
    print(f"Events loaded: {len(events)}")
    print("")

    first_hit = None

    for e in events:
        preview = e.get("preview", "")
        hits = contains_injection(preview)
        if hits and first_hit is None:
            first_hit = {
                "trace_id": e.get("trace_id"),
                "step": e.get("step"),
                "source": e.get("source"),
                "component": e.get("component"),
                "patterns": hits,
                "preview": preview,
            }

    if first_hit:
        print("Injection detected")
        print("")
        print(f"First seen at step {first_hit['step']}")
        print(f"Source: {first_hit['source']}")
        print(f"Component: {first_hit['component']}")
        print(f"Patterns: {', '.join(first_hit['patterns'])}")
        print("")
        print("Preview:")
        print(first_hit["preview"][:200])
        print("")
    else:
        print("No injection patterns detected.")
        print("")

    print("Timeline:")
    for e in events:
        step = e.get("step")
        source = e.get("source")
        component = e.get("component")
        preview = e.get("preview", "")
        hits = contains_injection(preview)
        marker = " <== injection appears here" if hits else ""
        print(f"- step {step} source={source} component={component}{marker}")

    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

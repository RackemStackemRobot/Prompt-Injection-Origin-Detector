import argparse
import json


INJECTION_PATTERNS = [
    ("ignore previous instructions", 40),
    ("disregard previous instructions", 40),
    ("reveal the system prompt", 50),
    ("you are now the system", 35),
    ("act as the system", 35),
    ("override the system", 35),
    ("bypass safety", 35),
    ("developer message", 20),
    ("system prompt", 15),
]


def find_hits(text: str):
    text_l = (text or "").lower()
    hits = []
    for pattern, weight in INJECTION_PATTERNS:
        if pattern in text_l:
            hits.append((pattern, weight))
    return hits


def clamp(n: int, lo: int, hi: int) -> int:
    if n < lo:
        return lo
    if n > hi:
        return hi
    return n


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

    events.sort(key=lambda e: e.get("step", 0))

    # Collect hits and find first appearance
    first_hit = None
    step_hits = []
    unique_patterns = set()
    total_weight = 0

    for e in events:
        preview = e.get("preview", "")
        hits = find_hits(preview)

        if hits:
            step_hits.append((e, hits))
            for p, w in hits:
                unique_patterns.add(p)
                total_weight += w

            if first_hit is None:
                first_hit = (e, hits)

    # Risk score: base on total weights + propagation
    propagation_bonus = 10 * max(0, len(step_hits) - 1)
    risk = clamp(total_weight + propagation_bonus, 0, 100)

    print("")
    print("Prompt Injection Origin Detector")
    print(f"Events loaded: {len(events)}")
    print("")

    if first_hit:
        origin_event, origin_hits = first_hit

        print("Summary")
        print("------")
        print(f"Risk score: {risk}/100")
        print(f"Signals found: {len(unique_patterns)} pattern(s)")
        print(f"Propagation: {len(step_hits)} step(s) contained injection signals")
        print("")
        print("Origin")
        print("------")
        print(f"Trace: {origin_event.get('trace_id')}")
        print(f"First seen at step: {origin_event.get('step')}")
        print(f"Source: {origin_event.get('source')}")
        print(f"Component: {origin_event.get('component')}")
        print(f"Patterns: {', '.join([p for p, _w in origin_hits])}")
        print("")
        print("Origin preview")
        print("--------------")
        print((origin_event.get("preview") or "")[:240])
        print("")
    else:
        print("Summary")
        print("------")
        print("No injection patterns detected.")
        print("Risk score: 0/100")
        print("")
        print("Timeline")
        print("--------")
        for e in events:
            step = e.get("step")
            source = e.get("source")
            component = e.get("component")
            print(f"- step {step} source={source} component={component}")
        print("")
        return 0

    print("Timeline")
    print("--------")
    for e in events:
        preview = e.get("preview", "")
        hits = find_hits(preview)
        step = e.get("step")
        source = e.get("source")
        component = e.get("component")

        if hits:
            patterns = ", ".join([p for p, _w in hits])
            print(f"- step {step} source={source} component={component}  HIT: {patterns}")
        else:
            print(f"- step {step} source={source} component={component}")

    print("")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

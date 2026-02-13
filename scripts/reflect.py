#!/usr/bin/env python3
"""
Kairos Daily Reflection — Demo Script

Reads today's signals from a JSONL file, analyzes trends,
and proposes persona dimension adjustments.

Usage:
    python reflect.py --signals-dir ./memory/signals --soul ./config/SOUL.md --baseline ./config/baseline.md

Or with sample data:
    python reflect.py --signals-dir ./examples --soul ./examples/soul-before.md --baseline ./templates/baseline.md --dry-run
"""

import json
import os
import sys
import argparse
from datetime import datetime, timedelta
from collections import defaultdict
from pathlib import Path

# ─── Config ──────────────────────────────────────────────

TREND_WINDOW_DAYS = 3
MAX_DRIFT_PER_DAY = 1
REBOUND_WINDOW_DAYS = 14
MAX_SELF_DISCOVERED = 4

DIMENSION_KEYWORDS = {
    "warmth": ["warm", "kind", "friendly", "cold", "harsh", "nice", "gentle", "caring"],
    "distance": ["formal", "casual", "stiff", "relaxed", "professional", "chill", "friendly"],
    "proactivity": ["initiative", "proactive", "autonomous", "anticipat", "just do it", "don't ask"],
    "humor": ["funny", "humor", "laugh", "joke", "lol", "haha", "witty", "amusing"],
    "caution": ["careful", "cautious", "bold", "risk", "safe", "trust", "autonomous"],
    "verbosity": ["short", "brief", "long", "verbose", "concise", "too much", "less", "more detail", "bullet"],
}

# ─── Signal Loading ──────────────────────────────────────

def load_signals(signals_dir: str, days: int = 7) -> dict[str, list[dict]]:
    """Load signals from JSONL files for the last N days."""
    signals_by_date = defaultdict(list)
    signals_path = Path(signals_dir)

    # Try both naming patterns
    for f in sorted(signals_path.glob("*.jsonl")):
        try:
            with open(f) as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    sig = json.loads(line)
                    date = sig["ts"][:10]
                    signals_by_date[date].append(sig)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ⚠ Skipping malformed signal in {f.name}: {e}", file=sys.stderr)

    return dict(signals_by_date)


def classify_signal(signal: dict) -> list[str]:
    """Map a signal to relevant dimensions based on keywords."""
    text = (signal.get("summary", "") + " " + signal.get("context", "")).lower()
    matches = []
    for dim, keywords in DIMENSION_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            matches.append(dim)
    return matches


# ─── Trend Detection ────────────────────────────────────

def detect_trends(signals_by_date: dict, window: int = TREND_WINDOW_DAYS) -> dict[str, dict]:
    """Detect multi-day trends for each dimension."""
    dim_signals = defaultdict(lambda: defaultdict(list))

    for date, signals in sorted(signals_by_date.items()):
        for sig in signals:
            dims = classify_signal(sig)
            for dim in dims:
                dim_signals[dim][date].append(sig)

    trends = {}
    for dim, by_date in dim_signals.items():
        dates_with_signals = sorted(by_date.keys())
        if len(dates_with_signals) >= window:
            # Calculate direction from signal types
            positive_types = {"approval", "emotion"}
            negative_types = {"correction"}
            
            total_intensity = 0
            signal_count = 0
            for date in dates_with_signals[-window:]:
                for sig in by_date[date]:
                    weight = sig.get("intensity", 3)
                    if sig["type"] in positive_types:
                        total_intensity += weight
                    elif sig["type"] in negative_types:
                        total_intensity -= weight
                    elif sig["type"] == "preference":
                        # Preferences indicate desired change
                        total_intensity += weight
                    else:  # style
                        total_intensity += weight * 0.5
                    signal_count += 1

            avg = total_intensity / signal_count if signal_count else 0
            direction = 1 if avg > 0 else -1 if avg < 0 else 0

            trends[dim] = {
                "direction": direction,
                "strength": abs(avg),
                "days": len(dates_with_signals),
                "total_signals": signal_count,
            }

    return trends


# ─── Reflection ──────────────────────────────────────────

def generate_reflection(signals_by_date: dict, trends: dict) -> str:
    """Generate a human-readable reflection report."""
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Count totals
    all_signals = []
    for sigs in signals_by_date.values():
        all_signals.extend(sigs)

    type_counts = defaultdict(int)
    for sig in all_signals:
        type_counts[sig["type"]] += 1

    lines = [
        f"# {today} Daily Reflection",
        "",
        "## Signal Summary",
        f"- Total signals analyzed: {len(all_signals)}",
        f"- Date range: {min(signals_by_date.keys())} to {max(signals_by_date.keys())}",
        f"- Breakdown: {', '.join(f'{t} ({c})' for t, c in sorted(type_counts.items()))}",
        "",
        "## Dimension Evaluation",
        "| Dimension | Direction | Strength | Days | Signals | Proposed Change |",
        "|-----------|-----------|----------|------|---------|----------------|",
    ]

    for dim, trend in sorted(trends.items()):
        direction = "↑" if trend["direction"] > 0 else "↓" if trend["direction"] < 0 else "—"
        change = f"+{MAX_DRIFT_PER_DAY}" if trend["direction"] > 0 else f"-{MAX_DRIFT_PER_DAY}" if trend["direction"] < 0 else "0"
        lines.append(
            f"| {dim} | {direction} | {trend['strength']:.1f} | {trend['days']} | {trend['total_signals']} | {change} |"
        )

    if not trends:
        lines.append("| — | — | — | — | — | No trends detected |")

    lines.extend([
        "",
        "## Proposed Actions",
    ])

    if trends:
        for dim, trend in sorted(trends.items()):
            if trend["direction"] != 0:
                action = "increase" if trend["direction"] > 0 else "decrease"
                lines.append(f"- **{dim}**: {action} by {MAX_DRIFT_PER_DAY} (trend strength: {trend['strength']:.1f})")
    else:
        lines.append("- No changes proposed (insufficient trend data)")

    return "\n".join(lines)


# ─── Main ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Kairos Daily Reflection")
    parser.add_argument("--signals-dir", required=True, help="Directory containing signal JSONL files")
    parser.add_argument("--soul", default=None, help="Path to current SOUL.md")
    parser.add_argument("--baseline", default=None, help="Path to baseline.md")
    parser.add_argument("--days", type=int, default=7, help="Days of signals to analyze (default: 7)")
    parser.add_argument("--dry-run", action="store_true", help="Print report without modifying files")
    parser.add_argument("--output", default=None, help="Output reflection to file (default: stdout)")
    args = parser.parse_args()

    print("🕰️  Kairos Daily Reflection")
    print(f"   Signals: {args.signals_dir}")
    print(f"   Window:  {args.days} days")
    print()

    # Load signals
    signals = load_signals(args.signals_dir, args.days)
    if not signals:
        print("⚠ No signals found. Nothing to reflect on.")
        return

    print(f"📊 Loaded {sum(len(v) for v in signals.values())} signals across {len(signals)} days")
    print()

    # Detect trends
    trends = detect_trends(signals)
    print(f"📈 Detected trends for {len(trends)} dimensions")
    print()

    # Generate reflection
    report = generate_reflection(signals, trends)
    print(report)

    if args.output and not args.dry_run:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w") as f:
            f.write(report)
        print(f"\n✅ Reflection saved to {args.output}")

    if args.dry_run:
        print("\n🔒 Dry run — no files modified")


if __name__ == "__main__":
    main()

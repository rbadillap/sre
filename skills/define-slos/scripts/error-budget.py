#!/usr/bin/env python3
"""Error budget for an SLO target over a window.

Usage:
  error-budget.py --slo 99.9 --window-days 30
  error-budget.py --slo 99.9 --window-days 30 --good 998500 --valid 1000000

Reads nothing, writes nothing: it only calculates.
"""

import argparse
import sys


def format_duration(minutes: float) -> str:
    if minutes >= 1440:
        return f"{minutes / 1440:.2f} days"
    if minutes >= 60:
        return f"{minutes / 60:.2f} hours"
    if minutes >= 1:
        return f"{minutes:.1f} minutes"
    return f"{minutes * 60:.1f} seconds"


def main() -> int:
    parser = argparse.ArgumentParser(description="Error budget for an SLO target over a window.")
    parser.add_argument("--slo", type=float, required=True, help="target in percent, for example 99.9")
    parser.add_argument("--window-days", type=float, required=True, help="SLO window in days, for example 30")
    parser.add_argument("--good", type=int, help="good events so far in the window")
    parser.add_argument("--valid", type=int, help="valid events so far in the window")
    args = parser.parse_args()

    if not 0 < args.slo < 100:
        print("error: --slo must be between 0 and 100, exclusive", file=sys.stderr)
        return 2
    if args.window_days <= 0:
        print("error: --window-days must be positive", file=sys.stderr)
        return 2
    if (args.good is None) != (args.valid is None):
        print("error: give --good and --valid together", file=sys.stderr)
        return 2

    allowed_bad = 1 - args.slo / 100
    window_minutes = args.window_days * 1440

    print(f"SLO: {args.slo}% over {args.window_days:g} days")
    print(f"Allowed failure: {allowed_bad * 100:.4g}% of valid events")
    print(f"As time fully down: {format_duration(allowed_bad * window_minutes)} per window")
    print(f"Per day, spread evenly: {format_duration(allowed_bad * 1440)}")

    if args.good is not None:
        if args.valid <= 0 or not 0 <= args.good <= args.valid:
            print("error: need 0 <= --good <= --valid and --valid > 0", file=sys.stderr)
            return 2
        bad = args.valid - args.good
        budget_events = allowed_bad * args.valid
        achieved = args.good / args.valid * 100
        consumed = bad / budget_events * 100 if budget_events else float("inf")
        print(f"Achieved so far: {achieved:.4f}%")
        print(f"Budget consumed: {consumed:.1f}% ({bad} bad of {budget_events:.0f} allowed at this volume)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

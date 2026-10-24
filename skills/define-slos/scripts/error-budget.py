#!/usr/bin/env python3
"""Error budget for an SLO target over a window.

Usage:
  error-budget.py --slo 99.9 --window-days 30
  error-budget.py --slo 99.9 --window-days 30 --good 998500 --valid 1000000
  error-budget.py --slo 95 --window-days 28 --events-per-window 20

Time-based figures only make sense for SLIs measured continuously (requests,
health samples). For SLIs counting rare events (releases, jobs, deployments),
pass --events-per-window and read the budget in events.

Reads nothing, writes nothing: it only calculates.
"""

import argparse
import math
import sys


def format_duration(minutes: float) -> str:
    if minutes >= 1440:
        return f"{minutes / 1440:.2f} days"
    if minutes >= 60:
        return f"{minutes / 60:.2f} hours"
    if minutes >= 1:
        return f"{minutes:.1f} minutes"
    return f"{minutes * 60:.1f} seconds"


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Error budget for an SLO target over a window.")
    parser.add_argument("--slo", type=float, required=True, help="target in percent, for example 99.9")
    parser.add_argument("--window-days", type=float, required=True, help="SLO window in days, for example 30")
    parser.add_argument("--good", type=int, help="good events so far in the window")
    parser.add_argument("--valid", type=int, help="valid events so far in the window")
    parser.add_argument("--events-per-window", type=float, help="expected valid events per window, for event-based SLIs")
    args = parser.parse_args()

    for name in ("slo", "window_days", "events_per_window"):
        value = getattr(args, name)
        if value is not None and not math.isfinite(value):
            return fail(f"--{name.replace('_', '-')} must be a finite number")
    if not 0 < args.slo < 100:
        return fail("--slo must be between 0 and 100, exclusive")
    if args.window_days <= 0:
        return fail("--window-days must be positive")
    if (args.good is None) != (args.valid is None):
        return fail("give --good and --valid together")
    if args.good is not None and (args.valid <= 0 or not 0 <= args.good <= args.valid):
        return fail("need 0 <= --good <= --valid and --valid > 0")
    if args.events_per_window is not None and args.events_per_window <= 0:
        return fail("--events-per-window must be positive")

    allowed_bad = 1 - args.slo / 100
    window_minutes = args.window_days * 1440

    print(f"SLO: {args.slo}% over {args.window_days:g} days")
    print(f"Allowed failure: {allowed_bad * 100:.4g}% of valid events")

    if args.events_per_window is not None:
        budget = allowed_bad * args.events_per_window
        print(f"Event-based: {budget:.2f} bad events allowed per window, out of {args.events_per_window:g}")
        if budget < 1:
            print("warning: the budget is less than one event; a single failure breaks the SLO.")
            print("         Lower the target, lengthen the window, or alert on every failure instead of a budget.")
    else:
        print(f"As time fully down: {format_duration(allowed_bad * window_minutes)} per window")
        print(f"Per day, spread evenly: {format_duration(allowed_bad * 1440)}")
        print("(Time figures assume a continuously measured SLI. For rare events, use --events-per-window.)")

    if args.good is not None:
        bad = args.valid - args.good
        budget_events = allowed_bad * args.valid
        achieved = args.good / args.valid * 100
        print(f"Achieved so far: {achieved:.4f}%")
        if budget_events < 1:
            print(f"Budget so far: {budget_events:.2f} bad events allowed at this volume; {bad} happened")
        else:
            print(f"Budget consumed: {bad / budget_events * 100:.1f}% ({bad} bad of {budget_events:.1f} allowed at this volume)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

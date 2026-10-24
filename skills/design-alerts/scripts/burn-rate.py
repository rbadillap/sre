#!/usr/bin/env python3
"""Burn rate thresholds for multiwindow error budget alerts.

Budget consumed = burn rate x (alert window / SLO window).
The default rows use the burn rates and windows recommended in the Google SRE
Workbook, chapter "Alerting on SLOs"
(https://sre.google/workbook/alerting-on-slos/): two page rows and one ticket.
Burn rates stay fixed for any SLO window; the budget each row consumes follows.

Usage:
  burn-rate.py --slo 99.9 --window-days 30
  burn-rate.py --slo 99.9 --window-days 28 --events-per-hour 600
  burn-rate.py --slo 99.9 --window-days 30 --consumed 3 --alert-hours 2

Reads nothing, writes nothing: it only calculates.
"""

import argparse
import math
import sys

# (severity, long window hours, short window minutes, burn rate)
DEFAULTS = [
    ("page", 1, 5, 14.4),
    ("page", 6, 30, 6.0),
    ("ticket", 72, 360, 1.0),
]
MIN_EVENTS = 100


def fail(message: str) -> int:
    print(f"error: {message}", file=sys.stderr)
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Burn rate thresholds for error budget alerts.")
    parser.add_argument("--slo", type=float, required=True, help="target in percent, for example 99.9")
    parser.add_argument("--window-days", type=float, required=True, help="SLO window in days, for example 30")
    parser.add_argument("--events-per-hour", type=float, help="typical valid events per hour, to check each window holds enough")
    parser.add_argument("--consumed", type=float, help="custom alert: percent of budget consumed, up to 100")
    parser.add_argument("--alert-hours", type=float, help="custom alert: long window in hours")
    args = parser.parse_args()

    for name in ("slo", "window_days", "events_per_hour", "consumed", "alert_hours"):
        value = getattr(args, name)
        if value is not None and not math.isfinite(value):
            return fail(f"--{name.replace('_', '-')} must be a finite number")
    if not 0 < args.slo < 100:
        return fail("--slo must be between 0 and 100, exclusive")
    if args.window_days <= 0:
        return fail("--window-days must be positive")
    if (args.consumed is None) != (args.alert_hours is None):
        return fail("give --consumed and --alert-hours together")
    if args.events_per_hour is not None and args.events_per_hour <= 0:
        return fail("--events-per-hour must be positive")

    allowed_bad = 1 - args.slo / 100
    window_hours = args.window_days * 24

    rows = [(sev, long_h, short_m, burn) for sev, long_h, short_m, burn in DEFAULTS]
    if args.consumed is not None:
        if not 0 < args.consumed <= 100 or args.alert_hours <= 0:
            return fail("--consumed must be above 0 and at most 100, and --alert-hours positive")
        burn = (args.consumed / 100) * window_hours / args.alert_hours
        rows.append(("custom", args.alert_hours, args.alert_hours * 60 / 12, burn))

    print(f"SLO {args.slo}% over {args.window_days:g} days: allowed failure {allowed_bad * 100:.4g}%")
    print(f"{'severity':<8} {'long':>7} {'short':>8} {'burn':>7} {'budget':>8} {'alert if error rate >':>22}")
    warnings = []
    for severity, long_h, short_m, burn in rows:
        if long_h > window_hours:
            warnings.append(f"{severity} {long_h:g}h: the alert window is longer than the SLO window.")
            continue
        consumed = burn * long_h / window_hours * 100
        threshold = burn * allowed_bad * 100
        print(f"{severity:<8} {long_h:>6g}h {short_m:>6g}m {burn:>7.2f} {consumed:>7.2f}% {threshold:>21.3f}%")
        if threshold >= 100:
            warnings.append(f"{severity} {long_h:g}h: the threshold is {threshold:.0f}%, which an error rate can't reach. "
                            "The target is too loose for this row; drop the row or alert on counts.")
        if burn < 1:
            warnings.append(f"{severity} {long_h:g}h: burn rate {burn:.2f} is below 1, so it fires while the service is within its SLO.")
        if args.events_per_hour is not None:
            short_events = args.events_per_hour * short_m / 60
            if short_events < MIN_EVENTS:
                warnings.append(f"{severity} {long_h:g}h: the {short_m:g}-minute window holds about {short_events:.0f} events. "
                                f"Below {MIN_EVENTS}, a few failures swing the rate: alert on counts or on every failure instead.")
    print("Fire only when both the long and the short window are over the threshold.")
    for warning in warnings:
        print(f"warning: {warning}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

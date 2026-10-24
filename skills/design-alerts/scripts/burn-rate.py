#!/usr/bin/env python3
"""Burn rate thresholds for multiwindow error budget alerts.

Budget consumed = burn rate x (alert window / SLO window).
Defaults follow the recommended parameters in the Google SRE Workbook,
chapter "Alerting on SLOs" (https://sre.google/workbook/alerting-on-slos/).

Usage:
  burn-rate.py --slo 99.9 --window-days 30
  burn-rate.py --slo 99.9 --window-days 30 --consumed 3 --alert-hours 2

Reads nothing, writes nothing: it only calculates.
"""

import argparse
import sys

# (severity, long window hours, short window minutes, budget consumed in percent)
DEFAULTS = [
    ("page", 1, 5, 2.0),
    ("page", 6, 30, 5.0),
    ("ticket", 72, 360, 10.0),
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Burn rate thresholds for error budget alerts.")
    parser.add_argument("--slo", type=float, required=True, help="target in percent, for example 99.9")
    parser.add_argument("--window-days", type=float, required=True, help="SLO window in days, for example 30")
    parser.add_argument("--consumed", type=float, help="custom alert: percent of budget consumed")
    parser.add_argument("--alert-hours", type=float, help="custom alert: long window in hours")
    args = parser.parse_args()

    if not 0 < args.slo < 100:
        print("error: --slo must be between 0 and 100, exclusive", file=sys.stderr)
        return 2
    if args.window_days <= 0:
        print("error: --window-days must be positive", file=sys.stderr)
        return 2
    if (args.consumed is None) != (args.alert_hours is None):
        print("error: give --consumed and --alert-hours together", file=sys.stderr)
        return 2

    allowed_bad = 1 - args.slo / 100
    window_hours = args.window_days * 24

    rows = [(sev, long_h, short_m, pct) for sev, long_h, short_m, pct in DEFAULTS]
    if args.consumed is not None:
        if args.consumed <= 0 or args.alert_hours <= 0:
            print("error: --consumed and --alert-hours must be positive", file=sys.stderr)
            return 2
        rows.append(("custom", args.alert_hours, args.alert_hours * 60 / 12, args.consumed))

    print(f"SLO {args.slo}% over {args.window_days:g} days: allowed failure {allowed_bad * 100:.4g}%")
    print(f"{'severity':<8} {'long':>7} {'short':>8} {'budget':>7} {'burn':>6} {'alert if error rate >':>22}")
    for severity, long_h, short_m, pct in rows:
        burn = (pct / 100) * window_hours / long_h
        threshold = burn * allowed_bad * 100
        print(
            f"{severity:<8} {long_h:>6g}h {short_m:>6g}m {pct:>6g}% {burn:>6.1f} {threshold:>21.3f}%"
        )
    print("Fire only when both the long and the short window are over the threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

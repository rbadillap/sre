# Alerting policy: <system>

<!-- Filled by the design-alerts skill. Label claims: verified (say how), hypothesis (say what would confirm it), not verified (say why). -->

Written on: <date>
Written by: <person or agent>

## Reframe

<!-- As it arrived, what that assumed, and the question answered instead. -->

## Alerts that exist

<!-- One row per alert, or write "no history available". -->

| Alert | Fired (last weeks) | Led to action? | Keep, change or delete |
|---|---|---|---|
| <alert> | <count> | <yes / no> | <decision> |

## Pages

<!-- Kind: symptom, budget burn (thresholds from the script) or rare event. -->

| Alert | Kind | Threshold | Windows (long / short) | Broken down by, minimum volume or "small by design" | Runbook | Owner | Label |
|---|---|---|---|---|---|---|---|
| <alert> | <kind> | <value> | <1h / 5m> | <group, volume> | <link> | <one person> | <label> |

## Tickets and dashboards

| Signal | Why it doesn't page | Goes to |
|---|---|---|
| <cause> | <reason, or the exception that makes it page> | <ticket / dashboard> |

## Past incidents

<!-- What the policy would have done. -->

| Incident | Would have paged? | When | If not, why that's acceptable or what changed |
|---|---|---|---|
| <link> | <yes / no> | <time after start> | <reason> |

## Review

Monthly review owner: <person>
Next review: <date>
On-call load reported to: <whoever sets priorities>

<!-- Each review adds a row. Out-of-hours pages are counted apart. -->

| Period | Pages | Out of hours | Didn't need action |
|---|---|---|---|
| <month> | <count> | <count> | <count> |

## Not verified

<!-- What you couldn't check, and why. -->

- <item>

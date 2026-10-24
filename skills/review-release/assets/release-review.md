# Release review: <release or change>

<!-- Filled by the review-release skill. One file per release. Label claims: verified (say how), hypothesis (say what would confirm it), not verified (say why). -->

Reviewed on: <date>
Reviewed by: <person or agent>
Change: <link to the diff, or "description only: ...">
Delivered by: <pipeline, scripts or tools>

## Reframe

<!-- As it arrived, what that assumed, and what this review actually checks. -->

## What users get

<!-- The release, not the deploy. -->

## State

| Category | What changes | Shared or per instance | Label |
|---|---|---|---|
| Data stores | <change, or none> | | |
| Caches | | | |
| Queues | | | |
| Files | | | |
| Stored configuration | | | |
| Delivery records (artifacts, versions, inventory) | | | |

## Compatibility

<!-- Shared state only. -->

| Transition | Safe? | How it's tested |
|---|---|---|
| <old reads new> | | |

## Way back

| Artifact | Rollback-safe or forward plan | Condition | How |
|---|---|---|---|
| <code, configuration, data change, infrastructure> | | <what the rollback depends on> | |
| After full release, found bad later | | | |

## Rollout

Smallest step: <size>
Gate between steps: <what it checks; person or script>

| Step | Group or share | Observation time | Waits for (effect and delay) | Abort if |
|---|---|---|---|---|
| 1 | | | | |

## Monitoring for the new behavior

<!-- Gaps, or "none". -->

## Verdict

<!-- Ready, ready with conditions, or not ready. -->

Conditions, if any:

1. <condition>

Options, if not ready:

| Option | Depends on |
|---|---|
| <option> | <condition> |

Decision owner: <person or role>
Accepted risks, if any: <what, and by whom>

## Not verified

- <item>

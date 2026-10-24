# Release review: <release or change>

<!-- Filled by the review-release skill. One file per release. -->

Reviewed on: <date>
Reviewed by: <person or agent>
Change: <link to the pull request or description>

## What users get

<!-- The release, not the deploy: what changes for people. -->

## State

<!-- Everything that outlives a process. Write "none: stateless change" if so. -->

| State | What changes | Old reads new? | New reads old? | How it's tested |
|---|---|---|---|---|
| <schema, cache, queue, file> | <change> | <yes / no> | <yes / no> | <test> |

## Way back

| Part of the change | Rollback-safe or forward plan | How |
|---|---|---|
| <part> | <rollback-safe / forward plan> | <steps> |

## Rollout

| Step | Share of traffic or users | Observation time | Compare on | Abort if |
|---|---|---|---|---|
| 1 | <5%> | <longer than the effect's delay> | <errors, latency, business signal> | <criteria> |

## Monitoring for the new behavior

<!-- What would show that the new behavior is failing. Mark gaps. -->

## Verdict

<!-- Ready, ready with conditions, or not ready. -->

## Options, if not ready

| Option | Condition |
|---|---|
| <option> | <only if...> |

Decision owner: <person or role>
Accepted risks, if any: <what, and by whom>

## Not verified

- <item>

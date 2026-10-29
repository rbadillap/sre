# Incident: <short description>

<!-- Filled by the respond-to-alert skill, as a running record. Add a line for every fact and action: when it happened, with its source and precision; when it was recorded, from the clock, if different; who did it; and, for an action, its status (proposed, done, result). -->

Started: <date and time, with time zone>
Severity: <level>
Declared as an incident: <yes, at time / no, and why>
Status: <investigating / mitigated / resolved>
Responder: <person>
Communications owner: <person, if different>

## Reframe

<!-- As it arrived, what that assumed, and the problem worked on instead. -->

## Impact

<!-- Confirmed impact only. Label anything not confirmed as a hypothesis. -->

- Who: <regions, tenants, users>
- What: <errors, latency, unavailable feature>
- Since: <time>

## What changed

<!-- Deploys, configuration, scheduled jobs, traffic, providers, certificates. Or "nothing found", with what was checked. -->

## Timeline

<!-- An action gets a new line for each status: proposed, done, result. Earlier lines stay, so the sequence isn't lost. -->

| Happened (source) | Recorded | Fact or action, and who | Status | Verified, hypothesis or not verified |
|---|---|---|---|---|
| <hh:mm, from log / record / person's report, or unknown> | <hh:mm from the clock, "same", or "unknown"> | <what was seen or done, by whom> | <for an action: proposed / done / result; "—" for a fact> | <label, and how it was verified> |
| 10:03 (error log) | 10:15 | Error rate at 40% in one region | — | verified: dashboard |
| 10:16 (proposed) | same | Pause the nightly job, undo by resuming it | proposed | — |
| 10:18 (person's report) | 10:19 | The on-call engineer paused the job | done | reported by the on-call engineer |
| 10:24 (error log) | 10:25 | Error rate back to normal | result | verified: dashboard |

## Hypotheses

| Hypothesis | Status | Evidence |
|---|---|---|
| <hypothesis> | <open / confirmed / ruled out> | <what showed it> |

## Mitigations

| Time | Action | How to undo it | Did it work? |
|---|---|---|---|
| <hh:mm> | <action> | <undo> | <signal that confirmed it> |

## Escalations

| Time | Who | Why |
|---|---|---|
| <hh:mm> | <person or team> | <criterion met> |

## Updates sent

| Time | To | Summary |
|---|---|---|
| <hh:mm> | <customers / team / leadership> | <what was said> |

## Handoff

- What happened:
- What was done, and why:
- Still open:
- Decided not to do:

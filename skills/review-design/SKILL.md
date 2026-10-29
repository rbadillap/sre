---
name: review-design
description: Reviews how a new or changed system will behave under failure before it carries real traffic, covering dependencies, shutdown and restart, capacity, retries and duplicate work, and what the team needs to operate it. Use for a production readiness review, before launching a service, before adding a dependency, or when a design will be hard to change later. Phrases like "production readiness", "is this ready for production", "review the architecture", "what can go wrong", "launch review".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: design
  sre-safety: proposes
---

# Review a design

**The question:** how does this system fail, and will the team know what to do when it does?

**The result:** `reliability/readiness/<system>.md`, from [the template](assets/readiness.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It reviews and writes findings. It changes nothing.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Establish what's reviewed.** A design document, the code, the running system, or a mix. Say which.
2. **Reframe.** Apply `reframe-first`. The question isn't whether it works, but how it fails and how fast it recovers.
3. **Map dependencies.** For each one: what happens to users when it's slow, when it's down, and when it comes back. Is the dependency critical, or can the system degrade without it?
4. **Check shutdown and restart.** What happens to work in progress when an instance stops: is it finished, handed back, or lost? How long does a stop take, and is the system given that long? What happens when everything restarts at once?
5. **Check health checks.** Each check answers one question: can it take work, does it need a restart, has it finished starting. No shared dependency in a check that restarts instances, or a small outage restarts everything.
6. **Check repeated and concurrent work.** Apply `idempotency` to anything retried or redelivered.
7. **Check state.** Apply `state-is-special`: where state lives, how it's backed up, and how its structure changes over time (`expand-contract`).
   - **Restores are tested as an ongoing practice, not once.** Look for an owner and a frequency with its reason; evidence of the last restore and its result, with the data checked usable and the recovery time measured; an alert if the test fails or stops running; and a new test after a relevant change to how recovery works. This skill reviews that practice. It doesn't schedule or run a restore.
8. **Check capacity and overload.** What's the limit, what happens past it (queue, shed, slow down, fall over), and is there room for an instance to fail or be replaced.
9. **Check operations.** Are there SLOs (`define-slos`), alerts that page on symptoms (`design-alerts`), a runbook for the first five minutes, and an owner? Can it be released in steps (`review-release`)?
10. **Write findings by risk,** each with what to change and whether it blocks the launch. Apply `paved-road` to the fixes. Label every claim (`evidence-before-claims`).

## Done when

- What was reviewed is named, and the reframe is written.
- Every dependency has its effect when slow, down and recovering, and is marked critical or not.
- Shutdown, restart, health checks, repeated work, state and capacity each have a finding or a "no issue found".
- Restore tests have an owner, a frequency with its reason, the last result with the data checked usable and the recovery time, an alert if they fail or stop, and a new test after relevant changes, or each missing part is a finding.
- Operations has SLOs, alerts, a runbook and an owner, or the gap is a finding.
- Every finding has a risk, a change and a blocking flag, and every claim is labeled.

Next: for missing SLOs or alerts, recommend `define-slos` or `design-alerts`; before launch, `review-release`.

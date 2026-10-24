---
name: evidence-before-claims
description: Discipline. Verify before saying something is true, and say what wasn't verified. Applied by the orchestrators in this package before stating a cause, declaring a fix effective or reporting a result.
license: MIT
metadata:
  sre-layer: discipline
---

# Evidence before claims

**Verify before saying something is true, and say what wasn't verified.**

## When

Before naming a cause, before saying a mitigation worked, before marking anything done, and in every written result.

## When not

Never skip it. When there's no time to verify, the claim is written as a hypothesis, and the work goes on.

## How

1. **Label every statement** as one of:
   - **Verified**: a signal, log, command output or record shows it. Say which.
   - **Hypothesis**: likely, not yet shown. Say what would confirm or rule it out.
   - **Not verified**: couldn't be checked. Say why.
2. **Turn hypotheses into checks.** "The job is exhausting connections" becomes a check: which clients hold the connections, and did the timing match?
3. **Test the action, not only the cause.** A mitigation is also an experiment. If the signal recovers after it, that supports the cause. If nothing changes, undo it and reconsider.
4. **Confirm with the signal users live.** A fix is effective when the user-facing signal recovers, not when the process restarts.

## The mistake it prevents

A guess travels as a fact, and the next decision is built on it.

---
name: respond-to-alert
description: Guides the response to a production alert or an incident. It scopes the problem, finds where it hurts, mitigates safely, communicates, and decides when to escalate. Use when an alert fires, users report errors or slowness, latency or error rates jump, or something is down. Phrases like "latency is up", "users can't log in", "we're getting 503s", "is this an incident", "should I wake someone up".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: respond
  sre-safety: proposes
---

# Respond to an alert

**The question:** what is hurting users, how do we stop it safely, and who else needs to be here?

**The result:** `reliability/incidents/<date>-<slug>.md`, from [the template](assets/incident.md), kept as a running timeline.

**Safety:** proposes. It reads signals and proposes actions. A person runs every action in production, and anything irreversible is a proposal with its risk.

**Disciplines:** the steps apply disciplines from this package by name. If one isn't installed, say so in the result and recommend installing the whole package. Don't guess its rule.

## Steps

1. **Start the timeline.** Create the incident file now, and add a line with the time for every fact and every action from here on.
2. **Reframe.** Apply `reframe-first`, and write the reframe in the record.
3. **Scope it.** Apply `scope-and-signal`: regions, tenants, errors or latency, since when. Write the unknowns as unknowns.
4. **Decide the severity, and declare if it's an incident.** If users are affected beyond the team's thresholds, declare it now and open a channel. Don't wait for the cause. Apply `verified-impact` for the first update, even without a cause.
5. **Follow the path of the request.** Walk the path users take, from the edge to the data: entry point, authentication, application, cache, queue, database, external dependencies. Compare latency and errors at each step to find where the time goes.
6. **Look for what changed, even with no deploy.** Configuration, scheduled jobs, traffic (one large customer, retries piling up), dependency or provider maintenance, certificates, data growth.
7. **Mitigate with what can be undone.** Apply `reversible-first`, including its check of second-order effects, and write each mitigation with how to undo it. If a mitigation touches data or state, apply `state-is-special` and hand it to a person.
8. **Confirm the mitigation worked.** Apply `evidence-before-claims`: the user-facing signal recovers. If nothing changes, undo it and reconsider the hypothesis. When the mitigation is a new release, it goes through the same checks that let the failure through, so its "success" proves little: confirm it over a window longer than the failure's delay.
9. **Escalate on clear criteria.** Bring in another person when any of these is true, and bring the context (what you checked, what you ruled out, what you think it is):
   - Users are still affected past the team's escalation threshold and there's no safe, reversible fix. If the team has none, use 15 to 20 minutes as a default, and list setting one as open in the handoff.
   - The fix touches data or state: a restore, a failover, a migration.
   - Security might be involved.
   - The cause is on a provider's side.
   - The incident is large enough that one person shouldn't fix and communicate at the same time.
10. **Keep updating.** Apply `verified-impact` on a regular rhythm until it's resolved.
11. **Close with a handoff.** When the impact is over, write what happened, what was done and why, what's still open, and what was decided not to do.

Investigation examples by platform are in [references/investigation.md](references/investigation.md).

## Done when

- The reframe is written.
- The scope is written: regions, groups, errors or latency, since when, with unknowns marked.
- The severity is set, and whether an incident was declared.
- What changed is written, or "nothing found" with what was checked.
- Every mitigation has its time, how to undo it, and whether it worked.
- Every escalation has its time and the criterion met, or "no escalation" with why.
- Every update sent is recorded.
- The user-facing signal is back to normal, confirmed.
- The timeline has every fact and action with its time and its label (verified, hypothesis, not verified).
- Every hypothesis is confirmed, ruled out or still open.
- The handoff is written.

Next: recommend `write-postmortem`.

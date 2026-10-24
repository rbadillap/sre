---
name: reconcile-drift
description: Handles infrastructure that no longer matches its code, separating what's dangerous from what's merely different, keeping an audit trail, and never applying blindly. Use when an infrastructure-as-code plan shows unexpected changes, when someone changed resources by hand, or when a plan wants to destroy or replace something important. Phrases like "terraform drift", "the plan wants to replace the database", "someone changed this in the console", "plan shows changes we didn't make".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: respond
  sre-safety: proposes
---

# Reconcile drift

**The question:** what changed outside the code, how dangerous is it, and how do code and reality match again without breaking anything?

**The result:** `reliability/changes/<date>-<slug>.md`, from [the template](assets/change-record.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It never runs an apply. Every change is a proposal for a person, with its audit trail.

## Steps

1. **Reframe.** Apply `reframe-first`. Drift that opens access (a public port, a broad permission) may be a security incident. If so, switch to `contain-security-incident` now.
2. **List every difference** between the code and reality, from a plan that only reads the current state. Don't apply anything yet.
3. **Sort them by urgency.** Apply `scope-and-signal`:
   - **Urgent:** opens access, exposes data, or weakens security.
   - **Dangerous to apply:** the plan would destroy or replace something with state (databases, volumes, buckets) or something others depend on (addresses, names, identifiers).
   - **Ordinary:** differences with no risk.
4. **Find who changed it and when,** from the audit logs: the identity, the time, the tool. Unknown identities, or the system's own identities changing things, point to a compromise.
5. **For each urgent difference, contain it narrowly.** Change only that rule or that permission, with your own named identity and a record of why. Before removing a permission, check what actually uses it, so the fix doesn't break a workload (`reversible-first`).
6. **For each dangerous one, find why the tool wants it.** Usually an attribute that forces replacement. Fix the code so the plan becomes an update or nothing. If a replacement is truly needed, plan it as its own change with a backup first and a way to switch over, not a destroy and create (`state-is-special`).
7. **For every difference, decide which side is right.** If the change in reality was correct, it goes into the code. If the code is right, reality goes back to it. Nothing stays as unexplained drift.
8. **Propose guardrails.** Apply `paved-road`: protection on stateful resources, a check in the pipeline that fails plans which destroy them, regular drift detection, and changes through the pipeline instead of by hand.
9. **Label every claim, and write the result.**

Tool examples: [references/terraform.md](references/terraform.md).

## Done when

- The reframe is written, and anything that opens access has been handed to `contain-security-incident`.
- Every difference is listed and sorted as urgent, dangerous to apply, or ordinary.
- Who changed what and when is written, from the audit logs, or marked not found.
- Every urgent difference has a narrow containment proposal; every dangerous one has its cause and a fix.
- Every difference has a decision: into the code, or back to the code.
- Guardrails are proposed, and every claim is labeled.

Next: for a replacement that's truly needed, recommend `review-release`; if the drift was unexplained, `write-postmortem`.

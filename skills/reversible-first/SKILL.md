---
name: reversible-first
description: Discipline. Stop the impact before finding the root cause, starting with actions that can be undone; anything irreversible waits for a person. Applied by the orchestrators in this package before proposing a mitigation, a rollback or a change in production.
license: MIT
metadata:
  sre-layer: discipline
---

# Reversible first

**Mitigate first with what can be undone, leaving anything irreversible to a person.**

## When

Whenever users are affected and a choice of action exists, and whenever a skill is about to propose a change in production.

## When not

When the mitigation itself would destroy what is needed later: evidence in a security incident, or data that a restore would overwrite. Then preserve first, and mitigate in a way that keeps it.

## How

1. **Prefer the action that can be undone:**

   | Instead of | Prefer |
   |---|---|
   | Deleting a job | Pausing it, and stopping its next scheduled run |
   | Blocking all traffic | Rate-limiting the one tenant or client causing it |
   | Deleting a compromised identity | Disabling it and revoking its sessions |
   | Rolling back a release that changed data | Turning off the feature flag |

2. **Check the second-order effect before acting.** Ask what the action does to everything around it. Scaling an application up can make a saturated database worse, because each new instance opens more connections. Restarting pods can drop work in progress.
3. **Write how to undo it, before doing it.** If the undo can't be written, the action isn't reversible.
4. **Hand irreversible actions to a person.** Deleting, restoring, failing over, migrating data and changing access always end in a proposal: what, why, the risk, and how it would be undone if it could.
5. **Confirm it worked.** After a mitigation, check the user-facing signal recovered. If it didn't, undo it and reconsider the cause.

## The mistake it prevents

Either users wait while the team searches for the root cause, or a fast fix causes a second incident.

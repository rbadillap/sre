---
name: plan-migration
description: Plans a change to stored data, schemas, indexes, cache formats or message formats so every running version keeps working and the way back is clear. Use before a database migration, a schema or index change, a change to a cache or message format, a data backfill, or moving data between systems. Phrases like "migration", "add a column", "change the index", "new cache format", "move the data", "is this migration safe".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: design
  sre-safety: proposes
---

# Plan a migration

**The question:** how does this structure change without a moment when a running version breaks, and how do we get out if it goes wrong?

**The result:** `reliability/migrations/<change>.md`, from [the template](assets/migration-plan.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It writes a plan. It runs no migration, restore or data change; every one of those is a step for a person.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Establish the change.** What structure changes, from what to what, and which code reads and writes it.
2. **Reframe.** Apply `reframe-first`. A migration isn't a deploy step: it changes data that outlives every version of the code, and a rollback won't undo it.
3. **List who reads and writes it.** Every version, service, job and tool, including the versions that will run at the same time during a rollout or after a rollback.
4. **Split it into steps.** Apply `expand-contract`. Write each step with what it adds, moves or removes, and the release it belongs to. Data copies run as their own step, separate from deploys.
5. **Check each step for safety.** For each one: can it run twice (`idempotency`)? Does it lock or slow what users use, and for how long? How big is it, and can it run in batches? What breaks if it stops halfway?
6. **Write the way back for each step.** Apply `state-is-special`. Mark each step reversible or not, and how. For a restore, say how much data written after the snapshot would be lost.
7. **Write how each step is verified.** What to check after it, such as counts, constraints or samples, before going to the next one.
8. **Mark the decisions for a person.** Every step that can't be undone, and every restore, is a decision with its risk, not a step that runs on its own (`reversible-first`).
9. **Label every claim.** Apply `evidence-before-claims`.
10. **Write the result.**

## Done when

- The change is established and the reframe is written.
- Everyone who reads or writes the structure is listed, including versions running together.
- Every step has what it does, its release, whether it can run twice, its impact on users, its size, what breaks if it stops halfway, its way back and its verification.
- Every irreversible step and every restore is marked as a decision for a person, with the data a restore would lose.
- Every claim is labeled verified, hypothesis or not verified.

Next: recommend `review-release` for each release in the plan.

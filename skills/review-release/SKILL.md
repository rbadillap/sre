---
name: review-release
description: Reviews a change before it ships to production, and proposes how to release it safely. Use before deploying, before approving a pull request that changes behavior, data formats, schemas, caches or infrastructure, or when someone asks to ship under time pressure. Phrases like "is this safe to deploy", "ready to ship", "can we release Friday", "the rollback didn't work", "plan the rollout".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: ship
  sre-safety: proposes
---

# Review a release

**The question:** will this change reach users safely, and can we get out if it doesn't?

**The result:** `reliability/releases/<release>.md`, from [the template](assets/release-review.md).

**Safety:** proposes. It reviews and writes a plan. It doesn't deploy, merge or change production.

## Steps

1. **Reframe.** Apply `reframe-first`. A deploy and a release are different: a deploy can succeed while the release fails. Review what users will get, not only whether the code installs.
2. **Find the state.** Apply `state-is-special`. List everything the change writes or reads that outlives a process: schemas, cache formats, queue messages, files, stored configuration. If there's none, say so and move faster.
3. **Check compatibility across versions.** Every version that can run at the same time during the rollout, or after a rollback, must read what the others write. Name the transitions that must be safe (old reads new, new reads old) and how they're tested.
4. **Decide the way back.** For each part of the change, mark it **rollback-safe** or **needs a forward plan**. Automated rollback only belongs where going back is actually safe. A snapshot is part of a recovery plan, not a safe rollback.
5. **Plan the rollout.**
   - Start with a small share of traffic or users, and grow in steps.
   - Set the observation time at each step longer than the delay of the effect you're waiting for. Something that shows after cache entries expire needs at least that long.
   - Compare the new version with the stable one on errors, latency, and the business signal the change touches (logins, payments, deliveries), with a minimum of traffic before deciding.
   - Write the abort criteria in advance.
   - If the change touches shared state, the formats must be compatible before the rollout starts, because a canary writing to a shared store can break the stable version.
6. **Check monitoring for the new behavior.** If nothing would show that the new feature is failing, that's a gap. Apply `scope-and-signal`.
7. **When it isn't ready, offer options, not a veto.** Apply `reversible-first`. Common options, each with its condition:
   - Ship it turned off behind a flag, and enable it when the team is present. Only if any data change is compatible on its own.
   - Enable it for one tenant first. Only if shared dependencies don't expose everyone else.
   - Ship with minimum conditions: a tested recovery or forward fix, monitoring for the new behavior, a named owner, and people available during and after.
8. **Name who decides.** This skill makes risks and options clear. The person who owns the business risk decides, within the policies that exist. Mandatory security or compliance controls go through their exception process. If the decision goes against the recommendation, record which risk was accepted and by whom.
9. **Write the result** in `reliability/releases/<release>.md`, marking what was verified and what was assumed (`evidence-before-claims`).

Platform-specific examples are in [references/progressive-delivery.md](references/progressive-delivery.md).

## Done when

- Every piece of state is listed, or the change is marked stateless.
- Every part of the change is marked rollback-safe or forward plan.
- The rollout has steps, observation times, comparison signals and abort criteria.
- If it isn't ready, the options are written with their conditions, and the decision owner is named.

Next: if the release fails in production, recommend `respond-to-alert`.

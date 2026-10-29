---
name: review-release
description: Reviews a change before it ships to production, and proposes how to release it safely. Use before deploying, before approving a pull request that changes behavior, data formats, schemas, caches, configuration or infrastructure, before an over-the-air update to a device fleet, or when someone asks to ship under time pressure. Phrases like "is this safe to deploy", "ready to ship", "can we release Friday", "plan the rollout".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: ship
  sre-safety: proposes
---

# Review a release

**The question:** will this change reach users safely, and can we get out if it doesn't?

**The result:** `reliability/releases/<release>.md`, from [the template](assets/release-review.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It reviews and writes a plan. It doesn't deploy, merge or change production.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Establish the change.** Read the diff, or the description if there's no diff yet, and say which one you reviewed. Also read how it will ship: the pipeline, scripts or tools that move it to production.
2. **Reframe.** Apply `reframe-first`. A deploy can succeed while the release fails. Review what users will get, not only whether the change installs.
3. **Find the state.** Apply `state-is-special`, for the change and for the delivery itself. Answer each category, writing "none" where it applies: data stores, caches, queues, files, configuration stored outside the code, and the records of the system that delivers the release (artifact names, versions, device or server inventory). Say for each whether it's shared across versions or kept per instance.
4. **Check compatibility across versions.** For shared state, name the transitions that must be safe during the rollout and after a rollback, and how they're tested.
5. **Decide the way back.** For each artifact the release ships (code, configuration, data change, infrastructure), mark it **rollback-safe** or **needs a forward plan**, with any condition the rollback depends on. Also write the way back after the release is fully out and found bad later.
6. **Plan the rollout.** Read [references/progressive-delivery.md](references/progressive-delivery.md) for your platform, then:
   - Release in steps: a share of traffic, a group of users or tenants, or a group of devices. Write how big the smallest step is.
   - **Name the gate between steps:** what it checks, and whether a person or a script moves to the next step.
   - Set the observation time at each step longer than the delay of the effects you're waiting for. List the candidate effects and their delays.
   - Write abort criteria in advance. Compare with the stable version when there's traffic to compare; when there isn't, use absolute thresholds.
7. **Check monitoring for the new behavior.** Apply `scope-and-signal`. If nothing would show that the new behavior is failing, it's a gap.
8. **Give a verdict: ready, ready with conditions, or not ready.** For "ready with conditions", list each condition. For "not ready", offer options with the condition each depends on, applying `reversible-first`. Typical options: ship it turned off and enable it later; release to the smallest group first and hold; ship with minimum conditions (a tested recovery or forward fix, monitoring for the new behavior, a named owner, people available during and after). Adapt them when there are no flags or tenants.
9. **Name who decides,** whatever the verdict. This skill makes risks and options clear; the person who owns the business risk decides, within existing policies. Mandatory security or compliance controls go through their exception process. If the decision goes against the recommendation, record which risk was accepted and by whom.
10. **Label every claim.** Apply `evidence-before-claims`.
11. **Write the result.**

## Done when

- The change reviewed is named (diff or description) and the reframe is written.
- Every state category is answered, including "none", and marked shared or per instance.
- Every artifact is marked rollback-safe or forward plan, with its conditions, and the way back after full release is written.
- The rollout names its steps, the gate between them, observation times with the effects they wait for, and abort criteria.
- Monitoring gaps for the new behavior are listed, or marked none.
- The verdict is given, with its conditions or options, and the decision owner is named.
- Every claim is labeled verified, hypothesis or not verified.

Next: if the release fails in production, recommend `respond-to-alert`.

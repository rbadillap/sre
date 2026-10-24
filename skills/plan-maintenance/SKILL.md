---
name: plan-maintenance
description: Plans maintenance that takes capacity away, such as draining nodes, upgrading clusters or hosts, rotating machines or updating devices in batches, so users don't notice. Use before node drains, cluster or OS upgrades, host replacements, or any maintenance window, and when past maintenance caused errors. Phrases like "drain the nodes", "cluster upgrade", "maintenance window", "errors during upgrades", "rotate the hosts".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: ship
  sre-safety: proposes
---

# Plan maintenance

**The question:** how do we take capacity away and give it back without users noticing?

**The result:** `reliability/runbooks/<maintenance>.md`, from [the template](assets/runbook.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It writes a runbook. A person runs every step.

## Steps

1. **Establish the maintenance.** What's taken away (nodes, hosts, devices), how many at a time, and for how long.
2. **Reframe.** Apply `reframe-first`. If past maintenance caused errors, compare what recovered fast with what didn't: the difference is usually replicas, shutdown handling or health checks, not the maintenance itself.
3. **Check each workload affected.** For each one:
   - **Replicas and spread:** enough instances, spread so one unit of maintenance never holds all of them.
   - **Disruption limits:** a limit on how many instances can be down at once, and enough replicas that the limit can be met, so maintenance isn't blocked forever.
   - **Shutdown:** the time a stop takes fits the time the platform allows, including any delay to let traffic move away first.
   - **Spare capacity:** room to place the instances being moved.
4. **Check state.** Apply `state-is-special`. For databases, queues and anything with a leader or a quorum, follow its own maintenance procedure: one member at a time, planned leader changes before taking a member away.
5. **Write the order and the batches.** Smallest batch first. Between batches, what must be true before continuing, and how long to wait.
6. **Write the stop conditions.** Which signals stop the maintenance, and what to do then (`reversible-first`): how to give capacity back.
7. **Write how to confirm it's done.** Every workload back to its replicas, no errors above normal, and anything that moved is healthy (`evidence-before-claims`).
8. **Label every claim, and write the result.**

Platform examples: [references/kubernetes.md](references/kubernetes.md).

## Done when

- The maintenance is established and the reframe is written.
- Every affected workload has its replicas, spread, disruption limit, shutdown time and spare capacity checked, or a finding.
- Stateful systems follow their own procedure, step by step.
- The order, batches, checks between batches and stop conditions are written.
- How to confirm completion is written, and every claim is labeled.

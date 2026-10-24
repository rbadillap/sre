# Maintenance on Kubernetes

Examples for step 3 of the skill.

## Drains

- `kubectl cordon <node>` stops new pods from landing on the node; `kubectl drain <node> --ignore-daemonsets` evicts the pods on it.
- A drain uses evictions, which respect PodDisruptionBudgets. Deleting pods directly skips them.
- When an eviction is refused because of a budget, the drain waits. Don't force it: a refusal means the budget doesn't allow another disruption right now.

## PodDisruptionBudgets

- `maxUnavailable: 1` or a percentage for larger services.
- With one replica and `minAvailable: 1`, no eviction is ever allowed, and the drain blocks forever. Run at least two replicas, or accept the disruption explicitly.
- Budgets apply to voluntary evictions such as drains. They don't control rolling updates; `maxUnavailable` and `maxSurge` in the Deployment do.

## Spread

- `topologySpreadConstraints` across nodes and zones, so one node or zone never holds every replica.

## Shutdown

- When a pod is evicted, it gets SIGTERM and is removed from Service endpoints at the same time, and routing updates aren't instant. A short `preStop` delay lets traffic move away before the application stops.
- `terminationGracePeriodSeconds` has to cover the `preStop` delay plus the application's own shutdown.

## Stateful workloads

- Follow the operator's procedure for the database or queue. For a replica set with a primary, step the primary down before draining its node, so the election is planned.

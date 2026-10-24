# Maintenance on Kubernetes

Examples for step 3 of the skill.

## Drains

- `kubectl cordon <node>` stops new pods from landing on the node; `kubectl drain <node> --ignore-daemonsets` evicts the pods on it.
- A drain refuses to evict pods that use `emptyDir` volumes unless you add `--delete-emptydir-data`, and that flag deletes the data in those volumes. Check which pods keep anything there before using it.
- A drain uses evictions, which respect PodDisruptionBudgets. Deleting pods directly skips them.
- When an eviction is refused because of a budget, the drain waits. Don't force it: a refusal means the budget doesn't allow another disruption right now.

## PodDisruptionBudgets

- `maxUnavailable: 1` or a percentage for larger services.
- With one replica and `minAvailable: 1`, no eviction is ever allowed, and the drain blocks forever. Run at least two replicas, or accept the disruption explicitly.
- Budgets apply to voluntary evictions such as drains. They don't control rolling updates; `maxUnavailable` and `maxSurge` in the Deployment do.

## Spread

- `topologySpreadConstraints` across nodes and zones, so one node or zone never holds every replica.

## Shutdown

- When a pod is evicted or deleted, it's marked as terminating, and its removal from Service endpoints starts in parallel with its shutdown. Shutdown runs the `preStop` hook first and sends SIGTERM only after the hook finishes. Routing updates aren't instant, so a short `preStop` delay keeps the process serving while traffic moves away.
- `terminationGracePeriodSeconds` has to cover the `preStop` delay plus the application's own shutdown.

## Stateful workloads

- Follow the operator's procedure for the database or queue. For a replica set with a primary, step the primary down before draining its node, so the election is planned.

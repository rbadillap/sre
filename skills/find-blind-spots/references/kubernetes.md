# Blind spots on Kubernetes

Examples of the patterns in the skill, for workloads running on Kubernetes.

## Success that isn't

- `kubectl apply` returns success when the API server accepts the object, not when the workload is healthy. A deploy step that ends at `apply` reports success while pods crash. Check the outcome with `kubectl rollout status deployment/<name> --timeout=<t>`, then watch for restarts during a soak period.
- A pod can be `Running` and `Ready` while restarting every few minutes. Watch the restart count over time, not only the current phase.
- A rollout can complete while a new version fails only under real traffic. Readiness proves the pod answers, not that requests succeed.

## Shallow health checks

- A readiness probe that only returns 200 from a handler proves the process runs. If the service needs its database, disk or a downstream, the probe should reflect that, without making every pod unready when a shared dependency blips.
- Never put a shared dependency in a liveness probe: when the dependency fails, every pod restarts at once.

## Failure before the request

- An ingress controller restarting under CPU pressure drops connections before they reach any service metric. Watch ingress errors and restarts, and node CPU, next to service metrics.
- NetworkPolicy, DNS (CoreDNS) and certificate expiry fail before the application sees anything.

## Averages

- Break request metrics down by namespace, deployment and version label, so one bad version inside a mixed rollout is visible.

## Silent backlogs

- Pending pods (`kubectl get pods --field-selector=status.phase=Pending`) mean work that can't be scheduled: no capacity, affinity or node selector rules nothing satisfies, a volume that can't be bound. (A PodDisruptionBudget doesn't cause Pending pods; it blocks evictions, which shows up as a drain that doesn't finish.)
- Evictions and `OOMKilled` events show up in `kubectl get events`, not in application metrics.

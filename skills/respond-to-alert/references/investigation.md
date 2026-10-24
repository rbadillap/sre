# Investigation, by platform

Examples for steps 5 to 7 of the skill.

## Kubernetes

- Pods restarting: `kubectl get pods`, then `kubectl describe pod <pod>` for events, and `kubectl logs <pod> --previous` for the container that died. Common causes: `OOMKilled`, a failing probe, a missing config or secret.
- Ingress failing liveness with node CPU near 100%: the ingress may lack CPU rather than be broken. Restarting it again won't help. Find what uses the CPU on those nodes, give the ingress reserved CPU (requests), and consider relaxing its liveness check while the cause is fixed.
- What changed: `kubectl rollout history`, recent events across namespaces (`kubectl get events -A --sort-by=.lastTimestamp`), and new DaemonSets or CronJobs.
- Pausing a CronJob without deleting it: `kubectl patch cronjob <name> -p '{"spec":{"suspend":true}}'`. Running jobs keep going; stop their pods only if the impact requires it.

## Databases

- Connection pool near its limit: find which clients hold the connections before blaming one. On MongoDB, `db.currentOp()` and connection counts by application name; on PostgreSQL, `pg_stat_activity` grouped by `application_name` and state.
- Slow queries: the slow query log, and whether a new query pattern started at the same time as the impact.
- Primary elections or failovers: check the replica set or cluster status and its recent events.

## Queues

- A backlog with no errors: check the age of the oldest message and the redelivery count. Messages that keep coming back point to a poison message or a consumer that crashes before acknowledging.

## Traffic

- One tenant flooding the service: break request rate down by tenant or API key, and rate-limit that one rather than all.
- Many clients behind one address: enterprise devices often share a single public IP, so a per-IP rate limit can block thousands of them while service metrics look normal.

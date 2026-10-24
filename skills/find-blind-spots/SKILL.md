---
name: find-blind-spots
description: Finds failures that current monitoring can't see, and proposes signals or checks to cover them. Use when dashboards look green but users complain, when something failed and no alert fired, when a tool reports "success" you don't trust, or before trusting a new system's monitoring. Phrases like "nothing alerted", "everything looks healthy", "how did we miss this", "is our monitoring enough".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: observe
  sre-safety: reads-only
---

# Find blind spots

**The question:** what can fail here without any signal noticing?

**The result:** `reliability/observability/blind-spots.md`, from [the template](assets/blind-spots.md). Create `reliability/` if it doesn't exist.

**Safety:** reads only. It looks at code, configuration and signals, and changes nothing except its own result file.

## Steps

1. **Reframe.** Apply `reframe-first`. The question isn't "do we have monitoring" but "would we know if someone couldn't do X". Write the reframe in the result.
2. **List what users need to do.** The few actions that matter. Users can be internal: an operator shipping a release or reaching a device is a user, as much as a customer logging in or paying.
3. **List the signals that exist.** For each one: what it measures, where it's measured (on the user's side, at the entry point such as a load balancer or ingress, in the service, or in a dependency), whether it pages, warns or only shows on a dashboard, and who sees it. If nothing pages anyone, write that down: it's the first gap.
4. **Look for failures before the request.** Before anything else, ask what can stop a user's action from ever reaching the system: name resolution, certificates, proxies, limits at the entry point, clients or devices that stop reporting. Signals measured inside the service can't see these.
5. **Check every pattern against every user action.** Use the table below. For each action, write the gaps found, and in one line the patterns that don't apply, so a reviewer can see they were considered.
6. **Rank the gaps.** Apply `scope-and-signal`. Rank by reach (how many users, devices or tenants) and by how long the failure could go unnoticed. Write both.
7. **Propose a signal or a check for each gap that matters.** A gap matters if it can reach more than one user or device, or go unnoticed for more than a day. Apply `paved-road`: a check in the pipeline can be better than an alert. Each proposal says what it measures or checks, where, whether it pages or warns, and its owner.
8. **Label every claim.** Apply `evidence-before-claims`, on signals as well as gaps.
9. **Write the result.**

## Patterns

| Pattern | What hides there | A signal or check that sees it |
|---|---|---|
| **Failure before the request** | Name resolution, certificates, proxies, limits at the entry point, clients that never connect | Expected versus actual activity per client or tenant; errors at the entry point; synthetic clients |
| **Sources that go silent** | Devices, agents or jobs that stop reporting. No report means no error | Last-seen time per source, with an alert on silence |
| **Success that isn't** | A tool reports success when it only started the work: a deploy that returns before the workload is healthy, a job that exits 0 having done nothing, a script whose pipeline hides a failed step | A check of the outcome, not the command |
| **Recovery that hides or fails** | An automatic restart that masks a fault; a rollback reported as done but never checked; a recovery that needs something already cleaned up | A signal on every automatic recovery, and a health check after it |
| **Shallow health checks** | A check that proves the process runs, not that it can do its job | A check that exercises what the service needs, without making a shared dependency restart everything |
| **Averages** | One tenant, region, device group or version failing inside a healthy total | The same signal broken down, with a minimum volume |
| **Delayed effects** | A failure that starts minutes or hours after a change: caches expiring, memory leaking, queues filling, disks growing | Signals watched over a window longer than the delay; growth rates, not only levels |
| **Silent backlogs** | Work that piles up without errors: retries, dead letters, uploads that stopped | Age of the oldest item; size of retry and dead-letter queues |
| **Alert routing** | Alerts that depend on metadata someone has to maintain, like ownership tags | A default set of alerts for everything; metadata only decides who gets them |
| **Identity** | A new client, device or credential accepted without anyone noticing | A signal on every new identity accepted |
| **The monitor itself** | A watcher that runs on the thing it watches, and fails with it | A heartbeat from the watcher, checked from somewhere else |

Platform examples: [references/kubernetes.md](references/kubernetes.md).

## Done when

- The reframe is written.
- Every user action has its gaps, or is marked covered with the signal that covers it, and lists the patterns that don't apply.
- Every gap has its reach, how long it could go unnoticed, and a rank.
- Every proposal says page or warn, or that it's a check, and has an owner.
- Every claim is labeled verified, hypothesis or not verified.

Next: for a gap that already caused an incident, recommend `write-postmortem`.

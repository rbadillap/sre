---
name: find-blind-spots
description: Finds failures that current monitoring can't see, and proposes signals to cover them. Use when dashboards look green but users complain, when something failed and no alert fired, when a tool reports "success" you don't trust, or before trusting a new service's monitoring. Phrases like "nothing alerted", "everything looks healthy", "how did we miss this", "is our monitoring enough".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: observe
  sre-safety: reads-only
---

# Find blind spots

**The question:** what can fail here without any signal noticing?

**The result:** `reliability/observability/blind-spots.md`, from [the template](assets/blind-spots.md).

**Safety:** reads only. It looks at code, configuration and signals, and changes nothing.

## Steps

1. **Reframe.** Apply `reframe-first`. "We have monitoring" is not the question; "would we know if users couldn't do X" is.
2. **List what users need to do.** Name the few actions that matter: log in, check for updates, pay, receive a notification. Each blind spot is measured against one of these.
3. **List the signals that exist.** For each one: what it measures, where it's measured (client, edge, service, dependency), and who gets paged.
4. **Ask what each signal can't see.** Go through every pattern below, for every user action. Write each gap with the user action it hides.
5. **Rank the gaps.** By how many users a failure would reach, and how long it could go unnoticed. Apply `scope-and-signal`: look at the worst tenant, not the average.
6. **Propose a signal for each gap that matters.** Each proposal names what it measures, where, and whether it should page or only warn. Prefer signals close to the user's experience. Apply `paved-road`: a proposal is a default or a check, not a reminder.
7. **Separate what you checked from what you assumed.** Apply `evidence-before-claims`. If you couldn't see a signal's configuration, say so.
8. **Write the result** in `reliability/observability/blind-spots.md`.

## Patterns to check

| Pattern | What hides there | A signal that sees it |
|---|---|---|
| **Failure before the request** | DNS, TLS, proxies, certificates, rate limits at the edge, clients that never connect. Request metrics only count what arrives | Expected versus actual activity per client or tenant; edge errors (TLS, auth, rate limit); synthetic clients |
| **Success that isn't** | A tool reports success when it only started the work: a deploy that returns before the workload is healthy, a job that exits 0 having done nothing | A check of the outcome, not the command: the workload healthy after a soak period, the job's output present |
| **Shallow health checks** | A check that proves the process runs, not that it can do its job: write to disk, reach the database | A check that exercises what the service needs, without making a shared dependency restart everything |
| **Averages** | One tenant, region or version failing inside a healthy total | The same signal broken down by tenant, region and version, with a minimum volume |
| **Delayed effects** | A failure that starts minutes or hours after a change: caches expiring, queues filling, disks growing | Signals watched across a window longer than the delay; growth rates, not only levels |
| **Silent backlogs** | Work that piles up without errors: retries, dead letters, uploads that stopped | Age of the oldest item, size of retry and dead-letter queues |
| **Alert routing** | Alerts that depend on metadata someone has to maintain, like ownership tags. Missing metadata means no alert | A default set of alerts for every service; metadata only decides who gets them |

Platform-specific examples are in [references/kubernetes.md](references/kubernetes.md).

## Done when

- Every user action from step 2 has its gaps listed, or is marked as covered, with the signal that covers it.
- Every proposed signal says page or warn.
- The result is written, and what wasn't verified is marked.

Next: for a gap that already caused an incident, recommend `write-postmortem`.

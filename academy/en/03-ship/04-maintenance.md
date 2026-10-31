---
title: "Maintenance"
stage: ship
order: 4
status: approved
teaches: "Plan maintenance that takes capacity away: check what each step removes and what comes back empty, set batches, and write what stops the work and what you do then."
sources:
  - title: "Slack Engineering, Slack's Incident on 2-22-22"
    url: https://slack.engineering/slacks-incident-on-2-22-22/
  - title: "Google Cloud, Networking Incident #19009 (June 2, 2019)"
    url: https://status.cloud.google.com/incident/cloud-networking/19009
  - title: "Kubernetes, Safely Drain a Node"
    url: https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/
  - title: "Kubernetes, Disruptions"
    url: https://kubernetes.io/docs/concepts/workloads/pods/disruptions/
skills: [plan-maintenance]
version: "0.1.1"
---

# Maintenance

_Sources: [Slack's report on its incident of February 22, 2022](https://slack.engineering/slacks-incident-on-2-22-22/), [Google's report on its network incident of June 2, 2019](https://status.cloud.google.com/incident/cloud-networking/19009), and the Kubernetes documentation: [Safely Drain a Node](https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/) and [Disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)._

## The question

Maintenance takes capacity away on purpose. How do you take it away and give it back without users noticing, and what makes you stop?

## What happened at Slack

Slack calls this work maintenance on its Consul agents, which run on each instance and handle service discovery (how services find each other). Memcached, its cache, sits in front of its databases.

- **The plan:** a step upgraded the binary on a percentage of the fleet, followed by "a sequential (and fairly slow) restart" of the agent. This was meant to avoid "a coordinated wave of restarts which might destabilize a service".
- **What a restart did:** when an agent shuts down, it removes its node from the service catalog, and adds it back when it starts. On a cache node, Mcrib, the system that manages the cache configuration, replaced the node that left with a spare. "The new cache node will be empty."
- **The batches:** two earlier steps of 25% of the fleet ran the week before, "without any incident". The step on February 22 was also 25%.
- **That day:** "we hit a tipping point and entered a cascading failure scenario as we hit peak traffic for the day." In a cascading failure, one failure causes the next. The cache hit rate (how often data is found in the cache) dropped.
- **Why an empty cache hurt:** one query, run when a client starts, for the members of group messages, is normally served from the cache. On a miss, it had to run on every shard (every piece of the split database). Read load "increased superlinearly in relation to the percentage of cache misses", meaning faster than the misses grew. Most of those queries timed out, so the cache couldn't refill.
- **Stopping:** "Early in the incident" Slack paused the restarts, before suspecting they were related. "However, by then it didn't make a difference".
- **Recovering:** Slack throttled client startup (limited how many apps could start), changed the query, and the caches refilled.

The report doesn't give the time of the February 22 step or the pause, the share of cache nodes restarted, or whether stop conditions were written.

## What happened at Google

Times are US/Pacific, on June 2, 2019. Google's cluster software automates maintenance. Each job is labeled for maintenance: typically moved to another machine, or stopped and rescheduled afterwards.

Two normally harmless misconfigurations and a bug combined: network control jobs were configured to be stopped, the software running them was marked eligible for a rare type of maintenance, and a bug let the maintenance software "deschedule multiple independent software clusters at once", even across physical locations.

- **11:45:** maintenance started in one location. The list of jobs to stop included logical clusters that also had network control jobs in other locations, and those were stopped too.
- **11:47 to 11:49:** users began to see impact: routing between some locations was withdrawn, which cut network capacity.
- **13:01:** the cause was found, and engineers halted the automation. With all instances stopped in several locations, configuration had been lost and had to be rebuilt.
- **16:10:** full service resumed, after capacity started coming back at 15:19.

The page isn't fully consistent: the impact section lists packet loss from 11:38, before the 11:45 start, and the page header ends the incident at 15:40, not 16:10.

## What Kubernetes documents

Neither case above is about Kubernetes. Its documentation names the mechanics.

- **Drain:** `kubectl drain` evicts the pods (running instances) from a node before maintenance, letting their containers shut down gracefully.
- **Disruption limit:** a PodDisruptionBudget (PDB) limits how many replicas (copies) of an application are down at once from voluntary disruptions (ones someone starts, such as drains). With 3 replicas and `minAvailable: 2`, only 1 can be unavailable, and drains that would break that are blocked, even when run in parallel. A blocked drain keeps retrying until it succeeds or reaches a timeout you can set.

## Reading the cases

The rest of this lesson is its own reading and method.

- **Ask what comes back empty.** Slack's work was on an agent, not on the cache, and cache nodes still came back without their contents. A spare took each node's place, so a count of nodes wouldn't show the loss.
- **A clean batch is evidence about that batch.** The two steps before February 22 had no incident, and that day's did. Slack places the tipping point at peak traffic but doesn't compare the steps, so peak traffic can't be called the only difference.
- **Know what's really in a batch.** Google's event started in one location and reached others. Spread protects you only if the maintenance respects it, so check what each item on the list reaches, not only where the work starts. The report doesn't say whether anyone could see this list beforehand.
- **Slow isn't a stop condition.** Slack's restart was slow on purpose, and the hit rate still dropped. A stop condition is a signal and a limit, written beforehand.
- **Stopping isn't recovering.** Slack's pause "didn't make a difference" by then. At Google, full service came about three hours after the halt, by the report's 16:10. So the plan needs a second part: what you do if stopping isn't enough. See [Mitigate what can be undone](../05-respond/03-mitigate-what-can-be-undone.md).

## How to do it

1. Say what's taken away, how many at a time, and for how long.
2. For each workload, check enough replicas, spread so one unit of maintenance never holds all of them, a disruption limit that can be met, room for what's moved, and a shutdown that fits the time the platform allows.
3. Ask what comes back empty or has to rebuild, and where its load goes meanwhile. For databases, queues and anything with a leader, follow its own procedure.
4. Write the batches: smallest first, the exact list in each, the time of day, and what must be true before the next one.
5. Write the stop conditions: which signal, what limit, and who stops. Use a signal that moves before users notice, along with one users feel.
6. Write what you do after stopping: how to give capacity back, and how to reduce load if stopping isn't enough.
7. Confirm it's done: every workload back to its replicas, and errors at normal.

## Worked example

An example written for this lesson, from Slack's report. The checks and stop conditions are this lesson's additions, not Slack's plan.

- **Taken away:** the Consul agent, restarted one instance at a time, in steps of 25%.
- **Comes back empty:** a memcached node whose agent restarts is replaced by an empty spare. The load goes to the database, through the group message query, on every shard.
- **Before each batch:** check the time of day against peak traffic, and that the cache hit rate is back to normal.
- **Stop when:** cache hit rate falls below, or load on that database rises above, a limit taken from a normal peak.
- **If stopping isn't enough:** throttle client startup, which is what Slack did.

_If you use rbadillap/sre: `plan-maintenance` writes a runbook for a person to run, covering each workload's checks, batches, stop conditions and how to confirm it's done. No step asks what comes back empty, or how to reduce load if stopping isn't enough, so add those yourself._

## In one sentence

"Before maintenance I write what each step takes away and what comes back empty, how big each batch is, which signal stops me, and what I do if stopping isn't enough."

## Exercise

A hypothetical case. You'll reboot 12 nodes for a kernel update, between 02:00 and 06:00 UTC.

- Nodes 1 to 6 each run one replica of `api`, with a PDB requiring 5 of the 6 available. There's room for replacements. You drain these nodes one at a time, 10 minutes each.
- Nodes 7 to 12 each run one cache instance, which stays on its node. It's empty during its 10-minute reboot and the 30 minutes it takes to refill. Each batch waits for the one before it, so a cache batch takes 40 minutes.
- In that window, your database runs at 30% of its limit. Assume each empty cache instance adds 10 percentage points, and that it's safe up to 60%. Real load may not grow in a straight line: Slack's didn't.
- Your normal error rate is under 0.1%.

1. What happens if you start a second `api` drain before the first replacement is available? Why?
2. What's the largest cache batch that stays within the database limit? Which size do you start with?
3. Start with one cache node, then use the largest batch. How many cache batches is that, and does all the work fit the window?
4. Write two stop conditions, and what you do if each one fires.
5. Think of the last maintenance on a system you work on. What came back empty, and where did its load go?

---

_Written with an AI assistant from the sources above._

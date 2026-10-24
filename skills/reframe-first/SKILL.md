---
name: reframe-first
description: Discipline. Before solving a reliability problem, state what the real problem is. Applied by the orchestrators in this package at the start of the work, and whenever a fix "should have worked" but didn't.
license: MIT
metadata:
  sre-layer: discipline
---

# Reframe first

**Before solving, say what the real problem is.**

## When

At the start of every piece of work, and again when the evidence stops matching the story: a fix that should have worked and didn't, a dashboard that's green while users complain, a rollback that changed nothing.

## When not

When the problem is already confirmed and named by evidence, don't reopen it for the sake of the step. Reframing is a check, not a ritual.

## How

1. Write the problem as it arrived, in one sentence.
2. Ask what that sentence assumes. "The API is slow but the cluster is healthy" assumes the cluster is where the problem would show.
3. Write the problem again, in terms of what users live and what is actually known.
4. If the two sentences differ, work on the second one, and say so in the result.

Common reframes:

| It arrives as | It often is |
|---|---|
| "Latency is up, CPU and memory are normal" | Something the service waits on: a database, a cache, a queue, a dependency |
| "No deploy happened" | Something else changed: traffic, a scheduled job, configuration, a provider |
| "Infrastructure drifted" | A possible security incident, if the drift opens access |
| "The rollback didn't fix it" | The change touched data or shared state, which a rollback doesn't revert |
| "The service is up" | A check that only proves the process runs, not that it can do its job |

## The mistake it prevents

Spending the first hour of an incident on the wrong problem, with full energy: restarting healthy pods while a database runs out of connections.

---
name: idempotency
description: Discipline. An operation that can run more than once must give the same result, so retries, redeliveries and repeated messages can't break anything. Applied by the orchestrators in this package when designing workers, queues, APIs, migrations or recovery steps.
license: MIT
metadata:
  sre-layer: discipline
---

# Idempotency

**Anything that can happen twice must be safe to happen twice.**

## When

Whenever work can be retried or delivered again: queue consumers, webhooks, API calls with retries, scheduled jobs, deploy and recovery steps, data migrations.

## When not

Work that truly happens once, with no retry anywhere in its path, doesn't need it. Check the whole path before deciding that: clients, proxies and queues all retry.

## How

1. **Assume at-least-once.** Most queues and networks deliver at least once, not exactly once. A clean shutdown reduces duplicates; it doesn't remove them.
2. **Give every unit of work a stable ID,** set by whoever creates it, not by whoever processes it.
3. **Record the ID with the effect, atomically.** Store the processed ID in the same write as the result, behind a uniqueness constraint. A second attempt fails the constraint and is skipped.
4. **Acknowledge after the work is durable,** never before. A crash between the work and the acknowledgement then means a safe retry, not a lost message.
5. **Guard order as well as repetition.** Keep a version or the last applied event ID with the state, and apply an update only if it's newer.
6. **Bound the record.** Expire stored IDs after a period much longer than the longest possible redelivery.
7. **Know where it can't be guaranteed.** Effects outside your systems, like an email or a call to a provider without an idempotency key, can still happen twice. Make the choice between a rare duplicate and a missed effect explicit.

## The mistake it prevents

A retry or a redelivered message charges twice, notifies twice, or overwrites newer state with older state.

---
name: state-is-special
description: Discipline. Data and shared state get their own plan, because rolling back code doesn't roll back data. Applied by every orchestrator in this package when a change, an incident or a recovery touches databases, caches, queues or stored files.
license: MIT
metadata:
  sre-layer: discipline
---

# State is special

**Data and state get their own plan, because rolling back code doesn't roll back data.**

## When

Whenever a change, an incident or a recovery touches anything that outlives a process: database rows and schemas, cache entries, queue messages, files, configuration stored outside the code.

## When not

For stateless changes, don't invent risk. A change that only alters logic, with no stored format or shared data involved, can follow the normal rollback path.

## How

1. **Ask what this leaves behind.** If the new version writes something the old version can't read, a rollback won't help.
2. **Make state changes compatible before they ship.** Add the new form next to the old one, move to it, and remove the old one only when going back is no longer needed (expand and contract). Every version that can run at the same time must read what the others write.
3. **Make repeated work safe.** Assume messages and requests can arrive twice. Give each one a stable ID and make processing it a second time a no-op.
4. **Treat a snapshot as part of a recovery, not as a rollback.** Restoring a snapshot loses everything written after it. Say how much, and let a person decide.
5. **Unknown cached data is a miss, unless it guards security.** If cached data can be rebuilt, an unknown format should be treated as a miss. If it protects something, like a revocation list, fail safe instead of skipping the check.
6. **Shared state breaks isolation.** A canary that writes to a shared store can break the stable version. Make formats compatible before a progressive rollout starts.

## The mistake it prevents

The rollback succeeds and the data stays broken.

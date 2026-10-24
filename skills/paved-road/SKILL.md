---
name: paved-road
description: Discipline. Prevent the next incident by turning what was learned into a default, not a reminder, so the reliable path is also the easiest one. Applied by every orchestrator in this package when proposing follow-ups, prevention or standards.
license: MIT
metadata:
  sre-layer: discipline
---

# Paved road

**Make the safe path the easy path. A lesson becomes a default, not a reminder.**

## When

Whenever work ends in "this should not happen again": postmortem actions, review findings, standards for a team.

## When not

When the fix is a one-off correction with no pattern behind it, don't build a road for it. A road is for something people will do again.

## How

1. **Ask where the lesson can live so nobody has to remember it.** In order of preference:
   1. A default in a shared module, template or configuration.
   2. A check in the pipeline that fails before production.
   3. A template field that asks the question that was missed.
   4. An alert that sees what nobody saw.
   5. A document, only when none of the above fits.
2. **Make the safe way cheaper than the unsafe way.** If the safe path takes more steps, people will route around it.
3. **Give every follow-up an owner and a place.** An action with no owner isn't a follow-up.

## The mistake it prevents

The same incident comes back months later with a different team, who never read the postmortem.

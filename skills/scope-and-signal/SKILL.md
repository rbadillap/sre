---
name: scope-and-signal
description: Discipline. Find out how far a reliability problem reaches, and pick the signals that describe what users live, before acting. Applied by the orchestrators in this package when sizing an incident, a release risk or a monitoring gap.
license: MIT
metadata:
  sre-layer: discipline
---

# Scope and signal

**Find out how far it reaches before acting, and which signals actually describe it.**

## When

Before choosing a mitigation, an escalation or a fix. Again whenever a new fact changes the size of the problem.

## When not

Don't let scoping delay a mitigation that is safe and reversible. If users are clearly affected and a reversible action exists, take it, and keep scoping in parallel.

## How

1. **Size it.** Answer each, and say which answers are still unknown:
   - Which regions, zones or clusters?
   - All tenants or customers, or some? Which ones?
   - Errors, latency, or both?
   - Since when? What does the start line up with?
2. **Pick the signal users live.** Prefer the signal closest to the user's experience over the one closest to the server. A request metric can't see requests that never arrived.
3. **Look at the worst case, not the average.** An average across tenants hides one tenant at 90% availability behind a 99.95% total. Break signals down by tenant, region and version.
4. **Separate signal from noise.** Compare with the same hour on a normal day, not only the last hour. A change that happens in one interval is rarely a natural pattern.

## The mistake it prevents

A fix aimed at the whole system that misses a problem living in one corner, or a team that trusts a green dashboard while one customer is down.

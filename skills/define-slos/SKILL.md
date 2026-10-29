---
name: define-slos
description: Defines service level indicators and objectives from what users actually need to do, with eligibility and attribution rules and an error budget. Use when a team needs to define reliability, when dashboards are green but customers complain, when engineering and product disagree about whether a service is healthy, or when a customer asks for an SLA. Phrases like "what should our SLO be", "define SLIs", "error budget", "customers say it's unreliable", "can we promise 99.99%".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: define
  sre-safety: proposes
---

# Define SLOs

**The question:** what does "working" mean for the people who use this, and how much failure is acceptable?

**The result:** `reliability/slos/<system>.md`, from [the template](assets/slo.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It reads the system and writes a definition. It changes no monitoring or configuration.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Reframe.** Apply `reframe-first`. The question isn't how available the servers are, but whether users can do what they came to do, on time.
2. **Map the journey.** List the steps users go through for each action that matters. Users can be internal (an operator shipping a release) or devices acting for users (a device checking for updates).
3. **Choose an SLI for each step that matters,** written as good events over valid events, measured as close to the user as possible. Say where it's measured.
4. **Write eligibility.** Which users, devices or requests count. Something genuinely unable to reach the system, like a device turned off, shouldn't count against it; something that suddenly stops reaching it might be the system's fault, so watch it separately (see `find-blind-spots`).
5. **Write attribution rules before the next incident.** Which failures count against the service and which don't. If incidents already happened, write the rules first and then apply them to those incidents as a test, never the other way around.
6. **Set each SLO.** A target over a window, at or below what the system achieves today and above the point where users start to notice. Find what it achieves from data; with no data, write the target as a hypothesis and say what will measure it. Find where users notice from complaints, support tickets or the people who use it; if nobody can say, start with the current level and revisit after a window. Apply `scope-and-signal`: per tenant, customer or device group as well as in total, so a large group can't hide a small one.
7. **Calculate the error budget.** Run `scripts/error-budget.py` with each target and window. For SLIs that count rare events (releases, jobs, deployments), pass the expected events per window and read the budget in events, not time. Write the budget and the policy: what changes when it runs out.
8. **If an SLA is requested, compare it.** An SLA has to be looser than the SLO, and the SLO looser than what the system achieves. Use the script to show what the SLA allows in minutes. List what the SLA would need: history at that level, dependencies that support it, response time that fits it, and clear exclusions. Offer an alternative if it doesn't fit, such as an SLA on what the customer actually needs.
9. **Write who agreed.** SLOs are a decision between the people who build and the people who use or sell the system. Name who agreed, or write that it's not agreed yet.
10. **Label every claim** (`evidence-before-claims`), and write the result.

## Done when

- The reframe is written.
- Every user action listed has its journey, and every step chosen has an SLI with where it's measured; steps left out say why.
- Eligibility and attribution rules are written, and tested on past incidents if there were any.
- Every SLO has a target with where it came from (data or hypothesis), a window, a breakdown, its error budget from the script in time or events, and a budget policy.
- If an SLA was requested, it's compared with the SLO, with what it would need and an alternative.
- Who agreed is named, or "not yet agreed" is written.
- Every claim is labeled verified, hypothesis or not verified.

Next: recommend `design-alerts` to alert on the error budget.

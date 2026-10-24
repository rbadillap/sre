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

## Steps

1. **Reframe.** Apply `reframe-first`. The question isn't how available the servers are, but whether users can do what they came to do, on time.
2. **Map the journey.** List the steps users go through for each action that matters. Users can be internal (an operator shipping a release) or devices acting for users (a device checking for updates).
3. **Choose an SLI for each step that matters,** written as good events over valid events, measured as close to the user as possible. Say where it's measured.
4. **Write eligibility.** Which users, devices or requests count. Something genuinely unable to reach the system, like a device turned off, shouldn't count against it; something that suddenly stops reaching it might be the system's fault, so watch it separately (see `find-blind-spots`).
5. **Write attribution rules, before any incident.** Which failures count against the service and which don't. Decide them now, so nobody adjusts them after an incident to protect a number.
6. **Set each SLO:** a target over a window, below what the system achieves today and above what users notice. Apply `scope-and-signal`: per tenant or customer as well as in total, so a large tenant can't hide a small one.
7. **Calculate the error budget.** Run `scripts/error-budget.py` with each target and window. Write the budget and the policy: what changes when it runs out.
8. **If an SLA is requested, compare it.** An SLA has to be looser than the SLO, and the SLO looser than what the system achieves. Use the script to show what the SLA allows in minutes. List what the SLA would need: history at that level, dependencies that support it, response time that fits it, and clear exclusions. Offer an alternative if it doesn't fit, such as an SLA on what the customer actually needs.
9. **Label every claim.** Apply `evidence-before-claims`. Current achievement needs data; without data, it's a hypothesis.
10. **Write the result.**

## Done when

- The reframe is written.
- Every user action that matters has its journey, and each step that matters has an SLI with where it's measured.
- Eligibility and attribution rules are written.
- Every SLO has a target, a window, a breakdown, its error budget from the script, and a budget policy.
- If an SLA was requested, it's compared with the SLO, with what it would need and an alternative.
- Every claim is labeled verified, hypothesis or not verified.

Next: recommend `design-alerts` to alert on the error budget.

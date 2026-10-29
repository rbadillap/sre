---
name: design-alerts
description: Designs alerting that pages for real user impact and stays quiet otherwise, using symptoms, error budget burn rates and clear page versus warning rules, tested against past incidents. Use when on-call gets too many pages or misses what matters, when setting alerts for a new SLO or service, or after an incident nobody was paged for. Phrases like "too many alerts", "alert fatigue", "we weren't paged", "what should page", "burn rate alerts".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: observe
  sre-safety: proposes
---

# Design alerts

**The question:** what should wake someone up, and what can wait until morning?

**The result:** `reliability/alerting/<system>.md`, from [the template](assets/alerting-policy.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It writes a policy. It doesn't change alerting configuration.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Reframe.** Apply `reframe-first`. The question isn't which metrics to watch, but which situations need a person now.
2. **List the alerts that exist,** with what fired in the last weeks and whether each page led to an action. If there's no history, say so.
3. **Page on symptoms; route causes elsewhere.** A page is for something users feel. Causes such as high CPU or a filling disk go to dashboards or tickets, unless they predict user impact soon enough that someone must act.
4. **Alert on the error budget, when there's enough volume.** For each SLO from `define-slos`, run `scripts/burn-rate.py` with its target, window and typical events per hour. It prints two page rows (fast and medium burn) and one ticket row (slow burn), each with a long window for significance and a short one so the alert clears soon after recovery. Act on its warnings: where a window holds too few events, or a threshold can't be reached, alert on counts or on every failure instead.
5. **Alert on events that are rare and always matter.** For SLIs that count rare events (a release, a job, a deployment), a failure is a page or a ticket on its own, not a rate.
6. **Break down without noise.** Apply `scope-and-signal`. Alert per tenant, region, device group or version where an average can hide a failure. Set a minimum volume so a tiny group can't page anyone by chance, except groups that are small by design and must always be watched, such as a canary: alert on their events directly.
7. **Cover the blind spots.** Signals for failures before the request, and for sources that go silent, come from `find-blind-spots`. Add the ones that should page.
8. **Test the policy against past incidents.** For each incident in `reliability/incidents/` or the team's history, work out what each alert would have seen, and whether it would have paged and when. An incident that pages nobody under the new policy is a finding: adjust, or write why it's acceptable.
9. **Every page has a runbook and an owner.** A page without a first step wastes the first ten minutes.
10. **Plan the review.** Every month, look at each page: if it didn't need action, change it or delete it. Count the pages per period, with out-of-hours pages apart, and report the number to whoever sets priorities. On-call load is a number, not something the team absorbs.
11. **Label every claim** (`evidence-before-claims`), and write the result.

## Done when

- The reframe is written.
- Existing alerts are listed with whether they led to action, or the lack of history is noted.
- Every page is a symptom, a budget burn with its threshold and windows from the script, or a rare event, with a runbook and an owner.
- Every breakdown has a minimum volume or is marked small by design.
- The blind-spot signals that should page are included, or `find-blind-spots` hasn't been run and that's noted.
- Every past incident checked has what would have paged and when, or a written reason.
- Causes are routed to dashboards or tickets, with any exception explained.
- The monthly review is planned, with an owner and who receives the on-call load, and every claim is labeled.

Next: if no one has looked for blind spots yet, recommend `find-blind-spots`.

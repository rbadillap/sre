---
name: design-alerts
description: Designs alerting that pages for real user impact and stays quiet otherwise, using symptoms, error budget burn rates and clear page versus warning rules. Use when on-call gets too many pages or misses what matters, when setting alerts for a new SLO or service, or after an incident nobody was paged for. Phrases like "too many alerts", "alert fatigue", "we weren't paged", "what should page", "burn rate alerts".
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

## Steps

1. **Reframe.** Apply `reframe-first`. The question isn't which metrics to watch, but which situations need a person now.
2. **List the alerts that exist,** with what fired in the last weeks and whether each page led to an action. If there's no history, say so.
3. **Page on symptoms; route causes elsewhere.** A page is for something users feel. Causes such as high CPU or a filling disk go to dashboards or tickets, unless they predict user impact soon enough that someone must act.
4. **Alert on the error budget.** For each SLO from `define-slos`, set burn rate alerts: a fast burn pages, a slow burn opens a ticket. Use two windows per alert, a long one for significance and a short one so the alert clears soon after recovery. Run `scripts/burn-rate.py` with the SLO and window to get the thresholds.
5. **Break down without noise.** Apply `scope-and-signal`. Alert per tenant, region or device group where an average can hide a failure, with a minimum volume so a tiny group can't page anyone.
6. **Cover the blind spots.** Signals for failures before the request, and for sources that go silent, come from `find-blind-spots`. Add the ones that should page.
7. **Every page has a runbook and an owner.** A page without a first step is a page that wastes the first ten minutes.
8. **Plan the review.** Every month, look at each page: if it didn't need action, change it or delete it.
9. **Label every claim.** Apply `evidence-before-claims`.
10. **Write the result.**

## Done when

- The reframe is written.
- Existing alerts are listed with whether they led to action, or the lack of history is noted.
- Every page is a symptom or a budget burn, with its threshold from the script where it's a burn rate, a minimum volume where it's broken down, a runbook and an owner.
- Causes are routed to dashboards or tickets, with any exception explained.
- The monthly review is planned, with an owner.
- Every claim is labeled verified, hypothesis or not verified.

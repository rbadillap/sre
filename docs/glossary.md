# Glossary

The words the skills share. When a skill uses one of these terms, it means exactly this.

## The package

- **Orchestrator.** A skill that runs one moment of the work, like responding to an alert. Its name starts with a verb. See [layers](layers.md#orchestrators).
- **Discipline.** A skill that holds one rule the orchestrators follow. Its name states a principle, not a task. See [layers](layers.md#disciplines).
- **Router.** The `sre` skill, which points to the right orchestrator for a situation.
- **Template.** The structure a skill fills to leave a reusable result.
- **Paved road.** A way of working delivered as a default, so the reliable path is also the easiest one. In this package, the templates and the `reliability/` folder.
- **`reliability/`.** The one folder in your repository where every skill writes its results.
- **Safety level.** What a skill is allowed to do: read only, propose, or act with approval. See [layers](layers.md#safety).
- **Learning loop.** The path from an incident to an approved change in the package itself. See [layers](layers.md#learning).

## Defining reliability

- **SLI (service level indicator).** A measurement of what users experience, written as good events over valid events. For example, the share of check-ins that succeed.
- **SLO (service level objective).** The target for an SLI over a window, such as 99.9% of check-ins succeeding over 28 days.
- **Error budget.** The failure an SLO allows: with a 99.9% SLO, 0.1% of events may fail. When the budget runs out, reliability work comes before new features.
- **SLA (service level agreement).** A contract with a customer, with consequences if it's missed. It should be looser than the SLO, and the SLO looser than what the service really achieves.
- **Eligibility.** The rule that decides which users, devices or requests count in an SLI. Offline devices, for example, may not be eligible.
- **Attribution rule.** The rule, set before any incident, that decides whether a failure counts against the service. Errors seen at the service's own edge count; a customer's confirmed network outage doesn't.

## Observing

- **Symptom.** Something users feel, such as errors or slow responses. Pages are for symptoms.
- **Cause.** Something that may lead to a symptom, such as high CPU or a full disk. Causes go to dashboards and tickets, not pages.
- **Burn rate.** How fast an incident is spending the error budget. A fast burn pages someone; a slow burn opens a ticket.
- **Blind spot.** A failure no current signal can see. A request that never reaches the service is invisible to request metrics.

## Shipping

- **Deploy.** Putting a new version in production.
- **Release.** Users actually getting the change. A deploy can succeed while the release fails.
- **Canary.** A release to a small share of traffic first, compared with the stable version before going further.
- **Observation time.** How long a canary runs before the next step. It has to be longer than the delay of the effect it waits for.
- **Rollback-safe.** A change that can be undone by going back to the previous version. Changes to shared data often aren't.
- **Forward plan.** The recovery for a change that isn't rollback-safe: fix forward instead of going back.
- **Expand and contract.** Changing a data structure in separate steps: add the new form next to the old one, move to it, and remove the old one only when going back is no longer needed.
- **Idempotency.** An operation that gives the same result when it runs more than once, so a retry or a repeated message can't break anything.

## Responding

- **Mitigation.** Stopping the impact, before the root cause is known.
- **Reversible action.** One that can be undone, such as pausing a job or rate-limiting a tenant.
- **Escalation.** Bringing in another person. It happens on clear criteria: users affected with no safe fix, data at stake, or a provider involved.
- **Confirmed impact.** What is known to be affected, as opposed to what is suspected.
- **Postmortem.** The written account of an incident: timeline, contributing factors, actions with owners, and why it wasn't detected sooner.

# The lifecycle

Reliability work moves through six stages. The package's orchestrators are organized by stage, not by topic.

| Stage | The question | Orchestrators |
|---|---|---|
| **Define** | What does "working" mean for the people who use this? | `define-slos` |
| **Design** | Will it hold up through changes and failures? | `review-design`, `plan-migration` |
| **Ship** | Will this change reach production safely? | `review-release`, `plan-maintenance` |
| **Observe** | Do we see what users live, not only what servers report? | `design-alerts`, `find-blind-spots` |
| **Respond** | How do we contain it, mitigate it and decide who to call? | `respond-to-alert`, `contain-security-incident`, `reconcile-drift` |
| **Learn** | What changes so this doesn't happen again? | `write-postmortem`, `learn-from-incident` |

## It's a loop

Learn feeds back into Define and Design. A postmortem can change an SLO, a review checklist or an alert. Without that return, the stages are a list.

## You can enter at any stage

Development work usually moves in order: idea, plan, code, review, merge. Reliability work doesn't. An alert enters at Respond at three in the morning, whatever stage the team was in. So orchestrators don't assume the previous stage happened. Each one starts from the situation in front of it, and recommends the next skill when it's done: Respond hands off to Learn, and Learn ends in proposals that a person approves, which change what Define and Design start from.

## Where it comes from

The stages aren't new. The same pieces show up in established frameworks, ordered in different ways:

| Source | How it organizes the work | How it maps |
|---|---|---|
| [ITIL v3 service lifecycle](https://en.wikipedia.org/wiki/ITIL) | Service Strategy, Service Design, Service Transition, Service Operation, Continual Service Improvement | Define ≈ Strategy, Ship ≈ Transition, Observe and Respond ≈ Operation, Learn ≈ Continual Service Improvement |
| [Google's Service Reliability Hierarchy](https://sre.google/sre-book/part-III-practices/) | Monitoring, Incident Response, Postmortem and Root-Cause Analysis, Testing, Capacity Planning, Development, Product, from most basic to most advanced | The same pieces, ordered as a pyramid of needs instead of a loop |
| [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final) (2012) | Preparation; Detection and Analysis; Containment, Eradication and Recovery; Post-Incident Activity | Respond in detail, for security incidents, ending in learning. [Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) (2025) supersedes it and frames incident response within the NIST Cybersecurity Framework 2.0 |

That the stages match these frameworks is the point: the lifecycle rests on practice that has been tested for years.

## What's different here

In those frameworks, the last stage ends in a document: a postmortem, an improvement plan, a lessons-learned report. Someone reads it, sometimes.

In this package, Learn can change the skills themselves. A postmortem leads to a proposed change in a template, an alert policy or a discipline, and a person approves it. The next time, the agent already works with the lesson. That's the [learning loop](layers.md#learning).

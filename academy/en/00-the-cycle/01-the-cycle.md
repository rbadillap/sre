---
title: "The cycle"
stage: the-cycle
order: 1
status: approved
teaches: "The six stages, why they form a loop, and why you enter wherever the problem arrives."
sources:
  - title: "Google SRE book, Part III: Practices"
    url: https://sre.google/sre-book/part-III-practices/
  - title: "ITIL"
    url: https://en.wikipedia.org/wiki/ITIL
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
skills: []
version:
---

# The cycle

_Sources: [Google's SRE book, Part III](https://sre.google/sre-book/part-III-practices/), [ITIL v3](https://en.wikipedia.org/wiki/ITIL), and [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/)._

## The question

Reliability work looks like a list of topics: SLOs, alerts, incidents, postmortems. The question here is different: in what order do these things happen, and how do they connect?

## Six stages, each with one question

1. **Define.** What does "working" mean for the people who use this?
2. **Design.** Will it hold up through changes and failures?
3. **Ship.** Will this change reach production safely?
4. **Observe.** Do we see what users live, not only what servers report?
5. **Respond.** How do we contain it, mitigate it and decide who to call?
6. **Learn.** What changes so this doesn't happen again?

## What the sources say

The stages aren't new. The same pieces appear in established frameworks, in different orders:

- **Google's SRE book** arranges them as a hierarchy of needs, from the most basic to the most advanced: monitoring, incident response, postmortems and root-cause analysis, testing and release procedures, capacity planning, development, and product.
- **ITIL v3** arranges them as a service lifecycle: strategy, design, transition, operation, and continual service improvement.

The order changes; the pieces don't.

## It's a loop, not a list

Learn feeds back into Define and Design. A postmortem can change an SLO, a review checklist or an alert. Without that return, the stages are only a list.

GitLab's 2017 outage shows the loop. Each finding below comes from its postmortem:

- **Respond:** during a replication incident, data was deleted on the primary database instead of the secondary.
- **Respond:** the restore came from a snapshot about six hours old, after other recovery options failed or weren't available.
- **Observe:** the backups had been failing without anyone noticing, because the alert emails were being rejected.

Read through the cycle, the lesson isn't "be careful with commands". It lands in two other stages: in Design, restores that are tested before they're needed; in Observe, an alert that reaches someone. One incident in Respond changes Observe and Design.

## You enter wherever the problem arrives

Development work usually moves in order: idea, plan, code, review, merge. Reliability work doesn't. An alert enters at Respond at three in the morning, whatever stage the team was in. So each stage starts from the situation in front of it, not from the assumption that the previous stage happened.

_If you use rbadillap/sre: its skills are organized by these six stages, and the `sre` router points a situation to the right one._

## In one sentence

"Reliability work is a loop of six stages, define, design, ship, observe, respond and learn, and what you learn changes how you define and design next time."

## Exercise

Think of the last incident you saw or read about. Which stage did it enter at? And what would have to change, in which stage, so it doesn't come back?

---

_Written with an AI assistant from the sources above._

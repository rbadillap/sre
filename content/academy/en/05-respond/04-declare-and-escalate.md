---
title: Declare and escalate
stage: respond
order: 4
status: draft
teaches: When something is an incident, how big the response is, and what to bring when you call someone.
sources: Google SRE book, Managing Incidents (https://sre.google/sre-book/managing-incidents/); PagerDuty Incident Response documentation, Severity Levels (https://response.pagerduty.com/before/severity_levels/) and During an Incident (https://response.pagerduty.com/during/during_an_incident/); Atlassian, April 2022 outage (https://www.atlassian.com/engineering/post-incident-review-april-2022-outage)
skill: respond-to-alert
version: 0.1.1
---

# Declare and escalate

_Sources: [Google's SRE book, "Managing Incidents"](https://sre.google/sre-book/managing-incidents/); PagerDuty's incident response documentation, ["Severity Levels"](https://response.pagerduty.com/before/severity_levels/) and ["During an Incident"](https://response.pagerduty.com/during/during_an_incident/); and [Atlassian's review of the April 2022 outage](https://www.atlassian.com/engineering/post-incident-review-april-2022-outage)._

## The question

Calling for help too late costs time. Calling without context costs the other person's time. Three questions come before the call: is this an incident, how big is the response, and what do I bring?

## A real case

At Atlassian in April 2022, a script deleted 883 customer sites. Internal monitoring didn't detect it. The first customer support ticket arrived at 07:46 UTC, and the major incident process started at 08:17 UTC.

## Is it an incident?

Google's SRE book gives three questions. If any answer is yes, it's an incident, and it's run as one:

1. Do you need to involve a second team to fix the problem?
2. Is the outage visible to customers?
3. Is the issue still unsolved after an hour of concentrated analysis?

On timing, the book is direct: it's better to declare an incident early than to start the process hours into a growing problem.

## How big is the response?

PagerDuty's guidance ties the response to a severity level:

- **SEV-1 and SEV-2** are major incidents: page an incident commander (IC) and follow the full incident process.
- **SEV-3** goes to the service's team as an urgent page, and an IC is paged if the response needs coordinating.
- **SEV-4 and SEV-5** are a low-urgency page or a ticket.

Two rules from the same guidance:

- If you're unsure between two levels, treat it as the higher one. Severity is debated in the postmortem, not during the incident.
- Each level's definition should be specific and measurable, such as the share of users or accounts affected.

Escalating is moving up this scale when the facts change, and bringing in the people that level calls for.

## Who does what

Google's book splits the work into roles, so one person isn't fixing and communicating at once: the incident commander holds the overall picture, operations is the only group changing the system, communications is the public face, and planning handles the longer-term work, like filing bugs. PagerDuty's IC does the same: resolves the incident by delegating to experts, not by fixing it alone.

## What to bring

PagerDuty asks experts to report their findings to the IC, and to say so when the cause isn't confirmed yet. Put as findings: what you checked, what you ruled out, and what you think it is, with the confirmed parts kept apart from the hypothesis. The person you call starts from there instead of from zero.

_If you use rbadillap/sre: `respond-to-alert` asks for the team's escalation criteria, and suggests a default when there are none._

## In one sentence

"I declare early, set the severity by written criteria and round up when unsure, and when I bring someone in, I bring what I checked, what I ruled out, and what I think it is."

## Exercise

Three parts:

1. In the Atlassian case, which of Google's three questions was already true at 07:46 UTC?
2. Your team has no written criteria. Write a definition for SEV-1 and SEV-2 based on the share of users affected, with your own thresholds.
3. You've been on an incident for 20 minutes, users are still affected, and your one fix didn't work. Write the message you'd send when you page someone: three lines, no more.

---

_Written with an AI assistant from the sources above._

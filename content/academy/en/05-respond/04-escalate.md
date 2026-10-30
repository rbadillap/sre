---
title: Escalate
stage: respond
order: 4
status: draft
teaches: Clear criteria, with context.
sources: PagerDuty Incident Response documentation, During an Incident (https://response.pagerduty.com/during/during_an_incident/); Google SRE book, Managing Incidents (https://sre.google/sre-book/managing-incidents/)
skill: respond-to-alert
version: 0.1.1
---

# Escalate

_Sources: [PagerDuty's incident response documentation, "During an Incident"](https://response.pagerduty.com/during/during_an_incident/), and [Google's SRE book, "Managing Incidents"](https://sre.google/sre-book/managing-incidents/)._

## The question

Calling for help too late costs time. Calling without context costs the other person's time. The question is: when do I bring someone in, and what do I bring?

## What PagerDuty's guidance says

- If no incident commander (IC) is on the call, page one. The guidance is not to hesitate: paging an IC is encouraged even when it may turn out not to be needed.
- The IC's job is to resolve the incident as quickly and safely as possible, by delegating to the right experts, not by fixing it alone.
- Subject matter experts report their findings to the IC, and say so when they're still investigating without a confirmed cause.
- The IC can split off sub-teams when the incident grows or gets more complex.
- Someone other than the person fixing sends regular status updates to stakeholders.

## When to escalate

Google's SRE book gives three questions. If any answer is yes, it's an incident, and it's run as one:

1. Do you need to involve a second team to fix the problem?
2. Is the outage visible to customers?
3. Is the issue still unsolved after an hour of concentrated analysis?

Its advice on timing matches PagerDuty's: it's better to declare an incident early than to start the process hours into a growing problem.

The book also splits the work into roles, so one person isn't fixing and communicating at once: the incident commander holds the overall picture, operations is the only group changing the system, communications is the public face, and planning handles the longer-term work, like filing bugs. When someone's load gets too heavy, they ask for more people.

## What to bring

What PagerDuty asks experts to report to the IC: your findings, and whether the cause is confirmed or still being investigated. Put as findings, that's what you checked, what you ruled out, and what you think it is, with the confirmed parts apart from the hypothesis. The person you call starts from there instead of from zero.

_If you use rbadillap/sre: `respond-to-alert` asks for the team's escalation criteria, and suggests a default when there are none._

## In one sentence

"I declare early, on criteria written before the incident, and when I bring someone in, I bring what I checked, what I ruled out, and what I think it is."

## Exercise

Two parts:

1. Your team has no written criteria. Using Google's three questions as a starting point, write the criteria you'd propose, with one threshold of your own.
2. You've been on an incident for 20 minutes, users are still affected, and your one fix didn't work. Write the message you'd send when you page someone: three lines, no more.

---

_Written with an AI assistant from the sources above._

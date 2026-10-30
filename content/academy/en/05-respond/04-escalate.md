---
title: Escalate
stage: respond
order: 4
status: draft
teaches: Clear criteria, with context.
sources: PagerDuty Incident Response documentation, During an Incident (https://response.pagerduty.com/during/during_an_incident/)
skill: respond-to-alert
version: 0.1.1
---

# Escalate

_Source: [PagerDuty's incident response documentation, "During an Incident"](https://response.pagerduty.com/during/during_an_incident/)._

## The question

Calling for help too late costs time. Calling without context costs the other person's time. The question is: when do I bring someone in, and what do I bring?

## What PagerDuty's guidance says

- If no incident commander (IC) is on the call, page one. The guidance is not to hesitate: paging an IC is encouraged even when it may turn out not to be needed.
- The IC's job is to resolve the incident as quickly and safely as possible, by delegating to the right experts, not by fixing it alone.
- Subject matter experts report their findings to the IC, and say so when they're still investigating without a confirmed cause.
- The IC can split off sub-teams when the incident grows or gets more complex.
- Someone other than the person fixing sends regular status updates to stakeholders.

## When to escalate

The guidance leans toward calling early, and a team turns that into criteria written before the incident, so nobody has to judge it alone at three in the morning. Typical criteria:

1. Users are still affected past the team's threshold, and there's no safe, reversible fix.
2. Data or security might be involved.
3. The cause is on a provider's side.
4. The incident is big enough that one person shouldn't fix it and communicate at the same time.

## What to bring

The same thing an expert reports to the IC: what you checked, what you ruled out, and what you think it is, saying clearly which parts are confirmed and which are still a hypothesis. The person you call starts from there instead of from zero.

_If you use rbadillap/sre: `respond-to-alert` lists escalation criteria like these, with a default threshold when the team has none._

## In one sentence

"I escalate on criteria we wrote before the incident, and I bring what I checked, what I ruled out, and what I think it is."

## Exercise

You've been on an incident for 20 minutes, users are still affected, and your one fix didn't work. Write the message you'd send when you page someone: three lines, no more.

---

_Written with an AI assistant from the source above._

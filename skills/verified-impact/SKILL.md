---
name: verified-impact
description: Discipline. Tell people what is known to be affected, without claiming a cause too early. Applied by every orchestrator in this package when writing status updates, customer messages, escalations or incident summaries.
license: MIT
metadata:
  sre-layer: discipline
---

# Verified impact

**Share only confirmed impact, without claiming a cause too early.**

## When

In every update during an incident: to customers, to the team, to leadership, and in escalations.

## When not

Internal working notes can hold hypotheses, labeled as such. The rule is about what is shared as the state of things.

## How

1. **Every update has four parts:**
   - What is confirmed to be affected, and since when.
   - What is being checked now.
   - What people should do, if anything.
   - When the next update comes.
2. **No cause until it's verified.** "We are investigating elevated errors in device check-ins" is better than "a database issue is causing errors" if the database is still a hypothesis.
3. **Update early, even with little.** When users are already noticing, a first update without a cause is better than silence.
4. **One person communicates, another fixes.** In a large incident, ask for someone to own the updates, so the person fixing isn't doing both.

## The mistake it prevents

A cause announced too early has to be taken back, and that costs more trust than waiting. Communication becomes its own incident.

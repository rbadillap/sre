---
name: write-postmortem
description: Writes a blameless postmortem from an incident: timeline, impact, contributing factors, why it wasn't detected sooner, and follow-up actions that change defaults. Use after an incident is mitigated, or when someone asks for a postmortem, an incident review, a retrospective or "what happened and how do we stop it happening again".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: learn
  sre-safety: proposes
---

# Write a postmortem

**The question:** what happened, why did it happen and go unnoticed, and what changes so it doesn't come back?

**The result:** `reliability/postmortems/<date>-<slug>.md`, from [the template](assets/postmortem.md).

**Safety:** proposes. It reads the incident record and writes a document. It changes nothing in production.

## Steps

1. **Start from the record.** Read the incident file in `reliability/incidents/` if it exists. If not, rebuild the timeline from logs, messages and people, and say so.
2. **Write the impact, confirmed.** Apply `verified-impact`: who, what, for how long, measured with the signal users live. Separate measured numbers from estimates.
3. **Rebuild the timeline.** Every key fact and decision with its time: when it started, when it was detected, when people responded, when it was mitigated, when it was resolved. The gaps between those times are findings.
4. **Find the contributing factors, not one root cause.** Incidents usually need several things to go wrong. For each factor, say what made it possible. Write about systems and decisions, not people: "the alert depended on a tag nobody maintained", not "the team forgot the tag".
5. **Ask why it wasn't detected sooner.** This question always gets its own section. If a signal was missing, name it, and recommend `find-blind-spots`.
6. **Write what went well.** What limited the impact is worth keeping on purpose.
7. **Turn lessons into defaults.** Apply `paved-road`. Every follow-up action says where it lives (a default, a pipeline check, a template field, an alert) and has one owner and a date. Prefer few actions that change defaults over many reminders.
8. **Separate facts from guesses.** Apply `evidence-before-claims` across the whole document.
9. **Note lessons for the playbook.** If the incident showed that a runbook, a template or a rule the team follows was wrong or missing, write it in its own section, so it can be reviewed and adopted.
10. **Write the result** in `reliability/postmortems/<date>-<slug>.md`.

## Done when

- Impact, timeline, contributing factors and detection each have their section.
- Every action has a place, an owner and a date.
- Every claim is marked as measured, estimated or not verified.
- The language describes systems and decisions, not people.

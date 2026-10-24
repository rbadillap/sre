---
name: write-postmortem
description: Writes a blameless postmortem from an incident, with the timeline, the impact, the contributing factors, why it wasn't detected sooner, and follow-up actions that change defaults. Use after an incident is mitigated, or when someone asks for a postmortem, an incident review, a retrospective or "what happened and how do we stop it happening again".
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
2. **Reframe.** Apply `reframe-first`. The incident record has the reframe of the response; the postmortem asks a different question: not what broke, but what let it break and stay unnoticed.
3. **Write the impact, confirmed.** Apply `verified-impact`: who, what, for how long, measured with the signal users live.
4. **Rebuild the timeline.** Every key fact and decision with its time: when it started, when it was detected, when people responded, when it was mitigated, when it was resolved. The gaps between those times are findings.
5. **Find the contributing factors, not one root cause.** Incidents usually need several things to go wrong. For each factor, say what made it possible. Write about systems and decisions, not people: "the alert depended on a tag nobody maintained", not "the team forgot the tag".
6. **Ask why it wasn't detected sooner.** This question always gets its own section. If a signal was missing, name it, and recommend `find-blind-spots`.
7. **Ask whether a check that existed wasn't used.** If a review, a runbook or a skill would have caught this but wasn't run, that's a contributing factor of its own: say which, and why it wasn't run.
8. **Write what went well.** What limited the impact is worth keeping on purpose.
9. **Turn lessons into defaults.** Apply `paved-road`. Every follow-up action says where it lives (a default, a pipeline check, a template field, an alert) and has one owner and a date. Prefer few actions that change defaults over many reminders.
10. **Separate facts from guesses.** Apply `evidence-before-claims` across the whole document.
11. **Note lessons for the playbook.** If the incident showed that a runbook, a template or a rule the team follows was wrong, missing or not used, write it in its own section with a status: proposed, or adopted (where, and when).
12. **Write the result** in `reliability/postmortems/<date>-<slug>.md`.

## Done when

- The reframe is written.
- Impact, timeline, contributing factors and detection each have their section.
- Checks that existed but weren't used are named, or "none" is written.
- Every playbook lesson has a status.
- Every action has a place, an owner and a date.
- Every claim is labeled verified, hypothesis or not verified.
- The language describes systems and decisions, not people.

Next: recommend `learn-from-incident` to turn the playbook lessons into proposals.

---
name: learn-from-incident
description: Turns the lessons of a postmortem or review into proposed changes to how the team and this package work, such as templates, alert policies, runbooks, the skills themselves, or how and when they get used, for a person to approve. Use after a postmortem, after a review that found the process was wrong, or when the same kind of incident happens again. Phrases like "what should we change", "this keeps happening", "update the playbook", "lessons learned".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: learn
  sre-safety: proposes
---

# Learn from an incident

**The question:** what should change so the next person, or the next agent, doesn't hit this again?

**The result:** `reliability/learning/<date>-<slug>.md` in the team's repository, from [the template](assets/proposal.md). Create `reliability/` if it doesn't exist. Proposals for this package are drafts that a person can later open in the package's own repository (see step 7).

**Safety:** proposes. It never edits a skill, template, runbook or policy itself. A person approves each proposal, and someone else applies it.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Start from the record.** Read the postmortem in `reliability/postmortems/` and its incident record, or the review that prompted this.
2. **Reframe.** Apply `reframe-first`. The question isn't what went wrong in this incident, but what in the way of working let it happen or slowed the response.
3. **Find the lessons.** Read the contributing factors, "why it wasn't detected sooner", "checks that existed but weren't used", and the playbook lessons. For each, name the moment it hurt: a step that was missing, a step that misled, a question nobody asked, a signal that didn't exist, or a check that existed and wasn't used.
   - Also look for recurring manual work the record shows: toil. For each, write the task, how often it happens, the human time per run, the period, and where those numbers come from. Estimates are fine when labeled; write unknowns as unknown. Don't work out the team's total toil from incidents, and never use these numbers to judge a person.
4. **Check what already covers it.** Before proposing anything, look for the lesson where it would live: the package's skills, the team's `reliability/` paths and runbooks, and earlier learning records. Each lesson is then one of:
   - **New:** nothing covers it.
   - **Covered, but not used:** a rule or a check existed and nobody ran it. The lesson is about when it gets used: a trigger in a runbook or a pipeline, a router entry, the phrases in a skill's description. Ask why it wasn't run.
   - **Already adopted:** a change was made after the incident. Record where and when, and propose nothing.
5. **Place each new or unused lesson.** Apply `paved-road`. Where does it live so nobody has to remember it?
   - **This package:** a step, a template field, a pattern, a discipline, or a trigger that makes a skill get used.
   - **The team's paths:** a runbook, an alert policy, an SLO, a checklist, wherever the team keeps them.
   - **The system itself:** a default or a pipeline check. Those go back to the postmortem's actions; record that they were sent back.
6. **Write each proposal precisely.** The file, the current text, the proposed text, and why, with the line of the record it comes from. A lesson that can't be written as a change yet is recorded as not ready, with what's missing.
7. **Check package proposals against its review rules.** The rules are in the package's repository, under `docs/review/` (https://github.com/rbadillap/sre/tree/main/docs/review). If a proposal breaks one, say which, and propose changing the rule separately. Package proposals are drafts: after a person approves one, they rewrite it in general terms, with no private details from the incident, and only then open it as an issue or pull request in that repository.
8. **Check for repetition.** If an earlier learning record or incident pointed at the same lesson, link it. A lesson that comes back after a fix means the fix lived in the wrong place. Report a repeated lesson to whoever sets priorities, as reliability work, and apply the budget policy from `define-slos` if there is one.
9. **Label every claim** (`evidence-before-claims`), and write the result for a person to approve.

## Done when

- The record it comes from is linked, and the reframe is written.
- Every lesson has the moment it hurt and a state: new, covered but not used, or already adopted.
- Recurring manual work the record shows has its task, frequency, time per run, period and source, or "none found" is written.
- Every new or unused lesson has a place; lessons sent back to the system are recorded as sent.
- Every proposal has the file, the current text, the proposed text, the reason and the source line, or is recorded as not ready with what's missing.
- Every package proposal is checked against the review rules, with any rule change proposed separately.
- Repeated lessons are linked and reported to whoever sets priorities, and every claim is labeled.

Next: a person approves or rejects each proposal; approved package proposals go to the package's repository.

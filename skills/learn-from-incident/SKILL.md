---
name: learn-from-incident
description: Turns the lessons of a postmortem or review into proposed changes to how the team and this package work, such as templates, alert policies, runbooks or the disciplines themselves, for a person to approve. Use after a postmortem, after a review that found the process was wrong, or when the same kind of incident happens again. Phrases like "what should we change", "this keeps happening", "update the playbook", "lessons learned".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: learn
  sre-safety: proposes
---

# Learn from an incident

**The question:** what should change so the next person, or the next agent, doesn't hit this again?

**The result:** `reliability/learning/<date>-<slug>.md`, from [the template](assets/proposal.md). Create `reliability/` if it doesn't exist.

**Safety:** proposes. It never edits a skill, template, runbook or policy itself. A person approves each proposal, and someone else applies it.

## Steps

1. **Start from the record.** Read the postmortem in `reliability/postmortems/` and its incident record, or the review that prompted this.
2. **Reframe.** Apply `reframe-first`. The question isn't what went wrong in this incident, but what in the way of working let it happen or slowed the response.
3. **Find the lessons.** Read the contributing factors, "why it wasn't detected sooner", and the playbook lessons. For each, name the moment it hurt: a step that was missing, a step that misled, a question nobody asked, a signal that didn't exist.
4. **Place each lesson.** Apply `paved-road`. Where does it live so nobody has to remember it?
   - **This package:** a step in an orchestrator, a field in a template, a pattern in a table, or a discipline.
   - **The team's paths in `reliability/`:** a runbook, an alert policy, an SLO, a readiness checklist.
   - **The system itself:** a default, a check in the pipeline. Those go back to the postmortem's actions, not here.
5. **Write each proposal precisely.** The file, the current text, the proposed text, and why, with the line of the record it comes from. A proposal that can't be written as a change isn't ready.
6. **Check it against the review rules.** A proposal for this package must pass the rules in its review pages, such as `docs/review/skills.md`. If it breaks one, say which and propose changing the rule separately.
7. **Check for repetition.** If an earlier proposal or incident already pointed at the same lesson, say so: a lesson that comes back is a sign the first fix lived in the wrong place.
8. **Label every claim** (`evidence-before-claims`), and write the result for a person to approve.

## Done when

- The record it comes from is linked, and the reframe is written.
- Every lesson has the moment it hurt and the place it lives.
- Every proposal has the file, the current text, the proposed text, the reason and the source line.
- Every proposal for this package is checked against its review rules.
- Repeated lessons are marked, and every claim is labeled.

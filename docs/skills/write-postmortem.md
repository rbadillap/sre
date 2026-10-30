# write-postmortem

Writes a blameless postmortem after an incident: what happened, why it happened and went unnoticed, and what changes so it doesn't come back. It asks a different question from the response. Not what broke, but what let it break and stay unnoticed.

The method the agent follows is in [`SKILL.md`](../../skills/write-postmortem/SKILL.md). This page helps you choose the skill and read what it leaves.

## When to choose it

- An incident is mitigated, and the team needs to understand it and stop it from coming back.
- Someone asks for a postmortem, an incident review or a retrospective.

Choose another skill when:

- The incident is still going on: [`respond-to-alert`](../../skills/respond-to-alert/SKILL.md), or [`contain-security-incident`](../../skills/contain-security-incident/SKILL.md) for a security incident.
- The postmortem is written, and its lessons should become changes to the playbook: [`learn-from-incident`](../../skills/learn-from-incident/SKILL.md).

## What to have before starting

- The incident record in `reliability/incidents/`, if `respond-to-alert` was used. Without it, the timeline is rebuilt from logs, messages and people, and the postmortem says so.
- The signal users felt, to confirm the impact: who, what and for how long.
- Earlier postmortems in `reliability/postmortems/`, to find an incident with the same cause.
- Access to the people who responded, for what no log shows.

## What you get back

A file at `reliability/postmortems/<date>-<slug>.md`, from [the template](../../skills/write-postmortem/assets/postmortem.md). How to read it:

- **Impact** is confirmed with the signal users live, not with server health.
- **The timeline** has a time for each key moment: start, detection, response, mitigation, resolution. A long gap between two of them is a finding.
- **Contributing factors** come in plural. Incidents usually need several things to go wrong, and each factor says what made it possible.
- **Why it wasn't detected sooner** always has its own section, including pages the team got used to dismissing.
- **Earlier incidents with the same cause** are linked, with why their actions didn't prevent this one. "None found" is a valid answer.
- **Follow-up actions** say where they live (a default, a pipeline check, a template field, an alert), with one owner and a date. "Be more careful" isn't an action.
- **The language** is about systems and decisions, not people: "the system allowed the delete without confirming the host", not "the engineer picked the wrong server".
- **Labels** mark each claim as verified, hypothesis or not verified.

## What it doesn't solve

- It changes nothing in production. The actions it proposes are for people to take.
- It doesn't stop at one root cause. It looks for every contributing factor.
- It doesn't judge people. Blame makes people less likely to bring problems to light ([Google SRE book, Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)).

## Common questions

**Why several factors instead of a root cause?** Looking for contributing factors keeps the analysis from stopping at the first failure it finds. It looks at the conditions and decisions that let the incident happen, and each one is a chance to prevent the next.

**What if the same thing already happened?** The postmortem links the earlier one and asks why its actions didn't work: never done, done as a reminder instead of a default, or done in the wrong place. The new actions climb toward a default or a blocking check.

**Can we skip "what went well"?** It's short, but keep it. What limited the impact is worth keeping on purpose.

**Who writes it?** The skill drafts it from the available record and marks what it could not verify.

## Next step

Turn the playbook lessons into proposals with `learn-from-incident`.

Terms used here are defined in the [glossary](../glossary.md).

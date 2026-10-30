# define-slos

Decides what "working" means for the people who use a system, and how much failure is acceptable. It leaves a written definition: the indicators, the targets, the error budget and what happens when the budget runs out.

The method the agent follows is in [`SKILL.md`](../../skills/define-slos/SKILL.md). This page helps you choose the skill and read what it leaves.

## When to choose it

- A team needs to define reliability for a service, a job or a device fleet for the first time.
- Dashboards are green but customers complain, or engineering and product disagree about whether the service is healthy.
- A customer asks for an SLA, or someone asks "can we promise 99.99%?".

Choose another skill when:

- The SLOs exist and the question is what should page someone: [`design-alerts`](../../skills/design-alerts/SKILL.md).
- Users are affected right now: [`respond-to-alert`](../../skills/respond-to-alert/SKILL.md).
- The worry is failures that no signal can see: [`find-blind-spots`](../../skills/find-blind-spots/SKILL.md).

## What to have before starting

- Who uses the system and what they come to do. Internal users and devices count.
- Any data on what the system achieves today: success rates, latency, counts of releases or jobs. Without data, the targets come back as hypotheses, with what would measure them.
- Past incidents, if there are any. They test the attribution rules.
- Who should agree: the people who build the system and the people who use or sell it.

## What you get back

A file at `reliability/slos/<system>.md`, from [the template](../../skills/define-slos/assets/slo.md). How to read it:

- **SLIs** are written as good events over valid events, with where each is measured. Closer to the user is better.
- **Eligibility** says which users, devices or requests count. **Attribution rules** say which failures count against the service. Both are written before the next incident, so an incident can't bend them.
- **Each SLO** has a target, a window, a breakdown (per tenant or group as well as in total), and where the target came from: data, or a hypothesis.
- **The error budget** comes from a script, in time or, for rare events like releases, in events. If the budget is less than one event, a single failure breaks the SLO, and the file says so.
- **The budget policy** says what changes when the budget runs out. A budget with no policy is only a number.
- **Labels** mark each claim as verified, hypothesis or not verified.

## What it doesn't solve

- It doesn't change monitoring, dashboards or configuration. It proposes a definition; people decide.
- It doesn't set alerts. That's `design-alerts`, which reads these SLOs.
- It can't make a target true. A target with no data behind it stays a hypothesis until a window of data confirms it.

## Common questions

**Why not 99.99%?** A target above what the system achieves today is broken from day one. The skill sets targets at or below today's level and above where users start to notice.

**Our releases happen a few times a week. Does a percentage still work?** Read the budget in events. With 40 releases a month and a 99% target, the budget is 0.4 failures, so the first failure breaks it. Lower the target, lengthen the window, or treat every failure as an event of its own.

**What if nobody agrees yet?** The file says "not yet agreed". An SLO is a decision between people, and the file doesn't pretend otherwise.

**Is an SLA the same thing?** No. An SLA is a contract with consequences. It should be looser than the SLO, and the SLO looser than what the system achieves.

## Next step

Alert on the error budget with `design-alerts`.

Terms used here are defined in the [glossary](../glossary.md).

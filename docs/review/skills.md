# Reviewing a skill

This page covers orchestrators and the router. Disciplines have [their own page](disciplines.md).

## Shape

**1. It answers a reliability question and leaves a reusable result.**
- Why: SRE is what the package is about; platform engineering is how it delivers. A skill that only gives advice leaves nothing for the next time. A skill that only fills templates has no reliability question behind it.
- Check: the skill names the question it answers ("is this release safe to ship?") and the file it leaves in `reliability/`.

**2. The name says the layer.**
- Why: a reader, or an agent, should know what a skill is from its name alone.
- Check: orchestrators start with a verb (`respond-to-alert`, `review-release`). Disciplines are nouns (`reversible-first`). The router is `sre`. Names are lowercase, digits and hyphens, as the Agent Plugins spec requires.

**3. The description says when to use it, in the words of that moment.**
- Why: the agent picks a skill by matching its description against what someone just wrote. A description of what the skill is, instead of when it's needed, gets missed.
- Check: the description includes phrases someone would type at that moment ("latency is up", "we're draining nodes tomorrow"), not only a summary.

**4. It's short, with the detail in layers.**
- Why: the agent loads the whole `SKILL.md` every time. Detail it doesn't need costs context and attention.
- Check: `SKILL.md` holds the steps and the decisions. Examples, long explanations and stack-specific material live in `references/`.

## Safety

**5. It declares its safety level.**
- Why: a skill that acts in production is a different thing from one that reads. People need to know which one they're running.
- Check: `SKILL.md` states one level: reads only, proposes changes, or acts with approval.

**6. It never runs anything irreversible on its own.**
- Why: a bad code change makes a bad commit. A bad production action can take a service down or lose data.
- Check: every step that deletes, restores, fails over, migrates data or changes access ends with a proposal and waits for a person. Look for commands in the steps and ask what happens if they run twice, or by mistake.

## Method

**7. It follows the method, in order.**
- Why: the value of the package is how it thinks, not the topics it covers. A skill with good shape and a skipped step teaches the agent to skip that step.
- Check: compare the steps with the moves the orchestrator needs (table below). Every move is there, in that order, with a concrete mechanism and not only its name.

| Orchestrator | Moves, in order |
|---|---|
| `respond-to-alert` | Reframe the problem. Scope it (regions, tenants, errors or latency). Look for what changed, even with no deploy. Mitigate with what can be undone. Share only confirmed impact. Escalate on clear criteria: time without a safe fix, data at stake, a provider involved |
| `review-release` | Separate the deploy from the release. Check state compatibility across the versions that can coexist. Decide whether rollback is safe or the change needs a forward plan. Set the observation time longer than the effect it waits for, and name what the gate between steps checks and who moves past it |
| `find-blind-spots` | Ask what each signal can't see. Look for failures before the request reaches the service. Look at the worst tenant, not the average |
| `define-slos` | Reframe from server health to what users need. Map the journey, users can be internal. SLIs as good over valid, measured close to the user. Eligibility and attribution rules written before any incident. Targets broken down so a large tenant can't hide a small one. Budget from the script, with a policy |
| `design-alerts` | Reframe from metrics to situations that need a person. Page on symptoms and budget burn; route causes elsewhere. Two windows per burn alert, thresholds from the script. Minimum volume on breakdowns. A runbook and an owner per page. A monthly review |
| `review-design` | Name what's reviewed. Reframe from "does it work" to "how does it fail". Dependencies slow, down and recovering. Shutdown, health checks, repeated work, state, capacity. Operations ready. Findings by risk, with a blocking flag |
| `plan-migration` | Reframe a migration as a change to data that outlives the code. Everyone who reads and writes it. Steps by expand and contract, data copies apart from deploys. Each step safe to repeat, sized, with a way back and a check. Irreversible steps and restores go to a person |
| `plan-maintenance` | Reframe past failures by comparing what recovered with what didn't. Replicas, spread, disruption limits, shutdown time, spare capacity. Stateful systems by their own procedure. Batches, checks between them, stop conditions. Confirm completion |
| `contain-security-incident` | Bring in security. Reframe drift or odd access as possible compromise. Preserve evidence before changing anything. Revoke sessions, disable without deleting, remove added access, close the way in. Protect legitimate workloads. Search persistence from the first suspicious action. Rotate what was reachable. Restore only when every condition holds |
| `reconcile-drift` | Reframe drift that opens access as a possible incident. List differences without applying. Sort by urgency. Find who and when. Contain narrowly with a named identity. Find why a replacement is wanted and fix the code. Decide which side is right for every difference. Propose guardrails |
| `learn-from-incident` | Start from the record. Reframe from what went wrong to what in the way of working let it happen. Place each lesson where nobody has to remember it. Write each proposal as an exact change with its source. Check it against the review rules. Mark repeated lessons |
| `write-postmortem` | Start from the record. Confirm the impact. Rebuild the timeline. Find contributing factors, not one root cause, about systems and not people. Ask why it wasn't detected sooner. Turn lessons into defaults, each with an owner |

New orchestrators add their row here in the same pull request.

**8. It uses disciplines by name and doesn't copy them.**
- Why: two copies of a rule drift apart, and then the package disagrees with itself.
- Check: the skill says "apply `reversible-first`" and doesn't restate the discipline's explanation or mechanisms. Naming the move in one line, as rule 7 asks, isn't copying. Repeating how the discipline does it is.

**9. Every part of the situation gets an answer.**
- Why: the easiest step to skip is the one nobody asked about twice. Skipped parts are the most common gap in SRE answers.
- Check: if the skill handles a situation with several parts (investigate, prioritize, escalate), each part has its own step and its own output.

## Output

**10. It writes only to `reliability/`, and names the template it fills.**
- Why: one folder is the paved road. If each skill writes where it likes, there's no road.
- Check: every file the skill creates is under `reliability/` and comes from a template in the skill's own `assets/` folder.

**11. The method is in the body; the stack is in `references/`.**
- Why: the same skill should work for a team on Kubernetes, on serverless or on bare metal.
- Check: `SKILL.md` reads the same if you replace "Kubernetes" with any other platform. Commands and product names appear only in `references/`.

**12. It doesn't assume one kind of system.**
- Why: a skill written for a web service with traffic and tenants misleads on a device fleet, a batch job or an internal platform.
- Check: words like traffic, tenant or feature flag come with what to do when they don't apply. Users can be internal: an operator shipping a release is a user.

## Done

**13. "Done when" can be checked, and covers every step that produces something.**
- Why: a skill can be "done" while skipping the steps that find the most.
- Check: every criterion can be answered yes or no by reading the result. Every step whose output goes into the template appears in a criterion, including the reframe and the verified, hypothesis and not verified split.

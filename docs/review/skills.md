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
| `review-release` | Separate the deploy from the release. Check state compatibility across the versions that can coexist. Set the observation time longer than the effect it waits for. Decide whether rollback is safe or the change needs a forward plan |
| `find-blind-spots` | Ask what each signal can't see. Look for failures before the request reaches the service. Look at the worst tenant, not the average |

New orchestrators add their row here in the same pull request.

**8. It uses disciplines by name and doesn't copy them.**
- Why: two copies of a rule drift apart, and then the package disagrees with itself.
- Check: the skill says "apply `reversible-first`" and doesn't restate the discipline's text.

**9. Every part of the situation gets an answer.**
- Why: the easiest step to skip is the one nobody asked about twice. Skipped parts are the most common gap in SRE answers.
- Check: if the skill handles a situation with several parts (investigate, prioritize, escalate), each part has its own step and its own output.

## Output

**10. It writes only to `reliability/`, and names the template it fills.**
- Why: one folder is the paved road. If each skill writes where it likes, there's no road.
- Check: every file the skill creates is under `reliability/` and comes from a template in `templates/`.

**11. The method is in the body; the stack is in `references/`.**
- Why: the same skill should work for a team on Kubernetes, on serverless or on bare metal.
- Check: `SKILL.md` reads the same if you replace "Kubernetes" with any other platform. Commands and product names appear only in `references/`.

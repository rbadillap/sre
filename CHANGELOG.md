# Changelog

What changed in each released version, and why. An entry is written when a version is released, summarizing everything since the last one; work in progress lives in the git history. Changes that come from the learning loop say which kind of incident or review taught them, in general terms.

The package follows [semantic versioning](https://semver.org): a new skill or template is a minor version; a change that breaks how an existing skill is used, or where it writes, is a major version.

## 0.1.1

No new skills or templates. The existing skills ask more, and the templates have room for it.

- **Disciplines are read, not guessed.** Every orchestrator and the router find a discipline's `SKILL.md` and read it before applying it. If it isn't installed, they say so, recommend installing the whole package, and mark what depends on it as incomplete. `make validate` checks that the paragraph is the same everywhere.
- **Incident timelines** keep the time an event happened apart from the time it was recorded. The record time comes from a clock, never from the conversation. Every action has a status (proposed, done, result) and says who did it, and the agent keeps the scribe's record while it investigates. This applies to `respond-to-alert` and `contain-security-incident`, with example rows in both templates.
- **Escalation** uses the team's threshold, with 15 to 20 minutes as a default when there's none. It also escalates when the person running a step can't confirm its target or go on safely.
- **Irreversible steps:** `reversible-first` checks the target first, asks for an independent review when risk or policy requires it, and stops when the target can't be confirmed.
- **Releases:** `review-release` covers changes that reach production outside the pipeline (rules, flags, configuration, content) and sets conditions for an emergency path. It also checks work that can run twice, applying `idempotency`. The device fleet examples check that recovery survives the failure it's meant to fix.
- **Responding to repeated effects:** `respond-to-alert` treats them as a hypothesis, and checks that a retry or replay is safe before proposing it. A timeout doesn't prove the work didn't happen.
- **Data changes:** a down migration counts as a way back only if it has been run. `expand-contract` keeps the copy from overwriting newer writes, keeps both forms in sync through the switch, and moves reads only when nothing writes the old form alone.
- **Restores:** `review-design` checks that restores are tested as an ongoing practice, with an owner, a frequency and its reason, the last result, and an alert if the test fails or stops.
- **Repeated incidents and toil:** `write-postmortem` looks for an earlier incident with the same cause and treats pages the team got used to as findings. `learn-from-incident` records recurring manual work and reports repeated lessons to whoever sets priorities. `paved-road` raises the action when a lesson comes back, has tools refuse what breaks a checkable limit, and ranks fixes for toil by the load and risk they remove, against their cost. `design-alerts` reports on-call load as a number: pages, and incidents and time spent when there's data.
- **Glossary:** down migration, escalation threshold, scribe, toil and on-call load.
- **Calculators:** `error-budget.py` computes in exact decimals from the input text, so a budget of exactly one event doesn't warn, and shows enough decimals to tell the achieved value from the target.
- **Security references:** network isolation works in both directions. Policies are additive, so a deny policy can leave a pod open, and relabeling a pod is an option to check, not a fix.
- **Evals:** a new `respond-to-alert` scenario from a public storage outage after a capacity removal. The eval rules accept public postmortems as real use, linked, with what was added for the exercise marked.

Shaped by real use:

- Teaching SRE with the package, one block at a time, kept finding places where a good answer wasn't in the skill. Each became a proposal, checked against the package and its sources, and approved before it was applied.
- Public postmortems were compared with the skills step by step, without claiming a skill would have found the cause sooner. They covered a storage outage, a global proxy outage, a lost database and a content update that crashed devices on boot. The gaps were changes outside the pipeline, untested restores, irreversible steps without a check of the target, and recovery that depended on the thing that failed.
- An independent review corrected the calculators' rounding, the network isolation reference and the data copy in `expand-contract`.

## 0.1.0

The first release.

- **A router,** `sre`, that points a situation to the right orchestrator.
- **Twelve orchestrators,** one per moment of the work, each with its template: `define-slos`, `review-design`, `plan-migration`, `review-release`, `plan-maintenance`, `design-alerts`, `find-blind-spots`, `respond-to-alert`, `contain-security-incident`, `reconcile-drift`, `write-postmortem` and `learn-from-incident`.
- **Nine disciplines:** `reframe-first`, `scope-and-signal`, `reversible-first`, `state-is-special`, `evidence-before-claims`, `verified-impact`, `paved-road`, `idempotency` and `expand-contract`.
- **Two calculators:** `error-budget.py` in `define-slos` and `burn-rate.py` in `design-alerts`.
- **Docs:** the method, the lifecycle, the layers, the landscape, the glossary and the review rules.
- **Two evals,** drawn from real runs on an over-the-air update fleet.

Shaped before release by real use:

- Two rounds of runs by agents that had never seen the package, on a working prototype, found gaps in the skills themselves: templates without a place for what the steps asked, labels that didn't match, skills that assumed a web service with traffic, and "done" criteria that skipped the steps that found the most. Each became a fix and, where it applied, a review rule.
- A live incident, a release that crashed after its canary check, was handled with `respond-to-alert` and written up with `write-postmortem`. The postmortem's lesson became part of `respond-to-alert`: a fix shipped as a new release is confirmed past the failure's delay.
- An independent review of the whole package corrected security references (session revocation for leaked keys and stolen tokens), Kubernetes details and the calculators' input checks.

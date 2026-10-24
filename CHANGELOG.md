# Changelog

What changed in each released version, and why. An entry is written when a version is released, summarizing everything since the last one; work in progress lives in the git history. Changes that come from the learning loop say which kind of incident or review taught them, in general terms.

The package follows [semantic versioning](https://semver.org): a new skill or template is a minor version; a change that breaks how an existing skill is used, or where it writes, is a major version.

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

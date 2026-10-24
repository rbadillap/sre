# sre

A senior SRE's method, packaged as agent skills.

Most SRE skill packs are organized like the chapters of a book: one skill for SLOs, one for incidents, one for postmortems. This one follows the work itself. It moves through a lifecycle (define, design, ship, observe, respond, learn), and every orchestrator leaves a reusable result in your repository, under `reliability/`.

> **Status:** version 0.1.0, the first release. See the [changelog](CHANGELOG.md).

## What's inside

- **A router,** `sre`, that points a situation to the right skill.
- **Twelve orchestrators,** one per moment of the work: `define-slos`, `review-design`, `plan-migration`, `review-release`, `plan-maintenance`, `design-alerts`, `find-blind-spots`, `respond-to-alert`, `contain-security-incident`, `reconcile-drift`, `write-postmortem` and `learn-from-incident`.
- **Nine disciplines,** the rules every orchestrator applies by name, like "mitigate with what you can undo first".
- **Templates** inside each orchestrator, the paths the skills leave behind so the next time is easier.
- **Two calculators:** the error budget for an SLO, and burn rate thresholds for alerts.

Skills investigate and propose. Anything that can't be undone waits for a person. What an incident teaches becomes a proposed change to the skills, and a person approves it.

## Install

It's an [Agent Plugins](https://agent-plugins.org) plugin with [Agent Skills](https://agentskills.io) inside.

```sh
npx skills add rbadillap/sre
```

Or install it as a plugin from `https://github.com/rbadillap/sre` in any client that supports Agent Plugins.

## Use

Describe the situation to your agent in your own words ("latency is up and the cluster looks healthy", "can we ship this on Friday?", "Terraform wants to replace the database"). The skill's description matches what you say. If you're not sure where to start, ask for the `sre` skill.

## Learn more

- [The method](docs/method.md): seven moves every skill applies.
- [The lifecycle](docs/lifecycle.md): six stages, and where they come from.
- [Layers](docs/layers.md): router, orchestrators, disciplines, templates, safety and learning.
- [Landscape](docs/landscape.md): what else exists, and where this fits.
- [Review](docs/review/README.md): the rules every change meets.

## License

[MIT](LICENSE)

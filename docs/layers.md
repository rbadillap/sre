# Layers

The package has four layers. Each one has a single job.

| Layer | Job | Where it lives |
|---|---|---|
| Router | Sends you to the right orchestrator | `skills/sre/` |
| Orchestrators | Run one moment of the work | `skills/<verb-name>/` |
| Disciplines | Hold the rules every orchestrator follows | `skills/<noun-name>/` |
| Templates | Become the reusable result in your repository | `skills/<verb-name>/assets/` |

## Router

`sre` listens to the situation ("latency is up", "we're draining nodes tomorrow", "Terraform wants to replace the database") and points to the orchestrator for it. Use it when you're not sure where to start.

## Orchestrators

An orchestrator runs one moment of the work, from one stage of the [lifecycle](lifecycle.md). It asks the questions, applies the disciplines in order, and leaves a file in `reliability/`.

- Names start with a verb: `respond-to-alert`, `review-release`, `define-slos`.
- An orchestrator applies disciplines by name. It doesn't call another orchestrator. When the work moves to another stage, it recommends the next one: `respond-to-alert` ends by recommending `write-postmortem`.
- Before applying a discipline, an orchestrator finds its `SKILL.md` and reads it: installed isn't the same as loaded. If the discipline isn't installed, the orchestrator says so in its result, recommends installing the whole package, goes on only with work that doesn't depend on it, and marks what depends on it as incomplete. It doesn't guess the rule, because a guessed rule is a second copy that drifts. The router does the same. `make validate` checks that every orchestrator and the router carry the same paragraph.

## Disciplines

A discipline is one rule, small and shared. The seven [moves of the method](method.md) are disciplines, plus two mechanisms that come up so often they earn their own: `idempotency` and `expand-contract`.

- Names state a principle, not a task: `reversible-first`, `state-is-special`, `expand-contract`. An orchestrator's name is a task you ask for (`respond-to-alert`); a discipline's is a rule you follow.
- A discipline has no stack. Product names and commands live in an orchestrator's `references/`.
- Keeping each rule in one place means the package can't disagree with itself.

## Templates

Templates are where reliability meets platform engineering. **Reliability is what the package is about. Platform engineering is how it delivers.** A skill doesn't stop at advice: it fills a template and leaves the result in your repository, so the next person starts from a path instead of a blank page.

Each template lives in the `assets/` folder of the orchestrator that fills it. The Agent Skills format resolves files relative to the skill, so the template has to travel with it.

Everything the skills write goes under one folder:

```
your-repo/
└── reliability/
    ├── slos/
    ├── readiness/
    ├── migrations/
    ├── releases/
    ├── runbooks/
    ├── alerting/
    ├── observability/
    ├── incidents/
    ├── changes/
    ├── postmortems/
    └── learning/
```

One folder is the paved road. If each skill wrote where it liked, there would be no road.

A simple test keeps the two halves together: every skill answers a reliability question and leaves a platform result. If it only gives advice, it's missing the platform half. If it only fills templates, it's missing the reliability question.

## Safety

Every orchestrator and the router declare one level, in their body and in `metadata` as `sre-safety`. Disciplines don't declare one: they hold rules and never act on their own.

| Level | `sre-safety` | Means |
|---|---|---|
| Reads only | `reads-only` | Looks at code, configuration and signals. Changes nothing except its own result file in `reliability/` |
| Proposes | `proposes` | Writes a plan in `reliability/` with actions for a person to run. Runs nothing in production |
| Acts with approval | `acts-with-approval` | Can run a step after a person approves it, one step at a time. No skill uses this level yet |

Every level may write its own result in `reliability/`, and create the folder if it doesn't exist yet. That file is the only thing a skill changes without asking.

No skill runs anything irreversible on its own: deleting, restoring, failing over, migrating data or changing access always ends in a proposal for a person.

## Learning

The last stage of the lifecycle is where this package differs from a book. `learn-from-incident` reads a postmortem and proposes changes:

- to a template, so the next result asks the question that was missed;
- to an alert policy, so the signal that was missing exists;
- to a discipline, when the rule itself was wrong or incomplete.

It proposes; a person approves. Approved changes are listed in `CHANGELOG.md` with their reason when the next version is released, so the package improves with each incident without losing track of why.

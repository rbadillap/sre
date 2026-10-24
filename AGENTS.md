# AGENTS.md

Rules for any agent working in this repository. How the package works is in `docs/`; this page is rules only.

## Before you change anything

- Read the review page for what you're changing, in `docs/review/`. A change is ready when every rule that applies passes.
- If a rule doesn't fit, change the rule in its own pull request first. Never skip it quietly.

## Writing

- English, plain words, short sentences.
- Nothing personal: no companies, people, employers or private incidents. Examples are general.
- A claim about an external framework, spec or number links to its source, and you've checked the source says it.
- Documents describe how things are now. History goes in `CHANGELOG.md`.
- Every rule says why it exists, on the same page. This repository has no decision records.
- Use the terms in `docs/glossary.md` as defined there. A new shared term goes into the glossary in the same change.

## Skills

- One folder per skill under `skills/`, with a `SKILL.md`. No nested folders: the Agent Plugins spec only reads immediate children.
- Orchestrators start with a verb; disciplines are nouns. Lowercase, digits and hyphens only.
- Every skill declares its safety level. No skill runs anything irreversible on its own.
- Skills write only to `reliability/`, from a template in their own `assets/` folder.
- Stack-specific examples go in the skill's `references/`, one level deep.
- Every `SKILL.md` has `name` matching its folder, a `description` that says when to use it, `license: MIT`, and `metadata` with `sre-layer` and, for orchestrators, `sre-stage` and `sre-safety`.
- Disciplines are applied by name, never copied.
- A new orchestrator adds its row of moves to `docs/review/skills.md` in the same change.

## Manifest

- `plugin.json` stays valid against the Agent Plugins 1.0.0 schema.
- Bump `version` with every release, following the rules in `CHANGELOG.md`.

## Validation

- Run `make validate` before every commit that touches `skills/` or `plugin.json`. It needs `uv`.
- Pin tool versions in the `Makefile` from their live registries, at least 7 days old.

## Commits

- Message format: `area: what changed, in plain words`. Areas are the folder or file touched: `docs`, `skills`, `templates`, `evals`, `base`.
- One commit per document, skill or template, so each can be reviewed or reverted alone.
- Every user-visible change adds a line to `CHANGELOG.md` under Unreleased.
- Commits are signed. If signing fails, stop and ask; never bypass it.
- No co-author trailers or generated-by lines for AI tools, in commits or pull requests.
- Edit files with your editing tools, not with shell scripts over the source.

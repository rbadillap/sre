# AGENTS.md

Rules for any agent working in this repository, each with its reason. How the package works is in `docs/`; this page is rules only.

## Before you change anything

- Read the review page for what you're changing, in `docs/review/`. A change is ready when every rule that applies passes. Why: the review pages are how a person and an agent judge a change the same way.
- If a rule doesn't fit, change the rule in its own pull request first. Why: a rule skipped quietly stops being a rule.

## Writing

- English, plain words, short sentences. Inside `academy/`, a lesson is written in the language of its `<lang>` folder. Why: readers may be on call, tired or reading in a second language, and a lesson is easier to learn from in the reader's own language.
- Nothing personal: no companies, people, employers or private incidents. A link to public material, such as a provider's postmortem or guide, keeps its attribution; the text around it stays in general terms. In `academy/`, a lesson may name the organizations and products a linked public case needs, as long as its claims match the source, published facts stay apart from the lesson's interpretation and examples, and no people's identities, employer experiences or private details are added. Why: the package teaches a method, in public, and a citation without its source can't be checked; in a lesson, the public case is what's being taught. The exception doesn't reach skills, disciplines or evals.
- A claim about an external framework, spec or number links to its source, and you've checked the source says it. Why: a method that cites wrongly loses trust.
- Documents describe how things are now. A lesson may tell the story of a past incident; what it says about the package still describes the package as it is. Why: readers need the current rule; history is in git, and in `CHANGELOG.md` at each release.
- Every rule says why it exists, on the same page. Why: this repository has no decision records, so the reasoning lives next to the rule.
- Use the terms in `docs/glossary.md` as defined there, and add a new shared term in the same change. Why: skills read the same words the same way.

## Skills

- One folder per skill under `skills/`, with a `SKILL.md`, and no nesting. Why: the Agent Plugins spec only reads immediate children.
- Orchestrators are named as a task, starting with a verb; disciplines as a principle; lowercase, digits and hyphens only. Why: the name tells the layer, and the specs require the characters.
- Orchestrators and the router declare a safety level, in the body and as `sre-safety`. No skill runs anything irreversible on its own. Why: people need to know what a skill may do before running it.
- Skills write only to `reliability/`, from a template in their own `assets/` folder. Why: one folder is the paved road, and a skill can be installed alone.
- Stack-specific examples go in the skill's `references/`, one level deep. Why: the method has to work on any platform.
- Every `SKILL.md` has `name` matching its folder, a `description` that says when to use it, `license: MIT`, and `metadata` with `sre-layer`, plus `sre-stage` for orchestrators and `sre-safety` for orchestrators and the router. Why: the specs require the first ones, and `make validate` checks the `sre-*` keys so the docs and the skills can't disagree.
- Disciplines are applied by name, never copied. Why: two copies drift apart.
- A new orchestrator adds its row of moves to `docs/review/skills.md` in the same change. Why: the row is what its review checks.
- A change to how a skill behaves reviews its page in `docs/skills/`, if it has one, and updates in the same change whatever the change left out of date. A page holds no steps, "done" criteria or safety limits of its own; it links to `SKILL.md` for them. Why: `SKILL.md` is written for agents and the page for people, and two sets of steps drift apart. A typo fix doesn't need a page change.

## Manifest

- `plugin.json` stays valid against the Agent Plugins 1.0.0 schema. Why: clients reject an invalid manifest.
- Bump `version` with every release, following the rules in `CHANGELOG.md`. Why: users update by version.

## Validation

- Run `make validate` before every commit that touches `skills/` or `plugin.json`. It needs `uv`. Why: a broken frontmatter makes a skill invisible to agents.
- Pin tool versions in the `Makefile` from their live registries, at least 7 days old. Why: reproducible checks, and time for bad releases to be pulled.

## Commits

- Message format: `area: what changed, in plain words`, where the area is the folder or file touched (`docs`, `skills`, `evals`, `academy`, `base`). `academy` is for lessons; the rules about them in `docs/review/` use `docs`. Why: the log reads as a list of changes.
- Lessons follow `docs/review/academy.md`, and only a person marks a lesson `approved`. Why: a lesson teaches people directly, so a person answers for it.
- One commit per document, skill or template. Why: each can be reviewed or reverted alone.
- `CHANGELOG.md` gets an entry only when a version is released. Why: between releases, git is the record; the changelog is for users.
- Commits are signed. If signing fails, stop and ask; never bypass it. Why: signatures are how readers know who changed what.
- No co-author trailers or generated-by lines for AI tools, in commits or pull requests. Why: the author is the person who reviewed and signed the change.
- Edit files with your editing tools, not with shell scripts over the source. Why: edits stay exact and reviewable.

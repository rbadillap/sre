# Landscape

What already exists for SRE work with agents, and where this package fits. Surveyed on 2026-10-23. Projects change; check the links for their current state.

## What's out there

**Tool connectors.** Packages that give an agent access to an incident or observability product: incident.io, Datadog, Grafana, Sentry, Sumo Logic, OneUptime, Microsoft's Azure SRE Agent. They give access, not a method. They work well alongside this package: a skill decides what to look at, a connector reaches it.

**Platform packs.** SRE skills built around one cloud. The broadest is [sre-extension](https://agent-plugins.directory/gemini-cli-extensions/sre-extension.md) from `gemini-cli-extensions`: sixteen skills for investigation, mitigation, SLOs and postmortems, including a safety-minded investigator, mostly for Google Cloud.

**Topic packs.** General SRE skills organized by subject:

- [sre-practice-skills](https://github.com/paulip114/sre-practice-skills): eight skills (SLOs, alerting, incident response, postmortems, on-call, releases, capacity, data reliability). They produce documents and checklists.
- [operations](https://agent-plugins.directory/joao-aires/operations.md) by joao-aires: twelve platform-independent skills for incidents, recovery, capacity, runbooks and postmortems.
- [sre-engineer](https://jeffallan.github.io/claude-skills/skills/devops/sre-engineer/) by jeffallan: one skill with a specialist persona, a six-step workflow and must-do and must-not-do rules.
- Large collections such as [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), where SRE is one corner among hundreds of skills.

**Guides.** Anthropic's cookbooks show how to build [an SRE incident responder](https://platform.claude.com/cookbook/managed-agents-sre-incident-responder) and [a site reliability agent](https://platform.claude.com/cookbook/claude-agent-sdk-03-the-site-reliability-agent), with infrastructure changes going only through pull requests.

**A structural reference.** [mattpocock/skills](https://github.com/mattpocock/skills) isn't about SRE, but it shows how a set of skills can follow a lifecycle with layers: skills you invoke to run a flow, and shared skills that hold the discipline. This package borrows that idea of structure, not its method.

## What they share

Most SRE packs are organized like the chapters of a book: one skill for SLOs, one for incidents, one for postmortems. Each is a guide on its own.

## Where this package fits

| | Most SRE packs | This package |
|---|---|---|
| Organized by | Topic | [Lifecycle stage](lifecycle.md), with [layers](layers.md) |
| What a skill teaches | A subject | A moment of the work, applying a shared [method](method.md) |
| What a skill leaves | Advice or a document | A reusable result in `reliability/` |
| Safety | Rarely stated | Declared by every orchestrator; nothing irreversible runs alone |
| Learning | Ends in a postmortem | Postmortems lead to proposed changes to the skills, with approval |
| Proof | Not shown | Evals drawn from real use, starting with two |

The topics are covered elsewhere. What this package adds is the structure that connects them and the loop that improves them.

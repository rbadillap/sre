# sre

A senior SRE's method, packaged as agent skills.

Most SRE skill packs are organized like the chapters of a book: one skill for SLOs, one for incidents, one for postmortems. This one follows the work itself. It moves through a lifecycle (define, design, ship, observe, respond, learn), and every skill leaves a reusable result in your repository, under `reliability/`.

> **Status:** in design. Nothing to install yet.

## How it works

- **Orchestrators** run one moment of the work, like responding to an alert or reviewing a release.
- **Disciplines** are the rules every orchestrator follows, like "mitigate with what you can undo first".
- **Templates** are the paths the skills leave behind, so the next time is easier.
- **Learning** closes the loop: what an incident teaches becomes a proposed change to the templates and disciplines, and a person approves it.

Skills investigate and propose. Anything that can't be undone waits for a person.

## License

[MIT](LICENSE)

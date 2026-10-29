---
name: sre
description: Router for site reliability work. Use when you're not sure which reliability skill fits, or when someone describes a production situation in general terms ("something's wrong in production", "help me with reliability", "where do I start"). It reads the situation and points to the right orchestrator in this package.
license: MIT
metadata:
  sre-layer: router
  sre-safety: reads-only
---

# SRE router

**The question:** which moment of the work is this?

**The result:** a recommendation of one orchestrator, with the reason. It writes nothing.

**Safety:** reads only.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Read the situation.** Apply `reframe-first` in one line: what's actually being asked?
2. **Pick the stage.** If more than one fits, the earliest urgent one wins: something hurting users now is Respond, whatever else is going on.
3. **Recommend one orchestrator,** with one sentence on why, and the next one it will likely lead to.

| The situation sounds like | Stage | Orchestrator |
|---|---|---|
| Users are affected now: errors, slowness, something down, an alert firing | Respond | `respond-to-alert` |
| A credential, key or account may be compromised; access nobody granted | Respond | `contain-security-incident` |
| Infrastructure differs from its code; a plan wants to replace something important | Respond | `reconcile-drift` |
| An incident is over and needs a written review | Learn | `write-postmortem` |
| A postmortem or review should change how the team works | Learn | `learn-from-incident` |
| A change is about to ship, or someone wants to ship under pressure | Ship | `review-release` |
| Nodes, hosts or devices need maintenance, upgrades or drains | Ship | `plan-maintenance` |
| A change touches stored data, schemas, caches or message formats | Design | `plan-migration` |
| A new or changed system needs a check before it carries real traffic | Design | `review-design` |
| "What does reliable mean for this?"; customers disagree with the dashboards | Define | `define-slos` |
| Too many pages, or pages that miss what matters | Observe | `design-alerts` |
| Something failed and nothing noticed; "is our monitoring enough?" | Observe | `find-blind-spots` |

## Done when

- One orchestrator is recommended, with its reason and the likely next one.

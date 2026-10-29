---
name: contain-security-incident
description: Guides the first response to a suspected or confirmed security incident, such as leaked credentials, unexpected access, an identity or key nobody created, or exposure of a service that should be private. Contain first, preserve evidence, find persistence, and protect legitimate workloads. Phrases like "credentials leaked", "someone created a user", "suspicious API calls", "this port is open to the internet", "compromised key".
license: MIT
metadata:
  sre-layer: orchestrator
  sre-stage: respond
  sre-safety: proposes
---

# Contain a security incident

**The question:** how do we stop further access now, without destroying evidence or taking down what's legitimate?

**The result:** `reliability/incidents/<date>-<slug>.md`, from [the template](assets/security-incident.md), kept as a running record.

**Safety:** proposes. Every containment action is a proposal for a person, with its risk and how to undo it. Nothing the attacker created is deleted; a compromised workload is replaced only after its evidence is captured.

**Disciplines:** the steps apply disciplines from this package by name. Before applying one, find its `SKILL.md` and read it. If it isn't installed, don't guess its rule: say so in the result, recommend installing the whole package, go on only with work that doesn't depend on it, and mark what depends on it as incomplete.

## Steps

1. **Start the record, and bring in security.** Open the incident file with times from now on. A suspected compromise is a security incident until shown otherwise: page the security owner, and don't wait for them to start containing.
   - **Keep two times apart.** When something happened comes from where it was recorded: a log, a record, or a person's report, with that source and its precision ("about 10:00" stays approximate). When you wrote the line comes from the system clock, or a clock tool if there's no shell. If neither is available, write the time as unknown and ask for it when it matters, without stopping other work. Never work out a time from how long the conversation has taken. Write the time zone in the header, and keep both times when they differ.
   - **Give every action a status.** You only see what you run or read. An action you propose goes in the timeline as proposed, then as done, reported by a person (with their name) or seen by you, then with its result. Proposing an action doesn't prove it ran. Ask only for what the record is missing. You also do the scribe's record keeping ([PagerDuty's guide](https://response.pagerduty.com/training/scribe/)), while you investigate, which a dedicated scribe doesn't.
2. **Reframe.** Apply `reframe-first`. Drift, an odd account or an open port may be a symptom of access, not a mistake.
3. **Preserve evidence before changing anything.** Export the audit logs that cover the period, and save the current configuration of everything you're about to change.
4. **Contain the access, within the first minutes.** Apply `reversible-first`, with its exception: preserve, then contain.
   - **Stop current sessions,** including temporary credentials and tokens that are still valid, with whatever the platform offers to revoke sessions issued before now. Disabling a key or a password alone can leave sessions created from it working.
   - **Disable what the attacker created,** such as keys or accounts, without deleting them.
   - **Remove the access that was added,** such as an admin permission or an open network rule.
   - **Close the way in:** if a workload was the entry point, it can mint fresh credentials. Isolate it, capture its evidence, then replace it.
5. **Protect legitimate workloads.** Workloads that share the compromised identity usually get new credentials on their own after a session revocation. Say how each one is affected, and plan to move them to identities of their own, with only the access each needs. Don't keep an untrusted workload online to avoid downtime.
6. **Find persistence.** Search the audit logs from the first suspicious action, not from when you noticed: identities, keys, trust or access policies, scheduled jobs, functions, instances and network changes the attacker could have made.
7. **Assume exposure of everything reachable.** Rotate every secret the compromised identity could read. Ask whether user or customer data could have been read: if yes, legal and customer communication are part of the incident (`verified-impact`).
8. **Set the conditions to restore normal operations.** All of them, not one: no activity from the attacker since containment, persistence removed, the entry point found and fixed, secrets rotated, workloads on trusted identities, and the security owner's approval. Keep extra monitoring afterwards.
9. **Label every claim** (`evidence-before-claims`), and hand off to `write-postmortem`.

Platform examples: [references/cloud.md](references/cloud.md).

## Done when

- The reframe is written and security is involved, with the time.
- Evidence was preserved before the first change, and where it is is written.
- Every containment action is recorded with its time, how to undo it, and whether it worked.
- Every legitimate workload sharing the identity has its impact and plan.
- The persistence search covers the period from the first suspicious action, with what was found.
- Secrets to rotate and possible data exposure are listed.
- The restore conditions are written, with their status.
- Every claim is labeled verified, hypothesis or not verified.

Next: recommend `write-postmortem`.

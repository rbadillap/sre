# The method

Seven moves. They come back in every kind of reliability work, whether the problem is a slow API, a risky release or a leaked credential. The package teaches these moves, not a list of topics.

Each move is a [discipline](layers.md#disciplines): a skill that every orchestrator applies by name.

## 1. Reframe first

**Before solving, say what the real problem is.**

The way a problem arrives is rarely the problem. "The API is slow, but the cluster is healthy" usually means something is waiting, not that nothing is wrong. "Terraform shows drift" can be a security incident. "The rollback didn't fix it" means the release changed data, not code.

Without this move, the work goes into the wrong problem with full energy.

Discipline: `reframe-first`.

## 2. Scope it, and separate signal from noise

**Find out how far it reaches before acting, and which signals actually describe it.**

All regions or one? All tenants or a few? Errors, latency, or both? Then look for the signal that matches what users live, not the one that is easiest to read. An average hides the worst tenant, and a request metric can't see requests that never arrived.

Without this move, a fix aimed at the whole system hits a problem that lives in one corner, or the team trusts a green dashboard.

Discipline: `scope-and-signal`.

## 3. Mitigate first, with what can be undone

**Stop the impact before finding the root cause, and start with actions that can be reversed.**

Pause a job instead of deleting it. Rate-limit one tenant instead of blocking everyone. Revoke sessions instead of deleting a role. Anything that can't be undone, like a restore, a failover or a data change, waits for a person.

Watch the second-order effects. Scaling up an application can make a saturated database worse, because each new instance opens more connections.

Without this move, either users wait while the team investigates, or a fast fix causes a second incident.

Discipline: `reversible-first`.

## 4. State is special

**Data and state get their own plan, because rolling back code doesn't roll back data.**

A release that changed a cache format, a migration that dropped a constraint, a message processed twice: these survive a rollback. So changes to state are made compatible before they ship (expand, then contract), operations are made safe to repeat, and a snapshot is not treated as a safe rollback on its own, since restoring it loses everything written after it.

Without this move, the rollback succeeds and the data stays broken.

Disciplines: `state-is-special`, with `expand-contract` and `idempotency` for the two most common mechanisms.

## 5. Evidence before claims

**Verify before saying something is true, and say what wasn't verified.**

A hypothesis is a hypothesis until a signal confirms it. "The job is exhausting connections" becomes a fact when the database shows who holds them. "The fix worked" becomes a fact when the error rate and the user-facing signal recover. And when something couldn't be checked, the report says so.

Without this move, a guess travels as a fact, and the next decision is built on it.

Discipline: `evidence-before-claims`.

## 6. Share only confirmed impact

**Tell people what is known to be affected, without claiming a cause too early.**

Customers, the team and leadership need to act on what is happening, not on a theory. Say what is confirmed, what is being checked, and when the next update comes. A cause announced too early has to be taken back later, and that costs more trust than waiting.

Without this move, communication creates its own incident.

Discipline: `verified-impact`.

## 7. Make the safe path the easy path

**Prevent the next one by turning what was learned into a default, not a reminder.**

A lesson that lives in a document gets forgotten. A lesson that lives in a template, a check in the pipeline or a default in a shared module gets applied by everyone, even people who never heard of the incident.

This is where reliability meets platform engineering: the reliable way of working is delivered as a path the team uses without thinking about it.

Without this move, the same incident comes back with a different team.

Discipline: `paved-road`.

## Two habits that run through all seven

- **Answer every part of the situation.** When a problem has several parts (investigate, prioritize, escalate), each one gets its own step and its own result. The part nobody asks about twice is the one that gets skipped.
- **Name the mechanism, not only the idea.** "Make it idempotent" is an idea. "Store the event ID with a unique index and skip it when it comes back" is a mechanism. Skills always go down to the mechanism.

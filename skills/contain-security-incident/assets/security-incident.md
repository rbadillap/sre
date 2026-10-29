# Security incident: <short description>

<!-- Filled by the contain-security-incident skill, as a running record. Label claims: verified (say how), hypothesis (say what would confirm it), not verified (say why). For each line, write when it happened, with its source and precision, and when it was recorded, from the clock, if different; who did it; and, for an action, its status (proposed, done, result). Nothing is deleted. -->

Started: <date and time, with time zone>
Status: <containing / contained / recovering / closed>
Responder: <person>
Security owner: <person, paged at time>

## Reframe

## Evidence preserved

| What | Where it's kept | Time |
|---|---|---|
| <audit logs for period> | | |
| <configuration before changes> | | |

## Timeline

| Happened (source) | Recorded | Fact or action, and who | Status | Label |
|---|---|---|---|---|
| <hh:mm, from log / record / person's report, or unknown> | <hh:mm, from the clock> | <what was seen or done, by whom> | <for an action: proposed / done / result> | <verified: how / hypothesis / not verified> |

## Containment

| Time | Action | How to undo it | Worked? |
|---|---|---|---|
| <hh:mm> | <revoke sessions / disable key / remove access / isolate workload> | <undo> | <signal that confirmed it> |

## Legitimate workloads

| Workload | Shares the identity? | Effect of containment | Plan |
|---|---|---|---|
| <name> | <yes / no> | <new credentials on its own / breaks> | <own identity, least access> |

## Persistence search

Searched from: <first suspicious action, with time>

| Kind | Found | Action |
|---|---|---|
| Identities and keys | | |
| Trust and access policies | | |
| Scheduled jobs, functions, instances | | |
| Network changes | | |

## Exposure

- Secrets to rotate:
- Could user or customer data have been read?
- Legal and customer communication:

## Restore conditions

| Condition | Status |
|---|---|
| No attacker activity since containment | |
| Persistence removed | |
| Entry point found and fixed | |
| Secrets rotated | |
| Workloads on trusted identities | |
| Security owner's approval | |

## Not verified

- <item>

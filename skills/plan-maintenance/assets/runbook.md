# Runbook: <maintenance>

<!-- Filled by the plan-maintenance skill. Label claims: verified (say how), hypothesis (say what would confirm it), not verified (say why). -->

Written on: <date>
Written by: <person or agent>
Runs on: <date and window>
Run by: <person>

## The maintenance

- Taken away: <nodes, hosts, devices>
- At a time: <how many>
- For how long: <duration>

## Reframe

## Workloads affected

| Workload | Replicas and spread | Disruption limit | Shutdown fits? | Spare capacity | Finding | Label |
|---|---|---|---|---|---|---|
| <name> | | | | | | |

## Stateful systems

| System | Procedure | Steps |
|---|---|---|
| <database, queue> | <link> | |

## Order

| Batch | What | Before continuing | Wait |
|---|---|---|---|
| 1 | <smallest batch> | <what must be true> | <time> |

## Stop conditions

| Signal | Then |
|---|---|
| <signal> | <how to give capacity back> |

## Confirm it's done

- [ ] Every workload at its replicas
- [ ] Errors at normal levels
- [ ] Moved workloads healthy

## Not verified

- <item>

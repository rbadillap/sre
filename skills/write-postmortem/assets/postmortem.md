# Postmortem: <short description>

<!-- Filled by the write-postmortem skill. Blameless: describe systems and decisions, not people. Label claims: verified (say how), hypothesis (say what would confirm it), not verified (say why). -->

Date of the incident: <date>
Written on: <date>
Authors: <people or agent>
Incident record: <link to reliability/incidents/...>

## Summary

<!-- Three sentences: what happened, the impact, what changes. -->

## Reframe

<!-- Not what broke, but what let it break and stay unnoticed. -->

## Impact

| | Value | Label |
|---|---|---|
| Who was affected | <regions, tenants, users, devices> | <label> |
| What they couldn't do | <action> | <label> |
| Duration | <from - to> | <label> |

## Timeline

| Time | Event | Label |
|---|---|---|
| <hh:mm> | Started | <label> |
| <hh:mm> | Detected, by <alert / customer / person> | <label> |
| <hh:mm> | Response started | <label> |
| <hh:mm> | Mitigated | <label> |
| <hh:mm> | Resolved | <label> |

## Earlier incidents with the same cause

<!-- Link each one, and say why its actions didn't prevent this one: never done, done as a reminder instead of a default, or done in the wrong place. Or "none found". -->

| Earlier incident | Its action | Why it didn't prevent this one | Label |
|---|---|---|---|
| <link> | <action> | <never done / a reminder / the wrong place> | <label> |

## Contributing factors

<!-- Several, usually. For each: what happened, what made it possible, and its label. -->

1. <factor>: <what made it possible> (<label>)

## Why it wasn't detected sooner

<!-- Always filled. Name the missing signal, if any, with its label. A signal that existed and people were used to, such as a page that gets dismissed, is a finding too. -->

## Checks that existed but weren't used

<!-- A review, a runbook or a skill that would have caught it. Which, and why it wasn't run. Or "none". -->

## What went well

## Follow-up actions

<!-- Each one is a default, a check, a template field or an alert. Reminders are a last resort. -->

| Action | Where it lives | Owner | Due |
|---|---|---|---|
| <action> | <default / pipeline check / template / alert / document> | <one person> | <date> |

## Lessons for the playbook

<!-- Runbooks, templates or rules that were wrong, missing or not used. -->

| Lesson | Status (proposed, or adopted in where, when) |
|---|---|
| <lesson> | <status> |

## Not verified

<!-- What you couldn't check, and why. -->

- <item>

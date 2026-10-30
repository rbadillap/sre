---
title: Reframe first
stage: respond
order: 1
status: draft
teaches: The real problem before the obvious one.
sources: Cloudflare, 2019-07-02 (https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)
skill: reframe-first
version: 0.1.1
---

# Reframe first

_Source: [Cloudflare's report on the outage of July 2, 2019](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)._

## The question

When something breaks, the first explanation that fits is rarely checked. The question is: what is actually being asked, before you act on the obvious answer?

## What happened at Cloudflare

- At 13:42 UTC, a new rule for the web application firewall (WAF) was deployed to every server at once. The rule was meant to run in a mode that blocks nothing, but it still ran.
- CPU on the servers that handle web traffic went to nearly 100% across the network, and visitors to Cloudflare domains got 502 errors.
- Early on, people speculated it was a new kind of attack.
- At 14:00, the team identified the WAF as the cause, and ruled out an attack.

## Why the first explanation was wrong

An attack fits the symptoms: CPU everywhere, errors everywhere, at once. But an attack and a bad change call for opposite actions. An attack calls for more defense. A bad change calls for removing the change. Acting on the wrong frame makes the response slower, or worse.

Reframing means writing the problem down in one line before acting, and asking what else fits the same symptoms. Here, "everything got slow at the same moment, everywhere" also fits "something was deployed everywhere at the same moment". Asking what changed is part of the reframe.

_If you use rbadillap/sre: `reframe-first` is the discipline every skill applies first._

## In one sentence

"Before acting on the obvious explanation, write the problem in one line and ask what else fits the same symptoms, starting with what changed."

## Exercise

Your service's error rate jumps in every region at the same minute. Write two explanations that fit, and the first check that would tell them apart.

---

_Written with an AI assistant from the source above._

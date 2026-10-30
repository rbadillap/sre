---
title: "Reframe first"
stage: respond
order: 1
status: approved
teaches: "Write what you know without a cause, list what else fits, and choose the check that tells the explanations apart."
sources:
  - title: "Cloudflare, Details of the Cloudflare outage on July 2, 2019"
    url: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
  - title: "Google SRE book, Effective Troubleshooting"
    url: https://sre.google/sre-book/effective-troubleshooting/
skills: [reframe-first]
version: "0.1.1"
---

# Reframe first

_Sources: [Cloudflare's report on the outage of July 2, 2019](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/), and [Google's SRE book, "Effective Troubleshooting"](https://sre.google/sre-book/effective-troubleshooting/)._

## The question

The first explanation that fits the symptoms can still be wrong. Before you act on it: what do you actually know, and what else fits?

## What happened at Cloudflare

All times are UTC.

- **13:42:** an engineer deployed a minor change to the rules of the web application firewall (WAF). It was meant to run in "simulate" mode, where nothing is blocked. Even in that mode the rule still executes, and this one had a regular expression that consumed excessive CPU.
- **13:45:** the first page, an alert to the on-call team, went out for a test of the WAF. Then came many other failing tests, a global traffic drop alert, widespread 502 errors (the error page visitors saw), and reports of CPU exhaustion from cities worldwide.
- **In the first moments:** there was speculation that it was a new kind of attack.
- **14:00:** the WAF was identified as the cause, and an attack was dismissed. The evidence given for the WAF was live CPU data from a machine, `strace` (a tool that shows what a process is doing), and error logs. The report doesn't say what ruled out an attack.
- **14:07:** the WAF was turned off worldwide. By 14:09, traffic and CPU were back to expected levels.

## Reading the case

The report doesn't say whether the attack theory cost time.

What follows is this lesson's reading. "CPU exhausted worldwide and traffic dropping" fits both a new attack and a bad change, but the two lead to different actions. Turning off a firewall fixes one of them, and removes one layer of protection during the other. That's why the explanation has to be checked before acting on it.

## How to do it

Google's book describes troubleshooting as forming possible causes and testing them. Three of its points apply here:

- **Don't latch on to the past.** It warns against reasoning that a cause happened once, so it must be happening again.
- **Look at what changed.** Recent changes to a system can be a productive place to start.
- **Choose a check that separates explanations.** An ideal test rules one group of explanations in and another out, though the book notes this may be difficult in practice.

Put as three steps, in this lesson's words:

1. Write what you know in one line, without a cause.
2. List what else fits, starting with what changed.
3. Choose the check that tells them apart.

For this case, an example written for this lesson: the line is "CPU is exhausted worldwide and traffic is dropping", not "we're under attack". A first check is which process is using the CPU. That finds the component, not the cause, so the next check is what changed in that component.

Also this lesson's reading: the question doesn't end at recovery. After traffic recovered, Cloudflare ran tests in a single city, asking "was it really that particular change that caused the problem?", before turning the WAF back on at 14:52.

_If you use rbadillap/sre: `reframe-first` covers the first step: write the problem as it arrived, ask what that sentence assumes, and write it again from what users live and what is known._

## In one sentence

"Before I act, I write what I know without a cause, ask what else fits, starting with what changed, and pick the check that tells them apart."

## Exercise

A hypothetical case: at 10:00, your service's error rate jumps in every region within the same minute. A configuration change went out to all regions at 09:58.

1. Write what you know in one line, without a cause.
2. Write two explanations that fit.
3. Name one check that tells them apart, and the result that would support each.
4. Think of the last incident on your team, or one you've read about. What was the first explanation, and what check settled it, if any?

---

_Written with an AI assistant from the sources above._

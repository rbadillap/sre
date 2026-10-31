---
title: "Rolling out in steps"
stage: ship
order: 2
status: approved
teaches: "Plan a rollout in steps: how small to start, what gate sits between steps, how long to watch at each one, and what number stops it."
sources:
  - title: "Cloudflare, Details of the Cloudflare outage on July 2, 2019"
    url: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
  - title: "Google SRE workbook, Canarying Releases"
    url: https://sre.google/workbook/canarying-releases/
skills: [review-release]
version: "0.1.1"
---

# Rolling out in steps

_Sources: [Cloudflare's post on its outage of July 2, 2019](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/) and [Google's SRE workbook, "Canarying Releases"](https://sre.google/workbook/canarying-releases/)._

## The question

Tests can't catch everything, so some bad changes will reach production. How do you make sure a bad change stops while it's still small: where do you start, what decides the next step, how long do you watch, and what stops it?

## What happened at Cloudflare

Cloudflare had two ways to ship.

- **Software:** four stages. First DOG, a location used only by employees. Then PIG, with "a small subset of customer traffic from non-paying customers". Then three Canary locations with paying and non-paying traffic. Then the world. The process "can take hours or days".
- **Web application firewall (WAF) rules:** tests, then global. The written procedure "specifically allows it to be pushed globally". The post says this was by design "because of the need to respond rapidly to threats". Rules go out through a system called Quicksilver, which "can push changes globally in seconds".

All times are UTC, on July 2, 2019:

- **13:31:** an engineer merged an approved change: a rule to detect cross-site scripting attacks. It was meant to run in "simulate" mode, where "real customer traffic passes through the rule but nothing is blocked". But "even in the simulate mode the rules actually need to execute".
- **13:37:** the tests passed. They checked what the rule should block and let through. "What it didn't do was test for runaway CPU utilization".
- **13:42:** the deployment started automatically. The rule's regular expression, a text-matching pattern, used up the CPU that serves HTTP and HTTPS traffic worldwide. Visitors to Cloudflare sites got 502 errors.
- **13:45:** the first page, from an outside test of the WAF.
- **14:00:** the team identified the WAF as the cause.
- **14:02:** someone proposed the "global terminate", a mechanism that disables one component worldwide. Cloudflare's own login service was down, so the team had to use a bypass that "wasn't frequently used".
- **14:07:** the WAF was turned off worldwide. By 14:09, traffic and CPU were back to expected levels. The post calls this 27 minutes down.

The post says: "Everything that occurred up to the point the rules were deployed was done “correctly”". It lists eleven weaknesses, including: "The SOP allowed a non-emergency rule change to go globally into production without a staged rollout." The SOP is the written procedure.

One planned change was staged rollouts for rules, "while retaining the ability to do emergency global deployment for active attacks". The post lists that without marking it done, and gives no later result.

**What the post doesn't say.** It says each stage moves on if the last was "successful". It names only "a final check for errors" at Canary, with no number or duration per stage. It doesn't say how far a staged rollout would have limited this outage. It says DOG catches problems, "And it frequently does", with no example. So this lesson's sources don't show a real gate stopping a real rollout.

## What the workbook says

Google's chapter defines canarying as "a partial and time-limited deployment of a change in a service and its evaluation". Its examples use a test application, not an incident.

- **Why start small.** A new version that fails 20% of requests, sent to 5% of traffic, gives a 1% overall error rate. The chapter calls this "a very simple model" that assumes uniform load, and assumes detection and rollback take about the same time either way. It also assumes a 100% failure rate as the worst case, though its example uses 20%.
- **The gate.** Compare the canary with the rest, called the control. If the canary's error rate is too far from the control's, pause and roll back, or call a person. If they're similar, go on.
- **Absolute numbers too.** Both groups can change together, so "It is important to also use absolute measures, such as defined SLOs". [What working means](../01-define/01-what-working-means.md) explains SLOs, SLIs and error budgets.
- **Which signals.** Start from your SLIs, the measures behind your targets. In a small first stage, prefer the clearest ones, such as crashes and failed requests.
- **How long.** It should "last long enough to be representative". Performance defects "typically manifest only under heavy load", so an off-peak canary may miss them. Metric intervals should be "either the same as or less than your canary duration". An hourly metric on a 30-minute canary gives a muddied signal.

## Reading the case

The rest of this lesson is its own reading and method.

- **A passing test says nothing about what it doesn't measure.** The job of a step is real traffic, with a signal for what the tests can't see.
- **A no-effect mode can still run.** Simulate mode blocked nothing, and the rule still ran. Before you count a change shipped in a no-effect mode as safe, check what it still executes.
- **A gate only protects what's still ahead of it.** The change could spread in seconds, and the first page came three minutes after the deployment started. That was too late to hold back the rest. Each step has to last longer than it takes to notice.
- **Stopping has to work during the failure.** Five minutes passed between proposing the global terminate and running it, with the login service down.

## How to do it

1. **Set the smallest step.** Name who's in it and how many. Work out what it risks: traffic exposed, times failure rate.
2. **Name the gate.** Write what it checks, and whether a person or a script moves to the next step.
3. **Set the observation time.** List the effects you're waiting for and how long each takes to appear. Watch for longer than the slowest one, and for at least one full metric interval. Include peak load.
4. **Write the abort criteria before you start.** Give a number compared with the control, and an absolute number. Name who acts on them.
5. **Check the way to stop.** How long does it take, has anyone run it recently, and does it depend on what you're shipping?
6. **Write the emergency path.** Write when it may be used, who decides, what's watched after, and how to recover. Everything else takes the steps.

## Worked example

An example written for this lesson, with invented numbers, for a non-emergency firewall rule in the shape of Cloudflare's stages.

- **Step 1, employees' traffic, 30 minutes.** Gate: a script. Abort on any crash, on failed requests above the control, or if CPU time serving requests is over 20% above the control or over 70% of capacity.
- **Step 2, 1% of non-paying traffic, 1 hour.** Gate: a script. Abort if the error rate is over 0.5 points above the control, if the service falls below its SLO, or on step 1's CPU limits.
- **Step 3, three locations with all traffic, through one daily peak.** Gate: a person, who checks step 2's numbers and reads the rule's false positives.
- **Step 4, everywhere.**
- **Way to stop:** turn the rule off from a tool that doesn't need the service's own login. Tested last week.
- **Emergency path:** an active attack that the on-call security lead confirms. It goes global at once. People watch CPU and errors for one hour, with the same way to stop.

CPU is here because of this case, though the workbook warns that CPU usage can make a canary "flaky or noisy".

_If you use rbadillap/sre: `review-release` asks for the smallest step, the gate and who moves it, an observation time longer than the effects you're waiting for, abort criteria written in advance, and the conditions of any emergency path. It uses absolute thresholds when there's no traffic to compare, while the workbook also wants them alongside the comparison._

## In one sentence

"I release to a small group first, watch for longer than the slowest effect I'm waiting for, go on only if a written check passes, and I write what stops it before I start."

## Exercise

A hypothetical service gets 100,000 requests per hour, evenly. Its SLO is 99.9% over four weeks, with 67,200,000 valid requests expected. A new version fails 20% of its requests. Detecting that and rolling back takes 30 minutes in every case. Count only the failures this version adds.

1. What's the error budget, in failed requests?
2. How many requests fail if the version goes to all traffic? And to a 5% canary? What share of the budget is each?
3. During the canary, what overall error rate does a service-wide graph show? Why isn't that graph enough?
4. Separately, for a different version: the team proposes a 30-minute canary. This version writes cache entries that are first read back 2 hours later, and problems may appear only then. The error metric is computed hourly. What's wrong with the plan? How long would you run the canary, and why?
5. The control's error rate is usually 0.02%. Write abort criteria with one number compared with the control and one absolute number, and name who acts on them.
6. Take a change you shipped recently, or one from a service you use. Which step would it have started at? Write what you'd watch, for how long, and what would stop it.

---

_Written with an AI assistant from the sources above._

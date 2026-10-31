---
title: "Toil"
stage: learn
order: 3
status: approved
teaches: "Decide whether a task is toil, work out how much of a team's time it takes, and rank fixes by the time and risk they remove against what they cost."
sources:
  - title: "Google SRE book, Eliminating Toil"
    url: https://sre.google/sre-book/eliminating-toil/
  - title: "Google SRE book, Being On-Call"
    url: https://sre.google/sre-book/being-on-call/
  - title: "Google SRE workbook, Eliminating Toil"
    url: https://sre.google/workbook/eliminating-toil/
  - title: "Cloudflare, Cloudflare outage on February 20, 2026"
    url: https://blog.cloudflare.com/cloudflare-outage-february-20-2026/
skills: [paved-road]
version: "0.1.1"
---

# Toil

_Sources: [Google's SRE book, "Eliminating Toil"](https://sre.google/sre-book/eliminating-toil/) and ["Being On-Call"](https://sre.google/sre-book/being-on-call/), [Google's SRE workbook, "Eliminating Toil"](https://sre.google/workbook/eliminating-toil/), and [Cloudflare's report on its outage of February 20, 2026](https://blog.cloudflare.com/cloudflare-outage-february-20-2026/)._

## The question

Every team has repetitive work. Which of it is toil, how much can a team carry, and which piece do you fix first?

## A real case: repairing network cards at Google (workbook)

- **The work:** each repair of a failed line card (a network card in a switch) needed an engineer to check it was safe to move traffic, move it away, reboot or repair, and move it back. The chapter calls this "a textbook example of toil".
- **What it cost:** "We couldn't grow the team fast enough to keep up with the volume of failures". Repeating the steps "introduced too many human errors".
- **What changed:** software began requesting the traffic move and opening a case for a technician, instead of alerting an engineer. It assessed risk automatically. The first failure only rebooted the card and reinstalled the software, and the second led to replacing it.
- **One episode, undated:** a technician started concurrent traffic moves on every line card waiting for repairs at a datacenter, "resulting in network congestion and user-visible packet loss". The chapter says the software didn't anticipate this because it wasn't tested with new technicians.

The case says the system "freed the engineering team from a large volume of toilsome work". It gives no count of hours saved.

## A second case: Cloudflare

Cloudflare's report doesn't use the word "toil". It describes a manual task, and what happened when Cloudflare tried to automate it.

- **The task:** removing customers' own IP address ranges from its Bring Your Own IP service, "a regular customer request that is done manually today", as of the report. The report gives no count of requests or hours.
- **Why Cloudflare automated it:** it calls these manual processes "risky because of their close proximity to Production".
- **What happened:** the new cleanup task queried an API with a bug. On February 20, 2026, about 1,100 address ranges were withdrawn from the Internet, 25% of the service's ranges.
- **Why testing missed it:** testing covered the customer's path, and "did not cover a scenario where the task-runner service would independently execute changes to user data without explicit input."

## What the books say

**What toil is.** The book: "the kind of work tied to running a production service that tends to be manual, repetitive, automatable, tactical, devoid of enduring value, and that scales linearly as a service grows." It adds that not every task has all of these.

**What isn't toil, by the same chapter:** overhead, such as team meetings and HR paperwork; work done for the first or second time; work that makes a permanent improvement, even if it's unpleasant ("it probably wasn't toil"); and work where human judgment is essential ("there's a good chance it's not toil").

**Measure hands-on time.** Running a script counts by "the hands-on time a human spends running that script (not the elapsed time)".

**How much to carry.** These are Google's own figures.

- **The cap:** the book says toil below 50% of each SRE's time. The workbook applies 50% to SRE teams' operational work, "including both toil- and non-toil-intensive work", and says the target "may not be appropriate for your organization".
- **On-call:** "no more than 25% can be spent on-call".
- **The floor:** with one week primary and one week secondary on-call per cycle, a 6-person rotation gives 2/6 = 33% as the lower bound on toil.

The two chapters don't fully match. The on-call chapter's 25% limit means a minimum of eight for a single-site team, and it accepts six per site for dual-site teams. The toil chapter's 6-person rotation comes to 33%, above that 25%, and it doesn't say which kind of team it is.

**How to rank fixes.** The workbook:

- Google SRE teams "often track toil in bugs and rank toil according to the cost to fix it and the time saved by doing so".
- Confirm the time saved is at least proportional to the time spent "first developing and then maintaining" the automation.
- "The optimal strategy for handling toil is to eliminate it at the source."
- Consider rejecting the task first: analyze "the cost of responding to the toil versus not doing so."
- Track measurements "before, during, and after".

## Reading the cases

The rest of this lesson is its own reading and method.

- **Automation is a change, with its own risk.** Both cases show a problem connected to automating manual work. Neither shows that automating was the wrong choice.
- **Workload isn't the only reason to fix it.** Cloudflare's stated reason was risk, and Google's included human errors. A rank based only on hours could miss that.

## How to do it

1. List the repetitive work with the people who do it, and test each item against the definition. Set aside overhead and first-time work.
2. For each item, write how often, hands-on minutes per run, the period, and where the numbers came from. Label estimates.
3. Add it up as a share of the team's hours. Work out the on-call floor separately.
4. For each item, ask first: can you stop doing it, or remove the need for it? Automate only after that.
5. Rank by hours saved per week and risk removed, against the cost to build and keep it running. Payback in weeks = hours to build ÷ (hours a week the task takes now − hours a week to keep the fix running). This assumes the fix removes the whole task.
6. Treat the saving as a hypothesis until you've measured it after the change.
7. Test the automation running on its own, not only the path a person follows.

## Worked example

For the line-card case, using only what the chapter gives:

- **Toil?** Yes, its "textbook example".
- **How often, minutes per run, hours saved:** not stated.
- **Risk removed:** human errors, through automated risk assessment.
- **New risk:** concurrent traffic moves the software didn't prevent.

To show the arithmetic, an example written for this lesson. All numbers are invented.

- **Restart a stuck export:** 10 runs a week, 12 minutes each: 2 hours a week. A fix takes 40 hours to build and 0.5 hours a week to keep running. Net saving: 1.5 hours a week. Payback: about 27 weeks.
- **Renew customer certificates by hand:** 2 runs a week, 45 minutes each: 1.5 hours a week. A fix takes 20 hours to build and 0.25 hours a week to keep running. Net saving: 1.25 hours a week. Payback: 16 weeks. A wrong certificate caused an outage last year.
- **Rank:** certificates first. They pay back sooner and remove a known risk.

_If you use rbadillap/sre: `paved-road` says a toil fix can remove the task, simplify it or automate it, and ranks fixes by recurring load and risk against what they cost to build and keep running. It treats an expected reduction as a hypothesis until it's measured. It doesn't define toil's traits or set a limit like Google's 50%._

## In one sentence

"Toil is repetitive manual work with no lasting value, so I measure the hands-on time, try to remove the task first, and rank fixes by the time and risk they remove against what they cost."

## Exercise

A hypothetical team of 6 engineers, each working 40 hours a week. All 6 share the rotation: one week primary and one week secondary in each 6-week cycle. Weekly work outside on-call:

- **A.** Rebuild a stale search index: 6 times a week, 20 hands-on minutes each. The rebuild runs for 2 hours. A fix that stops it going stale costs 10 hours, with nothing to keep running.
- **B.** Clear full disks after alerts: 20 times a week, 15 minutes each. An automated cleanup costs 40 hours, plus 0.5 hours a week to keep running. Last quarter, a manual cleanup deleted the wrong file and caused a one-hour outage.
- **C.** Team meeting: 1 hour a week, for all 6.
- **D.** A one-time move of customer data to a new region: 30 hours, this week only.

1. Which of these are toil? Why not the others?
2. How many hours of toil a week is that, and what share of the team's 240 hours?
3. What's the on-call floor for this rotation? How does it compare with Google's 25% limit? Can you tell from these facts how many sites the team has, or how much of an on-call week is really toil?
4. Work out the payback in weeks for A and B. Which do you fix first? Give your reason, including risk.
5. What would you test in B's fix, other than the path a person follows?
6. Pick one repetitive task from your own work. Write how often, the hands-on minutes, and the source of those numbers.

---

_Written with an AI assistant from the sources above._

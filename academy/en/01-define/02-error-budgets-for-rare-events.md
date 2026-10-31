---
title: "Error budgets for rare events"
stage: define
order: 2
status: approved
teaches: "Work out an error budget in time or in events, read a budget under one failure, and choose what to do about it knowing the limits of each option."
sources:
  - title: "Google SRE workbook, SLO Engineering Case Studies (Evernote's and The Home Depot's sections)"
    url: https://sre.google/workbook/slo-engineering-case-studies/
  - title: "U.S. Securities and Exchange Commission, Order in the matter of Knight Capital Americas LLC, Release No. 70694"
    url: https://www.sec.gov/litigation/admin/2013/34-70694.pdf
  - title: "Google SRE book, Embracing Risk"
    url: https://sre.google/sre-book/embracing-risk/
  - title: "Google SRE workbook, Alerting on SLOs"
    url: https://sre.google/workbook/alerting-on-slos/
  - title: "Google SRE workbook, Implementing SLOs"
    url: https://sre.google/workbook/implementing-slos/
skills: [define-slos]
version: "0.1.1"
---

# Error budgets for rare events

_Sources: [Evernote's and The Home Depot's sections of "SLO Engineering Case Studies"](https://sre.google/workbook/slo-engineering-case-studies/), [the SEC's order on Knight Capital](https://www.sec.gov/litigation/admin/2013/34-70694.pdf), [Google's SRE book, "Embracing Risk"](https://sre.google/sre-book/embracing-risk/), and Google's SRE workbook, ["Alerting on SLOs"](https://sre.google/workbook/alerting-on-slos/) and ["Implementing SLOs"](https://sre.google/workbook/implementing-slos/)._

## The question

An error budget, explained in [What working means](01-what-working-means.md), is the failure an SLO allows. How do you count it when the thing you measure happens only a few times, like a release or a nightly job? And what does it mean when the budget is less than one failure?

## Two published ways to measure

**In time, at Evernote.** Its first SLO was "99.95% uptime measured over a monthly window". It says it chose uptime to keep its first pass simple.

**In events, for batch jobs at The Home Depot.** Its SLO framework is called VALET. The chapter says that "with a little adjusting, batch applications can fit into this framework", and its mapping includes:

- **Availability:** "How often (as a percentage) the job completed by a certain time".
- **Errors:** "The records that failed to process".

The chapter gives no job counts or targets, so it doesn't show a budget for a job.

## What the sources say about time and events

- **What 43 minutes means.** The "Alerting on SLOs" table for a 99.9% SLO over 30 days gives 43 minutes to use the whole budget at a 100% error rate, and 3 days at a 1% error rate. So 43 minutes is the budget only if the service is fully down.
- **Units of work.** The book says most nonserving systems, such as batch, pipeline and storage systems, "have a well-defined notion of successful and unsuccessful units of work". Its batch example counts records, not runs of the job.

## What the workbook says about low traffic

"Alerting on SLOs" uses a service with 10 requests per hour and a 99.9% SLO. That's 7,200 requests in 30 days, and 0.1% of that is 7.2 failures. One failed request "consumed 13.9% of the 30-day error budget", and the SLO "allows for only seven failed requests in 30 days".

It asks what the impact of a single failed request is. Its answers are about requests and alerting, not about releases:

- "A high-availability target may be appropriate if failed requests are one-off, high-value requests that aren't retried."
- "It may make sense from a business perspective to investigate every single failed request." It adds that an alerting system tells you about that error too late.
- **Other options:** combine related services, or change the product so one failure costs less, for example with retries or a path that saves the request to run later. It says these changes "allow for more failed events in the error budget". In a combined group, one service failing completely may not count as significant.
- **Lower the SLO, or use a longer alerting window.** Lowering the SLO "involves a product decision", because it changes what people expect and when the error budget policy applies. The window here is the one "used for the alerting logic", not the SLO's window.

"Implementing SLOs" adds: "Our experience has shown that 100% reliability is the wrong target". It also says "Shorter time windows allow you to make decisions more quickly", and longer ones are better for strategic decisions.

On policies, the book describes one approach: releases continue while SLOs are met, and are "temporarily halted" if the budget runs out. It's one approach, not a standard.

## What happened at Knight Capital

The SEC's order concerns a market-access rule and doesn't mention SLOs or error budgets. Knight accepted it without admitting or denying its findings. This lesson uses only its account of one deployment.

- **The deployment.** From July 27, 2012, Knight deployed new code in stages to its order router. A technician "did not copy the new code to one of the eight SMARS computer servers". No second technician reviewed the deployment, and no written procedure required it.
- **August 1, 2012.** On the eighth server, orders triggered old, defective code. For 212 incoming orders, the router sent millions of orders to the market in about 45 minutes. Knight "lost over $460 million". Removing the new code from the seven good servers made the problem worse.
- **Not only the deployment.** The order says "a simple double-check of the deployment" could have "averted the events of August 1". It also finds that Knight lacked adequate controls and procedures, and that these shortcomings "were made more consequential" by the lack of sufficient controls in its order router.

It doesn't say how many deployments Knight made in a month, or give any target for them. None of this lesson's sources shows an error budget counted in releases, or one under one failure. The releases and numbers below are written for this lesson.

## Reading the cases

The rest of this lesson is its own reading and method.

- **A fraction of a failure can't happen.** A budget of 0.4 doesn't let you fail 0.4 of a release. Under one, the first failure misses the target.
- **That result may be correct.** The workbook says a high target "may be appropriate" for one-off, high-value requests. It doesn't say no failure is acceptable; that step, and applying it to releases, is this lesson's. In that window the only passing result is 100%, which the workbook calls "the wrong target", so keeping it needs a stated reason.
- **Knight shows why the cost of one event matters, and nothing more.** With no deployment count there's no budget to work out, and the order doesn't show that a budget would have changed anything.

## The ways out, and their limits

Options 1, 3 and 5 adapt the workbook's low-traffic options, which speak about requests and alerting. The stages in option 3, and options 2, 4 and 6, are this lesson's own.

1. **Lower the target.** Do it only if the new target still covers what users need. It's a product decision, not a math fix.
2. **Lengthen the SLO's window.** You count more events, so the budget grows. The rate of failure doesn't change, and you find out later.
3. **Reduce what one failure costs.** A release could be rolled out in stages or undone quickly. Knight deployed in stages, and removing the new code made things worse, so a stage or rollback helps only if it's checked. The workbook says its product changes "allow for more failed events in the error budget". In a release count, that happens only if you change what counts as a failure, and that change has to be honest about what users see.
4. **Respond to every failure.** A ticket, a page or a review for each failure is a decision about detection. It can run alongside the SLO.
5. **Group related events.** Counting many similar jobs gives a larger number, but one job that always fails can stop being visible.
6. **Keep the target.** Say plainly that one failure misses it, and agree what happens then.

## How to do it

1. Write what counts as a success, and which events are valid.
2. Choose the unit. For a service measured all the time, a budget can be read in time. For separate events, count them.
3. Work out the budget: the allowed failure rate multiplied by the valid events in the window. In time, 99.9% over 30 days allows 0.1% of 43,200 minutes, about 43 minutes fully down.
4. If the budget is under one, ask what one failure costs users. Then choose a way out above.
5. Write the policy, knowing that with a budget under one, it applies after every failure.

## Worked example

An example written for this lesson, with invented numbers: a team has 40 valid releases in 30 days, and a target of 99% successful releases.

- **Budget:** 1% of 40 is 0.4 failures.
- **One failure:** 39 of 40 is 97.5%, so the target is missed.
- **Lower the target to 95%:** 5% of 40 is 2 failures. Does 95% still cover what users need?
- **Use 90 days at the same pace:** 120 releases, and 1% is 1.2 failures. If failures keep their pace, that's 3 of 120: 97.5%, the same miss, reported later.

_If you use rbadillap/sre: `define-slos` does this count with `error-budget.py --events-per-window` and warns when the budget is under one event. The warning says: "Lower the target, lengthen the window, or alert on every failure instead of a budget." This lesson runs alerting alongside the budget instead._

## In one sentence

"For rare events like releases, I read the budget in events, not minutes. If it's under one, the first failure misses the target, and I have to decide if that's what we want."

## Exercise

A hypothetical case: in a 30-day window, a team had 43 valid releases. Its target is 98% successful releases. One release failed.

1. What's the budget in failed releases?
2. What's the success rate with one failure? Is the target met?
3. Someone proposes 95%. What's the budget now, and is the target met with two failures?
4. Someone else proposes keeping 98% over 90 days, at the same pace. How many releases is that, and what's the budget? What doesn't this change?
5. Name two things you'd need to know, which this case doesn't tell you, to decide if 98% is the right target.
6. Find something in your own work that happens only a few times in a window: a release, a backup, a report. Write what counts as a success, how many happen per window, and the budget at a target you choose. If it's under one, would you keep the target? Why?

---

_Written with an AI assistant from the sources above._

---
title: "Mitigate what can be undone"
stage: respond
order: 3
status: approved
teaches: "Choose the action that stops the harm, write how to undo it and what it costs, check what it does around it, and confirm it worked."
sources:
  - title: "Cloudflare, Details of the Cloudflare outage on July 2, 2019"
    url: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
  - title: "Google SRE book, Addressing Cascading Failures"
    url: https://sre.google/sre-book/addressing-cascading-failures/
  - title: "Meta Engineering, More details about the October 4 outage"
    url: https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/
skills: [reversible-first]
version: "0.1.1"
---

# Mitigate what can be undone

_Sources: [Cloudflare's report on the outage of July 2, 2019](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/), [Google's SRE book, "Addressing Cascading Failures"](https://sre.google/sre-book/addressing-cascading-failures/), and [Meta's "More details about the October 4 outage"](https://engineering.fb.com/2021/10/05/networking-traffic/outage-details/)._

## The question

Users are being hurt and you don't have the full cause yet. Which action stops the harm, and how do you get back if it's wrong?

## What happened at Cloudflare

All times are UTC, on July 2, 2019. A rule change to the web application firewall (WAF) was exhausting CPU worldwide. Visitors got widespread 502 errors (an error page), and an alert fired for a global traffic drop.

- **14:00:** the WAF was identified as the component causing the problem.
- **14:02:** the team proposed a "global terminate", a mechanism built into Cloudflare to disable a single component worldwide.
- **14:02 to 14:07:** getting to it was hard. Cloudflare uses its own products, and with its Access service down, the team couldn't log in to its internal control panel. It also couldn't reach other internal services, such as Jira and the build system, without a bypass that wasn't used often. Once back in, the team discovered that some members had lost access, because a security feature disables credentials that aren't used frequently.
- **14:07:** the WAF was terminated globally. By 14:09, traffic and CPU were back to expected levels. The report says the rest of Cloudflare's protection mechanisms kept operating.
- **Before turning it back on:** the team tested in a single city, with a subset of traffic and without its paying customers' traffic. The tests asked whether that change really caused the problem, and whether the rollback worked.
- **14:52:** with the cause understood and a fix in place, the WAF was turned back on globally.

There was also a rollback plan. In its list of what went wrong, the report says it "required running the complete WAF build twice taking too long." The report doesn't say the team compared it with the terminate during the incident.

## Reading the case

The report doesn't call this action reversible, and it doesn't say what the time without the WAF cost. What follows is this lesson's reading:

- **It stopped the harm, and it could be undone.** The WAF was off for 45 minutes and came back. It came back after the fix: turning it on sooner would have brought the same rule back.
- **It had a cost.** One layer of protection was off during those 45 minutes, so the choice wasn't free.
- **A plan on paper can be too slow.** The rollback needed two full builds.
- **The action has to be reachable when your own tools are down.** Access problems stood between the team and the terminate.
- **Coming back is a change too.** The return was tested small first. The report's stated tests were about the cause and the rollback, so treating it as a lesson about the return is this lesson's reading.

## What it does around it

This lesson's reading: an action can fail to help, or can hurt somewhere else. Three published warnings, the first two about a cascading failure, which Google's book describes as a failure that grows over time through positive feedback:

- **Restarting can hurt.** The book says to identify the source of a cascading failure before restarting, to make sure the restart "won't simply shift around load" (only move the load to other servers), and to make the change slowly. It warns: "Your actions may amplify an existing cascading failure if the outage is actually due to an issue like a cold cache", meaning an empty cache.
- **Adding capacity may not help.** The same chapter says adding tasks can be the quickest way to recover when the system is at degraded capacity and you have idle resources, but that in a "death spiral", a cycle that feeds itself, it may not be enough.
- **Coming back can hurt.** After Facebook's 2021 outage, Meta wrote that turning its services back on all at once could cause "a new round of crashes due to a surge in traffic", and that it carefully managed the increasing loads.

## How to do it

The steps below are this lesson's own method:

1. List the actions that could stop the harm, and prefer one you can undo.
2. Write how to undo it before you do it. If you can't write that, treat it as not reversible.
3. Write what it costs while it's on, and what it does to everything around it.
4. Leave what can't be undone, such as deleting data or restoring over it, for a person to decide, with the target checked.
5. After you act, check that the signal users experience recovered. If it didn't, undo it and reconsider the cause.

For this case, an example written for this lesson: "Terminate the WAF globally. Undo: once the cause is fixed, turn it back on, testing in one city first. Cost: one layer of protection off until then. Around it: the rest of the protection stays on. Confirm: traffic returns to expected levels, with CPU as a supporting signal."

_If you use rbadillap/sre: `reversible-first` applies the same discipline, without a step for cost, and adds when not to use it: when the mitigation would destroy what's needed later, such as evidence in a security incident, preserve that first._

## In one sentence

"I start with an action I can undo, I write the way back and the cost before I do it, and I check what it does around it and whether users recovered."

## Exercise

A hypothetical case: your database allows 500 connections and has 480 in use. Eight application instances hold 50 connections each, and a report job holds the other 80. The application is timing out; assume that's because it's waiting for database connections. The report can run later, and pausing it releases its 80 connections. You have two options: add 4 application instances, each needing 50 connections, or pause the report job.

1. How many connections would each option need, compared with the limit?
2. Which one do you try first, and why?
3. Write that option in the format of the example above: the action, how to undo it, what it costs, what it does around it, and how to confirm it worked.
4. Think of a mitigation on your team, or in a report you've read. How would it have been undone, and what did it cost while it was on?

---

_Written with an AI assistant from the sources above._

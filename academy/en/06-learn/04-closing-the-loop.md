---
title: "Closing the loop"
stage: learn
order: 4
status: approved
teaches: "Take a lesson from an incident back to the stages it changes, track whether each change has shipped, and check a repeat incident against the earlier actions."
sources:
  - title: "Google SRE book, Part III: Practices"
    url: https://sre.google/sre-book/part-III-practices/
  - title: "Google SRE workbook, Implementing SLOs"
    url: https://sre.google/workbook/implementing-slos/
  - title: "Cloudflare, Cloudflare outage on November 18, 2025"
    url: https://blog.cloudflare.com/18-november-2025-outage/
  - title: "Cloudflare, Cloudflare outage on December 5, 2025"
    url: https://blog.cloudflare.com/5-december-2025-outage/
  - title: "Cloudflare, Code Orange: Fail Small"
    url: https://blog.cloudflare.com/fail-small-resilience-plan/
  - title: "Cloudflare, Cloudflare outage on February 20, 2026"
    url: https://blog.cloudflare.com/cloudflare-outage-february-20-2026/
  - title: "Cloudflare, Code Orange: Fail Small is complete"
    url: https://blog.cloudflare.com/code-orange-fail-small-complete/
skills: [learn-from-incident]
version: "0.1.1"
---

# Closing the loop

_Sources: Cloudflare's posts of [November 18, 2025](https://blog.cloudflare.com/18-november-2025-outage/), [December 5, 2025](https://blog.cloudflare.com/5-december-2025-outage/), [December 19, 2025](https://blog.cloudflare.com/fail-small-resilience-plan/), [February 21, 2026](https://blog.cloudflare.com/cloudflare-outage-february-20-2026/) and [May 1, 2026](https://blog.cloudflare.com/code-orange-fail-small-complete/); [Google's SRE book, Part III](https://sre.google/sre-book/part-III-practices/); and [Google's SRE workbook, "Implementing SLOs"](https://sre.google/workbook/implementing-slos/)._

## The question

The postmortem is written and the actions are listed. What has to happen before the next incident, so the lesson changes what the team defines and designs, and not only what it wrote down?

## What happened at Cloudflare

Times are UTC.

- **November 18, 2025:** a database permissions change led to a doubled "feature file", which spread to the network and made its software fail. Main impact ended at 14:30, and all services at 17:06. The post lists follow-ups as starting, including "Reviewing failure modes for error conditions across all core proxy modules".
- **December 5, 2025:** from 08:47 to 09:12, about 28% of its HTTP traffic was affected. A configuration change went through a system that "does not perform gradual rollouts", and that it said was under review after November 18. The post calls the November change "unrelated", and the incident "similar".
- **What it said about its earlier actions:** "We believe these changes would have helped prevent the impact of today's incident but, unfortunately, we have not finished deploying them yet." It names the unfinished work: rollouts, emergency ("break glass") access and fail-open handling. November's list had no rollout item.
- **December 19, 2025:** it published a plan. It said both outages followed a similar pattern. It releases software in controlled steps, but "We have not applied that methodology to configuration changes." It set goals for "the end of Q1".
- **February 20, 2026:** another outage, for a subset of customers of one service, withdrew about 1,100 address ranges. The change was itself part of the program. The post says "preventative measures weren't fully deployed before the outage". It calls the outage not global, and its impact "unacceptably large".
- **May 1, 2026:** it said the program was complete.

The posts don't fully agree. December 19 gives November's outage as "approximately two hours and ten minutes". November's own post says failures began "at 11:20 UTC", its timeline has impact from 11:28 to 14:30, and all services resolved at 17:06. December 5 says "nearly all of our customer base" about both outages, while reporting "approximately 28% of all HTTP traffic" for its own. December 19 gives that as "28% of applications behind our network". The May post says "In most cases" about internal configuration changes, and also that teams on network products adopted the method "for all configuration deployments". December 19's goal was "Ensure all production systems are covered". The May post also says the team finished "Earlier this month" and is dated May 1, so the finish date isn't clear.

What the May post reports having changed:

- **Configuration releases:** "In most cases", internal configuration changes now roll out progressively, with health monitoring.
- **Failure behavior:** services use the last known good configuration where possible, and then [fail open](../02-design/01-how-it-fails.md) (serve with reduced function) or closed (don't serve), by a reviewed choice.
- **Emergency access:** backup access paths for 18 key services, and a drill on April 7, 2026, with more than 200 people.
- **SLOs:** "we have introduced additional service level objectives (SLOs) to all our services". It gives no names or targets, and only a general reason: "The global outages have made us review core processes".
- **Rules:** a mandatory set of engineering rules, with "Incidents surface gaps that become new RFCs" (RFC: Request For Comments, the process behind the rules).
- **Its claim:** "we have now completed the work that would have avoided" the November and December outages. That's Cloudflare's judgment, and the post offers no outside test of it. The post doesn't mention February.

## What the books say

- **Part III** orders reliability work as a hierarchy "from most basic to most advanced". It doesn't describe a loop. On repeats: "it's woefully boring to 'fix' the same issue over and over."
- **The workbook** tells you to compare known outages and support tickets with your SLOs ([What working means](../01-define/01-what-working-means.md) explains the terms). If some "are not captured in any SLI or SLO", that's "a strong sign that your SLO lacks coverage", and "Your SLIs and SLOs should change over time". You can move a measurement closer to the user, improve coverage "so you capture a higher percentage of user interactions", or tighten the SLO "If your SLIs indicated a problem, but your SLOs didn't prompt anyone to notice or respond".

## Reading the case

The rest of this lesson is its own reading and method. Calling this a loop, and sorting changes into the stages of [The cycle](../00-the-cycle/01-the-cycle.md), is this lesson's reading. Cloudflare doesn't use those stages.

- **A written action changes nothing until it ships.** On December 5, the changes it had planned after November were still being deployed. Cloudflare's own belief is that they would have helped. The case doesn't prove it.
- **A similar incident is a question about the earlier actions.** Were they done, and were they in the right place? Cloudflare's December 5 post answers the first one in public.
- **The lesson moved into the stages.** Configuration rollouts belong to Ship, failure behavior to Design, emergency access to Respond.
- **Define is where the case says least.** The post says SLOs were added, and nothing more. It doesn't show an incident leading to a specific SLO change, and this lesson's sources don't show one.
- **The fix can be the next risk.** February's change was part of the program, and it caused an outage. That doesn't show the program was wrong.
- **No before-and-after.** No post gives a measure of reliability across the program, so this lesson doesn't claim it made Cloudflare more reliable.

## How to do it

This method is the lesson's own.

1. For each lesson, ask which stage it changes:
   - **Define:** did an SLI or SLO see this? If not, what changes?
   - **Design:** which assumption was wrong?
   - **Ship:** which kind of change skipped a safeguard?
   - **Observe:** which signal was missing?
   - **Respond:** what slowed the response?
2. Write the change where the next work starts: the SLO document, the design review, the pipeline. See [From lesson to default](02-from-lesson-to-default.md).
3. Give each change a state: proposed, in progress or shipped. Keep the list where people will see it.
4. Check it after it ships, with something you can observe.
5. Say what risk stays while it isn't shipped, and who accepted that.
6. When an incident comes, search earlier actions. If one covers it, say whether it was never done, not finished, or in the wrong place.
7. Check new changes against the same rules. A safety change is still a change.

## Worked example

An example written for this lesson, using only Cloudflare's published facts. The sorting, the "still open" notes and the call on February are this lesson's.

- **Lesson:** a configuration change can reach the whole network in seconds.
- **Stage:** Ship.
- **State on December 5:** not finished. **State on May 1:** reported as done "In most cases".
- **Still open from the post:** which cases are left aren't listed, and whether February's follow-ups shipped isn't stated.
- **Define:** left blank, for the reason in the reading above.
- **Related check on February 20:** the change wasn't instantaneous ("applied iteratively"), so it isn't a plain repeat. The post links it to the program, and says measures for that API weren't fully deployed.

_If you use rbadillap/sre: `learn-from-incident` turns a postmortem's lessons into proposals, each with the file, the current text and the proposed text, for a person to approve. It looks for repeated lessons, and sends changes to the system itself back to the postmortem's actions. It applies no proposal itself, and doesn't follow an action until it ships, so keep those states yourself._

## In one sentence

"A lesson isn't closed when it's written, so I put it in the stage it changes, track whether it has shipped, and when an incident repeats I ask what happened to the earlier action."

## Exercise

A hypothetical case. A checkout service has this SLO: 99.9% of valid requests return no 5xx status code, over 30 days, measured at the server. In the last 30 days:

- 1,000,000 valid requests, with 400 returning a 5xx.
- One day, a bad front-end release showed a blank page to customers on 12,000 of those requests, which all returned status code 200. Support received 300 tickets.
- Four months ago, a similar blank page led to the action "add a measurement from the customer's browser". Its state is still "in progress".

1. What does the SLO report? How much of the 1,000 error budget is spent?
2. Count the blank pages as failures too. What's the result? Is the target met?
3. Which stage does each of these lessons change: the SLO's measurement misses blank pages; releases reach all customers at once? Say why.
4. Write the SLI change as a proposal, using the workbook's options.
5. How do you record the old action in this postmortem? What don't you know yet?
6. Pick a past incident from your own work, or one you've read about. Find one action from it. Has it shipped, and how could you tell?

---

_Written with an AI assistant from the sources above._

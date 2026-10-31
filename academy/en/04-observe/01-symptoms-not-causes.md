---
title: "Symptoms, not causes"
stage: observe
order: 1
status: approved
teaches: "Sort an alert into page, ticket or dashboard by asking what users feel, whether someone must act now, and whether a cause is definite and imminent enough to page for."
sources:
  - title: "Zalando Engineering, Operation-Based SLOs"
    url: https://engineering.zalando.com/posts/2022/04/operation-based-slos.html
  - title: "Google SRE book, Monitoring Distributed Systems"
    url: https://sre.google/sre-book/monitoring-distributed-systems/
  - title: "Slack Engineering, A Terrible, Horrible, No-Good, Very Bad Day at Slack"
    url: https://slack.engineering/a-terrible-horrible-no-good-very-bad-day-at-slack/
skills: [design-alerts]
version: "0.1.1"
---

# Symptoms, not causes

_Sources: [Zalando's "Operation-Based SLOs"](https://engineering.zalando.com/posts/2022/04/operation-based-slos.html), [Google's SRE book, "Monitoring Distributed Systems"](https://sre.google/sre-book/monitoring-distributed-systems/), and [Slack's post on its May 12, 2020 outage](https://slack.engineering/a-terrible-horrible-no-good-very-bad-day-at-slack/)._

## The question

An alert can wake someone for a number that hurt nobody. Another can stay quiet while users can't do their work. What should wake someone up, and what can wait until morning?

A page interrupts a person now. A ticket waits in a queue. A dashboard waits until someone looks.

## What happened at Zalando

Zalando, an online fashion store, tells this in its own post from 2022. The numbers are its own.

- **Where it started.** Its SREs reviewed the paging alerts of other teams. The default was to alert on signals that could indicate a wider failure, such as "Load average is high" or "Cassandra node is down". Thresholds were hard to pick.
- **What it pushed for.** It calls this Symptom Based Alerting. A team measures a signal that represents a customer experience, such as "Place Order", at the edge services, the ones that talk to customers. The post says "anything that may negatively affect the customer experience will be noticed by the signal at the edge."
- **A problem of ownership.** The team that owned the edge service would receive the pages and do the first triage. Zalando built an alert handler that reads tracing data, a record of one request across services, and pages the team closest to the problem. Its first symptom alerts were also too sensitive, as told in [Burn rate](02-burn-rate.md).
- **A problem of adoption.** "Even teams that did adopt CBOs, weren't disabling their cause based alerts." CBOs, Critical Business Operations, are its list of operations that matter most to the business, such as "Place Order".
- **The trial.** For 3 months, inside its SRE department, it looked at alerts every week and worked out which cause alerts could be safely disabled. Its CBOs there were its own platform's, such as "Ingest Metrics" and "Query Traces". By the end, it reports a false positive rate "from 56% to 0%" and "from 2 to 0.14 alerts per day", "without missing any relevant user-facing incidents". It disabled over 30 alerts.
- **What it hasn't solved.** CBOs only set availability targets. It's holding off on latency alerts, because its handler struggles to trace where a latency increase comes from.

The post says it tested "the whole flow": CBOs, SLO targets and these alerts together, so it doesn't separate what came from symptoms alone.

## What the book says

The chapter says monitoring should answer two questions: "what's broken, and why?" The "what" is the symptom. The "why" is a cause, possibly an intermediate one.

- **Its questions for a rule.** Does it detect a condition that is "urgent, actionable, and actively or imminently user-visible"? Does it definitely mean users are affected? "Is that action urgent, or could it wait until morning?" Could it be safely automated?
- **Its view of a page.** "Every page should be actionable." "If a page merely merits a robotic response, it shouldn't be a page."
- **Causes aren't banned.** Its words: "it's better to spend much more effort on catching symptoms than causes; when it comes to causes, only worry about very definite, very imminent causes." Its example of a prediction: "It looks like your database will fill its hard drive in 4 hours."
- **Where causes go.** Its conclusion reserves cause-oriented heuristics "to serve as aids to debugging problems". It favors a dashboard over email alerts for problems below the level of a page.

The chapter calls this philosophy "a bit aspirational".

It also tells a story from Google's Bigtable team, without a date. Its [SLO](../01-define/01-what-working-means.md) was based on a test client's average performance, and the worst 5% of requests were often much slower than the rest. Alerts fired near and past that SLO, in large numbers. Many pages "had either rote responses or received no response". The team "often missed the problems that actually affected users". It worked on performance, temporarily moved its target to the 75th percentile of request latency, and disabled email alerts.

## What happened at Slack

On May 12, 2020, a program that updated the load balancers' list of servers began to fail and exit early. The list grew stale through the day. The user-visible outage began at 4:45pm Pacific. The team was alerted that it was "serving more HTTP 503 errors than normal".

Afterward, it asked why monitoring hadn't caught the problem: "We had alerting in place for this precise situation, but unfortunately, it wasn't working as intended." The post doesn't say what that alert measured, when it would have fired, or whether it would have avoided the outage.

## Reading the cases

The rest of this lesson is its own reading and method.

- **A symptom alert can catch what nobody listed.** That's Zalando's argument, with numbers from one department. It isn't proof for your team.
- **A symptom alert can come after the harm has started.** The book calls black-box monitoring, testing what users would see, "symptom-oriented", and says it's "fairly useless" for problems not yet happening. Slack's 503 alert reported errors already being served. This lesson reads that as a reason to keep a place for very definite, very imminent causes.
- **Bigtable shows noise doesn't come only from causes.** Its noisy alerts were tied to an SLO, not to CPU or disks. A signal can look like a symptom and still not follow what users feel.

## How to do it

1. Write what the alert says in one line. Is it "what's broken" or "why"?
2. Ask who feels it now. If users do, it's a candidate for a page.
3. If it's a cause, ask if it's definite and imminent. Write the time left, and what happens to users then. If you can't, it doesn't page.
4. Ask if someone has to act now, and if that action needs thought. A fixed response is a candidate for automation.
5. Route it: a page if it can't wait, a ticket if it can wait for working hours, a dashboard if it only helps with debugging.
6. Say who receives the page. A signal at the edge lands on the edge team unless you decide otherwise.
7. Look back at each page later. If nobody needed to act, change it or delete it.

## Worked example

An example written for this lesson, with invented details. The first two alert names are the ones Zalando quotes.

| Alert | Kind | Can it wait? | Route |
|---|---|---|---|
| "Load average is high", while "Place Order" meets its target | Cause, no user impact seen | Yes | Dashboard |
| "Cassandra node is down", with redundancy left and no user impact | Cause | Until working hours | Ticket |
| "Place Order" failures above target at the edge | Symptom | No | Page |
| Database disk fills in 4 hours at the current rate, and writes stop then | Cause, definite and imminent | No | Page, with the reason written |

_If you use rbadillap/sre: `design-alerts` writes a policy that pages on symptoms, budget burn and rare events, and sends causes to dashboards or tickets unless they predict user impact soon enough that someone must act. That exception is worded more broadly than the book's "very definite, very imminent". It changes no alerting configuration._

## In one sentence

"I page on what users feel now, or on a cause that's definite and imminent, and everything else goes to a ticket or a dashboard."

## Exercise

A hypothetical case: a shop's alerts over the last four weeks.

- **A:** CPU above 90% on one of 40 web servers. It fired 30 times. Nobody acted, and checkout errors and latency stayed within target each time.
- **B:** checkout attempts failing above target at the load balancer. It fired twice. Customers couldn't pay, and both times someone rolled back a release.
- **C:** at the current rate, the orders database fills its disk in 4 hours. It fired once. New orders stop when the disk is full. Someone found what was filling it and added space.
- **D:** the public site's certificate expires in 20 days. It fired once. Renewing takes one person 30 minutes, in working hours.
- **E:** one attempt of the nightly export failed, and its automatic retry finished it on time. Nobody uses it before morning. It fired 12 times. Nobody acted.

1. Mark each alert as a symptom or a cause.
2. Route each one to a page, a ticket or a dashboard, or delete it, with one reason.
3. Which cause still pages? Which words from the book justify it?
4. B fired when customers were already failing. Which alerts in this list could warn before users are affected?
5. Take the last five alerts that reached you or your team, or five you can see in a tool you use. Mark each one as a symptom or a cause, and say if someone had to act. Which one would you move first, and where?

---

_Written with an AI assistant from the sources above._

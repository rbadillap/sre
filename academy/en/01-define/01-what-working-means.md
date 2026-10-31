---
title: "What working means"
stage: define
order: 1
status: approved
teaches: "Write an SLI, an SLO and an error budget for one action users need to complete, and say where it's measured and what counts as a failure."
sources:
  - title: "Google SRE workbook, SLO Engineering Case Studies (Evernote's section)"
    url: https://sre.google/workbook/slo-engineering-case-studies/
  - title: "Zalando Engineering, Operation-Based SLOs"
    url: https://engineering.zalando.com/posts/2022/04/operation-based-slos.html
  - title: "Google SRE workbook, Implementing SLOs"
    url: https://sre.google/workbook/implementing-slos/
  - title: "Google SRE book, Service Level Objectives"
    url: https://sre.google/sre-book/service-level-objectives/
skills: [define-slos]
version: "0.1.1"
---

# What working means

_Sources: [Evernote's section of "SLO Engineering Case Studies"](https://sre.google/workbook/slo-engineering-case-studies/), [Zalando's "Operation-Based SLOs"](https://engineering.zalando.com/posts/2022/04/operation-based-slos.html), [Google's SRE workbook, "Implementing SLOs"](https://sre.google/workbook/implementing-slos/), and [Google's SRE book, "Service Level Objectives"](https://sre.google/sre-book/service-level-objectives/)._

## The question

A graph can say a service is healthy while users can't do what they came to do. So what does "working" mean, and how do you write it down as a number?

## What Evernote did

Evernote wrote this part of the chapter itself, after moving from its own datacenters to Google Cloud.

- **It started from users.** Before the technical details, it asked: "what promises are you trying to uphold?" It chose one need first: "the availability of the Evernote service for users to access and sync their content across multiple clients."
- **Its first target:** "99.95% uptime measured over a monthly window", for certain services and methods. The number came from talks with customer support and product teams, and from user feedback, which the chapter calls more important.
- **Where it measured:** a third-party prober, a tool that sends test requests, called a status page every minute from outside Evernote's environment. That page "exercises most of our stack".
- **What counted as a failure:** maintenance counted as downtime. Evernote couldn't assume all its users knew about published maintenance windows, and those who didn't would see "generic and unexplained downtime".
- **Why the provider's graph wasn't enough:** Google promises 99.95% availability for Compute Engine, its virtual machines. That's a different SLO from Evernote's, with the same number. "Even when GCP SLO graphs are green (i.e., above 99.95%), Evernote's view of the same SLO might be very different". The chapter's reason is that an outage in Evernote's region may be lost in the global number. It describes this as a possibility, not as one reported incident.
- **What it knew was missing:** the first SLO covered "most, but not all, user interactions". After about nine months of using SLOs, Evernote was on version 3 of its SLO practice, and it planned to probe individual API calls and to use metrics from the client.

## What Zalando did

Zalando compares two approaches in its own post from 2022.

- **First, one SLO per service.** From 2016, it introduced SLOs per microservice, on whatever its owners chose, usually availability and latency. A product is built from many services, and product managers "had a hard time connecting the myriad of SLOs and their own expectations for the products they are responsible for".
- **Then, one SLO per customer action.** It moved to what it calls Critical Business Operations, such as "View Catalog", "Add Item to Cart" and "Place Order". The signal is measured at the edge services, the ones that talk to customers. Each SLO has an owner: for "Place Order", the senior manager who owns the customer experience of the checkout and sales order systems.
- **Success isn't only a status code.** It raised this in the first stage, with an example: a service with two fallbacks. The first one is still "good enough". The second avoids an error, but the answer may no longer be of acceptable quality: "Even though the response was successful from the client's perspective, we still count it as an error."
- **What the post doesn't claim.** It calls this a "new type" of SLO and says it "granted us quite a few advantages". It also says "the purpose of this post is not to present a new and better type of SLOs", and that one type or the other, or both, may fit a given organization. It gives no target for "Place Order". Its before-and-after numbers are about alerts, in a trial inside its own SRE department.

## The terms, as the sources define them

- **SLI, service level indicator.** The book: "a carefully defined quantitative measure of some aspect of the level of service that is provided." The workbook recommends a ratio: good events divided by total events.
- **SLO, service level objective.** The book: "a target value or range of values for a service level that is measured by an SLI." The workbook: above that target, "almost all users should be happy with your service", assuming they're happy with what it does. Below it, users are likely to complain or leave.
- **Error budget.** The workbook: "the SLO is a target percentage and the error budget is 100% minus the SLO."

Two more points from the same sources:

- **Start from users, not from what's easy to measure.** The book says to start with what users care about, and that starting with what's easy to measure leads to "less useful SLOs". It adds that what users care about is often hard or impossible to measure, so you end up approximating it.
- **Measure close to the user.** The workbook's example uses load balancer metrics because they're already available and closer to the user's experience than application server logs. The book warns that server-side metrics can miss problems that affect users.

**Where a target comes from.** The book says "Don't pick a target based on current performance". The workbook calls that advice true, and adds that current performance "can be a good place to start if you don't have any other information", as long as you have a process for changing the target later.

## Reading the cases

The rest of this lesson is its own reading and method. Neither case gives a before-and-after figure for what users experienced, so this lesson doesn't claim that SLOs made either service more reliable.

- **A true graph can answer a different question.** The provider's graph could be green, and a response could be successful, while the thing the user needed didn't happen as it should.
- **What counts as a failure is a decision.** Evernote decided maintenance counts. Zalando's example counts a poor fallback as an error. Someone else could decide differently, so the decision has to be written.
- **A first definition can be incomplete, if it says so.** Evernote knew its first SLO didn't cover everything, and kept changing it.

## How to do it

1. Pick one action users came to do, and list its steps.
2. Write the SLI as good events over valid events: the workbook's total, minus the events you decide don't count. Say what makes an event good, in words about the result the user needs.
3. Say where you measure it, as close to the user as you can, and what that place can't see.
4. Write which events are valid, and which failures count against the service, before the next incident.
5. Set a target and a window. Write where the target came from. If you have no data, write it as a hypothesis and say what will test it.
6. Work out the budget: 100% minus the target, multiplied by the valid events you expect. If events are few, read [Error budgets for rare events](02-error-budgets-for-rare-events.md).
7. Write who agreed, and what changes when the budget runs out. An SLO is a separate thing from a promise to a customer: a later lesson covers that.

## Worked example

An example written for this lesson. It borrows the name of Zalando's "Place Order" operation; the rule, the target and the counts are invented.

- **Action:** a customer places an order. **Steps:** cart, payment, confirmation.
- **SLI:** orders confirmed and saved, divided by valid attempts to place an order.
- **Where:** at the service that receives the customer's request. It can't see a customer whose request never arrives.
- **Valid:** attempts with a complete cart and a payment method. Load tests don't count.
- **Counts against the service:** a failure in checkout, or in a provider checkout depends on. An attempt the customer cancels doesn't count.
- **SLO:** 99.9% over four weeks, as a hypothesis, tested by the first four weeks of data.
- **Budget:** with 500,000 valid attempts, 0.1% is 500 failed orders.
- **Agreed:** not yet. **When the budget runs out:** not decided yet, and that's written too.

_If you use rbadillap/sre: `define-slos` works through these decisions for one system and writes them to `reliability/slos/<system>.md`. It proposes a definition and changes no monitoring or configuration._

## In one sentence

"Working means users can do what they came to do, so I count good events over valid events for that action, as close to the user as I can, and I write down what counts as a failure."

## Exercise

A hypothetical case: a food delivery app. The health checks on its servers passed 99.99% of the time in the last four weeks. Its team proposes this availability SLI: requests that don't return a 5xx status code, over all valid requests to place an order. These are the counts for the same four weeks:

- 200,000 valid attempts to place an order, each one a single request.
- 200 attempts returned a 5xx status code, and no order was created.
- 1,000 attempts returned status code 200 with a "try again later" page, and no order was created.
- All the other attempts created an order.

The proposed target is 99.5% over four weeks.

1. What does the team's SLI give as a percentage? Is the target met?
2. Write an SLI based on what the customer came to do. What does it give?
3. What's the budget in failed orders? How much of it is spent under your SLI?
4. Why doesn't the 99.99% answer the question "can customers place an order"?
5. Pick one thing users do with a system you work on or use. Write its SLI in words, say where you'd measure it, and name one failure that place couldn't see. Propose a target and a window, say where the target came from, and write what counts as a failure.

---

_Written with an AI assistant from the sources above._

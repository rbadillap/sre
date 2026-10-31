---
title: "An SLA is not an SLO"
stage: define
order: 3
status: approved
teaches: "Tell an SLA from an SLO, work out what each allows in minutes, and check that the promise is looser than the target and the target no tighter than what the system achieves."
sources:
  - title: "AWS, Amazon S3 Service Level Agreement"
    url: https://aws.amazon.com/s3/sla/
  - title: "AWS, Amazon S3 storage classes"
    url: https://aws.amazon.com/s3/storage-classes/
  - title: "AWS, Summary of the Amazon S3 service disruption in the Northern Virginia (US-EAST-1) region"
    url: https://aws.amazon.com/message/41926/
  - title: "Google SRE book, Service Level Objectives"
    url: https://sre.google/sre-book/service-level-objectives/
  - title: "Google SRE workbook, Implementing SLOs"
    url: https://sre.google/workbook/implementing-slos/
skills: [define-slos]
version: "0.1.1"
---

# An SLA is not an SLO

_Sources: [AWS's Amazon S3 Service Level Agreement](https://aws.amazon.com/s3/sla/), [AWS's S3 storage classes page](https://aws.amazon.com/s3/storage-classes/), [AWS's summary of the S3 disruption of February 28, 2017](https://aws.amazon.com/message/41926/), [Google's SRE book, "Service Level Objectives"](https://sre.google/sre-book/service-level-objectives/), and [Google's SRE workbook, "Implementing SLOs"](https://sre.google/workbook/implementing-slos/)._

## The question

A customer asks for 99.99% in the contract. Your team has a target of 99.9%. Are these the same kind of number, and which one should be higher?

An SLO is a target for a measure of service, as [What working means](01-what-working-means.md) explains.

## What AWS publishes for S3

AWS gives two availability numbers for S3 Standard, a storage class: "Designed to deliver 99.99% availability with an availability SLA of 99.9%". The agreement says it was last updated on November 28, 2023.

- **What's promised.** AWS "will use commercially reasonable efforts" to meet the percentage each monthly billing cycle. If it doesn't, the customer can be eligible for a credit.
- **The consequence.** For S3 Standard, below 99.9% gives a 10% credit, below 99.0% gives 25%, and below 95.0% gives 100%. The percentage applies to charges for that storage class in the affected Region for that billing cycle.
- **How it's measured.** For each account, request type and 5-minute interval, AWS divides "InternalError" and "ServiceUnavailable" errors by total requests. The monthly figure is 100% minus the average of those rates.
- **What it takes.** The customer must open a claim, with request logs.
- **Its limit.** "Unless otherwise provided in the AWS Agreement, your sole and exclusive remedy for any unavailability, non-performance, or other failure by us to provide Amazon S3 is the receipt of a Service Credit (if eligible)".

These pages don't call 99.99% an SLO. They don't say why the two numbers differ, or what availability S3 achieved.

## What happened on February 28, 2017

All times are PST. This happened in one Region, Northern Virginia (US-EAST-1). At 9:37 AM, a command with an input entered incorrectly removed more S3 servers than intended. Two subsystems needed a full restart, and "While these subsystems were being restarted, S3 was unable to service requests."

GET, LIST and DELETE requests began working again by 12:26 PM, and were working normally by 1:18 PM. S3 was operating normally at 1:54 PM, when PUT requests were back.

## What the Google sources say

- **An SLA, a service level agreement, has a consequence.** It's "an explicit or implicit contract with your users that includes consequences of meeting (or missing) the SLOs they contain." The book's test is to ask "what happens if the SLOs aren't met?": "if there is no explicit consequence, then you are almost certainly looking at an SLO."
- **Who decides.** Business and legal teams pick the consequences. "SRE's role is to help them understand the likelihood and difficulty of meeting the SLOs contained in the SLA."
- **Leave a margin.** "Using a tighter internal SLO than the SLO advertised to users gives you room to respond to chronic problems before they become visible externally."
- **Be conservative.** "Much of the advice on SLO construction is also applicable for SLAs. It is wise to be conservative in what you advertise to users".
- **Current performance.** The book says "Don't pick a target based on current performance". The workbook says current performance "can be a good place to start if you don't have any other information", as long as you have a process for changing the target. It adds: "don't let current performance limit you as you refine your SLO".
- **A target above what you achieve.** If you adopt a tighter SLO before the product can meet it, the workbook says "you'll be permanently out of SLO". It suggests an aspirational SLO instead, tracked but "explicitly called out in your error budget policy as not requiring action".

## Reading the case

The rest of this lesson is its own reading and method.

- **S3's pair only shows a shape.** A tighter number sits above a looser promise. This case can't prove the rule below.
- **This lesson's own rule: the SLO is no higher than what the system achieves, and the SLA is lower than the SLO.** No source here states it in this form. The book says much of its SLO advice applies to SLAs, but doesn't say the SLA must be lower than the SLO. That ordering is this lesson's step. The workbook's warning covers an SLO above what the system achieves, and its aspirational SLO is an exception. This rule is a check on today's numbers, not a limit on where the target can go later.
- **The rule checks an order. It doesn't choose a number.** A target can sit below what the system achieves and still leave users unhappy.
- **A margin doesn't stop one large outage.** The 2017 failure lasted longer than a month's allowance at either number, as the worked example shows.
- **A credit doesn't measure what the customer lost.** This agreement defines a percentage of S3 charges. It doesn't look at what the failure cost the customer's business.

## How to do it

1. Ask what happens if the number is missed. If a contract gives a consequence, it's an SLA. If nothing explicit happens, it's almost certainly an SLO.
2. Write three numbers over the same length of window: what the system achieved, the SLO, and the SLA asked for.
3. Check they measure the same thing, and say so if they don't.
4. Turn each number into minutes: window in minutes × (100% − target).
5. Check the order. If the SLA isn't lower than the SLO, or the SLO is above what the system achieved, write that as a finding.
6. Read the contract's measure, exclusions, claim process and remedy. Tell business and legal teams how likely a miss is. They pick the consequence.
7. If the number asked for doesn't fit, offer one that does, or a promise about what the customer actually needs.

## Worked example

An example written for this lesson. It applies the S3 agreement as last updated in 2023 to the 2017 timeline. The summary doesn't say what terms applied in 2017, or whether any credit was paid.

Hypothetical account: it uses S3 Standard in US-EAST-1 and sends only GET requests, evenly through the month. Assume every GET fails with a counted error from 9:37 AM to 12:26 PM, all GETs succeed after that as a best case, there are no other errors, and no exclusion applies.

- **Month:** 28 days, or 40,320 minutes.
- **99.9% allows:** about 40 minutes. **99.99% allows:** about 4 minutes. AWS doesn't give a window for its 99.99%, so applying it to a month is this example's choice.
- **Failure:** 169 minutes. 169 ÷ 40,320 is about 0.42%, so the monthly figure is about 99.58%.
- **Result:** below 99.9% and above 99.0%, so a 10% credit, if the customer claims it. Counting until 1:18 PM instead: 221 minutes, about 99.45%, the same credit.
- **Same assumptions, for an account sending only PUT requests, all failing until 1:54 PM:** 257 minutes, about 99.36%. It's the same 10% credit for 88 more minutes of failure.

_If you use rbadillap/sre: when an SLA is requested, `define-slos` compares it with the SLO, shows what it allows in minutes, lists what it would need, and offers an alternative. It requires the SLO to be at or below what the system achieves, and doesn't include the workbook's aspirational SLO._

## In one sentence

"An SLO is the target my team acts on, an SLA is a promise with a consequence, and I keep the promise lower than the target and the target no higher than what we achieve."

## Exercise

A hypothetical case. Availability is measured the same way for all these numbers, over 30-day windows of 43,200 minutes. The last six windows were 99.97%, 99.95%, 99.98%, 99.93%, 99.96% and 99.97%. The team's target is 99.9%, and nothing explicit happens when it's missed. A customer asks for a contract at 99.99%, with a 20% credit when it's missed. Someone in sales suggests offering 99.9% instead. A third option is 99.5%.

1. Which number is the SLO, and which is the SLA the customer asks for? How can you tell?
2. How many minutes does each allow per window: 99.99%, 99.9% and 99.5%?
3. In how many of the six windows would 99.99% have been missed? And 99.9%? And 99.5%?
4. Which of the three would follow this lesson's rule as an SLA? Why doesn't 99.9% follow it, even though no window missed it?
5. Pick a service you work on or use. Does it have a published SLA? If it does, write what happens when it's missed and how it's measured. If it doesn't, write what you'd want its SLO to measure, and who would have to agree to a promise.

---

_Written with an AI assistant from the sources above._

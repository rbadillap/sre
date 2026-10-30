---
title: "Scope and signal"
stage: respond
order: 2
status: draft
teaches: "By tenant, region and version; the average hides."
sources:
  - title: "Atlassian, Post-incident review on the April 2022 outage"
    url: https://www.atlassian.com/engineering/post-incident-review-april-2022-outage
skills: [scope-and-signal]
version:
---

# Scope and signal

_Source: [Atlassian's post-incident review of the April 2022 outage](https://www.atlassian.com/engineering/post-incident-review-april-2022-outage)._

## The question

"Is it working?" has no useful answer for a service with many customers. The useful question is: working for whom, where, and since when?

## What happened at Atlassian

- A script meant to remove a legacy app was given the IDs of entire customer sites instead of the app's IDs. The deletion API accepted both kinds of ID without telling them apart, and 883 sites were deleted at once.
- 775 customers lost access to their products. For some of them, the outage lasted up to 14 days.
- Atlassian says over 99.6% of its customers and users kept using its cloud products.
- Its internal monitoring didn't detect the problem. The first signal was a customer's support ticket.

## Why the total didn't show it

For the service as a whole, 99.6% of customers were fine. Any signal that averages across customers would have looked almost normal. For 775 customers, the product was gone.

That's the point of scoping by tenant, region, version or device group, as well as in total: a large healthy group can hide a small group that's completely down. Scope is also written with its unknowns, as unknowns: which customers, since when, and what we don't know yet.

_If you use rbadillap/sre: `scope-and-signal` is the discipline for this, and `define-slos` breaks targets down per tenant for the same reason._

## In one sentence

"I ask 'broken for whom, where, and since when', because a healthy average can hide a group of customers that's completely down."

## Exercise

Your dashboard shows 99.9% of requests succeeding. Name three ways to split that number that could reveal a group in trouble, and which one you'd check first for a multi-tenant product.

---

_Written with an AI assistant from the source above._

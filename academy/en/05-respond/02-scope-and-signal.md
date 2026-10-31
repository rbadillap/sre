---
title: "Scope and signal"
stage: respond
order: 2
status: approved
teaches: "Say who is affected, where and since when, what you counted and what you don't know yet, using the signal closest to users."
sources:
  - title: "Atlassian, Post-incident review on the April 2022 outage"
    url: https://www.atlassian.com/engineering/post-incident-review-april-2022-outage
  - title: "Amazon Builders' Library, Building dashboards for operational visibility"
    url: https://aws.amazon.com/builders-library/building-dashboards-for-operational-visibility/
  - title: "Google SRE book, Service Level Objectives"
    url: https://sre.google/sre-book/service-level-objectives/
skills: [scope-and-signal, define-slos]
version: "0.1.1"
---

# Scope and signal

_Sources: [Atlassian's post-incident review of the April 2022 outage](https://www.atlassian.com/engineering/post-incident-review-april-2022-outage), [Amazon's "Building dashboards for operational visibility"](https://aws.amazon.com/builders-library/building-dashboards-for-operational-visibility/), and [Google's SRE book, "Service Level Objectives"](https://sre.google/sre-book/service-level-objectives/)._

## The question

"Is it working?" has no useful answer for a service with many customers. The useful question is: working for whom, where, and since when?

## What happened at Atlassian

All times are UTC, on April 5, 2022.

- **The change:** Atlassian needed to delete an old app from customer sites. The team that ran the deletion received the IDs of entire cloud sites instead of the app's IDs. The API accepted both kinds of ID and assumed the input was correct.
- **07:38 to 08:01:** a script deleted 883 sites, representing 775 customers.
- **07:46:** an affected customer created the first support ticket. Atlassian's internal monitoring didn't detect an issue, and the report gives the reason: the sites were deleted through a standard workflow.
- **08:17:** Atlassian started its major incident process.
- **08:53:** the team confirmed that the ticket and the script run were related.

How the report measures the outage:

- For some of the 775 customers, it lasted up to 14 days. All were restored by April 18.
- Over 99.6% of customers and users kept using the cloud products without disruption during the restoration.
- Atlassian knew exactly which sites were affected from the start. The number of customers took longer. The first estimate was about 400, after subtracting Atlassian's own sites and noting that a significant portion of the rest were inactive, free or small accounts. Later, with what the report calls "a much more accurate view" and by Atlassian's official definition of a customer, the number was 775. The report adds that most users were within the first 400.
- Most affected customers couldn't reach support through the normal online form, which needs a valid site URL. Some contact information was deleted too, so Atlassian didn't have immediate access to key contacts.

Atlassian's own lesson about communication: "we should have been transparent about what we did know and what we didn't know", rather than waiting for a full picture.

## Reading the case

This case doesn't show a total hiding a group. Atlassian knew the affected sites from the script's list, and the report's reason for the missed detection is the standard workflow, not an average. The exercise below shows how a total hides a group, with hypothetical numbers.

The rest of this section is this lesson's reading. It takes two things from the case:

- **The signal closest to users can come first.** To the system, this was a normal workflow. To a customer, the site was gone, and the first signal the report records is that customer's ticket. You can't rely on tickets alone, though: most affected customers couldn't use the normal form.
- **A number needs its definition, and needs to say if it's an estimate.** The first estimate was about 400 customers, and the later count, by the official definition, was 775. Either number alone, with no definition next to it, tells the reader less than it seems to.

## How to do it

Two sources support splitting a total:

- **Amazon** says operators use dashboards to quantify customer impact during an event. Its customer experience dashboards help answer questions that are "likely to be" "How many customers are impacted?" and "Which customers are most impacted?" Its system-level dashboards can include error responses broken down by customer.
- **Google's book** makes a similar point about latency, not customers: "A simple average can obscure these tail latencies", meaning the slowest requests.

The steps below are this lesson's own method, not Amazon's, Google's or Atlassian's:

1. Answer who, where, what and since when: which customers, which regions and versions, errors or slowness, and when it started.
2. Choose the signal closest to what users experience. If your system shows no issue and users report a loss, treat their report as evidence, and find out why the system can't see it.
3. Look at the total, then split it by customer, region and version.
4. Write the scope with its definitions and its unknowns, and write it again when a fact changes it.

For this case, an example written for this lesson, using the numbers from the report: "883 sites deleted between 07:38 and 08:01 UTC. About 400 customers by first estimate, after removing Atlassian's own sites and allowing for many inactive, free or small accounts; not yet checked against the official definition. Unknown: which regions, and how to reach owners whose contact information was deleted."

_If you use rbadillap/sre: `scope-and-signal` asks these questions, and says not to let scoping delay a mitigation (an action that reduces the harm) that is safe and reversible. `define-slos` applies it to targets, by customer or device group as well as in total._

## In one sentence

"I ask 'broken for whom, where, and since when', and I say what I counted and what I don't know yet, because a healthy total can hide a group that's completely down."

## Exercise

A hypothetical case: in the last hour your service got 1,000,000 requests and 1,000 failed, so the dashboard shows 99.9%. All 1,000 failures came from one customer, who sent 1,000 requests.

1. What is the success rate for that customer?
2. Write the scope in one or two lines: what you know, and two things you don't know yet.
3. Suppose that in the next hour, none of that customer's requests reach your service, and the other 999,000 all succeed. What does the dashboard show for that hour, and what signal could still show the problem?
4. Take the main number on your team's dashboard, or on a service you use. Which split would you check first, and can you get it today?

---

_Written with an AI assistant from the sources above._

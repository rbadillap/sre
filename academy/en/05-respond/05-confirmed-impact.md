---
title: "Confirmed impact"
stage: respond
order: 5
status: draft
teaches: "Only confirmed impact, from the first update."
sources:
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
  - title: "Atlassian, Post-incident review on the April 2022 outage"
    url: https://www.atlassian.com/engineering/post-incident-review-april-2022-outage
skills: [verified-impact]
version:
---

# Confirmed impact

_Sources: [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/) and [Atlassian's review of the April 2022 outage](https://www.atlassian.com/engineering/post-incident-review-april-2022-outage)._

## The question

People affected by an incident want to know two things early: is it me, and how bad is it? The question is: what can I say before I know the cause, without saying something I'll have to take back?

## Two companies, two approaches

**GitLab, 2017:**
- It kept its notes in a public document during the incident, streamed the recovery live on YouTube, and posted updates on its status account for people not watching.
- Its postmortem gives the impact in numbers: roughly 5,000 projects, 5,000 comments and 700 new user accounts.
- It also gives two different end times for the lost data, 00:00 and 23:30 UTC, without reconciling them.

**Atlassian, 2022:**
- The first customer ticket arrived at 07:46 UTC, and the first status page update was posted at 09:03. Broad public communication came two days later.
- In its review, Atlassian says it should have communicated broadly much earlier, and been transparent about what it did know.
- It also couldn't reach many customers, because their contact information had been deleted with their sites.

## What to say, and when

1. **Send the first update before you know the cause.** Who is affected, what they can't do, since when, and when the next update comes. "We don't know the cause yet" is a valid line.
2. **Say only what's confirmed, and mark the rest.** Confirmed impact is what you've seen in the user-facing signal. Suspected impact is a hypothesis, labeled as one.
3. **Keep the numbers consistent.** Two different figures for the same thing make readers doubt both. GitLab's two end times are a small example.
4. **Keep a way to reach people that doesn't depend on the broken system.** Atlassian lost contact data along with the sites.

_If you use rbadillap/sre: `verified-impact` is the discipline for this, applied to every update in `respond-to-alert`._

## In one sentence

"My first update goes out before I know the cause: who is affected, since when, and when I'll update again, with only what's confirmed."

## Exercise

Ten minutes into an incident, you know checkout fails for some customers in one region, and you suspect it's all regions. Write the first update in four lines.

---

_Written with an AI assistant from the sources above._

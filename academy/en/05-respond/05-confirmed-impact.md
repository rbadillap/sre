---
title: "Confirmed impact"
stage: respond
order: 5
status: approved
teaches: "Send a first update without waiting for the full picture: what's confirmed, what's still an estimate, and when the next update comes."
sources:
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
  - title: "Atlassian, Post-incident review on the April 2022 outage"
    url: https://www.atlassian.com/engineering/post-incident-review-april-2022-outage
skills: [verified-impact]
version: "0.1.1"
---

# Confirmed impact

_Sources: [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/) and [Atlassian's review of the April 2022 outage](https://www.atlassian.com/engineering/post-incident-review-april-2022-outage)._

## The question

This lesson starts from two questions someone affected may ask: am I affected, and how bad is it? What can you say before you have the full picture, without saying something you'll have to take back?

## What happened at Atlassian

All times are UTC, in April 2022. A script deleted 883 sites on April 5, starting at 07:38. Atlassian's monitoring didn't detect the problem.

- **April 5, 07:46:** an affected customer created the first support ticket. Support acknowledged the incident by 08:31.
- **April 5, 08:53:** the team linked the ticket to the script.
- **April 5, 09:03:** the first status page update said Atlassian was investigating. At 11:13, another said the root cause had been identified.
- **April 7, 00:56:** Atlassian posted its first broad public message, on Twitter.
- **April 12:** Atlassian's CTO published details of what happened, who was affected, and that restoration could take up to two weeks.

What the review says about this:

- Atlassian prioritized direct contact with affected customers, but couldn't reach many of them, because their contact information was deleted with their sites. It took days to get a reliable list of key contacts.
- Most affected customers couldn't use the normal support form, because it needs a valid site URL.
- "We did not provide acknowledgment of the incident quickly and consistently through multiple channels".
- "Rather than wait until we had a full picture, we should have been transparent about what we did know and what we didn't know."
- General restoration estimates, "even if directional" (rough, showing only the general direction), and saying when a more complete picture was expected would have helped customers plan.

## What GitLab published

On January 31, 2017, GitLab.com was unavailable for many hours after data was accidentally removed from its primary database. Its postmortem, published February 10, says:

- **What was lost:** changes to database data, such as projects, comments, user accounts, issues and snippets, starting at 17:20 UTC.
- **What wasn't:** code repositories and wikis were unavailable during the outage but weren't part of the data loss.
- **Who wasn't affected:** users outside GitLab.com (GitLab Enterprise, GitHost, self-managed).
- **How sure it is:** "Our best estimate is that it affected roughly 5,000 projects, 5,000 comments and 700 new user accounts." It also says "It's hard to estimate how much data has been lost exactly."

The same post isn't fully consistent. It gives the end of the lost period as both 00:00 and 23:30 UTC, and describes the project and comment counts as both "roughly" and "at least".

During the incident, GitLab kept notes in a document that was private at first and then public, streamed the recovery on YouTube, and used Twitter for people not watching.

## Reading the case

The rest of this lesson is its own reading and method. Neither source shows a first update being taken back.

- **Don't wait for what you don't have yet.** Atlassian's problem wasn't a missing cause: it linked the script to the ticket at 08:53, before its first status update. By its own review, it was too slow to communicate broadly while it didn't have the full picture. What's missing can differ from one incident to another, and the cause is often part of it, so the same rule applies to the cause.
- **Saying who isn't affected is part of the impact.** GitLab's line about users outside GitLab.com answers "am I affected?". Its line about repositories and wikis answers "how bad is it?".
- **An estimate is fine if it's labeled.** GitLab's "best estimate" tells readers how much weight to give the number. This is a statement written after the incident, not a first update, so read it as a model for the wording. Its two end times show why to check a number before repeating it.
- **The way to reach people can't depend on what broke.** Atlassian lost site contacts, and most affected customers lost the support form.

## How to do it

1. Send the first update without waiting for the full picture. "We don't know the cause yet" is a valid line.
2. Say what's confirmed to be affected, who isn't as far as you can tell, and since when. Confirmed means you've seen it in a signal users experience, or users have reported it and you've checked.
3. Label everything else: an estimate is an estimate, and a suspected cause stays out of the update until it's checked. [Reframe first](01-reframe-first.md) shows why a first explanation can be wrong.
4. Say what you're checking, without naming a suspected cause, what people should do, if anything, and when the next update comes.
5. Keep one list of the numbers you've published, and say so when one changes.

For this case, an example written for this lesson, for Atlassian's first hour: "Some customers can't access their sites, since at least 07:46 UTC. We have no reports from other customers so far. We're checking what changed in site data and don't have a restoration estimate yet. If the support form doesn't work for you, write to [another channel]. At 10:00 UTC we'll update this and say when we expect an estimate."

_If you use rbadillap/sre: `verified-impact` gives each update four parts: what's confirmed and since when, what's being checked, what people should do, and when the next update comes. In a large incident, it also asks for one person to own the updates, so the person fixing isn't doing both._

## In one sentence

"My first update doesn't wait for the full picture: what's confirmed, since when, what's still an estimate, and when I'll update again."

## Exercise

A hypothetical case, with times in UTC: it's 14:20. Since 14:10, checkout has been failing for customers in Europe, and you've confirmed that in your error data and in customer reports. Your error data suggests about 20% of European checkouts fail, not yet checked against orders. Checkout in the US looks normal in your data. Someone says the payment provider is the cause, but nobody has checked. You're checking the payment step, customers can retry later, and you can update again at 14:50.

1. Write the first update in four lines.
2. Which claim did you leave out, and which number did you label? Why?
3. At 14:50, you've confirmed the US has been failing too, since 14:40, and the provider's status is normal. You're now checking the last change to checkout, customers can still retry later, and you can update again at 15:20. Write the second update.
4. Find a status page update from a service you use. Which parts does it present as confirmed, which as estimates, and is anything missing?

---

_Written with an AI assistant from the sources above._

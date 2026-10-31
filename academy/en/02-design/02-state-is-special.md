---
title: "State is special"
stage: design
order: 2
status: approved
teaches: "Say what a change leaves behind and whether the old version can read it, and in an incident write what each way back would lose before anyone chooses."
sources:
  - title: "GitHub, October 21 post-incident analysis"
    url: https://github.blog/news-insights/company-news/oct21-post-incident-analysis/
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
  - title: "Amazon Builders' Library, Ensuring rollback safety during deployments"
    url: https://builder.aws.com/content/3F04j2yRAAMBuPSPs50xwXZqg01/ensuring-rollback-safety-during-deployments
skills: [state-is-special]
version: "0.1.1"
---

# State is special

_Sources: [GitHub's October 21 post-incident analysis](https://github.blog/news-insights/company-news/oct21-post-incident-analysis/), [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/), and [Amazon's "Ensuring rollback safety during deployments"](https://builder.aws.com/content/3F04j2yRAAMBuPSPs50xwXZqg01/ensuring-rollback-safety-during-deployments)._

## The question

A rollback puts the old code in place. It doesn't change data that's already written. So before you choose a way back, what does each option do to the data, and what are you willing to give up to protect it?

## What happened at GitHub

All times are UTC, in October 2018.

- **October 21, 22:52:** maintenance work caused a loss of connectivity between GitHub's US East Coast network hub and its primary East Coast data center. It was restored in 43 seconds. During the break, Orchestrator, the tool that handles database failover, began moving clusters to direct writes to the West Coast. When connectivity returned, applications began writing there.
- **Two copies, each with its own writes:** the East Coast servers held a brief period of writes not replicated to the West. "Because the database clusters in both data centers now contained writes that were not present in the other data center, we were unable to fail the primary back over to the US East Coast data center safely."
- **23:07:** the team locked its deployment tooling.
- **The decision:** GitHub decided on what it calls failing-forward, a term it doesn't define. Applications in the East couldn't cope with the cross-country latency of writing to the West. "This decision would result in our service being unusable for many users. We believe that the extended degradation of service was worth ensuring the consistency of our users' data."
- **23:19:** it paused webhook delivery and GitHub Pages builds. "In other words, our strategy was to prioritize data integrity over site usability and time to recovery."
- **Restoring:** the plan was to restore from backups, synchronize replicas in both sites, return to a stable layout, and then process queued jobs. Restoring multiple terabytes took hours.
- **October 22, 11:12:** all primaries (the copies that take writes) were back on the East Coast. Dozens of read replicas (copies that serve reads) were hours behind, so users saw inconsistent data.
- **16:24 to 23:03:** after a failover to the original layout, GitHub kept its status degraded while it processed over five million webhook events. About 200,000 webhook payloads "had outlived an internal TTL", a time limit, and were dropped. Status went green at 23:03, after 24 hours and 11 minutes of degraded service.
- **The writes in between:** GitHub captured the binary logs, the database's record of its writes, for those not replicated. "For example, one of our busiest clusters had 954 writes in the affected window." When the post was published, it was still working out which could be reconciled automatically and which needed contact with users.

The post leaves two points open:

- **How long West had been taking writes.** Under the 23:13 heading, the post says "nearly 40 minutes" and then "30+ minutes". By its own times, 22:52 to 23:13 is 21 minutes. It doesn't say whether these lines look past 23:13.
- **What was lost.** It says "Ultimately, no user data was lost; however manual reconciliation for a few seconds of database writes is still in progress." It also reports the dropped webhook payloads. It doesn't say whether those count as user data, and doesn't give the final result of the reconciliation.

## What GitLab published

On January 31, 2017, data was accidentally removed from GitLab.com's primary database. To recover, GitLab used a snapshot created "roughly 6 hours before the outage". The other snapshot available would have meant losing "almost 24 hours of data". GitLab says it lost changes to database data "between 17:20 and 00:00 UTC". Elsewhere, the same post gives the end of that period as 23:30 UTC.

## What Amazon's article says about rollback

- **The usual obstacle.** "We found that the most common reason for not being able to roll back is a change of protocol."
- **Its example, not an incident.** A change starts compressing data before saving it. "After the new version writes some compressed data, rolling back isn't an option." The old version doesn't know it has to decompress.
- **Two-phase deployment, also a hypothetical in the article.** First, Prepare: all servers learn to read JSON as well as XML, and keep writing XML. Then Activate: they write JSON. Rolling back Activate is safe, because the prepared version reads both.
- **Its limit.** "While each of the two phases is safe for rolling back, we can't roll back both changes." So Amazon waits between phases, usually a few days.

## Reading the cases

The rest of this lesson is its own reading and method.

- **What these cases don't show.** This lesson's sources don't show a real incident where rolling back code left data broken. GitHub's case is a database failover, not a code rollback, so it's used here for a similar problem, not the same one.
- **A snapshot is a way back with a price.** GitLab's price was the changes after the snapshot. A restore gives you an older state, not the state you had.
- **Integrity over availability was a decision with a cost.** GitHub stated the cost: a service unusable for many users, and "extended degradation". The incident lasted 24 hours and 11 minutes in all. The post doesn't show what the other choice would have cost, so it doesn't prove this is right for every system.
- **Queued work is state too.** Webhooks waiting during the outage could outlive their time limit, and some did.

## How to do it

Before a change:

1. List what it leaves behind: rows, schemas, cache entries, queued messages, files, stored configuration.
2. Ask whether the old version can read what the new version writes. If not, rollback isn't your way back.
3. Split it: first read both formats, then write the new one, and wait between them.

During an incident:

4. Stop what makes it worse. Lock deployments, and pause jobs that write.
5. Save what can't be recreated, such as logs of writes that exist on only one side.
6. Write every way back, and for each one: what's lost, how many writes, how long it takes, and what users see meanwhile.
7. Have a person choose, and write who chose and why.
8. Afterwards, deal with the writes left over, and report what happened to them.

## Worked example

An example written for this lesson, using only GitHub's post:

| Way back | What it would lose | What users see | Time |
|---|---|---|---|
| Fail the primary back to the East at once | Post says it couldn't be done safely, with West's writes already taken | Not stated | Not stated |
| What GitHub did: restore the East from backups, replicate from the West, move primaries back | Post says no user data. Writes held only in the East still needed reconciling (954 in one busy cluster, no total given). About 200,000 webhook payloads dropped | Slow pages, inconsistent data, webhooks and Pages paused | Green 24 hours and 11 minutes after 22:52. No time given from the decision |

- **Who chose:** the post says "we", without naming a role, so this record stays blank.

_If you use rbadillap/sre: `state-is-special` is a discipline other skills apply, not a procedure. It asks what a change leaves behind, requires compatible formats, and treats a snapshot as part of a recovery that a person decides on._

## In one sentence

"Before I choose a way back I write what each option does to the data, because rolling back code doesn't roll back what's already written."

## Exercise

A hypothetical case. At 10:00, a release starts saving each order's price in a new format. The old version can't read that format, and the new version reads both. At 10:30, you find a bug that shows wrong prices on receipts. The bug is only in the new version, and the saved orders are correct.

- 20,000 orders were saved between 09:00 and 10:00, in the old format.
- 12,000 orders were saved between 10:00 and 10:30, in the new format.
- The last snapshot is from 09:00. Orders exist nowhere else.
- Option C is a fix to the new version that takes 40 minutes to ship. Assume it works, and receipts stay wrong until then.

1. Option A: roll back the code only. What happens to the 12,000 orders?
2. Option B: if you restore the 09:00 snapshot now, at 10:30, how many orders are lost?
3. Option C: keep the new version and ship the fix. What's lost, and what's the cost?
4. Write the three options as a table, with what each loses and what users see. Say who should choose. The numbers can't tell you what a wrong receipt costs your business, so write that as unknown.
5. How could the release have shipped in two phases, so rollback stayed possible?
6. Pick a recent change in a system you work on or use. What did it leave behind, and could the previous version read it?

---

_Written with an AI assistant from the sources above._

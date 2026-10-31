---
title: "Postmortems"
stage: learn
order: 1
status: approved
teaches: "Write a postmortem that separates what triggered an incident from what limited detection and recovery, stays blameless without inventing anything, and ends in actions with a place, an owner role and a check."
sources:
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
  - title: "Google SRE book, Postmortem Culture"
    url: https://sre.google/sre-book/postmortem-culture/
skills: [write-postmortem]
version: "0.1.1"
---

# Postmortems

_Sources: [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/) and [Google's SRE book, "Postmortem Culture"](https://sre.google/sre-book/postmortem-culture/)._

## The question

A postmortem records what broke. What else does it have to ask, so the team knows what should change?

## What happened at GitLab

All times are UTC and approximate, as in the post.

- **January 31, 17:20:** an engineer took an LVM snapshot (a copy of a disk at one moment) of the production database and loaded it into staging, for a load test.
- **19:00:** database load rose. GitLab suspects spam, and later found that a background job removing a GitLab employee's account was part of it.
- **23:00:** replication to the secondary database failed. Fixing it by hand meant wiping the secondary's data directory and copying the data again with `pg_basebackup`, work the post calls "not automated, nor was it documented properly". An engineer wiped it, and the tool hung.
- **23:30:** an engineer ran the wipe again, "errantly thinking they were doing so on the secondary". It ran on the primary. They stopped it a second or two after noticing, and around 300 GB was already gone.
- **Recovery, ending February 1:** copying data from staging took around 18 hours. The post names the staging disks as the main bottleneck, throttled to around 60 Mbps. The database was restored without webhooks at 17:00 on February 1, and final steps finished around 18:00.

What the engineers found when they went to recover:

- **Daily `pg_dump` backups:** the S3 bucket was empty. The job used PostgreSQL 9.2 tools on a 9.6 database and ended in an error. Failure emails were rejected by the receiving server: "we were never aware of the backups failing, until it was too late." The post doesn't say how long this had been happening.
- **Azure disk snapshots:** not enabled for database servers, "as we assumed that our other backup procedures were sufficient enough."
- **Replication:** broken, and the secondary was already wiped.
- **LVM snapshots:** "not really meant to be used for disaster recovery". One was about 6 hours old, the manual one from 17:20. The other was the daily one. The post says it was "almost 24 hours" old, and also says that run happens at 01:00, about 22.5 hours before 23:30.

GitLab restored from the 6-hour snapshot, "our only option to reduce data loss as much as possible". The post's later analysis says why the backup procedure wasn't tested regularly: "there was no ownership, as a result nobody was responsible for testing this procedure."

What was lost, and how long it took:

- **Lost:** changes to database data, such as projects, comments, user accounts, issues and snippets, from 17:20. The post ends that period at both 00:00 and 23:30. It describes the counts as both "roughly" and "at least" 5,000 projects and 5,000 comments, and it adds: "It's hard to estimate how much data has been lost exactly".
- **Not lost:** "Git repositories and Wikis were not removed as they are stored separately." Projects created after 17:20 came back from their Git repositories only "in their most basic form", without issues and merge requests.
- **How long:** the post says GitLab.com "was down for about 18 hours", and separately that restoring "took over 18 hours". Copying alone took "around 18 hours". It doesn't reconcile the three.

The post analyzes two problems: GitLab.com being down, and restoring taking so long. [From lesson to default](02-from-lesson-to-default.md) sorts its changes.

## What Google's book says

- **What a postmortem is:** "a written record of an incident, its impact, the actions taken to mitigate or resolve it, the root cause(s), and the follow-up actions to prevent the incident from recurring."
- **Blameless:** it focuses on contributing causes "without indicting any individual or team for bad or inappropriate behavior."
- **It keeps the actions:** the format "clearly identifies the actions that led to the incident."

GitLab's post never uses the word "blameless". It names no engineer. Its working document did, added by the engineer, and the post says "we will redact names in future cases as other engineers may not be comfortable with their name being published".

## Reading the case

The rest of this lesson is its own reading and method.

- **"What broke?" doesn't give a culprit.** Here it gives a fact: the primary's data directory was removed. A postmortem documents that, then widens the investigation: what conditions allowed the incident, and what made it hard to detect or recover from?
- **Two failures, two effects.** The deletion triggered the outage. The backup failures limited recovery. Neither explains the other.
- **Not everything stayed unnoticed.** The engineer noticed during the wipe and stopped it a second or two later. The post doesn't say how long it had run. The backup failures weren't noticed until the backups were needed.
- **The case doesn't show that working backups would have lost less data.** `pg_dump` was meant to run every 24 hours, so its newest copy could have been older than the 6-hour snapshot. The post does say the staging copy was needed because Azure snapshots weren't enabled and `pg_dump` wasn't working.
- **Be exact about the loss.** It was database data. Saying GitLab lost code would be wrong.
- **Blameless writing doesn't invent controls.** This rule is the lesson's own; neither source states it. Removing blame doesn't allow adding a safeguard that didn't exist, or deleting what someone did.

## How to do it

1. Write the impact: what was lost, for whom, from when. Label estimates, and say what wasn't affected, as in [Confirmed impact](../05-respond/05-confirmed-impact.md).
2. Write the timeline with times. Note the gaps.
3. Name what triggered the incident, then, separately, the conditions that allowed it.
4. For each failure, ask when anyone could have known, and what signal was missing.
5. List each recovery option. Say which worked, which didn't and why, and what that limited. Testing restores before you need them is covered in [Tested restores](../02-design/05-tested-restores.md).
6. Keep the action in the story. Don't judge the person, and don't describe a control you can't show.
7. Give every action a place, an owner role and a check. "Be more careful" isn't one. Say whether it's done or planned.

## Worked example

An example written for this lesson, using GitLab's facts. The wording and the action are this lesson's.

- **Impact:** database changes from 17:20 lost, with two end times published. An estimate of roughly, or at least, 5,000 projects (the post says both). Git repositories and wikis not lost. GitLab.com users only; self-managed and GitHost weren't affected.
- **Trigger:** the wipe ran on the primary during manual work to rebuild the secondary.
- **Conditions:** replication had stopped, and rebuilding it was manual and not properly documented.
- **Detection:** the deletion, by the engineer while it ran, with no time given. The backup failures, only at recovery, with failure emails being rejected.
- **Recovery:** the 6-hour snapshot was the best copy left, and the copy took around 18 hours.
- **A blameless sentence:** "While rebuilding the secondary, an engineer ran the wipe on the primary, believing it was the secondary."
  - Not "the data directory was removed", which hides the action.
  - Not "the host check failed to stop the command". The post describes no such check.
- **An action:** alert when the newest backup is older than expected. **Where:** the monitoring system, not the job's email. **Owner role:** the data durability owner. **Check:** stop the backup job in a test environment, and confirm the alert reaches someone. This helps find failed backups sooner. It doesn't stop a deletion.

_If you use rbadillap/sre: `write-postmortem` writes this document from the incident record, with a section on why it wasn't detected sooner, and gives each action a place, one named person and a date. It has no section on recovery and doesn't ask how to check an action, so add both._

## In one sentence

"The deletion triggered the outage and the backup failures limited recovery, so a postmortem examines both and says what should change."

## Exercise

A hypothetical situation, built from GitLab's facts. Assume a production database with these facts, and nothing else:

- A disk snapshot runs once a day at 01:00 UTC and is stored on staging.
- The daily `pg_dump` backup fails.
- The secondary can't be counted on, because rebuilding it wipes it.
- Assume a deletion like GitLab's happens again at 23:30 UTC.

1. With only the 01:00 snapshot, how many hours of database changes are lost?
2. Propose one action that reduces data loss even if a deletion happens again. Say where it lives, which role owns it, and how you'd check it works. Say the most hours your action could still lose.
3. Why shouldn't you claim your action prevents the deletion, or that it would have prevented all loss?
4. In your own system, which recovery task do you assume works, and how would you check it this week?

---

_Written with an AI assistant from the sources above._

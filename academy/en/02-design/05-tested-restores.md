---
title: "Tested restores"
stage: design
order: 5
status: approved
teaches: "Test whether a backup can bring data back: run a full restore, check the data is usable, time it, and give the test an owner, a schedule and an alert."
sources:
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
  - title: "Google SRE book, Data Integrity: What You Read Is What You Wrote"
    url: https://sre.google/sre-book/data-integrity/
skills: [review-design]
version: "0.1.1"
---

# Tested restores

_Sources: [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/) and [Google's SRE book, "Data Integrity"](https://sre.google/sre-book/data-integrity/)._

## The question

A backup job can run every day and save nothing. How do you find out whether you can get your data back, before the day you need it?

## What happened at GitLab

The post marks its timeline times as approximate. All are UTC. For primary copies, replicas and failover, see [State is special](02-state-is-special.md).

- **January 31, about 23:30:** while trying to restore database replication, an engineer wiped a database directory, thinking it was on the secondary server. It was on the primary. Around 300 GB was gone before the engineer stopped it. The secondary's data had already been wiped as part of the same repair, so neither host could be used.
- **Then:** the engineers looked for backups. "Unfortunately the process of both finding and using backups failed completely."

What GitLab found, procedure by procedure:

- **`pg_dump`, a logical export of the database, every 24 hours to Amazon S3.** "The S3 bucket was empty". The job used PostgreSQL 9.2 tools against a 9.6 database, and that difference made it end with an error.
- **The alert for that failure.** Failure emails were sent, but the receiving mail server rejected them, because they weren't signed using DMARC, an email authentication standard. "This means we were never aware of the backups failing, until it was too late."
- **Azure disk snapshots.** These were on for other servers, not the database servers: "we assumed that our other backup procedures were sufficient enough".
- **Replication.** The post says it was used primarily for failover, not for disaster recovery.
- **LVM snapshots, copies of the disk.** They were primarily used to copy production data to staging, and "are not really meant to be used for disaster recovery". One was almost 24 hours old. The other, roughly 6 hours old, had been made by hand by an engineer before starting work in staging.

The recovery:

- GitLab used the 6-hour snapshot, "our only option to reduce data loss as much as possible". The other option meant losing "almost 24 hours of data".
- Copying from staging to production took around 18 hours, on slow disks. GitLab finished around 18:00 UTC on February 1.
- It lost about 6 hours of database changes, from 17:20 UTC.

GitLab's own root cause question, and its answer: "Why was the backup procedure not tested on a regular basis? - Because there was no ownership, as a result nobody was responsible for testing this procedure."

The post lists work it was doing, including "Automated testing of recovering PostgreSQL database backups" and "Assign an owner for data durability". These are plans in the post, which doesn't report their result. It does say LVM snapshots were by then taken every hour.

## What Google's book says

The chapter's advice:

- "you only know that you can recover your recent state if you actually do so."
- It calls a full end-to-end test the only one to trust, because parts of a recovery can break even after a recent success.
- Test continuously, as part of normal operations, and automate it: a manual, staged test isn't done "either deeply or frequently enough".
- Alert when a recovery process fails to report its success.
- Check, among other things: "Are your backups valid and complete, or are they empty?", and whether recovery finishes in reasonable time.

Two of Google's own cases, both in its own account:

- **Gmail, February 2011.** Gmail lost a significant amount of user data and restored from tape. It was the first large-scale restore of live customer data from that system, but "similar situations had been previously simulated many times". The chapter says that's why Google could give an estimate, restore all accounts within several hours of that estimate, and recover "99%+" of the data before the estimated completion time.
- **Google Music, March 2012.** A deletion bug removed tracks. The recovery came weeks after the company's annual disaster recovery test, and the chapter calls that timing "one factor working in their favor". Its term for these tests is DiRT, which it doesn't spell out. "Despite the team's DiRT experience", restoring 1.5 petabytes "took longer than the two days estimated". A vendor left 1,862 tapes out of the recall, and 17 tapes were bad. Over 99.95% of the restore was done by the morning of March 11, after starting on March 8. An unrelated production failure then took the team for two days. The 436,223 tracks found on tape, of about 600,000 lost, were back on March 13.

## Reading the cases

The rest of this lesson is its own reading and method.

- **What the case supports.** GitLab says its backup procedure wasn't tested regularly, and ties that to no owner. A restore test that looks at the bucket finds it empty: that's this lesson's inference, not the post's claim.
- **What it doesn't support.** A test wouldn't have stopped the deletion. It's also unclear that it would have reduced the data lost. A working `pg_dump` runs every 24 hours, and the post doesn't say at what hour, so it might have been older than the 6-hour snapshot GitLab used. Testing tells you what you have. It doesn't choose how often you back up.
- **The alert was part of the backup.** The job failed, and the signal failed too. This lesson's rule follows Google's advice: alert when the success signal is missing, not only when a failure message arrives.
- **A test gives you numbers, not certainty.** Gmail shows an estimate that came close. Music shows one that didn't, even with a recent exercise. Neither shows what would have happened without testing.

## How to do it

1. List each thing you call a backup, and what you'd use it for.
2. Restore a whole copy to a separate place, end to end, the way you'd do it in an emergency.
3. Check that the data is usable: the application can read it, and counts and samples match what you expect. A finished restore job isn't enough.
4. Time it. Write how long it took, and how old the restored data was.
5. Compare both numbers with what you can accept.
6. Give the test an owner and a schedule, with a reason for that schedule.
7. Alert if the test fails, and if it stops running.
8. Test again after any change to the database version, the tooling, the storage or the size.

## Worked example

An example written for this lesson, using only GitLab's facts. "Not stated" means the post doesn't give one.

- **`pg_dump` to S3.** For: restoring the database. State found: empty bucket. Last restore test: not stated. Owner: none.
- **Azure snapshots.** For: restoring whole disks. State found: not on for database servers.
- **LVM snapshots.** For: refreshing staging. State found: two available, one used, about 6 hours old. Last restore test: not stated. Copy time: around 18 hours.

_If you use rbadillap/sre: `review-design` is a wider review of how a system fails. For restores, it looks for an owner, a frequency with its reason, the last result with the data checked usable and the recovery time measured, an alert if the test fails or stops, and a new test after relevant changes. It reviews that practice and doesn't schedule or run a restore._

## In one sentence

"A backup counts when I've restored it: the data is usable, I know how long it took and how much would be lost, and someone gets alerted if that test fails or stops."

## Exercise

A hypothetical case: a 1,200 GB database is backed up once a day at 02:00 UTC. A failure sends an email to a shared mailbox. The last restore test was 14 months ago, on a 300 GB database, and took 3 hours. Since then, the team has moved to a new major database version. Nobody owns the test. The business says it can lose at most 6 hours of data, and be down at most 8 hours. Assume restore speed is the same as in the last test.

1. What's the most data this schedule can lose? Is that within the limit?
2. How long would a restore take now? Is that within the limit? How much can you trust this number, and why?
3. The mailbox has shown no failures for 14 months. What does that tell you, and what doesn't it tell you?
4. Write the restore test for this database: what it restores, what it checks, who owns it, how often it runs and why, and what alerts.
5. Pick a backup in a system you work on or use. When was it last restored, how long did that take, and who would know if it stopped working? Write "unknown" where you don't know.

---

_Written with an AI assistant from the sources above._

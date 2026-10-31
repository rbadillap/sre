---
title: "Blind spots"
stage: observe
order: 3
status: approved
teaches: "List what each signal can't see, trace how an alert reaches a person, and find a monitor that depends on what it monitors."
sources:
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
  - title: "Slack Engineering, A Terrible, Horrible, No-Good, Very Bad Day at Slack"
    url: https://slack.engineering/a-terrible-horrible-no-good-very-bad-day-at-slack/
  - title: "Atlassian, Post-incident review on the April 2022 outage"
    url: https://www.atlassian.com/engineering/post-incident-review-april-2022-outage
  - title: "Roblox, Roblox Return to Service"
    url: https://about.roblox.com/newsroom/2022/01/roblox-return-to-service-10-28-10-31-2021
  - title: "AWS, Summary of the Amazon S3 service disruption in the Northern Virginia (US-EAST-1) region"
    url: https://aws.amazon.com/message/41926/
  - title: "Google SRE book, Monitoring Distributed Systems"
    url: https://sre.google/sre-book/monitoring-distributed-systems/
  - title: "Google SRE workbook, Alerting on SLOs"
    url: https://sre.google/workbook/alerting-on-slos/
skills: [find-blind-spots]
version: "0.1.1"
---

# Blind spots

_Sources: [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/), [Slack's post on May 12, 2020](https://slack.engineering/a-terrible-horrible-no-good-very-bad-day-at-slack/), [Atlassian's review of April 2022](https://www.atlassian.com/engineering/post-incident-review-april-2022-outage), [Roblox's "Return to Service"](https://about.roblox.com/newsroom/2022/01/roblox-return-to-service-10-28-10-31-2021), [AWS's S3 summary](https://aws.amazon.com/message/41926/), [Google's SRE book, "Monitoring Distributed Systems"](https://sre.google/sre-book/monitoring-distributed-systems/), and [Google's SRE workbook, "Alerting on SLOs"](https://sre.google/workbook/alerting-on-slos/)._

## The question

A quiet dashboard means no signal reached you. It doesn't mean nothing failed. What can fail here without any signal noticing, and what happens if the thing that tells you is broken too?

## Five public cases

**GitLab: the failure notice never arrived.** On January 31, 2017, GitLab accidentally removed data from its primary database, and looked for its backups.

- "When we went to look for the pg_dump backups we found out they were not there." pg_dump is PostgreSQL's backup tool. The S3 bucket (Amazon's storage service) holding them was empty.
- Notifications for failed cron jobs went by email, and the receiving server rejected those emails. "This means we were never aware of the backups failing, until it was too late."
- The sender had "no other means to report any errors". Nobody was responsible for testing the procedure: "there was no ownership".

**Slack: the alert existed and didn't work.** In the hours before its outage of May 12, 2020, a program that updated load balancers had been failing, and their list of servers had grown stale.

- "We had alerting in place for this precise situation, but unfortunately, it wasn't working as intended."
- The broken monitoring hadn't been noticed "partly because this system 'just worked' for a long time". With a low rate of change, fewer engineers were interacting with the monitoring and alerting.

**Atlassian: the action looked normal.** In April 2022, a script deleted 883 sites, starting at 07:38 UTC on April 5.

- The first support ticket came from a customer at 07:46.
- "Our internal monitoring did not detect an issue because the sites were deleted via a standard workflow."

**Roblox: the monitor relied on the thing that failed.** Its outage, starting October 28, 2021, lasted 73 hours. It involved Consul, which its services rely on to find one another.

- "Critical monitoring systems that would have provided better visibility into the cause of the outage relied on affected systems, such as Consul."
- It says this, with the difficulty of the diagnosis, "severely hampered the triage process" (triage: the first diagnosis).
- It reports the fix as done: "Our telemetry systems no longer depend on the systems that they are configured to monitor."

**AWS: the status tool relied on the thing that failed.** On February 28, 2017, at 9:37AM PST, a command with a wrong input removed more S3 servers than intended, in one region.

- Until 11:37AM PST, AWS was "unable to update the individual services' status" on its Service Health Dashboard, "because of a dependency the SHD administration console has on Amazon S3".
- It used Twitter and banner text on the dashboard instead, and changed the console to run across multiple regions.
- The summary says the dashboard "provides important visibility to our customers". It doesn't mention AWS's monitoring.

## What the sources say about each signal

- **Black-box monitoring,** testing what's visible from outside as a user would. The book says it's "fairly useless" for problems that haven't happened yet.
- **White-box monitoring,** using metrics from inside the system. The book says it can detect imminent problems and failures masked by retries. It depends on being able to inspect the system.
- **Errors at the load balancer.** The book says they can catch completely failed requests, "while only end-to-end system tests can detect that you're serving the wrong content."
- **Averages.** The book warns about the mean: at an average of 100 ms, "1% of requests might easily take 5 seconds".
- **Artificial traffic.** The workbook says you can synthesize "only a small portion" of request types, and that "if an issue affects real users but doesn't affect artificial traffic, the successful artificial requests hide the real user signal".

The book also says the path "through a page to a human" should be kept simple and understood by everyone on the team.

## Reading the cases

The rest of this lesson is its own reading and method. None of these sources says a working signal would have prevented its event, so this lesson doesn't either.

- **A signal is more than its measurement.** It's the measurement, the rule, the delivery and the person. GitLab's job did send its failure notice. The break came on the way to a person.
- **A broken alert looks like a healthy system.** At GitLab and at Slack, the quiet said nothing about health, until something else showed the problem.
- **Normal isn't the same as correct.** At Atlassian, the deletions went through a standard workflow, and a customer reported first. Signals about errors can miss an allowed action doing the wrong thing.
- **White-box monitoring sees only what's instrumented.** That's this lesson's reading of the book's point that it depends on being able to inspect the system.
- **The strongest case for "the monitor depends on what it monitors" is Roblox.** It's about diagnosis, not detection: the post doesn't say an alert failed to fire. AWS shows the same kind of dependency in a status tool, not a monitor.

## How to do it

1. List the few things users need to do. Include things needed only rarely, such as a restore.
2. For each one, list the signals: what each measures, where, and what it can't see.
3. Follow each alert to a person. Who receives it, through what, and how would you know if that broke?
4. Ask what each monitor needs in order to run and to reach you. Does it share a failure with what it watches?
5. Ask what a wrong result looks like when nothing returns an error.
6. For a signal that fires rarely, test it from start to person. Check the outcome too, not only whether an error was reported.
7. Rank the gaps by how many people they could reach and how long they could stay hidden. Give each gap an owner.

## Worked example

For GitLab's backups, an example written for this lesson. The first three lines come from the post. The rest is this lesson's own.

- **Need:** restore the database from a recent backup.
- **Signal that existed:** an email when a cron job failed.
- **Where it broke:** the receiving server rejected the email.
- **What this signal can't see:** a job that never starts sends no error, and a backup that finishes can still fail to restore.
- **A check that doesn't wait for an error:** the age of the newest backup, checked from outside the job, alerting when it's too old.
- **A check of the outcome:** restore a backup on a schedule, and check the result.
- **Owner:** one named person. The post's own list includes "Assign an owner for data durability".

_If you use rbadillap/sre: `find-blind-spots` checks each user action against a table of patterns, ranks the gaps, proposes a signal or check for each gap that matters, and changes nothing except its result file. It has a pattern for a monitor that fails with what it watches. Its "Alert routing" pattern covers ownership metadata, not delivery failing, as at GitLab; check delivery yourself._

## In one sentence

"For each thing users need, I ask what can fail without any signal noticing, and whether the alert could actually reach a person when it does."

## Exercise

A hypothetical case: a team runs a billing job every night at 02:00 UTC. This is what you know:

- When the job exits with an error, it sends a message to a chat channel. That chat service is run by the same team, on the same cluster as the job.
- A dashboard shows the job's run time. It alerts nobody.
- The job exits 0 when it finds no invoices to process.
- The last time anyone saw a failure message was eleven months ago.
- Customers normally get about 500 invoices each night. Last night the job exited 0 and processed none.
- Invoices must reach customers by 09:00 UTC.

1. Did any signal alert someone last night? Does that tell you the job worked?
2. Name three failures these signals can't see. Use only the facts above.
3. What happens to the failure message if the cluster is down?
4. Propose one check that sees the outcome, and one way to learn that the message path is broken. Say where each one runs, and if it pages or opens a ticket, as in [Symptoms, not causes](01-symptoms-not-causes.md).
5. Without more facts, what can't you conclude about last night?
6. Pick one alert in your own work, or one you can imagine for a service you use. Write its path to a person, step by step. Which step could break without anyone noticing? When did someone last see it fire?

---

_Written with an AI assistant from the sources above._

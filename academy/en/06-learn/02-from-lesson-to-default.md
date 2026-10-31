---
title: "From lesson to default"
stage: learn
order: 2
status: approved
teaches: "Turn a postmortem lesson into a default, a check or an alert instead of a reminder, and say what it can't stop and how you'd know it works."
sources:
  - title: "AWS, Summary of the Amazon S3 service disruption in the Northern Virginia (US-EAST-1) region"
    url: https://aws.amazon.com/message/41926/
  - title: "GitLab, Postmortem of database outage of January 31"
    url: https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
  - title: "Cloudflare, Code Orange: Fail Small is complete"
    url: https://blog.cloudflare.com/code-orange-fail-small-complete/
skills: [paved-road]
version: "0.1.1"
---

# From lesson to default

_Sources: [AWS's summary of the S3 disruption of February 28, 2017](https://aws.amazon.com/message/41926/), [GitLab's postmortem of January 31, 2017](https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/), and [Cloudflare's "Code Orange: Fail Small is complete"](https://blog.cloudflare.com/code-orange-fail-small-complete/)._

## The question

A postmortem ends with a list of actions. Some ask people to remember something. Others change what happens when nobody remembers. How do you write the second kind?

Here, a **default** means what a system or tool does unless someone changes it. A **reminder** means anything that only works if a person recalls it at the right moment, such as a note in a document.

## What AWS changed

All times are PST, on February 28, 2017, as in the summary.

- **9:37 AM:** while debugging a billing problem, "an authorized S3 team member using an established playbook" ran a command to remove a small number of servers. One input was entered incorrectly, and more servers were removed than intended.
- **The effect:** two subsystems needed a full restart, and S3 couldn't serve requests while they restarted. S3 was operating normally at 1:54 PM.

What the summary says about the tool: it "allowed too much capacity to be removed too quickly." Then, what AWS says it changed:

- **Done:** "We have modified this tool to remove capacity more slowly and added safeguards to prevent capacity from being removed when it will take any subsystem below its minimum required capacity level."
- **Its claim:** "This will prevent an incorrect input from triggering a similar event in the future." The summary shows no test of this.
- **In progress:** "We are also auditing our other operational tools to ensure we have similar safety checks."
- **Done:** the Service Health Dashboard's admin console, which depended on S3, now runs across multiple regions.

AWS doesn't use the words "default" or "reminder".

## What GitLab listed

On January 31, 2017, an engineer wiped a database directory, "errantly thinking they were doing so on the secondary". It ran on the primary. [Postmortems](01-postmortems.md) covers this incident. Sorted here by what the post says about each change:

- **Reported as done:** "LVM snapshots are now taken every hour instead of once per 24 hours."
- **Started:** a public backup dashboard, with `pg_dump` data only so far.
- **Listed as work in progress:** Prometheus monitoring for backups, automated testing of restores, clearer host prompts, better replication runbooks, and assigning "an owner for data durability".
- **Not what it chose:** it says it's focusing on recovery and on showing which host you're on, "instead of preventing production engineers from running certain commands." Its example: aliasing `rm` to something safer protects against that one command, "not against disk corruption or any of the many other ways you can lose data."

The post's list of issues includes the hourly snapshots. For the rest, it doesn't say which were finished, and it links a status issue (#1684).

## What Cloudflare says

Cloudflare's May 2026 post describes changes after its outages of November and December 2025. It calls them complete, and these are its own claims:

- Snapstone, a new internal component, provides "a unified way to bring progressive rollout, real-time health monitoring, and automated rollback to configuration deployments by default." Before it, this "wasn't consistently applied across the network."
- Its limits: teams "create these configuration units on demand", and the post's summary of the change begins "In most cases".
- On written rules: "Rules without enforcement are suggestions."

[Closing the loop](04-closing-the-loop.md) follows this case further.

## Reading the cases

The rest of this lesson is its own reading and method.

- **As AWS describes it, the limit doesn't depend on typing correctly.** A wrong input can still happen. The summary doesn't say whether anyone can override it.
- **More documentation isn't obviously the answer here.** The person already had an established playbook. The summary doesn't say what a better one would have done, and neither does this lesson.
- **GitLab's hourly snapshot changes how much a deletion can cost, without stopping the deletion.** The post doesn't say how it's scheduled; the daily one ran automatically. GitLab chose to reduce the cost of many mistakes over blocking one command. AWS says it added safeguards that prevent an action. Both are changes to the system. Which fits depends on what you're protecting against.
- **Not every change blocks.** GitLab's backup monitoring, if finished and if it alerts someone, would be an alert. It wouldn't stop a job from failing.
- **A default can have an edge.** As this lesson reads Cloudflare's post, "by default" covers the configuration teams bring into Snapstone. When you build a default, say what's outside it.
- **The gap in the evidence.** None of these sources tries a reminder, watches it fail, and then compares it with a default. They show what companies changed, and what they say about it. "Prefer a default" is this lesson's own rule, not a finding from these cases.

## How to do it

This order is the lesson's own. No source here states it.

1. Write the lesson as one sentence about the system, not about a person.
2. Check that it's worth building. A one-off correction with no pattern behind it doesn't need a default.
3. Ask where it can live so nobody has to remember it, in this order:
   1. A default in a shared module, template or configuration.
   2. A check in the pipeline that fails before production.
   3. A template field that asks the missed question.
   4. An alert that sees what nobody saw.
   5. A document, only if none of these fits.
4. If it's a limit, have the tool check it when it runs, and refuse what breaks it. "Are you sure?" isn't a limit. Decide how a real exception gets through, such as a second person or a separate, logged path. A flag anyone can type isn't a limit.
5. Make the safe way the cheaper way. If it takes more steps, people may go around it.
6. Give it an owner role and a test that shows it works.
7. Write what it doesn't stop.
8. If an earlier incident already produced an action for this, the new one is a default or a blocking check, not another document.

## Worked example

An example written for this lesson, from AWS's case. AWS publishes no rate or minimum. The reminder, the 5%, the owner and the test are invented.

- **Reminder version:** "Double-check inputs before removing capacity."
- **Lesson:** the removal tool accepts a request that takes a subsystem below its minimum.
- **Where it lives:** in the tool, as a limit it checks when it runs. That's first on the list: a default every run goes through. Second would be a pipeline check, but this command doesn't go through a pipeline in this example.
- **The rule:** refuse any removal that leaves a subsystem below its minimum, and remove at most 5% of servers per minute.
- **Owner role:** the team that owns the tool.
- **Test:** in a test environment, ask the tool to remove too many servers, and confirm that it refuses and removes nothing. Then ask for a large allowed removal, and confirm that it goes no faster than the rate.
- **What it doesn't stop:** a removal that stays above the minimum but still targets the wrong servers.

_If you use rbadillap/sre: `paved-road` gives this same order of places, asks for an owner, and moves a lesson that comes back up the list. When limits can be checked, it has the tool refuse what breaks them, so weigh GitLab's different choice yourself. It doesn't ask how to check that the change works, or what it won't stop._

## In one sentence

"A lesson that depends on someone remembering it isn't finished, so I look for where it can live as a default, a check or an alert, and I write what it still won't stop."

## Exercise

A hypothetical case. A cleanup script deletes customer records older than a date passed with `--before`. It has no limit on how many rows it deletes. It's run by hand, once a month, and a normal run deletes fewer than 500 rows. Last month an operator typed the wrong year, and it deleted 40,000 rows. A restore from the last backup recovered them after 3 hours. The postmortem's action says: "Remind operators to double-check the date."

1. Why is that action a reminder?
2. Rewrite it as a limit the tool checks. Choose a number from the facts above, and say why.
3. Say what happens when someone needs a real run above that number.
4. Give it an owner role and a test. What wouldn't it stop?
5. A different case: a one-time migration, already finished and not to be repeated, had a typo in it. Would you build a default? Why?
6. Find one follow-up action in your own team that's a reminder. Where could it live instead?

---

_Written with an AI assistant from the sources above._

---
title: "Live migrations"
stage: design
order: 3
status: approved
teaches: "Split a change to stored data into steps that keep every running version working: add the new form, copy the old data in small pieces, compare the two, move reads and then writes, and remove the old form last."
sources:
  - title: "Stripe, Online migrations at scale"
    url: https://stripe.com/blog/online-migrations
  - title: "GitHub, gh-ost: GitHub's online schema migration tool for MySQL"
    url: https://github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/
  - title: "Danilo Sato on martinfowler.com, Parallel Change"
    url: https://martinfowler.com/bliki/ParallelChange.html
skills: [plan-migration]
version: "0.1.1"
---

# Live migrations

_Sources: [Stripe's "Online migrations at scale"](https://stripe.com/blog/online-migrations), [GitHub's post on gh-ost](https://github.blog/news-insights/company-news/gh-ost-github-s-online-migration-tool-for-mysql/), and ["Parallel Change" on martinfowler.com](https://martinfowler.com/bliki/ParallelChange.html)._

## The question

You need to change how live data is stored, and you can't stop the service to do it. How do you split the change so no step breaks what's running, and how do you know each step worked?

## What Stripe did

Stripe's post, from February 2, 2017, describes one large migration of its "hundreds of millions of Subscriptions objects". Subscriptions were stored inside Customer records. Any change to a customer's subscriptions meant "updating the entire Customer record", so Stripe decided to move them to their own table.

The post gives three reasons this was hard:

- **Scale.** Its illustration, not a measurement: at one second per object, one at a time, one hundred million objects would take over three years.
- **Uptime.** "we couldn't simply pause the Subscriptions service during migrations".
- **Accuracy.** If it changed thousands of lines of code at once, "we would almost certainly overlook some edge cases".

It then follows four parts, which it calls a common pattern:

1. **Dual writing.** It created the new table, and new writes went to both tables. To limit the performance risk, it describes slowly raising the percentage of objects duplicated while watching operational metrics. Existing subscriptions were copied whenever they were updated. A backfill, a job that copies the remaining old data, did the rest.
2. **Changing reads.** It used Scientist, a GitHub library, to read from both tables, compare the results, and alert engineers if they differed. "After we verified that everything matched up, we started reading from the new table."
3. **Changing writes.** It reversed the order: write to the new table, then archive in the old one. It split the code into small units, and made the old field raise an error if any code still called it. The post's opening list says this phase is "to only write to the new table". Its detailed section still archives to the old one until part 4, and this lesson follows that section.
4. **Removing old data.** Once no code relied on the old field, it stopped writing it. It emptied the old array each time a subscription was loaded, then ran a final job for what remained.

How it did the backfill:

- It says the most expensive part is finding the objects to migrate. It ran that search on database snapshots in its Hadoop cluster, "an offline process that had no impact on our production databases".
- A job listed the subscription IDs to copy. A fleet of parallel processes copied them. The job then ran again to check that none were missing.

What the post doesn't give: how long it took, a count of mismatches, an availability figure, or a way back at any step.

## What GitHub published

GitHub's post, from August 1, 2016, announces gh-ost, a tool for changing MySQL tables. gh-ost builds a new copy of the table, called the ghost table. It reads later changes from the binary log, the database's record of its writes, and then swaps the tables.

- **What it reports going wrong with older tools,** which use triggers, code the database runs on each row change: "We have experienced near or complete lock downs in production, to the effect of rendering the table or the entire database inaccessible due to lock contention."
- **Pausing.** When throttled, gh-ost suspends row copying and row updates on the primary database, apart from small heartbeat writes. A load threshold, replication lag or a command can trigger this.
- **Testing.** GitHub keeps designated production replicas, database copies that serve no traffic, for test migrations. These don't really change the table's structure (`engine=innodb`). "We take complete checksum of entire table data from both the original table and ghost table and expect them to be identical."

## The name for the pattern

The article on martinfowler.com writes: "Parallel change, also known as expand and contract". It breaks a change into three phases. Expand supports "both the old and the new" versions. Migrate moves all users of the old version to the new one. Contract removes the old version. It says "Most database refactorings follow the parallel change pattern". It warns: "If the contract phase is not executed you might end up in a worse state than you started".

## Reading the cases

The rest of this lesson is its own reading and method. No source here compares a migration done this way with one that wasn't, so this lesson doesn't claim the pattern prevents failures. GitHub's lockdowns are about trigger-based tools, not about Stripe's method. gh-ost works from the binary log, while Stripe changed application code.

- **Stripe's parts fit expand and contract.** Stripe doesn't use the name. This lesson maps the new table and dual writes to expand, the copy and parts 2 and 3 to migrate, and part 4 to contract.
- **The two forms stay consistent until part 4.** During part 3, Stripe says the tables "need to stay consistent with each other at every step", and the old table kept receiving writes until part 4. That makes going back possible in principle, but Stripe doesn't describe doing it.
- **Copying is work with its own load.** Stripe calls a large migration "a lot of work for our production database", and moved the search for objects off production. GitHub's post stresses being able to pause.
- **Batches are this lesson's rule.** No source here recommends them. A load limit needs a place to stop, and a crash loses little.

## How to do it

1. List who reads and writes the data, including versions that run together during a deploy or a rollback.
2. Expand: add the new form and remove nothing. Have the new version write both. If the extra write could hurt, raise the percentage slowly.
3. Copy the old data as its own step, separate from any deploy. Don't start until every running version writes both. Use small batches, with a load limit that pauses the copy. It must be safe to run twice, as [Work that runs twice](04-work-that-runs-twice.md) explains, and it must never overwrite a newer write with older data.
4. Check that nothing is missing, then compare live reads from both forms. Move reads only when they match and every running version writes both.
5. Move writes: new form first, old form second.
6. Make any remaining use of the old form loud, with an error or an alert. An error breaks any path you missed, so choose knowing that.
7. Contract, last. Removing data can't be undone by a rollback, as [State is special](02-state-is-special.md) explains. Then finish it: a half-done contract leaves two forms to maintain.

For each step, write how you check it and how you go back.

## Worked example

An example written for this lesson, using only Stripe's facts.

- **Expand:** new Subscriptions table, new writes to both, percentage raised slowly, which the post describes as a way to limit the risk. **Check:** operational metrics.
- **Copy:** copy on update, then a backfill from a list of IDs. **Check:** the job runs again to confirm nothing is missing.
- **Reads:** read both and alert on differences. **Check:** results match, then reads move.
- **Writes:** new table first, old one second, in small units. **Check:** more comparisons, and an error if the old field is called.
- **Contract:** stop writing the old field, empty it on load, run a final job. **Check:** no code relies on the old field, and the final job finds what remains.
- **Way back, each step:** not stated in the post, so this record stays blank.

_If you use rbadillap/sre: `plan-migration` writes a plan with each step's release, effect on users, way back and check, and makes steps that can't be undone decisions for a person. It runs nothing._

## In one sentence

"I change live data in steps: add the new form, copy in small pieces that can stop, compare the two, move reads and then writes, and remove the old form last."

## Exercise

A hypothetical case: an `orders` table has 30 million rows, each with its delivery address in an `address` column. You want addresses in a new `addresses` table. Today's version reads and writes only `orders.address`. Deploys are rolling, so two versions run together for about 20 minutes. Assume the copy handles 1,000 rows per batch, and the database stays healthy at one batch per second.

1. Put these in order, and say why: remove the column; add the table; move writes; move reads; write to both; copy existing rows. Why can't the copy start while the version that writes both is still rolling out?
2. How long does the copy take?
3. The copy reads a row's address at 10:00:00. A customer changes that address at 10:00:01, and it's written to both places. The copy writes the old value at 10:00:02. What's wrong now, and what rule in the copy stops it?
4. You compare 1,000,000 live reads and find 40 differences. Do you move reads? What do you do next?
5. Why must the column stay until no version you might roll back to reads it?
6. Pick a stored structure in a system you work on or use. Who reads and writes it? Write your first step for changing it, and how you'd check that step.

---

_Written with an AI assistant from the sources above._

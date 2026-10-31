---
title: "Burn rate"
stage: observe
order: 2
status: approved
teaches: "Work out burn rates and thresholds from an SLO, read a page or ticket rule with a long and a short window, and choose what to do when low traffic makes one failure look large."
sources:
  - title: "Zalando Engineering, Operation-Based SLOs"
    url: https://engineering.zalando.com/posts/2022/04/operation-based-slos.html
  - title: "Google SRE workbook, Alerting on SLOs"
    url: https://sre.google/workbook/alerting-on-slos/
skills: [design-alerts]
version: "0.1.1"
---

# Burn rate

_Sources: [Zalando's "Operation-Based SLOs"](https://engineering.zalando.com/posts/2022/04/operation-based-slos.html) and [Google's SRE workbook, "Alerting on SLOs"](https://sre.google/workbook/alerting-on-slos/)._

## The question

An [error budget](../01-define/01-what-working-means.md) is the failure an SLO allows. How do you page when it's going fast, open a ticket when it's going slowly, and stay quiet for a short spike? And what changes when a service gets few requests?

## What happened at Zalando

Zalando had moved to alerts on customer actions, as told in [Symptoms, not causes](01-symptoms-not-causes.md). Those alerts first fired when the error rate breached the SLO.

- **The problem.** It "started getting reports that the alerts were too sensitive". There were "multiple occasions of short lived error spikes that resulted in pages to on-call responders".
- **The workaround.** Engineers added complex rules "on a trial and error basis (usually using time of day, throughput, duration of the error condition)".
- **The change.** Its alert handler moved to the "Multi Window Multi Burn Rate strategy". A page now depended on how fast the error budget was burning.
- **What it reports.** This "prevented on-call responders from being paged by short lived error spikes", and "we could pick up on slowly burning error conditions".

The post gives no burn rates, and no numbers for this change alone. It doesn't discuss low traffic.

## What the workbook says

**Burn rate** is "how fast, relative to the SLO, the service consumes the error budget". At a burn rate of 1, the budget reaches exactly 0 at the end of the SLO's window. For a 99.9% SLO over 30 days, the workbook's table gives:

| Burn rate | Error rate | Time to use the budget |
|---|---|---|
| 1 | 0.1% | 30 days |
| 2 | 0.2% | 15 days |
| 10 | 1% | 3 days |
| 1,000 | 100% | 43 minutes |

Budget consumed is the burn rate multiplied by the alert window, divided by the period.

**Why one long window fails, in its example.** With a 36-hour window, the alert keeps firing for 36 hours after a total outage.

**What it recommends as a starting point,** for a 99.9% SLO:

| Severity | Long window | Short window | Burn rate | Budget consumed |
|---|---|---|---|---|
| Page | 1 hour | 5 minutes | 14.4 | 2% |
| Page | 6 hours | 30 minutes | 6 | 5% |
| Ticket | 3 days | 6 hours | 1 | 10% |

- **Two windows.** The alert fires only when both are over the threshold. The short window checks that the budget is still being spent. Its guideline: "make the short window 1/12 the duration of the long window".
- **Page or ticket.** "If an issue will exhaust the error budget within hours or a few days, sending an active notification is appropriate." Otherwise, a ticket for the next working day is more appropriate.
- **A difference inside the chapter.** Its example configuration adds a ticket rule the table omits: burn rate 3, over 24 and 2 hours.
- **A loose target.** At 90%, the 2% page "could never fire", since a full outage uses only 1.4% of the budget in an hour.

## Low traffic, and a number that doesn't match

The workbook's example is a system with 10 requests per hour:

"a single failed request results in an hourly error rate of 10%. For a 99.9% SLO, this request constitutes a 1,000x burn rate and would page immediately, as it consumed 13.9% of the 30-day error budget."

The 1,000x doesn't match the rest of the chapter.

- Burn rate is the error rate divided by the allowed rate. 10% divided by 0.1% is **100x**.
- The chapter's own table gives 1,000x as a 100% error rate.
- Its 13.9% agrees with 100x: 100 × 1 hour ÷ 720 hours is 13.9%. An hour at 1,000x would be 139%.

This lesson reads that example as 100x. Either way it pages: 100 is far above the 14.4 in the first row.

Its options for low traffic, and the limits it gives, where it gives one:

- **Generate artificial traffic.** You can synthesize "only a small portion" of request types, and if real users are affected but test requests aren't, "the successful artificial requests hide the real user signal".
- **Combine related services into one group.** One service failing completely "may not count as a significant event".
- **Change the product,** so one failure costs less: retries, or a path that saves the request to run later.
- **Lower the SLO, or use a longer alerting window.** Lowering the SLO "involves a product decision". That section gives no limit for the longer window; the chapter's 36-hour example shows one, the long reset time.

If every failed request is worth investigating, it says "the alerting system notifies you of an error too late."

## Reading the cases

The rest of this lesson is its own reading and method.

- **A 100% rate can appear in a short window.** If that failed request is the only one in the last 5 minutes, the 5-minute rate is 100%, which is 1,000x for that window. The workbook doesn't say that's where its number comes from, and it says "hourly". Always say which window a burn rate belongs to.
- **No numbers to copy.** Zalando gives no values, and neither source shows a real low-traffic service.
- **At low volume, one event moves the rate a lot.** That's this lesson's reading. Unless you can add volume, ask what one failure costs users, as in [Error budgets for rare events](../01-define/02-error-budgets-for-rare-events.md).

## How to do it

1. Write the SLO, the window and the allowed failure rate.
2. Start from the workbook's table. Multiply each burn rate by the allowed rate to get the error rate threshold.
3. Check that each threshold can be reached. Above 100%, the row can't fire.
4. Fire only when both windows are over the threshold, and suppress overlapping alerts.
5. Count the events in each short window. If there are few, choose a low-traffic option and write its limit. The workbook gives no minimum, so set your own.
6. Replay a past incident. Would it have paged, and when?

## Worked example

An example written for this lesson, with invented numbers: a 99.9% SLO over 30 days, and the table above. The thresholds are 1.44%, 0.6% and 0.1%. Traffic is steady, and each case assumes no other errors.

| What happens | Burn rate | What fires |
|---|---|---|
| 10% errors for 5 minutes, then none | 100 for those 5 minutes | Nothing. The 1-hour average peaks near 0.83%, under 1.44%. It used about 1.2% of the budget. |
| 2% errors, sustained | 20 | A page after about 43 minutes, when the 1-hour average passes 1.44%. It has used 2% of the budget. |
| 0.3% errors, sustained | 3 | A ticket after 24 hours, when the 3-day average passes 0.1%. It has used 10% of the budget, and the rest lasts 9 more days at that rate. |

_If you use rbadillap/sre: `design-alerts` gets the three threshold rows from `burn-rate.py` and warns when a short window holds under 100 events. That number is the script's own. It suggests alerting on counts or on every failure, which isn't among the workbook's options._

## In one sentence

"I page when the budget is burning fast over a long window and is still burning in a short one, and with few requests I ask what one failure costs."

## Exercise

A hypothetical case: a service with a 99.5% SLO over 30 days (720 hours), using the burn rates and windows from the workbook's table. Traffic is steady, and each scenario starts with no earlier errors.

1. What's the allowed failure rate? What's the error rate threshold for each of the three rows?
2. The error rate becomes 8% and stays there. What's the burn rate? Which row fires first, and after how long? How much budget has been used by then? How long until the budget is gone?
3. The error rate becomes 1% and stays there. Does a page fire? What fires, after how long, and how much budget has been used by then?
4. A different service, same SLO, gets 6 requests per hour, evenly. One request fails, and it's the only request in the last 5 minutes. What's the burn rate over the last hour, and over the last 5 minutes? Does the first row fire? What share of the 30-day budget did that one failure use?
5. For that service, choose two of these options: artificial traffic, combining services, lowering the SLO, a longer alerting window. Name one limit of each.
6. Pick a service you know or use. Say what its SLO is, or propose one. Work out the three thresholds, and estimate its requests in 5 minutes. Would you trust a burn rate alert there? If not, what would you do?

---

_Written with an AI assistant from the sources above._

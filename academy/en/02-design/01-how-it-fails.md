---
title: "How it fails"
stage: design
order: 1
status: approved
teaches: "For each dependency, write what users see when it's slow, when it's down and when it comes back, and give each health check one question it can answer."
sources:
  - title: "AWS, Summary of the Amazon S3 service disruption in the Northern Virginia (US-EAST-1) region"
    url: https://aws.amazon.com/message/41926/
  - title: "AWS, Summary of the Amazon DynamoDB service disruption in the Northern Virginia (US-EAST-1) region"
    url: https://aws.amazon.com/message/101925/
  - title: "AWS Builder Center, Implementing health checks"
    url: https://builder.aws.com/content/3Ev53O39izHCtWLzp4XU6t8PC1O/implementing-health-checks
  - title: "Kubernetes documentation, Liveness, Readiness, and Startup Probes"
    url: https://kubernetes.io/docs/concepts/workloads/pods/probes/
skills: [review-design]
version: "0.1.1"
---

# How it fails

_Sources: [AWS's summary of the S3 disruption of February 28, 2017](https://aws.amazon.com/message/41926/), [AWS's summary of the disruption of October 19 and 20, 2025](https://aws.amazon.com/message/101925/), [the AWS Builder Center article "Implementing health checks"](https://builder.aws.com/content/3Ev53O39izHCtWLzp4XU6t8PC1O/implementing-health-checks), and [Kubernetes' page on probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/)._

## The question

A system depends on other systems. When one of them is slow, down or coming back, what do its users see, and do its health checks test what matters?

## What happened to S3 in 2017

All times are PST, on February 28, 2017.

- **9:37 AM:** a command with an input entered incorrectly removed more servers than intended. They supported two subsystems: index, which every GET, LIST, PUT and DELETE request needs, and placement, which allocates storage for new objects and needs index.
- **Down:** both needed a full restart, and S3 couldn't serve requests during it. Services that rely on S3 were also affected, including new EC2 instance launches and Lambda.
- **A dependency in the response tools:** until 11:37 AM, AWS couldn't update individual services' status on its Service Health Dashboard, "because of a dependency the SHD administration console has on Amazon S3".
- **Coming back:** "we have not completely restarted the index subsystem or the placement subsystem in our larger regions for many years." The restart and its safety checks "took longer than expected". S3 was operating normally at 1:54 PM.

## What happened at AWS in 2025

All times are PDT, on October 19 and 20, 2025.

- **Down:** at 11:48 PM, a race condition (a timing bug) left an empty DNS record for DynamoDB's regional endpoint. Systems using that endpoint couldn't connect. A system called DWFM manages the physical servers behind EC2 instances, and keeps a lease on each one. Its state checks depend on DynamoDB. They failed, and leases slowly timed out. Running EC2 instances weren't affected.
- **Coming back:** DynamoDB's DNS information was restored by 2:25 AM. DWFM then tried to re-establish leases, but there were so many that the work timed out before finishing, and more work was queued. AWS says DWFM "had entered a state of congestive collapse and was unable to make forward progress". The situation "had no established operational recovery procedure". At 4:14 AM, engineers throttled incoming work and began restarting some DWFM hosts. By 5:28 AM, all leases were back. A server without a lease can't host new launches, so launches failed with "insufficient capacity" errors.
- **Slow:** Network Manager, which gives new instances their network configuration, then had a large backlog. From 6:21 AM its propagation times increased. New instances could launch, but without the connectivity they needed.
- **The health check:** from 5:30 AM, connection errors rose on some load balancers. The health checking subsystem of Network Load Balancer (NLB) brought new instances into service before their network state had propagated. AWS says "in some cases health checks would fail even though the underlying NLB node and backend targets were healthy." Results alternated, so nodes and targets left DNS and came back. That added load, the health check subsystem degraded, and automatic DNS failover between Availability Zones was triggered, which took capacity out of service. At 9:36 AM, engineers disabled automatic failover.

The summary disagrees with itself on new launches: they began to succeed from 10:37 AM (opening) or by 5:28 AM (EC2 section), and were "operating normally" by 10:36 AM or at 1:50 PM, with recovery starting at 12:01 PM.

## What the health check guidance says

- **Three checks, three purposes (Kubernetes).** Startup probes verify whether the application has started. Liveness probes "determine when to restart a container". Readiness probes "determine when a container is ready to accept traffic". Kubernetes warns: "Incorrect implementation of liveness probes can lead to cascading failures."
- **Dependencies in a check (Amazon).** "Without fail-open protection, implementing a health check that tests a dependency turns that dependency into a "hard dependency."" If it's down, the service goes down too. Fail open means that when all servers fail their checks, the load balancer sends traffic to all of them anyway. A slow data store can still make servers "flap in and out of service" without reaching that point.
- **What Amazon's teams tend to do.** They keep fast load balancer checks local, testing only what the server doesn't share with its peers. Centralized systems react carefully to dependency checks, with thresholds.
- **A check can be too shallow (Amazon).** The article's author once wrote a bug that made a web server return blank error pages. Its check was deep enough to see the process responding, "but not deep enough to ensure it was responding correctly."

## Reading the cases

The rest of this lesson is its own reading and method. Neither summary says a design review would have found these problems, so this lesson doesn't claim that.

- **The three states are different failures.** The grouping into slow, down and coming back is this lesson's. In 2025, DNS came back at 2:25 AM and new instance launches kept failing for hours.
- **Coming back has its own failure.** S3's restart hadn't been run in its larger regions for many years. DWFM's situation had no procedure.
- **A health check can be wrong in both directions.** NLB's checks sometimes failed on healthy nodes. The blank-page server's check wasn't deep enough to see it was broken. In both, what was tested differed from what mattered.
- **What these cases don't show.** The slow state here is a configuration delay inside AWS, not a caller waiting on a slow service. No source here shows that case.

## How to do it

1. List every dependency, including what you'd use during an incident, as S3's dashboard shows: status page, deploy tool, recovery steps.
2. For each one, write what users see when it's down.
3. Write what they see when it's slow: how long a caller waits, and what it does then.
4. Write what happens when it comes back: what's queued, what reconnects at once, and whether a full restart has been run at today's size.
5. Mark each dependency as critical, or as one the system can degrade without.
6. Give each health check one question: has it started, can it take work, does it need a restart? Write what acts on a failure.
7. For each check, ask whether it would catch what users see, what it does across the fleet if something shared fails, and how much capacity it can remove at once.

## Worked example

An example written for this lesson. Its facts come from the two summaries; the question is this lesson's.

| Dependency | Slow | Down | Coming back |
|---|---|---|---|
| DWFM on DynamoDB | Not stated | Checks fail, leases time out, running instances unaffected | New launches fail with "insufficient capacity" errors. Work times out, is queued again, no forward progress until throttling and restarts |

Health check, NLB:

- **Question it should answer:** can this node take traffic?
- **What also made it fail:** network state not yet propagated, on a healthy node.
- **What acts on it:** the subsystem that removes nodes from service. When that subsystem degraded, its delays triggered automatic failover.
- **Limit on capacity removed:** none described in the summary. AWS says it's adding one on what an NLB can remove in such a failover.

_If you use rbadillap/sre: `review-design` asks for each dependency's effect when slow, down and recovering, and for health checks that each answer one question._

## In one sentence

"For each dependency I write what users see when it's slow, when it's down and when it comes back, and each health check answers one question without taking down what still works."

## Exercise

A hypothetical case. A shop runs on 10 identical instances. Each can handle 200 requests per second, and normal traffic is 1,500 per second. Placing an order calls a payment provider. Browsing doesn't. Each instance's health check calls the provider with a 1-second timeout. Three failures in a row, 10 seconds apart, restart the instance. A restart takes 2 minutes. Assume each order is one request, slow calls don't reduce capacity, and extra requests wait in a queue.

1. The provider goes fully down at 10:00:00, and every check starts failing then. About when do instances start restarting? What happens to customers who are only browsing?
2. Now the provider isn't down but slow: every call succeeds in 3 seconds, and orders are allowed to wait up to 10 seconds. What does the check do, and what would have happened to orders without it?
3. Assume you've fixed the check. Later, the provider comes back after an outage, all 10 instances are up, and 3,000 orders retry at once on top of normal traffic. How much spare capacity is there per second, and how many seconds does it take to clear the retries?
4. Rewrite the check: what's its one question, and what does it test?
5. Pick a system you work on or use. Name one dependency, and write what users would see when it's slow, down and coming back. Mark anything you don't know as unknown.

---

_Written with an AI assistant from the sources above._

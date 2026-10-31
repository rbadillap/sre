---
title: "A deploy is not a release"
stage: ship
order: 1
status: approved
teaches: "List every path a change can take to production, configuration and content included, and say for each one what checks a change, how many users it reaches at once, and how you get back."
sources:
  - title: "CrowdStrike, Preliminary Post Incident Review"
    url: https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/
  - title: "CrowdStrike, External Technical Root Cause Analysis, Channel File 291"
    url: https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf
  - title: "Microsoft, Helping our customers through the CrowdStrike outage"
    url: https://blogs.microsoft.com/blog/2024/07/20/helping-our-customers-through-the-crowdstrike-outage/
  - title: "Google SRE workbook, Canarying Releases"
    url: https://sre.google/workbook/canarying-releases/
skills: [review-release]
version: "0.1.1"
---

# A deploy is not a release

_Sources: [CrowdStrike's preliminary review](https://www.crowdstrike.com/en-us/blog/falcon-content-update-preliminary-post-incident-report/) and [root cause analysis](https://www.crowdstrike.com/wp-content/uploads/2024/08/Channel-File-291-Incident-Root-Cause-Analysis-08.06.2024.pdf), [Microsoft's post of July 20, 2024](https://blogs.microsoft.com/blog/2024/07/20/helping-our-customers-through-the-crowdstrike-outage/), and [Google's SRE workbook, "Canarying Releases"](https://sre.google/workbook/canarying-releases/)._

## The question

A change can arrive everywhere it was sent and still break things for users. And code isn't the only thing that reaches production. So what counts as a path to production, and what does each path check before users get the change?

## What happened at CrowdStrike

CrowdStrike's Falcon sensor runs on customers' computers, and includes a kernel driver, a program that runs in the core of the operating system. The root cause analysis says CrowdStrike updates the sensor's security content "in two ways".

- **Sensor Content** is built into each sensor release. The review describes automated testing first, then a staged rollout: CrowdStrike's own systems, then early adopters, then everyone. Customers can choose the latest version, or one or two versions older, for parts of their fleet.
- **Rapid Response Content** comes from the cloud, in files called Channel Files. A tool called the Content Validator checks it before it's published. The analysis says: "Rapid Response Content is configuration data; it is not code or a kernel driver."

The review doesn't describe a staged rollout for Rapid Response Content before the incident. It also doesn't say whether customers' version choices applied to it. Its list of what customers control names Sensor Content and Template Types, and omits Rapid Response Content.

The timeline, from the review:

- **February 28, 2024:** sensor 7.11 became generally available, with a new Template Type, a predefined form that content fills in.
- **March 5:** that Template Type passed a stress test, and the first content using it reached production.
- **April 8-24:** three more pieces of content for it were deployed, and they performed as expected.
- **July 19, 04:09 UTC:** two more were deployed. The review gives three reasons: the earlier testing, "trust in the checks performed in the Content Validator", and "previous successful IPC Template Instance deployments".
- **July 19, 05:27 UTC:** the update was reverted. Affected: Windows hosts on sensor 7.11 or later that received it in that window. Mac and Linux hosts weren't.

From the analysis: the Template Type defined 21 input fields, and the sensor code supplied 20. Earlier tests and content used a wildcard, a pattern that matches any value, for the 21st field. The analysis says the mismatch stayed hidden, in part, for that reason. One of the new pieces of content was the first to require the 21st field. The validator passed it. The review calls this "a bug in the Content Validator", and the analysis says the validator expected 21 inputs. On the customer's machine, the sensor tried to read a value that wasn't there, and the system crashed. The analysis calls the crash a "confluence" of three things: the mismatch, a memory read with no bounds check, and no specific test for a non-wildcard 21st field.

What CrowdStrike changed:

- "Each Template Instance should be deployed in a staged rollout." The analysis says the system was updated so that new content passes canary testing, then wider rings, with "bake-in time" after each promotion. A canary is a small first group that gets the change before everyone else. A ring is one group in a growing series.
- "Customers can choose where and when Rapid Response Content updates are deployed." The review listed this as planned. The later analysis describes it as done, with more to come.

The analysis says staged deployment "mitigates impact" when content causes failures. Neither document says how many machines it would have spared in this incident.

Microsoft's post says "We currently estimate" that 8.5 million Windows devices were affected, "less than one percent of all Windows machines". It dates the release to July 18, with no time zone. CrowdStrike says July 19, 04:09 UTC.

## What the workbook says

Google's chapter on canarying gives three points that apply here:

- **Many kinds of change carry risk.** "In Google's experience, a majority of incidents are triggered by binary or configuration pushes".
- **A service changes in more than one way.** It lists "binaries or code, environments such as JVM, kernel/OS, libraries, service config or flags, feature/experiment config, and user config."
- **Success is about customers.** "A successful release is a release made available to customers with no severe defects or SLO violations." An SLO is a reliability target.

## Reading the case

The rest of this lesson is its own reading and method.

The sources don't draw the line in this lesson's title. CrowdStrike uses both "released" and "deployed" for July 19. So these definitions are this lesson's own: a **deploy** is a change arriving where it runs. A **release** is users getting its effect.

- **The update arrived, and the release failed.** The content reached the sensors, and the failure appeared on the customer's machine. The check on the way had a bug, so a tool reporting success told you little.
- **Being configuration doesn't make a change safe.** The source says this content wasn't code. It still crashed systems.
- **Two paths can have very different steps.** The review describes stages for one path, and describes them for the other only as a later change. A review of the sensor release process alone wouldn't have looked at the path that delivered the trigger. The mismatch itself shipped in a sensor release, and those tests missed it too.
- **A good record only covers what it tested.** Four earlier deployments went well, and the review names them as part of the reason to trust the next one. They hadn't used the 21st field.

## How to do it

1. List everything that can change behavior in production. Start with the workbook's list. This lesson adds rules, content, data, and any emergency path.
2. For each path, write five things: who or what starts it, what checks it, how much of the user base it reaches at once, how you'd see it failing, and how you get back.
3. Compare the rows. Find the path with the fewest checks and the widest reach. Decide if that's deliberate, and write why. Some paths need speed, as [Rolling out in steps](02-rolling-out-in-steps.md) shows.
4. Define success by what users get, not by what the tool reports. [What working means](../01-define/01-what-working-means.md) shows how to write that as a number.

## Worked example

An example written for this lesson, using only the sources' facts, as they describe things before the incident, plus the revert:

- **Sensor Content.** Starts with: a sensor release. Checks: automated testing, and certification through Windows Hardware Quality Labs (WHQL). Reach: staged, with customers choosing the version. How you'd see it failing: not stated. Way back: not stated.
- **Rapid Response Content.** Starts with: content from detection engineers. Checks: the Content Validator, and a stress test when the Template Type was new. Reach: the review describes no stages. How you'd see it failing: not stated. Way back: reverting stopped new machines getting it, 78 minutes after release by the times above. It didn't cover machines already crashed: [Device fleets](03-device-fleets.md) covers those.

The blanks are part of the result. An inventory of your own system shouldn't have any.

_If you use rbadillap/sre: `review-release` asks you to name every path one change can take to production, including rules, flags and configuration that arrive through a console or an API, and any emergency path. It writes a review and doesn't deploy. It reviews one change at a time, so the inventory of a whole system in this lesson is yours to keep._

## In one sentence

"A deploy is a change arriving and a release is users getting its effect, so I list every path a change can take, configuration and content included, and for each one, what checks it, how many users it reaches at once, and how I get back."

## Exercise

A hypothetical service with 100,000 active users. It has four paths to production:

- **App code:** a pipeline with review and tests. It reaches 5% of users for the first 30 minutes, then the rest. Way back: redeploy, 10 minutes.
- **Feature flags:** a console, with no review. It reaches all users in 30 seconds. Way back: turn it off, 30 seconds.
- **Pricing rules:** a file edited in an admin tool. The tool checks the file's format, not its values. It reaches all users in 1 minute. Way back: restore the old file by hand.
- **Emergency fix:** a script that skips the tests. It reaches all users in 5 minutes. Nobody has written when it may be used.

An alert fires 5 minutes after a bad change first reaches users.

1. Someone reviews the pipeline and calls releases safe. Which paths did they not review?
2. At 10:00, a pricing rule is saved, and the tool says "published". At 10:01, every checkout shows a price of zero. Using this lesson's words, did the deploy work? Did the release?
3. For each path, how many users have the bad change when the alert fires? Assume it reached its first users the moment it started.
4. Pick the row you'd change first. Propose one change, and say what it costs in speed.
5. List the paths to production of a system you work on or use. Include one that doesn't go through the main pipeline. Fill in the five things from "How to do it", and write "unknown" where you don't know.

---

_Written with an AI assistant from the sources above._

---
title: "Drift"
stage: respond
order: 7
status: approved
teaches: "When infrastructure differs from its code: read the real system, list every difference, sort what's urgent from what's dangerous to apply, and decide which side is right."
sources:
  - title: "CircleCI, CircleCI UI Loading & build triggering issues (postmortem of April 4, 2025)"
    url: https://status.circleci.com/incidents/zh1qd6lrntl7
  - title: "HashiCorp, Manage resource drift"
    url: https://developer.hashicorp.com/terraform/tutorials/state/resource-drift
  - title: "HashiCorp, terraform plan command reference"
    url: https://developer.hashicorp.com/terraform/cli/commands/plan
skills: [reconcile-drift]
version: "0.1.1"
---

# Drift

_Sources: [CircleCI's postmortem of its April 4, 2025 incident](https://status.circleci.com/incidents/zh1qd6lrntl7), and HashiCorp's Terraform documentation: [Manage resource drift](https://developer.hashicorp.com/terraform/tutorials/state/resource-drift) and [the plan command](https://developer.hashicorp.com/terraform/cli/commands/plan)._

## The question

Your code says one thing and the real system says another. That difference is called drift. How do you find it, and how do you make the two match without breaking anything?

## What happened at CircleCI

This isn't the incident in [Security incidents](06-security-incidents.md). All times are UTC, on April 4, 2025. The postmortem was posted on May 2.

CircleCI says it manages its infrastructure "almost entirely with Terraform", a tool that creates and changes infrastructure from configuration files. That includes a web application firewall (WAF), which sits in front of its services and filters traffic.

- **00:16:** a WAF rule began blocking legitimate traffic.
- **00:26 to 00:52:** monitoring showed degraded performance, and customers reported they couldn't reach the UI or start builds. Another, unrelated incident was just ending, and the team spent time checking for a connection. At 00:52, it opened a new incident.
- **01:15:** the investigation had found broad connectivity issues. The team explored recent deployments and infrastructure changes, "but the cause remained unclear".
- **01:35:** automated Terraform drift detection found a difference between the defined and current WAF settings. A rule had been changed outside the standard Terraform process.
- **01:41:** the rule was reverted on the two entry points it affected, the CloudFront distributions for api.circleci.com and circleci.com.
- **01:49 and 01:55:** at 01:49, error rates decreased. At 01:55, full restoration was confirmed.

What the report says about the cause:

- A misconfiguration in IAM controls (who is allowed to do what) "allowed a specific role to make changes without using our infrastructure-as-code tooling".
- While investigating routine security monitoring, an operator changed the WAF configuration by hand, "believing they were taking read-only actions".
- Responders "did not prioritize investigating WAF configuration", expecting any change to have gone through the Terraform pipeline, "and there was no record of such changes".
- It was "nearly 80 minutes" from the change to its detection. Drift detection "identified the exact configuration change" and "led directly to the resolution of the incident".

What it says came next. One listed item is written as done: "We have implemented stricter IAM policies". Faster drift alerts, technical guardrails and monitoring of WAF behavior are written as in progress. Organization-wide restrictions on roles are written as still being investigated. The closing says "several measures" are already implemented, without listing them.

The report isn't fully consistent. It says a rule was "introduced" and also "changed", and that it was "removed" and also "reverted". So it isn't clear whether the rule was new or an existing rule edited. The summary ends the disruption at 01:49, and the timeline confirms full restoration at 01:55.

The report doesn't say how often drift detection runs, how the revert was made, whether anything else had drifted, or whether the code changed.

## What HashiCorp's documentation says

These points are about Terraform in general, not about CircleCI. Terraform keeps a state file, its record of the resources it manages. HashiCorp describes drift as that file being out of sync with the real infrastructure.

- **Why manual changes are risky:** if state and configuration don't match the infrastructure, Terraform "will attempt to reconcile your infrastructure, which may unintentionally destroy or recreate resources".
- **Looking without changing:** the plan command alone "does not actually carry out the proposed changes". `terraform plan -refresh-only` shows the drift, and a refresh-only operation "does not attempt to modify your infrastructure to match your Terraform configuration".
- **A normal plan proposes the revert, and an apply carries it out:** in HashiCorp's tutorial, without that flag, "Terraform would attempt to revert your manual changes". It goes on: "Instead, you will update your configuration".
- **A manual change can be intended:** refresh-only mode can help if you've changed something on purpose outside the usual workflow, "e.g. while responding to an incident", and need Terraform's records to match.

## Reading the case

The rest of this lesson is its own reading and method.

- **The code tells you what was intended, not what's there.** CircleCI's responders expected any change to have gone through the pipeline, and there was no record of such a change. A list of deployments can't show a change made outside them. So read the real system. [Reframe first](01-reframe-first.md) applies: list what else fits, including a change made outside the pipeline.
- **Drift can be the cause of an incident, not only a cleanup job.** That makes a drift check something to run during an incident. The case can't show how much time a more frequent check would have saved.
- **Ask how the change got in.** The one fix listed as done is on the permissions.
- **Neither side is automatically right.** At CircleCI, the rule was reverted. HashiCorp's incident example points the other way: a change made on purpose, where the records have to catch up. HashiCorp's tutorial also updates the configuration, instead of letting a normal plan revert a manual change.
- **Applying isn't a safe default.** HashiCorp's warnings above are the reason. The CircleCI case doesn't show them: nothing in the report says a plan wanted to destroy anything.

## How to do it

1. Ask what else this could be. Drift can be a security incident.
2. List every difference from read-only plans. With Terraform, run `terraform plan -refresh-only` (reality against Terraform's records) and a normal `terraform plan` (reality against the code). Apply nothing yet. If a difference opens access, treat it as a [security incident](06-security-incidents.md).
3. Sort each difference:
   - **Urgent:** it's hurting users now, or it opens access, exposes data or weakens security.
   - **Dangerous to apply:** the plan would destroy or replace something that holds data, or something others depend on.
   - **Ordinary:** no risk either way.
4. Find who changed it, when, and with what tool, from audit logs (the records of who did what). Write "not found" if they don't say. Treat it as a security incident too if it was made by an unknown identity, or by a system's own identity when it shouldn't have run.
5. For each urgent one, change only that rule or permission, under your own named account, and write why. Check what uses it first. Confirm the change worked, as in [Mitigate what can be undone](03-mitigate-what-can-be-undone.md).
6. For each dangerous one, find why the tool wants to destroy it, and fix the code until the plan shows an update or nothing. If a replacement is truly needed, plan it as its own change.
7. Decide for every difference: reality goes into the code, or reality goes back to the code.
8. Close the way in, and shorten the time to find the next one.

## Worked example

For this case, an example written for this lesson, using only the report's facts. The labels are this lesson's own.

- **Difference:** a WAF rule on two CloudFront distributions, blocking legitimate traffic.
- **Sorted as:** urgent, because it was hurting users.
- **Changed by:** an operator, by hand, using a role with a misconfigured permission. The rule began blocking at 00:16.
- **Fix:** rule reverted on both distributions at 01:41. How: not stated.
- **Which side was right:** the code, going by the revert. The report doesn't say it in those words.
- **Way in:** stricter IAM policies, written as done. Faster drift alerts, written as in progress.
- **Other differences:** not stated.

_If you use rbadillap/sre: `reconcile-drift` lists differences, sorts them as urgent, dangerous to apply or ordinary, and writes proposals without ever running an apply. Its urgent group covers access and security, not a difference that's blocking traffic._

## In one sentence

"When code and reality differ, I read the real system, list every difference without applying anything, and decide one by one which side is right."

## Exercise

A hypothetical case. A scheduled read-only plan on your production account reports three differences. Assume the audit logs are complete.

- **A:** a firewall rule now allows the database port from any address on the internet. It was changed last night at 18:00 by the pipeline's own identity, but the pipeline has no run at that time.
- **B:** the plan would replace the `orders` database, because its network setting was changed by hand. The on-call engineer made the change under a named account last week, during an incident, and the incident record says it's correct.
- **C:** a label on a storage bucket differs. A named engineer changed it, and nothing reads that label.

1. Sort each difference as urgent, dangerous to apply or ordinary.
2. Which do you handle first, and why might it not be a drift job at all?
3. For B, which side is right, and what do you change so that the plan stops wanting to replace the database?
4. Why not run an apply now, to make everything match?
5. Pick one resource your team manages as code. Could someone change it by hand today, and how long would it take you to find out?

---

_Written with an AI assistant from the sources above._

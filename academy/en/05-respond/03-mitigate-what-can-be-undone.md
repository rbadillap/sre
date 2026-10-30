---
title: "Mitigate what can be undone"
stage: respond
order: 3
status: draft
teaches: "Reversible first, and second-order effects."
sources:
  - title: "Cloudflare, Details of the Cloudflare outage on July 2, 2019"
    url: https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
skills: [reversible-first]
version:
---

# Mitigate what can be undone

_Source: [Cloudflare's report on the outage of July 2, 2019](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/)._

## The question

During an incident, the goal is to stop the harm first and find the full cause later. The question is: which action stops the harm and can still be undone if it's wrong?

## What Cloudflare did

- At 14:02 UTC, the team proposed turning off the WAF globally.
- At 14:07, it was turned off. By 14:09, traffic and CPU were back to expected levels worldwide.
- The WAF was turned back on globally at 14:52, after the team had confirmed the cause and the fix.
- The response was slowed down because an internal access service was also affected, and some engineers' credentials had expired.

## Why this was a good mitigation

Turning off the WAF stopped the harm in minutes, and it could be undone: the team turned it back on less than an hour later. It also had a cost, since customers ran without that protection for a while. A good mitigation is chosen knowing both: how to undo it, and what it costs while it's on.

Three habits make a mitigation safe:

1. **Write how to undo it before doing it.** If you can't write the undo, it isn't reversible.
2. **Check the second-order effect.** Scaling up an application can make a saturated database worse, because each new instance opens more connections.
3. **Hand irreversible actions to a person.** Deleting, restoring, failing over and migrating data end in a proposal, not an action.

_If you use rbadillap/sre: `reversible-first` is the discipline for this, and `respond-to-alert` asks for each mitigation's undo._

## In one sentence

"I mitigate with something I can undo, written down before I do it, and I check what it does to everything around it."

## Exercise

A database is saturated and the application is timing out. One option is to add more application instances. What could that do to the database, and what reversible option would you try first?

---

_Written with an AI assistant from the source above._

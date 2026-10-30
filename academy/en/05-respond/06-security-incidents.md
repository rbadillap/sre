---
title: "Security incidents"
stage: respond
order: 6
status: draft
teaches: "Preserve evidence, revoke, rotate."
sources:
  - title: "CircleCI, CircleCI incident report for January 4, 2023 security incident"
    url: https://circleci.com/blog/jan-4-2023-incident-report/
  - title: "NIST SP 800-61 Rev. 2, Computer Security Incident Handling Guide"
    url: https://csrc.nist.gov/pubs/sp/800/61/r2/final
skills: [contain-security-incident]
version:
---

# Security incidents

_Sources: [CircleCI's incident report of January 4, 2023](https://circleci.com/blog/jan-4-2023-incident-report/) and [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final), the Computer Security Incident Handling Guide. [Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) (2025) supersedes it; the sections cited here are from Rev. 2._

## The question

In an outage, the system is broken. In a security incident, the system may be working fine for someone who shouldn't be there. The question changes from "how do I restore service?" to "what could they reach, and how do I close every way back in?"

## What happened at CircleCI

- Malware on an engineer's laptop stole a valid single sign-on session that was already protected by two-factor authentication. The antivirus didn't detect the malware.
- With that session, the attacker reached production data, because the engineer's access allowed it.
- The timeline: the laptop was compromised on December 16, 2022, and data was taken on December 22. On December 29, a customer alerted CircleCI to suspicious activity. Customers were notified on January 4, 2023.
- Containment included shutting down the engineer's access, removing production access for nearly all employees, rotating exposed production hosts, and revoking or rotating customer tokens.
- Customers were asked to rotate their secrets, and to look for suspicious activity from December 16 onward.

## What's different from an outage

NIST's incident handling guide and the CircleCI case point to four differences:

1. **Containment is a decision with its own criteria.** Weigh the damage and theft at stake, the need to preserve evidence, service availability, the time and resources the strategy takes, how complete it is, and how long it lasts. Containing an attack can also cause more damage, so a disconnected host isn't proof the harm has stopped (NIST SP 800-61, 3.3.1).
2. **Preserve evidence early.** Capture a system's state as soon as you suspect an incident, before handlers and administrators change it while they investigate. If the evidence may be needed in court, log it and record every handoff (NIST SP 800-61, 3.3.2). Once the state changes, a snapshot no longer shows the system as the attacker left it.
3. **Find every affected system.** Disable breached accounts and identify all affected hosts, so each one gets fixed (NIST SP 800-61, 3.3.4). At CircleCI, that meant revoking all project API tokens and older personal API tokens, and rotating customers' GitHub and Bitbucket tokens.
4. **Revoke sessions, not only passwords, and search from the start.** At CircleCI, two-factor authentication didn't stop the attacker, who stole a session that had already passed it. Customers were asked to check for misuse from December 16, the day of the compromise, not the day it was found, because anything after the compromise could be misuse.

Recovery often includes higher levels of logging and monitoring, and a resource attacked once is often attacked again (NIST SP 800-61, 3.3.4).

_If you use rbadillap/sre: `contain-security-incident` follows these steps._

## In one sentence

"In a security incident I capture evidence before changing anything, choose containment knowing what it can break, revoke sessions, and rotate everything the stolen access could reach."

## Exercise

A CI system's API token was found in a public log. Before rotating it, what would you check first, and from what date would you search for misuse?

---

_Written with an AI assistant from the sources above._

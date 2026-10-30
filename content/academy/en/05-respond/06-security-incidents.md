---
title: Security incidents
stage: respond
order: 6
status: draft
teaches: Preserve evidence, revoke, rotate.
sources: CircleCI, January 4, 2023 incident report (https://circleci.com/blog/jan-4-2023-incident-report/); NIST SP 800-61 (https://csrc.nist.gov/pubs/sp/800/61/r3/final)
skill: contain-security-incident
version: 0.1.1
---

# Security incidents

_Sources: [CircleCI's incident report of January 4, 2023](https://circleci.com/blog/jan-4-2023-incident-report/) and [NIST SP 800-61](https://csrc.nist.gov/pubs/sp/800/61/r3/final)._

## The question

In an outage, the system is broken. In a security incident, the system may be working fine for someone who shouldn't be there. The question changes from "how do I restore service?" to "what could they reach, and how do I close every way back in?"

## What happened at CircleCI

- Malware on an engineer's laptop stole a valid single sign-on session that was already protected by two-factor authentication. The antivirus didn't detect the malware.
- With that session, the attacker reached production data, because the engineer's access allowed it.
- The timeline: the laptop was compromised on December 16, 2022, and data was taken on December 22. On December 29, a customer alerted CircleCI to suspicious activity. Customers were notified on January 4, 2023.
- Containment included shutting down the engineer's access, removing production access for nearly all employees, rotating exposed production hosts, and revoking or rotating customer tokens.
- Customers were asked to rotate their secrets, and to look for suspicious activity from December 16 onward.

## What's different from an outage

1. **Bring in security first.** An outage is owned by on-call. A possible compromise also needs the people who know how to investigate one.
2. **Preserve evidence before changing anything.** Wiping or rebuilding a machine too early destroys what tells you how they got in and what they touched.
3. **Revoke sessions, not only passwords.** At CircleCI, two-factor authentication didn't help, because the attacker stole a session that had already passed it.
4. **Rotate everything that was reachable.** Not only what you know was taken: anything the stolen access could reach.
5. **Search from the first suspicious action.** CircleCI asked customers to check from December 16, the date of the compromise, not the date it was found.

_If you use rbadillap/sre: `contain-security-incident` follows these steps. NIST SP 800-61 is the reference framework for incident handling._

## In one sentence

"In a security incident I bring in security, preserve evidence before changing anything, revoke sessions, and rotate everything the stolen access could reach."

## Exercise

A CI system's API token was found in a public log. Before rotating it, what would you check first, and from what date would you search for misuse?

---

_Written with an AI assistant from the sources above._

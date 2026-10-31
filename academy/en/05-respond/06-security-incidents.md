---
title: "Security incidents"
stage: respond
order: 6
status: approved
teaches: "Decide how to contain a security incident: what evidence to keep, what access to end, what to replace, and from what date to search."
sources:
  - title: "CircleCI, CircleCI Jan 4, 2023 security incident report"
    url: https://circleci.com/blog/jan-4-2023-incident-report/
  - title: "NIST SP 800-61 Rev. 2, Computer Security Incident Handling Guide"
    url: https://csrc.nist.gov/pubs/sp/800/61/r2/final
  - title: "NIST SP 800-61 Rev. 3, Incident Response Recommendations and Considerations for Cybersecurity Risk Management"
    url: https://csrc.nist.gov/pubs/sp/800/61/r3/final
skills: [contain-security-incident]
version: "0.1.1"
---

# Security incidents

_Sources: [CircleCI's report, published January 12, 2023, on its January 4 security incident](https://circleci.com/blog/jan-4-2023-incident-report/) and [NIST SP 800-61 Rev. 2](https://csrc.nist.gov/pubs/sp/800/61/r2/final), the Computer Security Incident Handling Guide._

## The question

A system can keep working while someone who shouldn't be there uses it. What do you keep, what access do you end, what do you replace, and from what date do you search?

## What happened at CircleCI

All times are UTC, as in the report.

- **December 16, 2022:** an engineer's laptop was compromised. Malware on it was used to steal "a valid, 2FA-backed SSO session", a single sign-on session that had already passed two-factor authentication. CircleCI's antivirus didn't detect the malware.
- **December 19:** the earliest unauthorized access the report records, confirmed later in the investigation. CircleCI has reason to believe it included reconnaissance (looking around before acting).
- **December 22:** data was taken from a subset of databases and stores, including customer environment variables, tokens and keys. The report calls this its last record of unauthorized activity in production.
- **Not dated in the report:** the engineer could generate production access tokens, and the third party escalated access to a subset of production systems. The data was encrypted at rest, but the third party extracted encryption keys from a running process.
- **December 29-31:** a customer alerted CircleCI to suspicious activity with a GitHub OAuth token, which lets one service act on GitHub. On December 30, CircleCI learned that customer's token had been compromised. On December 31 at 04:00, "out of an abundance of caution", it began rotating (replacing) all customers' GitHub OAuth tokens.
- **January 4, 2023:** by this date, its investigation had determined the scope and the entry path.
  - At 16:35, it shut down all access for the engineer.
  - At 18:30, it shut down production access for nearly all employees. It had no evidence anyone else was compromised, and did this "to limit the potential surface area".
  - At 22:30, it rotated all potentially exposed production hosts "to ensure clean production machines". After that, it says it was confident it had eliminated "both the attack vector and the potential of a lingering corrupted host".
- **January 5, at 02:30 (January 4 in PST):** it notified customers.
- **January 5-7:** it revoked all project API tokens, and personal API tokens created before January 5, and rotated customers' Bitbucket tokens. The GitHub rotation finished on January 7.

What it asked customers to do:

- Assume secrets stored on the platform in that period were accessed, and rotate them. For third-party systems, "there is no way for us to know if your secrets were used".
- Search for suspicious activity from December 16 until the date they finished rotating. It had no evidence of customer impact before December 19, and included the earlier days "out of an abundance of caution".

The report says "fewer than 5 customers" had told it of unauthorized access to third-party systems.

The report doesn't say when CircleCI preserved evidence.

## What NIST says

NIST withdrew Rev. 2 on April 3, 2025, and replaced it with [Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final), a full rewrite without these sections. Read these points as Rev. 2's advice, not NIST's current text.

- **Containment has criteria (3.3.1):** the damage and theft at stake, the need to preserve evidence, service availability, the time and resources the strategy takes, how well it works, and how long it lasts.
- **Waiting and acting both carry risk (3.3.1):** delaying containment to watch an attacker "is dangerous". Containing can also cause more damage: a malicious process may destroy data when it loses contact with another host, so a disconnected host isn't proof the damage has stopped.
- **Evidence (3.3.2):** it's "generally desirable" to capture a system's state as soon as you suspect an incident, before handlers and administrators change it. Not every incident needs it: "most malware incidents do not merit evidence acquisition". If evidence may go to court, log it and record each transfer between people, known as chain of custody.
- **After containment (3.3.4):** eradication may be necessary, such as disabling breached accounts, and it's important to identify all affected hosts. Recovery often adds logging and monitoring. NIST also says a resource successfully attacked "is often attacked again, or other resources within the organization are attacked in a similar manner".

## Reading the case

The rest of this lesson is its own reading and method.

- **Evidence and containment compete, so decide.** NIST wants evidence early, doesn't require it for every incident, and warns against delaying containment to watch an attacker. CircleCI's report can't show the right order. This lesson's rule: save what's quick and would be lost, such as logs and current settings, and don't let that hold up ending the access.
- **End the access, not only the password.** The stolen session had already passed two-factor authentication. The report calls the theft "session cookie theft, enabling them to impersonate the targeted employee". Neither source states this rule, but a stolen session doesn't need the password, so changing it may not be enough. Check that sessions and tokens end too.
- **Follow what the access could reach.** One laptop led to a session, then production access, then customer secrets, and possibly customers' other systems. What the access could reach is a reason to replace widely. CircleCI's first rotation began earlier, as a precaution, before it had determined the entry path.
- **Search from the earliest date the access could have started.** The customer's alert came on December 29. The investigation later placed the first unauthorized access on December 19, and CircleCI still asked customers to look from December 16. Starting at the alert would skip 13 days.
- **Containment has a cost.** Nearly all employees lost production access. The report gives the reason, not what it cost, but it removes access people use for their work. It's a real decision, with its reason written down.

## How to do it

1. Bring in whoever owns security, and keep a record with times. Start by asking what else this could be, as in [Reframe first](01-reframe-first.md).
2. Save what's quick and would be lost, and write where it is.
3. Choose containment against NIST's criteria, and write what it can break.
4. End the access: disable accounts, and end sessions and tokens.
5. Tell those affected what's confirmed, as in [Confirmed impact](05-confirmed-impact.md). Don't wait for the next steps: they may have to replace and search themselves.
6. List everything that access could reach. Treat it as exposed, and replace it.
7. Search from the earliest date the access could have started until the replacing is done, and keep more logging afterwards.

For this case, an example written for this lesson, using only the report's facts:

- **Access:** one engineer's stolen session. The engineer could generate production tokens.
- **Could reach:** a subset of production systems, customer environment variables, tokens and keys, and possibly customers' other systems.
- **Ended:** the engineer's access, and production access for nearly all employees.
- **Replaced:** production hosts, and customers' GitHub and Bitbucket tokens.
- **Revoked:** project API tokens, and personal API tokens created before January 5.
- **Asked of customers:** rotate their own secrets, and search from December 16 until they finished rotating.
- **Evidence kept:** not stated in the report, so this record stays blank instead of guessing.

_If you use rbadillap/sre: `contain-security-incident` preserves evidence, proposes containment with a way to undo it, including ending sessions, searches for what the attacker left behind, and lists what to replace. It requires evidence before the first change, and it doesn't weigh NIST's criteria._

## In one sentence

"In a security incident I save what would be lost, choose containment knowing what it can break, end the stolen access, replace everything it could reach, and search from the first day it could have started."

## Exercise

A hypothetical case: on November 10 at 09:00 UTC, you find your CI system's API token in a public build log. That log was first written on November 3 at 14:00 UTC. Assume this log is the only place the token appeared. The token can read repositories and start builds. The repositories hold no secrets, and builds can read one deploy key. The token's access log is available.

1. What do you save before you revoke the token? Why not spend longer on it?
2. From when until when do you search for misuse?
3. What do you assume about the token, and what do you replace?
4. Pick a credential your team uses. Do your logs go back far enough to search from the first day it could have been exposed?

---

_Written with an AI assistant from the sources above._

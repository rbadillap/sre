# Reviewing a template

A template is the paved road a skill leaves in someone's repository, under `reliability/`. It lives in the `assets/` folder of the skill that fills it.

**1. Someone else can reuse the result.**
- Why: a filled template that only its author understands isn't a road.
- Check: a teammate who wasn't there could act on the filled file alone.

**2. Every field says how to fill it.**
- Why: an empty heading invites a guess.
- Check: each field has a one-line instruction or an example, in a comment or placeholder.

**3. It separates what's known from what's assumed.**
- Why: a postmortem or a runbook that mixes facts and guesses misleads the next person.
- Check: fields that can hold a guess ask the writer to mark it as one.

**4. It has no stack.**
- Why: the same template serves every team.
- Check: no product names in the structure. Examples, if any, are marked as examples.

**5. One skill fills it, and says so.**
- Why: a template with no skill behind it drifts from the method.
- Check: the template names the skill that fills it, and that skill names the template back.

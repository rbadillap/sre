# Reviewing a template

A template is the paved road a skill leaves in someone's repository, under `reliability/`. It lives in the `assets/` folder of the skill that fills it.

**1. Someone else can reuse the result.**
- Why: a filled template that only its author understands isn't a road.
- Check: a teammate who wasn't there could act on the filled file alone.

**2. Every field says how to fill it.**
- Why: an empty heading invites a guess.
- Check: each field has a one-line instruction or an example, in a comment or placeholder. In a table, an empty cell is fine when its column header says what goes in it; the first row of each table shows the format.

**3. It separates what's known from what isn't, with the same three labels everywhere.**
- Why: a postmortem or a runbook that mixes facts and guesses misleads the next person. Different words for the same idea in different templates confuse both people and agents.
- Check: fields that can hold a guess use the labels of `evidence-before-claims`: verified, hypothesis, not verified.

**6. Every output the skill asks for has a field.**
- Why: if a step or a "Done when" criterion asks for something the template has no place for, the writer either drops it or invents a place, and the next reader can't find it.
- Check: go through the skill's steps and "Done when". Each output, including the reframe from `reframe-first`, has a field in the template.

**4. It has no stack.**
- Why: the same template serves every team.
- Check: no product names in the structure. Examples, if any, are marked as examples.

**5. One skill fills it, and says so.**
- Why: a template with no skill behind it drifts from the method.
- Check: the template names the skill that fills it, and that skill names the template back.

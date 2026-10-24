# Reviewing a document

These rules apply to every page in the repository, and to the words any change adds.

**1. A claim that can be checked links to its source.**
- Why: a method that cites ITIL, the Google SRE books or NIST has to cite them correctly, or it loses trust.
- Check: every claim about an external framework, a spec or a number has a link, and the link says what the text says. A view with no source is written as a view.

**2. It describes how things are now, not how they got here.**
- Why: readers need the current rule. The history of each change belongs in `CHANGELOG.md`.
- Check: no "we used to", "before this change" or "in the future we'll". Notes about a transition are removed when it ends.

**3. Plain words.**
- Why: the reader may be tired, on call, or reading in a second language.
- Check: short sentences, common words, one idea per sentence. Technical terms stay when they're the right ones; idioms go.

**4. English.**
- Why: one language for a public repository.
- Check: every page and every skill is in English.

**5. Nothing personal.**
- Why: the package teaches a method. People's stories, employers and private incidents don't belong in a public repository.
- Check: no names of companies, people or internal systems. Examples are written in general terms.

**6. The why sits next to the rule.**
- Why: this repository doesn't keep decision records. The reasoning lives in the documents themselves.
- Check: every convention or rule says why it exists, on the same page.

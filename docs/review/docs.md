# Reviewing a document

These rules apply to every page in the repository, and to the words any change adds.

**1. A claim that can be checked links to its source.**
- Why: a method that cites ITIL, the Google SRE books or NIST has to cite them correctly, or it loses trust.
- Check: every claim about an external framework, a spec or a number has a link, and the link says what the text says. A view with no source is written as a view.

**2. It describes how things are now, not how they got here.**
- Why: readers need the current rule. The history of each change belongs in `CHANGELOG.md`.
- Check: no "we used to", "before this change" or "in the future we'll". Notes about a transition are removed when it ends. A lesson in `academy/` may tell the story of a past incident; what it says about the package describes the package now.

**3. Plain words.**
- Why: the reader may be tired, on call, or reading in a second language.
- Check: short sentences, common words, one idea per sentence. Technical terms stay when they're the right ones; idioms go.

**4. English.**
- Why: one language for a public repository. Lessons are the exception, because people learn best in their own language.
- Check: every page and every skill is in English. A lesson in `academy/<lang>/` is in the language of its `<lang>` folder.

**5. Nothing personal.**
- Why: the package teaches a method. People's stories, employers and private incidents don't belong in a public repository.
- Check: no names of companies, people or internal systems. Examples are written in general terms. A link to public material keeps its attribution, because a citation has to be checkable; the text around it still doesn't name the company. A lesson in `academy/` may name the organizations and products a linked public case needs, because the case is what it teaches: its claims match the source, published facts stay apart from interpretation and examples, and it adds no people's identities, employer experiences or private details. The exception doesn't reach skills, disciplines or evals.

**6. The why sits next to the rule.**
- Why: this repository doesn't keep decision records. The reasoning lives in the documents themselves.
- Check: every convention or rule says why it exists, on the same page.

**7. A skill page explains; `SKILL.md` decides.**
- Why: a page in `docs/skills/` is for people choosing and reading a skill. If it held its own steps, it would become a second method that drifts from the one agents run.
- Check: the page says when to choose the skill over another, what to have before starting, what result comes back and how to read it, what it doesn't solve, common questions and the next step. It can sum up the purpose or explain a result. It has no sequence of steps, "done" criteria or safety limits of its own, and it links to `SKILL.md` for the method.

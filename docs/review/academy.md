# Reviewing a lesson

These rules apply to every lesson in `academy/`. A lesson teaches a topic of SRE from public sources. It isn't documentation of this package: the skills are the curriculum, not the subject.

Lessons also follow [docs.md](docs.md), with the scopes it gives them: their own language, named public cases, and stories of past incidents.

## Shape

**1. One file per lesson, where its frontmatter says.**
- Why: a reader, a site and `make validate` find lessons by their path.
- Check: the path is `academy/<lang>/<NN-stage>/<NN-lesson>.md`, in lowercase with hyphens. The frontmatter has `title`, `stage` (the stage folder without its number), `order` (the lesson's number), `status`, `teaches`, `sources`, `skills` and `version`, and `make validate` passes.

**2. It answers one question, with a goal the learner can reach.**
- Why: a lesson that covers everything teaches nothing in particular.
- Check: the lesson states its question near the top, and `teaches` says what the learner can do after it. Anything the learner needs first is explained, or linked to the lesson that explains it.

**3. The topic and a real case come first.**
- Why: people learn SRE from what happened and why, not from a product. A lesson that sells stops being trusted.
- Check: the lesson can be completed without installing this package. A skill appears only as a short reference, *"If you use rbadillap/sre: …"*, where it gives a concrete way to apply the topic, and not where it doesn't. One lesson can name several skills, and a skill can appear in several lessons.

## Sources

**4. Every fact comes from a linked public source, and says only what the source says.**
- Why: a lesson that cites wrongly teaches the wrong thing, and readers can't check a claim without its source.
- Check: every source in `sources` has a title and a URL, and each fact in the lesson can be found in one of them. Where two places in a source disagree, the lesson says so. A fact found wrong is fixed in the lesson and everywhere it was repeated.

**5. Published facts stay apart from the lesson's reading of them.**
- Why: a reader has to know what the source says and what the lesson concludes, so they can disagree with the second.
- Check: what the source reports is written as reported. The lesson's interpretation is written as interpretation, and an example phrasing, such as a blameless sentence, is marked as an example.

**6. No invented cases.**
- Why: a made-up incident presented as real is a false source.
- Check: every case presented as real has its public source. An exercise can use a hypothetical situation or numbers, marked as hypothetical. A lesson whose public case is still missing says `CASE NEEDED` and has no `sources`; it can't be `approved` until the case is found.

## Voice

**7. Plain words, steps in order, and the learner's own work in view.**
- Why: the reader may be learning in a second language, or between pages.
- Check: short sentences, technical terms exact, and a change stated as a change. The lesson works through its case as an example, gives one sentence the learner can say out loud, and asks the learner to connect the topic to their own work.

**8. Nothing is added that the sources or the author didn't give.**
- Why: an assistant may write a lesson, and an opinion or a story nobody gave is an invention.
- Check: the lesson has no opinion, experience or story beyond its sources. A view, when needed, is a quote from a person who gave it, or the lesson goes without.

## Exercise

**9. The exercise can be answered from what it gives.**
- Why: an exercise with a missing number, or one that asks for more than the evidence allows, teaches guessing.
- Check: the data needed is in the exercise, assumptions are stated, and it doesn't ask the learner to prove what the case can't support, such as an action that "would have prevented" a loss when it could only have reduced it.

## Status

**10. A lesson moves from `outline` to `draft` to `approved`, and only a person approves it.**
- Why: a lesson teaches people directly, so a person answers for its final text.
- Check: `outline` lists what it will teach and its sources. `draft` is written and waiting. `approved` means a person approved this text; a change to an approved lesson's facts or exercise returns it to `draft` until approved again.

**11. `version` is the release the lesson was checked against, or empty.**
- Why: a lesson that refers to a skill can go out of date when the skill changes, and an unchecked lesson shouldn't look checked.
- Check: `version` is empty until someone checks the lesson's references against a release. An approved lesson with skills in `skills` has a version. A newer release doesn't make an older version wrong; it means the lesson can be rechecked.

**12. It ends with a one-line disclosure.**
- Why: readers should know how the lesson was prepared.
- Check: the last line says how the lesson was written, for example *"Written with an AI assistant from the sources above."* It doesn't replace checking the sources or approval.

# academy

SRE lessons, taught from real incidents and public sources.

## Structure

```
content/academy/<lang>/<NN-stage>/<NN-lesson>.md
```

- **The root is the cycle:** `00-the-cycle`. Every other folder is one stage: define, design, ship, observe, respond, learn.
- **Each lesson is one file,** with frontmatter: `title`, `stage`, `order`, `status`, `teaches`, `sources`, `skill`.
- **`status`:** `outline` (a placeholder with what it teaches and its sources), `draft` (written, waiting for approval), or `approved`.
- **`checked_against`:** the rbadillap/sre release the lesson's skill reference was checked against. When the package changes, lessons checked against an older release get rechecked.
- **`<lang>`:** `en` for now. Another language gets its own folder, without moving files.

## How a lesson is written

The voice is the teaching voice in the rbadillap design contract (`DESIGN.md`, v4.2): sources first, the topic before any product, and drafts until approved.

Each lesson follows the same parts:

1. A source line, linked.
2. The question it answers.
3. What the sources say, only as they say it.
4. The topic, worked through the case.
5. A skill reference, only where one applies: _"If you use rbadillap/sre: …"_.
6. The idea in one sentence.
7. An exercise.
8. A one-line disclosure.

Lessons marked `CASE NEEDED` don't have a verified public case yet. No case is invented to fill the gap.

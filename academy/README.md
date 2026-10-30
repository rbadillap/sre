# academy

SRE lessons, taught from real incidents and public sources.

## Structure

```
academy/<lang>/<NN-stage>/<NN-lesson>.md
```

- **The root is the cycle:** `00-the-cycle`. Every other folder is one stage: define, design, ship, observe, respond, learn.
- **Each lesson is one file,** with frontmatter: `title`, `stage`, `order`, `status`, `teaches`, `sources`, `skills`, `version`.
- **`status`:** `outline` (a placeholder with what it teaches and its sources), `draft` (written, waiting for approval), or `approved`.
- **`version`:** the release of this package the lesson was checked against, or empty until it's checked.
- **`<lang>`:** `en` for now. Another language gets its own folder, without moving files.

## How a lesson is written

The rules for lessons, including their voice, are in [docs/review/academy.md](../docs/review/academy.md). `make validate` checks every lesson's path and frontmatter.

Lessons marked `CASE NEEDED` don't have a verified public case yet. No case is invented to fill the gap.

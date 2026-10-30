"""Check every lesson's frontmatter against docs/review/academy.md.

It checks shape only: fields, types, paths, sources, skills, status and
version. It doesn't check that a source says what the lesson says, or
that the lesson teaches well; people review that.
"""

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ACADEMY = ROOT / "academy"
SKILLS = {p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}

FIELDS = {"title", "stage", "order", "status", "teaches", "sources", "skills", "version"}
STATUSES = {"outline", "draft", "approved"}
PATH = re.compile(r"^(?P<lang>[a-z]{2})/(?P<stage_n>\d{2})-(?P<stage>[a-z0-9-]+)/(?P<order>\d{2})-[a-z0-9-]+\.md$")
VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    return yaml.safe_load(text[4:end]), text[end + 5:]


def check(path):
    rel = path.relative_to(ACADEMY).as_posix()
    errors = []
    match = PATH.match(rel)
    if not match:
        return [f"path isn't <lang>/<NN-stage>/<NN-lesson>.md"]

    parsed = frontmatter(path.read_text(encoding="utf-8"))
    if parsed is None:
        return ["no frontmatter between --- lines"]
    meta, body = parsed
    if not isinstance(meta, dict):
        return ["frontmatter isn't a mapping"]

    missing = FIELDS - meta.keys()
    extra = meta.keys() - FIELDS
    if missing:
        errors.append(f"missing {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"unknown {', '.join(sorted(extra))}")

    for field in ("title", "teaches"):
        if field in meta and not (isinstance(meta[field], str) and meta[field].strip()):
            errors.append(f"{field} must be text")

    if "stage" in meta and meta["stage"] != match["stage"]:
        errors.append(f"stage is {meta['stage']!r}, the folder says {match['stage']!r}")
    if "order" in meta and meta["order"] != int(match["order"]):
        errors.append(f"order is {meta['order']!r}, the file name says {int(match['order'])}")

    status = meta.get("status")
    if "status" in meta and status not in STATUSES:
        errors.append(f"status must be one of {', '.join(sorted(STATUSES))}")

    sources = meta.get("sources")
    if "sources" in meta:
        if not isinstance(sources, list):
            errors.append("sources must be a list (empty while the case is needed)")
        else:
            for i, source in enumerate(sources, 1):
                if not (isinstance(source, dict) and set(source) == {"title", "url"}
                        and isinstance(source["title"], str) and source["title"].strip()
                        and isinstance(source["url"], str) and source["url"].startswith("https://")):
                    errors.append(f"source {i} needs a title and an https url, and nothing else")

    skills = meta.get("skills")
    if "skills" in meta:
        if not isinstance(skills, list):
            errors.append("skills must be a list, empty when none applies")
        else:
            for skill in skills:
                if skill not in SKILLS:
                    errors.append(f"skill {skill!r} isn't in skills/")

    version = meta.get("version")
    if "version" in meta and version is not None and not (isinstance(version, str) and VERSION.match(version)):
        errors.append("version must be empty or a release like \"0.1.1\", in quotes")

    case_needed = "CASE NEEDED" in body or "CASE NEEDED" in str(meta.get("teaches", ""))
    if case_needed and sources:
        errors.append("CASE NEEDED with sources: list the case's source, or keep sources empty")
    if not case_needed and isinstance(sources, list) and not sources:
        errors.append("no sources: add them, or mark the lesson CASE NEEDED")
    if status == "approved":
        if case_needed:
            errors.append("approved while CASE NEEDED")
        if skills and version is None:
            errors.append("approved with skills but no checked version")

    return errors


def main():
    lessons = sorted(ACADEMY.rglob("*.md")) if ACADEMY.is_dir() else []
    lessons = [p for p in lessons if p.parent != ACADEMY]
    failed = 0
    for path in lessons:
        for error in check(path):
            print(f"{path.relative_to(ROOT)}: {error}")
            failed += 1
    if failed:
        return 1
    print(f"academy ok ({len(lessons)} lessons)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

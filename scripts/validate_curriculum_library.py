"""Validate structure, content, links, and executable cells in the 2,000 notebooks."""

from __future__ import annotations

import contextlib
import io
import json
import re
from pathlib import Path

from curriculum_catalog import load_catalog
from generate_curriculum_library import COURSE_PATHS, course_path, lesson_path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_HEADINGS = {
    "## Placement and prerequisites",
    "## Concept foundations",
    "## Mental model",
    "## A repeatable workflow",
    "## Annotated example",
    "## Guided lab",
    "## Solution blueprint",
    "## Common mistakes and fixes",
    "## Practice tasks",
    "## Knowledge check",
    "## Recap and reference",
}


def source(cell: dict) -> str:
    value = cell.get("source", "")
    return "".join(value) if isinstance(value, list) else value


def main() -> None:
    topics = load_catalog()
    errors: list[str] = []
    if len(topics) != 200:
        errors.append(f"Expected 200 topics; found {len(topics)}")
    if [topic.number for topic in topics] != list(range(1, 201)):
        errors.append("Topic numbers are not the exact 001-200 sequence")
    if any(len(topic.lessons) != 10 for topic in topics):
        errors.append("At least one topic does not have ten lessons")

    expected_paths: list[Path] = []
    word_count = 0
    code_cells = 0
    executed_cells = 0
    for topic in topics:
        for number, lesson in enumerate(topic.lessons, 1):
            path = lesson_path(topic, number, lesson)
            expected_paths.append(path)
            if not path.exists():
                errors.append(f"Missing notebook: {path.relative_to(ROOT)}")
                continue
            try:
                notebook = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"Invalid JSON: {path.relative_to(ROOT)}: {exc}")
                continue
            if notebook.get("nbformat") != 4:
                errors.append(f"Wrong notebook format: {path.relative_to(ROOT)}")
            cells = notebook.get("cells", [])
            ids = [cell.get("id") for cell in cells]
            if None in ids or len(ids) != len(set(ids)):
                errors.append(f"Missing or duplicate cell IDs: {path.relative_to(ROOT)}")
            document = "\n".join(source(cell) for cell in cells)
            missing = [heading for heading in REQUIRED_HEADINGS if heading not in document]
            if missing:
                errors.append(f"Missing sections in {path.relative_to(ROOT)}: {', '.join(missing)}")
            if "execute: false" not in document or "Course overview" not in document:
                errors.append(f"Missing execution or navigation metadata: {path.relative_to(ROOT)}")
            word_count += len(re.findall(r"\b[\w'-]+\b", document))
            for cell in cells:
                if cell.get("cell_type") != "code":
                    continue
                code = source(cell)
                code_cells += 1
                try:
                    compile(code, str(path), "exec")
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        exec(code, {"__name__": "__main__"})
                    executed_cells += 1
                except Exception as exc:  # noqa: BLE001 - validation reports exact lesson
                    errors.append(f"Code failure in {path.relative_to(ROOT)}: {type(exc).__name__}: {exc}")

    course_keys = {(topic.section, topic.course) for topic in topics}
    for section, course in sorted(course_keys):
        overview = ROOT / f"{COURSE_PATHS[(section, course)]}.ipynb"
        if not overview.exists():
            errors.append(f"Missing course overview: {overview.relative_to(ROOT)}")
            continue
        document = overview.read_text(encoding="utf-8")
        course_topics = [topic for topic in topics if topic.section == section and topic.course == course]
        if document.count('class=\\"topic-lesson-link\\"') != len(course_topics) * 10:
            errors.append(f"Wrong lesson-link count in {overview.relative_to(ROOT)}")

    if len(expected_paths) != 2_000 or len(set(expected_paths)) != 2_000:
        errors.append("Generated-path set is not exactly 2,000 unique paths")

    managed_files = []
    for topic in topics:
        folder = course_path(topic).with_suffix("") / f"{topic.number:03d}-{re.sub(r'[^a-z0-9]+', '-', topic.title.lower()).strip('-')[:72]}"
        if folder.exists():
            managed_files.extend(folder.rglob("*.ipynb"))
    if len(set(managed_files)) != 2_000:
        errors.append(f"Managed topic folders contain {len(set(managed_files))} notebooks, not 2,000")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors[:100]))
        if len(errors) > 100:
            print(f"... plus {len(errors) - 100} more errors")
        raise SystemExit(1)

    print(f"Validated {len(topics)} topics, {len(expected_paths):,} notebooks, and {len(course_keys)} course overviews.")
    print(f"Compiled and executed {executed_cells:,}/{code_cells:,} code cells; approximately {word_count:,} words checked.")


if __name__ == "__main__":
    main()

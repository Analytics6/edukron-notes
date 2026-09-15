"""Refresh generated notebook UI in an existing complete Quarto site tree.

This is the fast production path for presentation-only template changes. It keeps
Quarto's previously rendered prose, code, search index, and assets, while replacing
the HTML fragments owned by the notebook generators with their current source.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from bs4 import BeautifulSoup

from generate_curriculum_library import COURSE_PATHS


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


def cell_source(notebook: Path, cell_id: str) -> str:
    payload = json.loads(notebook.read_text(encoding="utf-8"))
    for cell in payload["cells"]:
        if cell.get("id") == cell_id:
            return "".join(cell["source"]).strip()
    raise ValueError(f"Missing cell {cell_id!r} in {notebook}")


def replace_tag_with_html(tag, html: str) -> None:
    fragment = BeautifulSoup(html, "html.parser")
    for node in list(fragment.contents):
        tag.insert_before(node)
    tag.extract()


def load_page(path: Path) -> BeautifulSoup:
    if not path.is_file():
        raise FileNotFoundError(f"Rendered page is missing: {path}")
    return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")


def save_page(path: Path, soup: BeautifulSoup) -> None:
    path.write_text(str(soup), encoding="utf-8", newline="\n")


def refresh_home() -> None:
    notebook = ROOT / "index.ipynb"
    page = SITE / "index.html"
    soup = load_page(page)
    masthead = soup.select_one(".blog-masthead")
    if masthead is None:
        raise ValueError("Homepage masthead was not found")
    replace_tag_with_html(masthead, cell_source(notebook, "masthead"))

    labels = [
        "Learning path",
        "Learning path",
        "Learning path",
        "Interview practice",
        "Project playbook",
    ]
    cards = soup.select(".blog-card .course-number")
    if len(cards) != len(labels):
        raise ValueError(f"Expected {len(labels)} homepage cards, found {len(cards)}")
    for card, label in zip(cards, labels, strict=True):
        card.string = label
    save_page(page, soup)


def refresh_course_overviews() -> int:
    refreshed = 0
    for relative in COURSE_PATHS.values():
        notebook = ROOT / f"{relative}.ipynb"
        page = SITE / f"{relative}.html"
        soup = load_page(page)

        old_hero = soup.select_one(".curriculum-summary")
        old_stats = soup.select_one(".course-stat-grid")
        old_start = soup.select_one(".course-start")
        if old_hero is not None and old_stats is not None and old_start is not None:
            replace_tag_with_html(old_hero, cell_source(notebook, "course-hero"))
            old_stats.extract()
            old_start.extract()
        elif soup.select_one(".course-workspace") is None:
            raise ValueError(f"Course UI was not found in {page}")

        old_syllabus = soup.select_one("section#full-syllabus")
        if old_syllabus is not None:
            replace_tag_with_html(old_syllabus, cell_source(notebook, "full-syllabus"))
        elif soup.select_one(".syllabus-search") is None:
            raise ValueError(f"Full syllabus UI was not found in {page}")

        layout = soup.select_one("#quarto-content")
        if layout is not None:
            layout_classes = [
                "page-layout-full" if name == "page-layout-article" else name
                for name in layout.get("class", [])
            ]
            if "page-layout-full" not in layout_classes:
                layout_classes.append("page-layout-full")
            layout["class"] = layout_classes
        margin_sidebar = soup.select_one("#quarto-margin-sidebar")
        if margin_sidebar is not None:
            margin_sidebar.extract()
        main = soup.select_one("main#quarto-document-content")
        if main is not None:
            main_classes = list(main.get("class", []))
            if "column-page" not in main_classes:
                main_classes.append("column-page")
            main["class"] = main_classes
        save_page(page, soup)
        refreshed += 1
    return refreshed


def generated_lessons() -> list[Path]:
    notebooks: list[Path] = []
    for base in (ROOT / "courses", ROOT / "interview-questions", ROOT / "project-flows"):
        for notebook in base.rglob("*.ipynb"):
            payload = json.loads(notebook.read_text(encoding="utf-8"))
            if any(cell.get("id") == "lesson-banner" for cell in payload["cells"]):
                notebooks.append(notebook)
    return sorted(notebooks)


def refresh_lessons() -> int:
    refreshed = 0
    for notebook in generated_lessons():
        relative = notebook.relative_to(ROOT).with_suffix(".html")
        page = SITE / relative
        soup = load_page(page)
        old_banner = soup.select_one(".lesson-banner")
        if old_banner is not None:
            replace_tag_with_html(old_banner, cell_source(notebook, "lesson-banner"))
        elif soup.select_one(".lesson-notebook") is None:
            raise ValueError(f"Lesson banner was not found in {page}")
        html = str(soup).replace("one of ten focused lessons", "a focused lesson")
        page.write_text(html, encoding="utf-8", newline="\n")
        refreshed += 1
    return refreshed


def validate_rendered_site(course_count: int, lesson_count: int) -> None:
    html_count = sum(1 for _ in SITE.rglob("*.html"))
    if html_count < 2_070:
        raise ValueError(f"Expected a complete site tree, found only {html_count} HTML pages")

    home = (SITE / "index.html").read_text(encoding="utf-8")
    if "10 subjects" in home or "masthead-notebook" not in home:
        raise ValueError("Homepage refresh validation failed")

    if course_count != 36:
        raise ValueError(f"Expected 36 refreshed course overviews, found {course_count}")
    if lesson_count != 2_000:
        raise ValueError(f"Expected 2,000 refreshed lessons, found {lesson_count}")

    for relative in COURSE_PATHS.values():
        html = (SITE / f"{relative}.html").read_text(encoding="utf-8")
        required = ("course-workspace", "syllabus-search", "curriculum-catalog")
        if "10 notebooks" in html or not all(marker in html for marker in required):
            raise ValueError(f"Course UI validation failed for {relative}")

    sample = SITE / "courses/full-stack-ai/python/001-python-language-foundations/01-python-and-jupyter-introduction.html"
    sample_html = sample.read_text(encoding="utf-8")
    if "lesson-notebook" not in sample_html or "Lesson 01 of 10" in sample_html:
        raise ValueError("Lesson UI validation failed")


def main() -> None:
    if not SITE.is_dir():
        raise FileNotFoundError("_site must contain a complete rendered gh-pages tree")
    shutil.copy2(ROOT / "styles.css", SITE / "styles.css")
    refresh_home()
    course_count = refresh_course_overviews()
    lesson_count = refresh_lessons()
    validate_rendered_site(course_count, lesson_count)
    print(
        f"Refreshed {lesson_count:,} lessons and {course_count} course overviews "
        f"inside a complete {sum(1 for _ in SITE.rglob('*.html')):,}-page site."
    )


if __name__ == "__main__":
    main()

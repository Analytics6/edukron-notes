"""Generate the Edukron Notes curriculum overview notebooks.

The detailed lesson content is intentionally not generated here. Each overview
acts as a stable destination for the top-level navigation and as a content
handoff checklist for the lesson material supplied later.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-09"

KERNEL_METADATA = {
    "kernelspec": {
        "display_name": "Python (Notebook Blog)",
        "language": "python",
        "name": "notebook-blog",
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.12.10",
    },
}

TRACKS = [
    {
        "key": "full-stack-ai",
        "title": "Full Stack AI",
        "icon": "cpu",
        "kind": "course",
        "directory": "courses/full-stack-ai",
        "description": "A complete path from programming and data foundations to production-ready generative and agentic AI systems.",
        "items": [
            ("python", "Python", "Programming foundations for data, automation, APIs, and AI applications."),
            ("sql", "SQL", "Querying, transforming, and validating relational data for analytics and AI."),
            ("data-science", "Data Science", "A reproducible workflow for cleaning, exploring, visualizing, and explaining data."),
            ("machine-learning", "Machine Learning", "Model training, evaluation, feature workflows, and responsible prediction."),
            ("artificial-intelligence", "Artificial Intelligence", "Search, reasoning, knowledge representation, planning, and intelligent systems."),
            ("deep-learning", "Deep Learning", "Neural networks, representation learning, optimization, and modern architectures."),
            ("generative-ai", "Generative AI", "Building and evaluating systems that generate text and other useful outputs."),
            ("large-language-models", "Large Language Models (LLMs)", "Tokens, transformers, prompting, adaptation, inference, and evaluation."),
            ("rag", "Retrieval Augmented Generation (RAG)", "Grounding model responses in retrieved, traceable knowledge."),
            ("agentic-ai", "Agentic AI", "Tool-using AI systems with planning, memory, guardrails, and observability."),
        ],
    },
    {
        "key": "azure-data-engineering",
        "title": "Azure Data Engineering",
        "icon": "database",
        "kind": "course",
        "directory": "courses/azure-data-engineering",
        "description": "An end-to-end path for designing, building, governing, and operating modern data platforms on Azure.",
        "items": [
            ("python", "Python", "Python for ingestion, transformation, orchestration, testing, and automation."),
            ("sql", "SQL", "SQL for analytical models, data quality, performance, and warehouse workloads."),
            ("fundamentals", "Data Engineering Fundamentals", "Core architecture, batch and streaming patterns, reliability, and governance."),
            ("azure-data-factory", "Azure Data Factory (ADF)", "Metadata-driven pipelines, orchestration, integration runtimes, and monitoring."),
            ("adls-gen2", "Azure Data Lake Storage Gen2 (ADLS Gen2)", "Secure, scalable lake storage with practical organization and access patterns."),
            ("azure-databricks", "Azure Databricks", "Collaborative lakehouse engineering, jobs, notebooks, governance, and performance."),
            ("pyspark", "PySpark", "Distributed data processing with DataFrames, transformations, tuning, and testing."),
            ("azure-synapse", "Azure Synapse Analytics", "Integrated SQL, Spark, pipelines, and analytics-serving patterns."),
            ("microsoft-fabric", "Microsoft Fabric", "Unified analytics with OneLake, engineering, warehousing, pipelines, and governance."),
            ("delta-lake", "Delta Lake", "Reliable lakehouse tables using transactions, schema controls, history, and optimization."),
        ],
    },
    {
        "key": "azure-devops",
        "title": "Azure DevOps",
        "icon": "infinity",
        "kind": "course",
        "directory": "courses/azure-devops",
        "description": "A practical path from source control and automation to secure cloud delivery, containers, infrastructure, and operations.",
        "items": [
            ("linux-shell-scripting", "Linux & Shell Scripting", "Command-line fluency and dependable scripts for delivery and operations."),
            ("git-version-control", "Git & Version Control", "Commit design, branching, collaboration, recovery, and maintainable history."),
            ("azure-repos", "Azure Repos", "Repository policies, pull requests, permissions, and team collaboration on Azure DevOps."),
            ("azure-pipelines", "Azure Pipelines (CI/CD)", "Automated build, test, release, environments, approvals, and deployment strategies."),
            ("yaml-pipelines", "YAML Pipeline Development", "Reusable, parameterized, secure, and testable pipeline definitions."),
            ("docker", "Docker & Containerization", "Images, containers, registries, networking, security, and production practices."),
            ("kubernetes-aks", "Kubernetes & AKS", "Workload orchestration, networking, scaling, upgrades, and Azure Kubernetes Service."),
            ("terraform", "Terraform Infrastructure as Code (IaC)", "Repeatable Azure infrastructure using state, modules, plans, and automation."),
            ("azure-cloud-services", "Azure Cloud Services", "Choosing and integrating Azure compute, networking, identity, storage, and monitoring."),
            ("devsecops-monitoring", "DevSecOps & Monitoring", "Security controls, supply-chain checks, telemetry, alerting, and incident learning."),
        ],
    },
    {
        "key": "interview-questions",
        "title": "Interview Questions",
        "icon": "question-circle",
        "kind": "interview",
        "directory": "interview-questions",
        "description": "Structured preparation pages for concept checks, scenario questions, coding discussions, and system-design interviews.",
        "items": [
            ("full-stack-ai", "Full Stack AI", "Interview preparation across Python, SQL, data science, ML, LLMs, RAG, and agents."),
            ("azure-data-engineering", "Azure Data Engineering", "Interview preparation for data architecture, pipelines, Spark, lakehouse, and Azure services."),
            ("azure-devops", "Azure DevOps", "Interview preparation for Git, CI/CD, containers, IaC, AKS, security, and operations."),
        ],
    },
    {
        "key": "project-flows",
        "title": "Project Flows",
        "icon": "kanban",
        "kind": "project",
        "directory": "project-flows",
        "description": "End-to-end implementation maps that connect requirements, architecture, delivery, testing, deployment, and operations.",
        "items": [
            ("full-stack-ai", "Full Stack AI", "A complete flow for designing, building, evaluating, deploying, and monitoring an AI product."),
            ("azure-data-engineering", "Azure Data Engineering", "A complete flow for delivering a governed and observable Azure data platform."),
            ("azure-devops", "Azure DevOps", "A complete flow for establishing secure, repeatable application and infrastructure delivery."),
        ],
    },
]

ITEM_ICONS = {
    "full-stack-ai": {
        "python": "code-square",
        "sql": "database",
        "data-science": "bar-chart-line",
        "machine-learning": "diagram-3",
        "artificial-intelligence": "robot",
        "deep-learning": "cpu",
        "generative-ai": "stars",
        "large-language-models": "chat-square-text",
        "rag": "search",
        "agentic-ai": "node-plus",
    },
    "azure-data-engineering": {
        "python": "code-square",
        "sql": "database",
        "fundamentals": "diagram-3",
        "azure-data-factory": "diagram-3",
        "adls-gen2": "hdd-stack",
        "azure-databricks": "layers",
        "pyspark": "lightning",
        "azure-synapse": "table",
        "microsoft-fabric": "boxes",
        "delta-lake": "database-check",
    },
    "azure-devops": {
        "linux-shell-scripting": "terminal",
        "git-version-control": "git",
        "azure-repos": "folder2-open",
        "azure-pipelines": "infinity",
        "yaml-pipelines": "filetype-yml",
        "docker": "box-seam",
        "kubernetes-aks": "boxes",
        "terraform": "building",
        "azure-cloud-services": "cloud",
        "devsecops-monitoring": "shield-check",
    },
    "interview-questions": {
        "full-stack-ai": "cpu",
        "azure-data-engineering": "database",
        "azure-devops": "infinity",
    },
    "project-flows": {
        "full-stack-ai": "cpu",
        "azure-data-engineering": "database",
        "azure-devops": "infinity",
    },
}


def lines(text: str) -> list[str]:
    text = text.strip() + "\n"
    return text.splitlines(keepends=True)


def raw_cell(cell_id: str, text: str) -> dict:
    return {"cell_type": "raw", "id": cell_id, "metadata": {}, "source": lines(text)}


def markdown_cell(cell_id: str, text: str) -> dict:
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": lines(text)}


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": KERNEL_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook(relative_path: str, cells: list[dict]) -> None:
    path = ROOT / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(notebook(cells), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def front_matter(title: str, description: str, category: str, page_type: str) -> str:
    safe_title = title.replace('"', '\\"')
    safe_description = description.replace('"', '\\"')
    return f'''---
title: "{safe_title}"
description: "{safe_description}"
author: "Edukron Notes"
date: "{DATE}"
categories: [{page_type}, {category}]
toc: true
page-layout: article
execute: false
---'''


def overview_cards(kind: str) -> str:
    if kind == "interview":
        return '''<div class="overview-grid">
  <div class="overview-card"><i class="bi bi-check2-circle" aria-hidden="true"></i><strong>Concept checks</strong><span>Clear definitions and concise explanations.</span></div>
  <div class="overview-card"><i class="bi bi-signpost-split" aria-hidden="true"></i><strong>Scenario questions</strong><span>Trade-offs, diagnosis, and design decisions.</span></div>
  <div class="overview-card"><i class="bi bi-terminal" aria-hidden="true"></i><strong>Practical rounds</strong><span>Code, SQL, configuration, and troubleshooting prompts.</span></div>
  <div class="overview-card"><i class="bi bi-chat-square-text" aria-hidden="true"></i><strong>Answer guides</strong><span>Short answer, deep dive, example, and follow-up format.</span></div>
</div>'''
    if kind == "project":
        return '''<div class="overview-grid">
  <div class="overview-card"><i class="bi bi-bullseye" aria-hidden="true"></i><strong>Problem and scope</strong><span>Business goal, users, constraints, and success measures.</span></div>
  <div class="overview-card"><i class="bi bi-diagram-3" aria-hidden="true"></i><strong>Architecture</strong><span>Components, interfaces, data flow, and design choices.</span></div>
  <div class="overview-card"><i class="bi bi-tools" aria-hidden="true"></i><strong>Implementation</strong><span>Build sequence, validation gates, and deliverables.</span></div>
  <div class="overview-card"><i class="bi bi-activity" aria-hidden="true"></i><strong>Operations</strong><span>Deployment, monitoring, security, cost, and improvement.</span></div>
</div>'''
    return '''<div class="overview-grid">
  <div class="overview-card"><i class="bi bi-journal-text" aria-hidden="true"></i><strong>Concept notes</strong><span>Plain-language explanations and useful mental models.</span></div>
  <div class="overview-card"><i class="bi bi-code-square" aria-hidden="true"></i><strong>Worked examples</strong><span>Code, commands, diagrams, or configurations with commentary.</span></div>
  <div class="overview-card"><i class="bi bi-pencil-square" aria-hidden="true"></i><strong>Practice</strong><span>Checks, exercises, and guided challenges in the notebook.</span></div>
  <div class="overview-card"><i class="bi bi-check2-circle" aria-hidden="true"></i><strong>Recap</strong><span>Key takeaways, common mistakes, and interview prompts.</span></div>
</div>'''


def status_table(kind: str) -> str:
    if kind == "interview":
        rows = [
            ("Question groups", "Curriculum review"),
            ("Difficulty levels", "Curriculum review"),
            ("Answer guides", "Scheduled after question approval"),
            ("Mock interview set", "Scheduled after question approval"),
        ]
    elif kind == "project":
        rows = [
            ("Use case", "Curriculum review"),
            ("Technology stack", "Curriculum review"),
            ("Architecture and stages", "Scheduled after flow approval"),
            ("Implementation notebooks", "Scheduled after flow approval"),
        ]
    else:
        rows = [
            ("Modules", "Curriculum review"),
            ("Datasets and examples", "Curriculum review"),
            ("Exercises and assessments", "Scheduled after module approval"),
            ("Capstone", "Scheduled after sequence approval"),
        ]
    table = ["| Overview component | Current status |", "|---|---|"]
    table.extend(f"| {name} | {status} |" for name, status in rows)
    return "\n".join(table)


def item_overview(track: dict, slug: str, title: str, description: str) -> list[dict]:
    page_label = {
        "course": "Course overview",
        "interview": "Interview-track overview",
        "project": "Project-flow overview",
    }[track["kind"]]
    module_label = {
        "course": "Course modules",
        "interview": "Question collections",
        "project": "Implementation stages",
    }[track["kind"]]
    icon = ITEM_ICONS[track["key"]][slug]
    return [
        raw_cell("front-matter", front_matter(f"{title} — Overview", description, track["key"], page_label.replace(" ", "-"))),
        markdown_cell(
            "overview-hero",
            f'''<div class="course-overview-hero">
<div class="overview-lead">
<span class="topic-icon"><i class="bi bi-{icon}" aria-hidden="true"></i></span>
<div><span class="overview-eyebrow">{page_label}</span><p>{description}</p></div>
</div>
</div>

<div class="overview-meta">
  <div><span>Learning path</span><strong>{track["title"]}</strong></div>
  <div><span>Format</span><strong>Jupyter notebooks</strong></div>
  <div><span>Content status</span><strong>Overview ready</strong></div>
</div>''',
        ),
        markdown_cell(
            "purpose",
            f'''## Purpose

This is the course map for **{title}** inside the **{track["title"]}** learning path. It defines the learning format and provides a stable home for the detailed notebook sequence.''',
        ),
        markdown_cell(
            "notebook-standard",
            f'''## Notebook format

Every approved topic will be published as a focused `.ipynb` lesson using the same readable structure:

{overview_cards(track["kind"])}''',
        ),
        markdown_cell(
            "content-status",
            f'''## {module_label}

::: {{.callout-note}}
### Syllabus in preparation
The detailed sequence will be published here after the curriculum is approved.
:::

{status_table(track["kind"])}''',
        ),
        markdown_cell(
            "back-link",
            f'''[<i class="bi bi-arrow-left" aria-hidden="true"></i> Back to {track["title"]}](index.html)''',
        ),
    ]


def track_index(track: dict) -> list[dict]:
    cards = "\n".join(
        f'  <a class="course-card" href="{slug}.html"><span class="card-icon"><i class="bi bi-{ITEM_ICONS[track["key"]][slug]}" aria-hidden="true"></i></span><span class="course-number">Overview</span><strong>{title}</strong><span>{description}</span></a>'
        for slug, title, description in track["items"]
    )
    page_label = "Learning path" if track["kind"] == "course" else track["title"]
    return [
        raw_cell("front-matter", front_matter(f'{track["title"]} — Overview', track["description"], track["key"], "program-overview")),
        markdown_cell(
            "program-intro",
            f'''<div class="program-intro">
<div class="overview-lead">
<span class="topic-icon"><i class="bi bi-{track["icon"]}" aria-hidden="true"></i></span>
<div><span class="overview-eyebrow">{page_label}</span><p>{track["description"]}</p></div>
</div>
</div>

::: {{.callout-tip}}
### Course map
Each subject has a dedicated overview. Detailed notebooks are added in the approved learning sequence.
:::''',
        ),
        markdown_cell(
            "program-items",
            f'''## Choose an overview

<div class="feature-grid curriculum-grid">
{cards}
</div>''',
        ),
        markdown_cell(
            "publishing-standard",
            f'''## Publishing standard

All material in this section will remain notebook-first: white reading surfaces, clear explanations, runnable or copy-ready examples where appropriate, visible outputs, exercises, and concise recaps. Each approved module will receive its own Jupyter notebook and a stable place in this course map.''',
        ),
    ]


def home_page() -> list[dict]:
    def track_card(track: dict) -> str:
        item_count = len(track["items"])
        item_label = "subjects" if track["kind"] == "course" else "collections"
        return f'''  <a class="blog-card" href="{track["directory"]}/index.html">
    <span class="card-icon"><i class="bi bi-{track["icon"]}" aria-hidden="true"></i></span>
    <span class="blog-card-copy"><span class="course-number">{item_count} {item_label}</span><strong>{track["title"]}</strong><span>{track["description"]}</span></span>
    <i class="bi bi-arrow-up-right" aria-hidden="true"></i>
  </a>'''

    course_cards = "\n".join(track_card(track) for track in TRACKS[:3])
    resource_cards = "\n".join(track_card(track) for track in TRACKS[3:])
    return [
        raw_cell(
            "front-matter",
            '''---
title: false
page-layout: full
toc: false
title-block-banner: false
execute: false
---''',
        ),
        markdown_cell(
            "masthead",
            '''<div class="blog-masthead">
<div>
<span class="blog-kicker">Technical notebook library</span>
<h1>Edukron Notes</h1>
<p>Course maps, executable tutorials, interview preparation, and implementation flows for AI, data engineering, and DevOps.</p>
</div>
<div class="masthead-mark" aria-hidden="true"><i class="bi bi-journal-code"></i></div>
</div>''',
        ),
        markdown_cell(
            "courses",
            f'''<div class="section-heading"><div><span>Courses</span><h2>Learning paths</h2></div><p>Structured from foundations to applied delivery.</p></div>

<div class="blog-grid blog-grid-primary">
{course_cards}
</div>''',
        ),
        markdown_cell(
            "resources",
            f'''<div class="section-heading"><div><span>Practice</span><h2>Interview and project libraries</h2></div><p>Focused preparation and end-to-end delivery maps.</p></div>

<div class="blog-grid">
{resource_cards}
</div>''',
        ),
        markdown_cell(
            "featured",
            '''<div class="section-heading"><div><span>Notebook archive</span><h2>Featured tutorials</h2></div><p>Runnable lessons from the existing library.</p></div>

<div class="article-list">
  <a href="courses/data-science/data-cleaning.html"><span class="article-icon"><i class="bi bi-funnel" aria-hidden="true"></i></span><span><strong>Cleaning real-world data</strong><small>Data Science · executable notebook</small></span><i class="bi bi-arrow-right" aria-hidden="true"></i></a>
  <a href="posts/gradient-descent.html"><span class="article-icon"><i class="bi bi-graph-down-arrow" aria-hidden="true"></i></span><span><strong>Gradient descent, visually</strong><small>Machine Learning · executable notebook</small></span><i class="bi bi-arrow-right" aria-hidden="true"></i></a>
  <a href="courses/machine-learning/kmeans-from-scratch.html"><span class="article-icon"><i class="bi bi-bounding-box-circles" aria-hidden="true"></i></span><span><strong>K-means from scratch</strong><small>Machine Learning · executable notebook</small></span><i class="bi bi-arrow-right" aria-hidden="true"></i></a>
  <a href="courses/artificial-intelligence/search-and-astar.html"><span class="article-icon"><i class="bi bi-signpost-split" aria-hidden="true"></i></span><span><strong>Search with A*</strong><small>Artificial Intelligence · executable notebook</small></span><i class="bi bi-arrow-right" aria-hidden="true"></i></a>
</div>''',
        ),
    ]


def main() -> None:
    write_notebook("index.ipynb", home_page())
    for track in TRACKS:
        write_notebook(f'{track["directory"]}/index.ipynb', track_index(track))
        for slug, title, description in track["items"]:
            write_notebook(
                f'{track["directory"]}/{slug}.ipynb',
                item_overview(track, slug, title, description),
            )
    page_count = 1 + sum(1 + len(track["items"]) for track in TRACKS)
    print(f"Generated {page_count} overview notebooks.")


if __name__ == "__main__":
    main()

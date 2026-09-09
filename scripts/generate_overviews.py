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
  <div class="overview-card"><strong>Concept checks</strong><span>Clear definitions and concise explanations.</span></div>
  <div class="overview-card"><strong>Scenario questions</strong><span>Trade-offs, diagnosis, and design decisions.</span></div>
  <div class="overview-card"><strong>Practical rounds</strong><span>Code, SQL, configuration, and troubleshooting prompts.</span></div>
  <div class="overview-card"><strong>Answer guides</strong><span>Short answer, deep dive, example, and follow-up format.</span></div>
</div>'''
    if kind == "project":
        return '''<div class="overview-grid">
  <div class="overview-card"><strong>Problem and scope</strong><span>Business goal, users, constraints, and success measures.</span></div>
  <div class="overview-card"><strong>Architecture</strong><span>Components, interfaces, data flow, and design choices.</span></div>
  <div class="overview-card"><strong>Implementation</strong><span>Build sequence, validation gates, and deliverables.</span></div>
  <div class="overview-card"><strong>Operations</strong><span>Deployment, monitoring, security, cost, and improvement.</span></div>
</div>'''
    return '''<div class="overview-grid">
  <div class="overview-card"><strong>Concept notes</strong><span>Plain-language explanations and useful mental models.</span></div>
  <div class="overview-card"><strong>Worked examples</strong><span>Code, commands, diagrams, or configurations with commentary.</span></div>
  <div class="overview-card"><strong>Practice</strong><span>Checks, exercises, and guided challenges in the notebook.</span></div>
  <div class="overview-card"><strong>Recap</strong><span>Key takeaways, common mistakes, and interview prompts.</span></div>
</div>'''


def status_table(kind: str) -> str:
    if kind == "interview":
        rows = [
            ("Question groups", "Awaiting your topic list"),
            ("Difficulty levels", "Awaiting your preference"),
            ("Answer depth", "Awaiting your examples or notes"),
            ("Mock interview set", "Added after questions are approved"),
        ]
    elif kind == "project":
        rows = [
            ("Use case", "Awaiting your project scenario"),
            ("Technology stack", "Awaiting your selected services and tools"),
            ("Architecture and stages", "Added from your project flow"),
            ("Implementation notebooks", "Added after the flow is approved"),
        ]
    else:
        rows = [
            ("Modules", "Awaiting your course contents"),
            ("Datasets and examples", "Awaiting your preferred material"),
            ("Exercises and assessments", "Added after modules are approved"),
            ("Capstone", "Added after the learning sequence is confirmed"),
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
    next_request = {
        "course": "Send the module names in the order you want them taught. You can also include notes, links, datasets, exercises, or existing repositories for each module.",
        "interview": "Send the questions or topic groups you want covered, plus the expected experience level and preferred answer depth.",
        "project": "Send the use case, required technologies, expected architecture, and any stages or deliverables that must appear in the flow.",
    }[track["kind"]]
    return [
        raw_cell("front-matter", front_matter(f"{title} — Overview", description, track["key"], page_label.replace(" ", "-"))),
        markdown_cell(
            "overview-hero",
            f'''<section class="course-overview-hero">
  <span class="overview-eyebrow">{page_label}</span>
  <p>{description}</p>
</section>

<div class="overview-meta">
  <div><span>Learning path</span><strong>{track["title"]}</strong></div>
  <div><span>Format</span><strong>Jupyter notebooks</strong></div>
  <div><span>Content status</span><strong>Overview ready</strong></div>
</div>''',
        ),
        markdown_cell(
            "purpose",
            f'''## Purpose

This page is the permanent overview for **{title}** inside the **{track["title"]}** learning path. It establishes where the material will live and how learners will move through it. The detailed syllabus is intentionally open until you provide the course contents.''',
        ),
        markdown_cell(
            "notebook-standard",
            f'''## Notebook format

Every approved topic will be published as a focused `.ipynb` lesson using the same readable structure:

{overview_cards(track["kind"])}''',
        ),
        markdown_cell(
            "content-status",
            f'''## Content status

::: {{.callout-note}}
### Ready for your material
The navigation and overview are published first. No detailed curriculum has been invented or locked in.
:::

{status_table(track["kind"])}''',
        ),
        markdown_cell(
            "next-step",
            f'''## What to send next

{next_request}

[← Back to {track["title"]}](index.html)''',
        ),
    ]


def track_index(track: dict) -> list[dict]:
    cards = "\n".join(
        f'  <a class="course-card" href="{slug}.html"><span class="course-number">Overview</span><strong>{title}</strong><span>{description}</span></a>'
        for slug, title, description in track["items"]
    )
    page_label = "Learning path" if track["kind"] == "course" else track["title"]
    return [
        raw_cell("front-matter", front_matter(f'{track["title"]} — Overview', track["description"], track["key"], "program-overview")),
        markdown_cell(
            "program-intro",
            f'''<section class="program-intro">
  <span class="overview-eyebrow">{page_label}</span>
  <p>{track["description"]}</p>
</section>

::: {{.callout-tip}}
### Overview pages are ready
Choose any item below. Detailed notebook lessons will be added after you provide the contents.
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
    cards = "\n".join(
        f'  <a class="course-card" href="{track["directory"]}/index.html"><span class="course-number">Top-level menu</span><strong>{track["title"]}</strong><span>{track["description"]}</span></a>'
        for track in TRACKS
    )
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
            "hero",
            '''<section class="hero">
  <div class="hero-kicker">Notebook-first learning library</div>
  <h1>Learn technology by working through it.</h1>
  <p>Edukron Notes organizes AI, data engineering, and DevOps into clear learning paths. Every published lesson is a Jupyter notebook designed for notes, examples, outputs, practice, and revision.</p>
  <div class="hero-actions"><a href="courses/full-stack-ai/index.html">Explore Full Stack AI</a><a href="courses/azure-data-engineering/index.html">Explore Data Engineering</a></div>
</section>''',
        ),
        markdown_cell(
            "paths",
            f'''## Top-level learning paths

<div class="feature-grid program-grid">
{cards}
</div>''',
        ),
        markdown_cell(
            "status",
            '''## Curriculum status

The complete navigation and individual overview pages are ready. Detailed module notebooks will be added from the course contents you provide next.

<div class="overview-meta home-meta">
  <div><span>Course overviews</span><strong>30</strong></div>
  <div><span>Interview overviews</span><strong>3</strong></div>
  <div><span>Project-flow overviews</span><strong>3</strong></div>
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

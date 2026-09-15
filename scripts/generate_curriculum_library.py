"""Generate the 200-topic, 2,000-notebook Edukron Notes curriculum library."""

from __future__ import annotations

import json
import os
import re
from collections import defaultdict
from pathlib import Path

from curriculum_catalog import Topic, load_catalog


ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-09-14"

KERNEL_METADATA = {
    "kernelspec": {
        "display_name": "Python (Notebook Blog)",
        "language": "python",
        "name": "notebook-blog",
    },
    "language_info": {
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "pygments_lexer": "ipython3",
        "version": "3.12",
    },
}

COURSE_PATHS = {
    ("Full Stack AI", "Python"): "courses/full-stack-ai/python",
    ("Full Stack AI", "SQL"): "courses/full-stack-ai/sql",
    ("Full Stack AI", "Data Science"): "courses/full-stack-ai/data-science",
    ("Full Stack AI", "Machine Learning"): "courses/full-stack-ai/machine-learning",
    ("Full Stack AI", "Artificial Intelligence"): "courses/full-stack-ai/artificial-intelligence",
    ("Full Stack AI", "Deep Learning"): "courses/full-stack-ai/deep-learning",
    ("Full Stack AI", "Generative AI"): "courses/full-stack-ai/generative-ai",
    ("Full Stack AI", "Large Language Models"): "courses/full-stack-ai/large-language-models",
    ("Full Stack AI", "RAG"): "courses/full-stack-ai/rag",
    ("Full Stack AI", "Agentic AI"): "courses/full-stack-ai/agentic-ai",
    ("Azure Data Engineering", "Python"): "courses/azure-data-engineering/python",
    ("Azure Data Engineering", "SQL"): "courses/azure-data-engineering/sql",
    ("Azure Data Engineering", "Data Engineering Fundamentals"): "courses/azure-data-engineering/fundamentals",
    ("Azure Data Engineering", "Azure Data Factory"): "courses/azure-data-engineering/azure-data-factory",
    ("Azure Data Engineering", "ADLS Gen2"): "courses/azure-data-engineering/adls-gen2",
    ("Azure Data Engineering", "Azure Databricks"): "courses/azure-data-engineering/azure-databricks",
    ("Azure Data Engineering", "PySpark"): "courses/azure-data-engineering/pyspark",
    ("Azure Data Engineering", "Azure Synapse Analytics"): "courses/azure-data-engineering/azure-synapse",
    ("Azure Data Engineering", "Microsoft Fabric"): "courses/azure-data-engineering/microsoft-fabric",
    ("Azure Data Engineering", "Delta Lake"): "courses/azure-data-engineering/delta-lake",
    ("Azure DevOps", "Linux & Shell Scripting"): "courses/azure-devops/linux-shell-scripting",
    ("Azure DevOps", "Git & Version Control"): "courses/azure-devops/git-version-control",
    ("Azure DevOps", "Azure Repos"): "courses/azure-devops/azure-repos",
    ("Azure DevOps", "Azure Pipelines"): "courses/azure-devops/azure-pipelines",
    ("Azure DevOps", "YAML Pipeline Development"): "courses/azure-devops/yaml-pipelines",
    ("Azure DevOps", "Docker & Containerization"): "courses/azure-devops/docker",
    ("Azure DevOps", "Kubernetes & AKS"): "courses/azure-devops/kubernetes-aks",
    ("Azure DevOps", "Terraform Infrastructure as Code"): "courses/azure-devops/terraform",
    ("Azure DevOps", "Azure Cloud Services"): "courses/azure-devops/azure-cloud-services",
    ("Azure DevOps", "DevSecOps & Monitoring"): "courses/azure-devops/devsecops-monitoring",
    ("Interview Questions", "Full Stack AI"): "interview-questions/full-stack-ai",
    ("Interview Questions", "Azure Data Engineering"): "interview-questions/azure-data-engineering",
    ("Interview Questions", "Azure DevOps"): "interview-questions/azure-devops",
    ("Project Flows", "Full Stack AI"): "project-flows/full-stack-ai",
    ("Project Flows", "Azure Data Engineering"): "project-flows/azure-data-engineering",
    ("Project Flows", "Azure DevOps"): "project-flows/azure-devops",
}

REFERENCES = {
    "Python": ("Python documentation", "https://docs.python.org/3/"),
    "SQL": ("PostgreSQL SQL tutorial", "https://www.postgresql.org/docs/current/tutorial-sql.html"),
    "Data Science": ("pandas user guide", "https://pandas.pydata.org/docs/user_guide/"),
    "Machine Learning": ("scikit-learn user guide", "https://scikit-learn.org/stable/user_guide.html"),
    "Artificial Intelligence": ("Artificial Intelligence: Foundations of Computational Agents", "https://artint.info/3e/html/ArtInt3e.html"),
    "Deep Learning": ("PyTorch tutorials", "https://docs.pytorch.org/tutorials/"),
    "Generative AI": ("Microsoft generative AI fundamentals", "https://learn.microsoft.com/training/paths/introduction-generative-ai/"),
    "Large Language Models": ("Hugging Face course", "https://huggingface.co/learn/llm-course/"),
    "RAG": ("Azure AI Search RAG overview", "https://learn.microsoft.com/azure/search/retrieval-augmented-generation-overview"),
    "Agentic AI": ("Microsoft AI agents overview", "https://learn.microsoft.com/azure/ai-foundry/agents/overview"),
    "Data Engineering Fundamentals": ("Azure Architecture Center data guide", "https://learn.microsoft.com/azure/architecture/data-guide/"),
    "Azure Data Factory": ("Azure Data Factory documentation", "https://learn.microsoft.com/azure/data-factory/"),
    "ADLS Gen2": ("Azure Data Lake Storage documentation", "https://learn.microsoft.com/azure/storage/blobs/data-lake-storage-introduction"),
    "Azure Databricks": ("Azure Databricks documentation", "https://learn.microsoft.com/azure/databricks/"),
    "PySpark": ("Apache Spark Python API", "https://spark.apache.org/docs/latest/api/python/"),
    "Azure Synapse Analytics": ("Azure Synapse documentation", "https://learn.microsoft.com/azure/synapse-analytics/"),
    "Microsoft Fabric": ("Microsoft Fabric documentation", "https://learn.microsoft.com/fabric/"),
    "Delta Lake": ("Delta Lake documentation", "https://docs.delta.io/latest/"),
    "Linux & Shell Scripting": ("GNU Bash manual", "https://www.gnu.org/software/bash/manual/"),
    "Git & Version Control": ("Git reference", "https://git-scm.com/docs"),
    "Azure Repos": ("Azure Repos documentation", "https://learn.microsoft.com/azure/devops/repos/"),
    "Azure Pipelines": ("Azure Pipelines documentation", "https://learn.microsoft.com/azure/devops/pipelines/"),
    "YAML Pipeline Development": ("Azure Pipelines YAML schema", "https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/"),
    "Docker & Containerization": ("Docker manuals", "https://docs.docker.com/manuals/"),
    "Kubernetes & AKS": ("Kubernetes documentation", "https://kubernetes.io/docs/"),
    "Terraform Infrastructure as Code": ("Terraform language documentation", "https://developer.hashicorp.com/terraform/language"),
    "Azure Cloud Services": ("Azure Architecture Center", "https://learn.microsoft.com/azure/architecture/"),
    "DevSecOps & Monitoring": ("Azure Well-Architected Framework", "https://learn.microsoft.com/azure/well-architected/"),
}


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")[:72]


def source_lines(text: str) -> list[str]:
    return (text.strip() + "\n").splitlines(keepends=True)


def raw_cell(cell_id: str, text: str) -> dict:
    return {"cell_type": "raw", "id": cell_id, "metadata": {}, "source": source_lines(text)}


def markdown_cell(cell_id: str, text: str) -> dict:
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source_lines(text)}


def code_cell(cell_id: str, text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": {},
        "outputs": [],
        "source": source_lines(text),
    }


def write_notebook(path: Path, cells: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    notebook = {
        "cells": cells,
        "metadata": KERNEL_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def course_path(topic: Topic) -> Path:
    return ROOT / f"{COURSE_PATHS[(topic.section, topic.course)]}.ipynb"


def lesson_path(topic: Topic, lesson_number: int, lesson: str) -> Path:
    overview = course_path(topic)
    folder = overview.with_suffix("") / f"{topic.number:03d}-{slugify(topic.title)}"
    return folder / f"{lesson_number:02d}-{slugify(lesson)}.ipynb"


def html_link(source: Path, target: Path) -> str:
    relative = os.path.relpath(target.with_suffix(".html"), source.parent)
    return Path(relative).as_posix()


def profile(topic: Topic) -> tuple[str, str, str, str]:
    course = topic.course
    if course in {"SQL", "Azure Synapse Analytics", "Microsoft Fabric"}:
        return ("data contract", "query or transformation", "validated dataset", "sql")
    if course in {"Python", "Data Science", "Machine Learning", "Artificial Intelligence", "Deep Learning"}:
        return ("typed input", "reproducible computation", "tested result", "python")
    if course in {"Azure Data Factory", "Azure Pipelines", "YAML Pipeline Development"}:
        return ("versioned configuration", "orchestrated stages", "auditable run", "yaml")
    if course in {"Docker & Containerization"}:
        return ("application source", "repeatable image build", "immutable artifact", "dockerfile")
    if course in {"Kubernetes & AKS"}:
        return ("declarative workload", "cluster reconciliation", "healthy service", "yaml")
    if course in {"Terraform Infrastructure as Code", "Azure Cloud Services"}:
        return ("desired infrastructure", "reviewed plan", "managed cloud state", "hcl")
    if course in {"Linux & Shell Scripting", "Git & Version Control", "Azure Repos"}:
        return ("versioned intent", "safe command workflow", "verifiable system state", "bash")
    if course in {"PySpark", "Azure Databricks", "Delta Lake", "ADLS Gen2", "Data Engineering Fundamentals"}:
        return ("governed source data", "distributed transformation", "quality-assured data product", "python")
    if topic.section == "Interview Questions":
        return ("clear question", "structured reasoning", "evidence-backed answer", "text")
    if topic.section == "Project Flows":
        return ("approved requirement", "controlled delivery workflow", "operable product", "text")
    return ("trusted context", "bounded intelligent workflow", "evaluated response", "python")


def example_block(topic: Topic, lesson: str) -> str:
    source, process, outcome, language = profile(topic)
    safe_name = slugify(lesson).replace("-", "_")[:32]
    if language == "sql":
        return f'''```sql
-- {lesson}: express intent, preserve lineage, and expose quality evidence.
WITH validated_input AS (
    SELECT *, CURRENT_TIMESTAMP AS processed_at
    FROM source_data
    WHERE business_key IS NOT NULL
),
deduplicated AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY business_key ORDER BY processed_at DESC
    ) AS record_rank
    FROM validated_input
)
SELECT * FROM deduplicated WHERE record_rank = 1;
```'''
    if language == "yaml":
        return f'''```yaml
# {lesson}: a small, reviewable unit of orchestration.
name: {slugify(lesson)}
inputs:
  source: {slugify(source)}
steps:
  - validate: contract
  - run: {slugify(process)}
  - verify: acceptance-criteria
outputs:
  artifact: {slugify(outcome)}
```'''
    if language == "dockerfile":
        return f'''```dockerfile
# {lesson}: deterministic build with a non-root runtime.
FROM python:3.12-slim AS runtime
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER 10001
CMD ["python", "-m", "app"]
```'''
    if language == "hcl":
        return f'''```hcl
# {lesson}: explicit inputs and observable outputs.
variable "environment" {{ type = string }}

locals {{
  workload_name = "edukron-${{var.environment}}"
  tags = {{ managed_by = "terraform", lesson = "{safe_name}" }}
}}

output "workload_name" {{ value = local.workload_name }}
```'''
    if language == "bash":
        return f'''```bash
#!/usr/bin/env bash
set -Eeuo pipefail
readonly WORKFLOW="{slugify(lesson)}"
printf 'starting %s\\n' "$WORKFLOW"
# validate -> change -> verify; return a non-zero code on failure
printf 'completed %s\\n' "$WORKFLOW"
```'''
    if language == "text":
        return f'''```text
Context: {topic.title}
Objective: demonstrate {lesson.lower()} with measurable acceptance criteria.
Decision: choose the smallest design that satisfies reliability and security.
Evidence: tests, logs, review notes, and a rollback or correction path.
Result: explain the tradeoff, not only the chosen technology.
```'''
    return f'''```python
from dataclasses import dataclass

@dataclass(frozen=True)
class {''.join(part.title() for part in safe_name.split('_'))[:40]}Plan:
    input_contract: str = "{source}"
    operation: str = "{process}"
    acceptance_evidence: str = "{outcome}"

plan = {''.join(part.title() for part in safe_name.split('_'))[:40]}Plan()
assert all(vars(plan).values())
plan
```'''


def lesson_cells(topic: Topic, lesson_number: int, lesson: str, previous: Path | None, following: Path | None) -> list[dict]:
    source, process, outcome, _ = profile(topic)
    path = lesson_path(topic, lesson_number, lesson)
    reference_title, reference_url = REFERENCES.get(topic.course, REFERENCES.get(topic.section, ("Microsoft Learn", "https://learn.microsoft.com/")))
    prereq = topic.lessons[lesson_number - 2] if lesson_number > 1 else "the course overview and the topic's purpose"
    next_skill = topic.lessons[lesson_number] if lesson_number < 10 else "the next syllabus topic or a portfolio extension"
    context = f"{topic.section} → {topic.course} → {topic.title}"
    frontmatter = f'''---
title: "{topic.number:03d}.{lesson_number:02d} {lesson.replace('"', "'")}"
description: "Notebook tutorial for {lesson.replace('"', "'")} in {topic.title.replace('"', "'")}."
categories: ["{topic.section}", "{topic.course}", "{topic.title}"]
toc: true
title-block-banner: false
code-fold: false
execute: false
---'''
    nav_parts = []
    if previous:
        nav_parts.append(f'<a class="lesson-nav-link" href="{html_link(path, previous)}"><span>← Previous</span><strong>{previous.stem[3:].replace("-", " ").title()}</strong></a>')
    nav_parts.append(f'<a class="lesson-nav-home" href="{html_link(path, course_path(topic))}"><span>Course overview</span><strong>{topic.course}</strong></a>')
    if following:
        nav_parts.append(f'<a class="lesson-nav-link lesson-nav-next" href="{html_link(path, following)}"><span>Next →</span><strong>{following.stem[3:].replace("-", " ").title()}</strong></a>')

    cells = [
        raw_cell("front-matter", frontmatter),
        markdown_cell("lesson-banner", f'''<div class="notebook-chrome lesson-notebook">
<div class="notebook-toolbar">
<span class="notebook-file"><i class="bi bi-journal-code" aria-hidden="true"></i><strong>{path.name}</strong></span>
<span class="notebook-status"><i class="bi bi-check-circle-fill" aria-hidden="true"></i> Trusted</span>
<span class="notebook-kernel"><i class="bi bi-cpu" aria-hidden="true"></i> Python 3</span>
</div>
<div class="notebook-cover">
<span class="lesson-kicker">Topic {topic.number:03d} · Lesson {lesson_number:02d}</span>
<h1>{lesson}</h1>
<p>{context}. Learn the concept, apply a repeatable workflow, and produce evidence that the result is correct.</p>
</div>
</div>'''),
        markdown_cell("placement", f'''## Placement and prerequisites

This notebook develops **{lesson}** as a focused lesson in **{topic.title}**. It assumes familiarity with **{prereq}**. No cloud credentials are required: platform examples are copy-ready patterns, and the executable checks use only Python's standard library.

### Learning objectives

By the end, you will be able to:

1. Explain where {lesson.lower()} belongs in the wider {topic.course} workflow.
2. Translate a requirement into an explicit {source}, {process}, and {outcome}.
3. Apply security, reliability, and observability checks before calling the work complete.
4. Defend design tradeoffs and recognize the most common failure modes.'''),
        markdown_cell("foundations", f'''## Concept foundations

**{lesson}** is useful when it converts intent into a result that another person or system can inspect. In this topic, the essential chain is **{source} → {process} → {outcome}**. Skipping any link creates ambiguity: an undefined input makes results untrustworthy, an implicit process is difficult to repeat, and an outcome without evidence is difficult to operate.

Treat the lesson as a contract, not a one-time command. State what enters the boundary, which assumptions are valid, what changes, and how success is measured. This framing works for code, data, cloud resources, interview answers, and project delivery because it separates the goal from the implementation detail.

Three qualities should be designed together:

- **Correctness:** acceptance criteria and tests prove that the intended behavior occurred.
- **Safety:** permissions, secrets, validation, and rollback limit the impact of mistakes.
- **Operability:** logs, metrics, ownership, and runbooks make the result supportable after release.

The first implementation should be intentionally small. Add scale, abstraction, or automation only after a baseline works and its evidence is visible. This keeps failure analysis local and makes every later optimization measurable.'''),
        markdown_cell("mental-model", f'''## Mental model

| Layer | Question | Evidence to retain |
|---|---|---|
| Purpose | Why do we need {lesson.lower()}? | Requirement and measurable outcome |
| Input | What {source} crosses the boundary? | Schema, version, owner, sensitivity |
| Process | How does {process} behave? | Reviewed configuration or code |
| Output | What makes the {outcome} usable? | Contract, checks, and consumer sign-off |
| Operations | What happens when it fails? | Telemetry, alert, recovery, and owner |

The table is a compact design review. If a row cannot be answered, record it as an assumption or risk before implementation.'''),
        markdown_cell("workflow", f'''## A repeatable workflow

1. **Frame the outcome.** Write one sentence describing the user or system value of {lesson.lower()}.
2. **Inventory constraints.** Capture scale, latency, cost, privacy, compatibility, and team skills.
3. **Define the contract.** Specify the {source}, normal cases, edge cases, and the expected {outcome}.
4. **Build the smallest slice.** Implement one path through {process} and keep it reproducible.
5. **Verify deliberately.** Test success, empty input, invalid input, partial failure, and retry behavior.
6. **Operationalize.** Add ownership, telemetry, documentation, and a safe correction or rollback path.

This order prevents tool selection from replacing problem definition. A production design may loop through the steps several times as evidence changes.'''),
        markdown_cell("example", f'''## Annotated example

The following pattern is intentionally compact. Adapt names and platform-specific properties, but retain the explicit input, transformation, output, and verification boundary.

{example_block(topic, lesson)}

### How to read it

The example names the unit of work, exposes inputs, and makes success inspectable. It avoids embedded secrets and hidden environment assumptions. In a real repository, pair it with automated validation, pinned dependencies, and a short operational note.'''),
        code_cell("executable-model", f'''from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class LessonContract:
    lesson: str
    source: str
    process: str
    outcome: str
    evidence: tuple[str, ...]

contract = LessonContract(
    lesson={lesson!r},
    source={source!r},
    process={process!r},
    outcome={outcome!r},
    evidence=("automated check", "review record", "operational signal"),
)

assert contract.lesson and len(contract.evidence) >= 3
asdict(contract)'''),
        markdown_cell("walkthrough", f'''## Walkthrough and design decisions

The executable contract above is a small design artifact. Immutability prevents accidental mutation during the lesson, while named fields make assumptions reviewable. The assertion is deliberately simple: it shows that a notebook should verify its own essential invariant rather than depend on visual inspection alone.

For **{lesson}**, enrich the contract with domain-specific limits. Examples include data schemas, model thresholds, deployment health checks, access policies, response-time budgets, or answer-scoring rubrics. Keep the core contract stable while implementation details evolve.

> **Decision rule:** prefer a design that makes failure visible and recovery routine over one that succeeds only under ideal conditions.'''),
        markdown_cell("guided-lab", f'''## Guided lab

**Scenario:** Your team must introduce {lesson.lower()} as part of {topic.title}. The first release serves one controlled environment, but it must be safe to repeat and simple to audit.

1. Write a one-sentence outcome and name the consumer.
2. List three properties of the {source} that must be validated.
3. Break {process} into three independently verifiable steps.
4. Define one positive, one boundary, and one failure test.
5. Choose a telemetry signal and a threshold that should alert an owner.
6. Describe a rollback, replay, or correction procedure.

### Acceptance criteria

- Inputs and outputs have named owners and contracts.
- The happy path and at least two failure paths are testable.
- No credentials or environment-specific values are embedded in the artifact.
- A reviewer can determine what ran, which version ran, and whether it succeeded.'''),
        markdown_cell("solution", f'''## Solution blueprint

A strong solution might use the following structure:

| Concern | Example decision for {lesson} |
|---|---|
| Outcome | Deliver a repeatable {outcome} for a named consumer |
| Contract | Reject missing identifiers and incompatible versions before {process} |
| Stages | Validate → perform the smallest change → verify the result |
| Tests | Normal input, empty or boundary input, invalid input, interrupted run |
| Security | Managed identity or scoped secret; least-privilege authorization |
| Telemetry | Run ID, duration, status, item count, and structured error category |
| Recovery | Preserve the last known good state and document replay or rollback |

The exact technology can vary. The important part is traceability from requirement to implementation, test evidence, and operational ownership.'''),
        code_cell("quality-check", f'''required_controls = {{
    "contract": True,
    "automated_check": True,
    "least_privilege": True,
    "telemetry": True,
    "recovery_path": True,
}}

missing = [name for name, present in required_controls.items() if not present]
readiness_score = 100 * (len(required_controls) - len(missing)) / len(required_controls)
assert not missing, f"Missing controls: {{missing}}"
{{"lesson": {lesson!r}, "readiness_score": readiness_score, "status": "ready for review"}}'''),
        markdown_cell("mistakes", f'''## Common mistakes and fixes

- **Starting with the tool.** Restate the outcome and constraints before choosing syntax or a service.
- **Treating the happy path as complete.** Add boundary, invalid-input, interruption, and retry tests.
- **Hiding state.** Version configuration and expose identifiers so a run can be reproduced.
- **Embedding secrets.** Use an approved secret store or workload identity and scope access narrowly.
- **Logging without context.** Include a run or correlation ID, stage, status, duration, and safe error category.
- **Optimizing without a baseline.** Measure correctness, cost, and latency before changing the design.
- **No recovery owner.** Document who responds and how to roll back, replay, or correct the result.'''),
        markdown_cell("practice", f'''## Practice tasks

1. **Explain:** describe {lesson.lower()} to a new teammate without naming a vendor product.
2. **Model:** draw the {source} → {process} → {outcome} boundary and mark trust boundaries.
3. **Implement:** adapt the example to a realistic object from your own project.
4. **Test:** add one assertion for a boundary condition and one for a failure condition.
5. **Operate:** define two metrics, one alert, and the first diagnostic action in a runbook.
6. **Extend:** connect this lesson to **{next_skill}** and identify the new contract between them.'''),
        markdown_cell("knowledge-check", f'''## Knowledge check

1. Why should {lesson.lower()} begin with an outcome rather than a tool choice?
2. Which evidence proves the {outcome} is both correct and operable?
3. Where should validation occur, and what should happen to rejected input?
4. How do idempotency or safe retries change recovery design?
5. Which tradeoff would you discuss in a design review?

<details>
<summary><strong>Suggested answers</strong></summary>

1. Outcomes remain stable while implementation options change; they make alternatives comparable.
2. Use automated checks plus versioned run evidence, telemetry, and consumer acceptance.
3. Validate at the boundary before side effects; quarantine or report rejected input with safe context.
4. They prevent duplicate effects and make replay a controlled recovery mechanism.
5. Explain a concrete balance such as simplicity versus scale, latency versus cost, or autonomy versus control.

</details>'''),
        markdown_cell("recap", f'''## Recap and reference

You can now place **{lesson}** inside **{topic.title}**, define its contract, implement a small verifiable slice, and attach security, reliability, and operational evidence. The durable mental model is:

> **Explicit input → controlled change → verified output → observable operation**

Continue with **{next_skill}** or strengthen this notebook by replacing the sample contract with an artifact from your own portfolio.

Official reference: [{reference_title}]({reference_url})'''),
        markdown_cell("lesson-nav", f'''<nav class="lesson-nav" aria-label="Lesson navigation">
{''.join(nav_parts)}
</nav>'''),
    ]
    return cells


def overview_cells(section: str, course: str, topics: list[Topic]) -> list[dict]:
    overview = course_path(topics[0])
    topic_blocks = []
    for topic in topics:
        links = "\n".join(
            f'<a class="topic-lesson-link" href="{html_link(overview, lesson_path(topic, number, lesson))}"><span>{topic.number:03d}.{number:02d}</span><strong>{lesson}</strong><i class="bi bi-arrow-right"></i></a>'
            for number, lesson in enumerate(topic.lessons, 1)
        )
        topic_blocks.append(f'''<details class="curriculum-topic"{' open' if topic == topics[0] else ''}>
<summary><span class="topic-number">Topic {topic.number:03d}</span><strong>{topic.title}</strong></summary>
<div class="topic-lessons">
{links}
</div>
</details>''')
    topic_html = "\n".join(topic_blocks)
    first = lesson_path(topics[0], 1, topics[0].lessons[0])
    catalog_id = f"{slugify(section)}-{slugify(course)}-catalog"
    return [
        raw_cell("front-matter", f'''---
title: "{course}"
description: "Complete notebook syllabus for {course} in {section}."
toc: false
page-layout: full
title-block-banner: false
execute: false
---'''),
        markdown_cell("course-hero", f'''<div class="course-workspace notebook-chrome">
<div class="notebook-toolbar">
<span class="notebook-file"><i class="bi bi-journal-code" aria-hidden="true"></i><strong>{overview.name}</strong></span>
<span class="notebook-status"><i class="bi bi-check-circle-fill" aria-hidden="true"></i> Trusted</span>
<span class="notebook-kernel"><i class="bi bi-diagram-3" aria-hidden="true"></i> Learning path</span>
</div>
<div class="course-workspace-hero">
<span class="overview-kicker">{section}</span>
<h1>{course}</h1>
<p>A complete notebook-first syllabus organized from foundations to applied delivery. Every lesson combines clear notes, a worked pattern, executable validation, a guided lab, a solution blueprint, practice, and knowledge checks.</p>
<div class="course-tags"><span><i class="bi bi-signpost-split"></i> Foundation to advanced</span><span><i class="bi bi-code-square"></i> Hands-on practice</span><span><i class="bi bi-patch-check"></i> Review ready</span></div>
<p class="course-start"><a class="btn btn-primary" href="{html_link(overview, first)}"><i class="bi bi-play-fill"></i> Start the first notebook</a></p>
</div>
</div>'''),
        markdown_cell("how-to-use", '''## How to use this course

Work through lessons in order for a complete pathway, or open a topic for focused reference. Type or adapt the examples, complete the guided lab before reading its blueprint, and preserve your test evidence as a portfolio artifact. Cloud and infrastructure examples are safe, copy-ready teaching patterns; execute them in your own sandbox only after substituting approved identities, names, and policies.'''),
        markdown_cell("full-syllabus", f'''<div class="syllabus-heading" id="notebook-syllabus">
<div><span class="overview-kicker">Course contents</span><h2>Notebook syllabus</h2><p>Open a topic to browse its lessons, or search the complete course by concept.</p></div>
<label class="syllabus-search" for="{catalog_id}-search"><i class="bi bi-search" aria-hidden="true"></i><input id="{catalog_id}-search" type="search" placeholder="Find a topic or lesson" autocomplete="off" aria-label="Search the {course} syllabus"></label>
</div>

<div class="curriculum-catalog" id="{catalog_id}">
{topic_html}
</div>
<p class="syllabus-empty" id="{catalog_id}-empty" hidden><i class="bi bi-search"></i> No matching lessons were found.</p>

<script>
document.addEventListener("DOMContentLoaded", () => {{
  const catalog = document.getElementById("{catalog_id}");
  const search = document.getElementById("{catalog_id}-search");
  const empty = document.getElementById("{catalog_id}-empty");
  if (!catalog || !search || !empty) return;

  search.addEventListener("input", () => {{
    const query = search.value.trim().toLowerCase();
    let visibleTopics = 0;
    catalog.querySelectorAll(".curriculum-topic").forEach((topic) => {{
      const summary = topic.querySelector("summary");
      const topicMatches = !query || summary.textContent.toLowerCase().includes(query);
      let visibleLessons = 0;
      topic.querySelectorAll(".topic-lesson-link").forEach((lesson) => {{
        const matches = topicMatches || lesson.textContent.toLowerCase().includes(query);
        lesson.hidden = !matches;
        if (matches) visibleLessons += 1;
      }});
      const showTopic = topicMatches || visibleLessons > 0;
      topic.hidden = !showTopic;
      if (showTopic) visibleTopics += 1;
      if (query && showTopic) topic.open = true;
    }});
    empty.hidden = visibleTopics > 0;
  }});
}});
</script>'''),
        markdown_cell("completion-standard", f'''## Completion standard

You have completed **{course}** when you can explain each topic, reproduce its core workflow, pass the notebook checks, defend the main tradeoffs, and combine the lessons into one reviewable portfolio project. Use the practice tasks as evidence rather than treating page reading alone as completion.'''),
    ]


def validate_catalog(topics: list[Topic]) -> None:
    if len(topics) != 200 or [topic.number for topic in topics] != list(range(1, 201)):
        raise ValueError("Catalogue must contain topics 001 through 200 exactly once.")
    if any(len(topic.lessons) != 10 for topic in topics):
        raise ValueError("Every topic must contain exactly ten lessons.")
    missing_paths = {(topic.section, topic.course) for topic in topics} - set(COURSE_PATHS)
    if missing_paths:
        raise ValueError(f"Missing course paths: {sorted(missing_paths)}")


def main() -> None:
    topics = load_catalog()
    validate_catalog(topics)
    by_course: dict[tuple[str, str], list[Topic]] = defaultdict(list)
    all_lessons: list[tuple[Topic, int, str, Path]] = []
    for topic in topics:
        by_course[(topic.section, topic.course)].append(topic)
        for number, lesson in enumerate(topic.lessons, 1):
            all_lessons.append((topic, number, lesson, lesson_path(topic, number, lesson)))

    for position, (topic, number, lesson, path) in enumerate(all_lessons):
        previous = all_lessons[position - 1][3] if position > 0 else None
        following = all_lessons[position + 1][3] if position + 1 < len(all_lessons) else None
        write_notebook(path, lesson_cells(topic, number, lesson, previous, following))

    for (section, course), course_topics in by_course.items():
        write_notebook(course_path(course_topics[0]), overview_cells(section, course, course_topics))

    print(f"Generated {len(all_lessons):,} lesson notebooks across {len(topics)} topics and {len(by_course)} course overviews.")


if __name__ == "__main__":
    main()

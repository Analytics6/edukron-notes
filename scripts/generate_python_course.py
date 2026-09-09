"""Generate the complete Full Stack AI Python notebook course."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "courses" / "full-stack-ai"
LESSON_DIR = COURSE_DIR / "python"
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


def clean(text: str) -> str:
    return textwrap.dedent(text).strip()


def source_lines(text: str) -> list[str]:
    return (clean(text) + "\n").splitlines(keepends=True)


def raw_cell(cell_id: str, text: str) -> dict:
    return {"cell_type": "raw", "id": cell_id, "metadata": {}, "source": source_lines(text)}


def markdown_cell(cell_id: str, text: str) -> dict:
    return {"cell_type": "markdown", "id": cell_id, "metadata": {}, "source": source_lines(text)}


def code_cell(cell_id: str, text: str, *, folded: bool = False) -> dict:
    metadata = {"code-fold": True, "code-summary": "Show solution"} if folded else {}
    return {
        "cell_type": "code",
        "execution_count": None,
        "id": cell_id,
        "metadata": metadata,
        "outputs": [],
        "source": source_lines(text),
    }


def write_notebook(path: Path, cells: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "cells": cells,
        "metadata": KERNEL_METADATA,
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path.write_text(json.dumps(document, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def lesson(number, slug, title, summary, objectives, concepts, worked, practice, solution, quiz, recap):
    return {
        "number": number,
        "slug": slug,
        "title": title,
        "summary": clean(summary),
        "objectives": objectives,
        "concepts": concepts,
        "worked": worked,
        "practice": clean(practice),
        "solution": clean(solution),
        "quiz": quiz,
        "recap": recap,
    }


LESSONS = [
    lesson(
        "01",
        "language-foundations",
        "Python Language Foundations",
        "Build accurate mental models for values, names, types, expressions, input, and readable scripts.",
        [
            "Explain how names reference Python objects.",
            "Use numbers, strings, booleans, and `None` deliberately.",
            "Convert values safely and format output with f-strings.",
            "Turn a small requirement into a readable sequence of statements.",
        ],
        [
            (
                "Values, objects, and names",
                """Python evaluates expressions into objects. A variable is a name bound to an object; it is not a box with a permanent type. `type()` reports the object's type, while `id()` identifies the object during one process. Use descriptive `snake_case` names and reserve uppercase names for constants by convention.""",
                """course_name = "Full Stack AI"
lesson_count = 18
completion_rate = 0.75
is_active = True
next_lesson = None

for name, value in {
    "course_name": course_name,
    "lesson_count": lesson_count,
    "completion_rate": completion_rate,
    "is_active": is_active,
    "next_lesson": next_lesson,
}.items():
    print(f"{name:16} -> {value!r:20} ({type(value).__name__})")""",
            ),
            (
                "Expressions and safe conversion",
                """Operators combine values. Arithmetic operators produce numbers; comparison operators produce booleans; `and`, `or`, and `not` combine truth values. Input arrives as text, so convert at the boundary and keep the rest of the program strongly shaped. Division with `/` always returns a float; `//` is floor division and `%` gives the remainder.""",
                """raw_price = "2499.50"
raw_quantity = "3"

price = float(raw_price)
quantity = int(raw_quantity)
subtotal = price * quantity
tax_rate = 0.18
total = subtotal * (1 + tax_rate)

print(f"Subtotal: ₹{subtotal:,.2f}")
print(f"Tax:      ₹{subtotal * tax_rate:,.2f}")
print(f"Total:    ₹{total:,.2f}")""",
            ),
            (
                "Readable scripts and invariants",
                """A useful script separates inputs, transformation, and output. An invariant is a fact that must stay true, such as quantity being non-negative. Check invariants early so invalid data cannot travel through the program. Comments should explain intent or a non-obvious decision, not repeat the code.""",
                """student = "Asha"
completed = 14
total_lessons = 18

if total_lessons <= 0:
    raise ValueError("total_lessons must be positive")
if not 0 <= completed <= total_lessons:
    raise ValueError("completed must be within the course range")

percentage = completed / total_lessons * 100
print(f"{student} has completed {percentage:.1f}% of the course.")""",
            ),
        ],
        (
            "Worked example: invoice calculator",
            "Translate the rules into named intermediate values. Keeping each business rule visible makes the calculation easy to verify.",
            """unit_price = 799.0
quantity = 4
discount_rate = 0.10 if quantity >= 4 else 0.0
tax_rate = 0.18

gross = unit_price * quantity
discount = gross * discount_rate
taxable = gross - discount
tax = taxable * tax_rate
grand_total = taxable + tax

print(f"Gross:       ₹{gross:,.2f}")
print(f"Discount:   -₹{discount:,.2f}")
print(f"Tax:         ₹{tax:,.2f}")
print(f"Grand total: ₹{grand_total:,.2f}")""",
        ),
        """1. Convert a Celsius temperature to Fahrenheit using `F = C × 9/5 + 32`.
2. Calculate simple interest from principal, annual rate, and years.
3. Given completed and total lessons, print a one-line progress report with one decimal place.
4. Add validation for a negative principal or a zero total lesson count.""",
        """celsius = 28
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius}°C = {fahrenheit:.1f}°F")

principal, annual_rate, years = 50_000, 0.08, 2
if principal < 0 or annual_rate < 0 or years < 0:
    raise ValueError("financial inputs cannot be negative")
interest = principal * annual_rate * years
print(f"Simple interest: ₹{interest:,.2f}")

completed, total = 7, 18
if total <= 0:
    raise ValueError("total must be positive")
print(f"Progress: {completed / total:.1%}")""",
        [
            ("Why does `input()` usually need conversion?", "It always returns a string."),
            ("What is the difference between `=` and `==`?", "`=` binds a name; `==` compares values."),
            ("When is `None` useful?", "It represents an intentional absence of a value."),
        ],
        ["Names reference objects.", "Validate at boundaries.", "Use named steps and formatted output to make rules auditable."],
    ),
    lesson(
        "02",
        "control-flow",
        "Control Flow and Problem Solving",
        "Express decisions and repetition with conditions, loops, comprehensions, and small problem-solving patterns.",
        [
            "Design mutually exclusive `if`/`elif`/`else` branches.",
            "Choose between `for` and `while` loops.",
            "Use `break`, `continue`, `enumerate`, `zip`, and comprehensions.",
            "Trace a solution with sample inputs before coding it.",
        ],
        [
            (
                "Conditions model business rules",
                """Order branches from most specific to most general. Python stops at the first true branch, so overlapping conditions must be intentional. Chained comparisons such as `0 <= score <= 100` read like mathematics and prevent duplicated names.""",
                """score = 82

if not 0 <= score <= 100:
    grade = "invalid"
elif score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
elif score >= 60:
    grade = "C"
else:
    grade = "Needs improvement"

print(grade)""",
            ),
            (
                "Iteration patterns",
                """Use a `for` loop when iterating over known items. Use `while` when repetition depends on changing state. `enumerate` supplies an index without manual counters, and `zip` walks aligned collections. Prefer direct iteration over `range(len(items))` unless the index itself is required.""",
                """topics = ["Python", "SQL", "Machine Learning"]
hours = [12, 8, 20]

for position, (topic, duration) in enumerate(zip(topics, hours), start=1):
    print(f"{position}. {topic}: {duration} hours")

remaining = 100
week = 0
while remaining > 0:
    week += 1
    remaining -= min(remaining, 30)
print(f"Backlog completed in {week} weeks")""",
            ),
            (
                "Comprehensions and loop control",
                """A comprehension is ideal for a simple map or filter that fits on one readable line. Use a normal loop when logic needs multiple branches, logging, error handling, or side effects. `continue` skips one iteration; `break` exits the nearest loop.""",
                """scores = [42, 78, 91, 66, 35]
passing = [score for score in scores if score >= 60]
bands = ["high" if score >= 85 else "standard" for score in passing]
print(passing, bands)

for score in scores:
    if score < 0:
        continue
    if score == 91:
        print("Target score found")
        break""",
            ),
        ],
        (
            "Worked example: rule-based shipping fee",
            "Model the free-shipping rule first, then apply location and weight surcharges. The order of decisions mirrors the policy.",
            """order_total = 1_800
weight_kg = 6.5
is_remote = True

if order_total >= 2_000:
    shipping = 0
else:
    shipping = 80
    if weight_kg > 5:
        shipping += 20 * (weight_kg - 5)
    if is_remote:
        shipping += 120

print(f"Shipping fee: ₹{shipping:.2f}")""",
        ),
        """1. Print `Fizz`, `Buzz`, `FizzBuzz`, or the number for values 1–30.
2. From a list of transactions, keep only positive values and stop if the sentinel `None` appears.
3. Build a dictionary mapping each course name to `short`, `medium`, or `long` based on its length.
4. Trace each algorithm by hand for at least three inputs before running it.""",
        """for number in range(1, 31):
    if number % 15 == 0:
        print("FizzBuzz")
    elif number % 3 == 0:
        print("Fizz")
    elif number % 5 == 0:
        print("Buzz")
    else:
        print(number)

transactions = [200, -50, 0, 375, None, 900]
accepted = []
for amount in transactions:
    if amount is None:
        break
    if amount <= 0:
        continue
    accepted.append(amount)

courses = ["AI", "Python", "Data Engineering"]
length_band = {
    name: "short" if len(name) <= 4 else "medium" if len(name) <= 10 else "long"
    for name in courses
}
print(accepted, length_band)""",
        [
            ("Why place the most specific branch first?", "The first true branch wins."),
            ("When is `while` preferable?", "When stopping depends on evolving state rather than a known collection."),
            ("When should a comprehension become a loop?", "When the logic is no longer immediately readable or needs side effects."),
        ],
        ["Branch order is part of correctness.", "Iterate directly over data.", "Trace before optimizing."],
    ),
    lesson(
        "03",
        "collections",
        "Collections and Data Structures",
        "Choose and combine lists, tuples, dictionaries, and sets for reliable data manipulation.",
        [
            "Select a collection from its ordering, uniqueness, lookup, and mutability needs.",
            "Slice and unpack sequences.",
            "Build nested records without accidental aliasing.",
            "Use sets and dictionaries for fast membership and lookup.",
        ],
        [
            (
                "Sequence choices: list and tuple",
                """Lists are ordered and mutable; tuples are ordered and usually represent fixed records. Slicing creates a new sequence. Unpacking gives positions meaningful names. Remember that copying a list is shallow: nested mutable objects are still shared unless copied explicitly.""",
                """modules = ["Python", "SQL", "ML", "LLMs"]
first, *middle, last = modules
modules.append("Agents")

point = (17.3850, 78.4867)
latitude, longitude = point

print(first, middle, last)
print(f"Location: {latitude}, {longitude}")
print(modules[1:4])""",
            ),
            (
                "Mappings model keyed records",
                """A dictionary maps unique hashable keys to values and preserves insertion order. Use `.get()` for an optional key, direct indexing when absence is an error, and `.items()` when both key and value are needed. Keep one record shape consistent across a collection.""",
                """learner = {
    "name": "Asha",
    "track": "Full Stack AI",
    "completed": {"Python", "SQL"},
    "scores": {"Python": 88, "SQL": 91},
}

learner["scores"]["ML"] = 84
average = sum(learner["scores"].values()) / len(learner["scores"])
print(learner.get("mentor", "Not assigned"))
print(f"Average: {average:.1f}")""",
            ),
            (
                "Sets express uniqueness and relationships",
                """Sets remove duplicates and support union, intersection, difference, and symmetric difference. They are ideal for permissions, tags, deduplication, and membership checks. Do not rely on set display order for presentation.""",
                """required = {"python", "sql", "git"}
learner_skills = {"python", "excel", "git", "python"}

missing = required - learner_skills
matched = required & learner_skills
all_skills = required | learner_skills

print("Matched:", sorted(matched))
print("Missing:", sorted(missing))
print("All:", sorted(all_skills))""",
            ),
        ],
        (
            "Worked example: aggregate order records",
            "A dictionary is a natural accumulator when each customer needs one running total.",
            """orders = [
    {"customer": "Asha", "amount": 1200},
    {"customer": "Ravi", "amount": 800},
    {"customer": "Asha", "amount": 650},
    {"customer": "Meera", "amount": 1500},
]

totals = {}
for order in orders:
    customer = order["customer"]
    totals[customer] = totals.get(customer, 0) + order["amount"]

ranking = sorted(totals.items(), key=lambda item: item[1], reverse=True)
print(ranking)""",
        ),
        """1. Deduplicate a list of email addresses case-insensitively while preserving first-seen order.
2. Count word frequency in a sentence.
3. Compare two teams' skill sets: shared, only-left, and only-right.
4. Group transaction dictionaries by category and calculate each category total.""",
        """emails = ["A@x.com", "b@x.com", "a@x.com", "C@x.com"]
seen = set()
unique = []
for email in emails:
    normalized = email.casefold()
    if normalized not in seen:
        seen.add(normalized)
        unique.append(email)

words = "python makes data work and python makes automation work".split()
frequency = {}
for word in words:
    frequency[word] = frequency.get(word, 0) + 1

team_a = {"python", "sql", "azure"}
team_b = {"python", "docker", "azure"}
comparison = {
    "shared": team_a & team_b,
    "only_a": team_a - team_b,
    "only_b": team_b - team_a,
}
print(unique, frequency, comparison)""",
        [
            ("Which structure represents unique tags?", "A set."),
            ("Why can a tuple be a dictionary key but a list cannot?", "A tuple can be hashable; a mutable list is not hashable."),
            ("What does a shallow copy share?", "References to nested mutable objects."),
        ],
        ["Model the data before coding.", "Use dictionaries for keyed lookup and sets for membership.", "Be explicit about mutability and copying."],
    ),
    lesson(
        "04",
        "functions",
        "Functions, Scope, and Functional Patterns",
        "Design small, testable functions with clear contracts, flexible parameters, and controlled side effects.",
        [
            "Write functions with one clear responsibility.",
            "Use positional, keyword-only, default, variadic, and unpacked arguments.",
            "Explain local, enclosing, global, and built-in scope.",
            "Compose pure transformations and document contracts.",
        ],
        [
            (
                "A function is a contract",
                """A strong function has explicit inputs, a useful return value, and a narrow responsibility. Prefer returning data over printing inside reusable logic. A docstring explains purpose, parameters, return value, and exceptional behavior; type hints describe the intended shapes but do not enforce them at runtime.""",
                """def calculate_total(subtotal: float, *, tax_rate: float = 0.18) -> float:
    # Return subtotal plus tax; reject negative values.
    if subtotal < 0:
        raise ValueError("subtotal cannot be negative")
    if not 0 <= tax_rate <= 1:
        raise ValueError("tax_rate must be between 0 and 1")
    return subtotal * (1 + tax_rate)


print(calculate_total(2_500))
print(calculate_total(2_500, tax_rate=0.05))""",
            ),
            (
                "Parameters and unpacking",
                """Default values are evaluated once when a function is defined, so never use a mutable object such as `[]` as a default. `*args` collects extra positional values; `**kwargs` collects extra named values. Keyword-only parameters after `*` make important call-site choices visible.""",
                """def build_profile(name: str, *skills: str, active: bool = True, **metadata):
    return {
        "name": name,
        "skills": list(skills),
        "active": active,
        "metadata": metadata,
    }


profile = build_profile(
    "Asha", "Python", "SQL", active=True, city="Hyderabad", experience=2
)
print(profile)""",
            ),
            (
                "Scope, purity, and composition",
                """Python resolves names through LEGB: local, enclosing, global, then built-ins. Hidden mutation of global state makes functions difficult to test. A pure function depends only on its inputs and returns a result without observable side effects; small pure functions compose well into pipelines.""",
                """def normalize_name(value: str) -> str:
    return " ".join(value.strip().title().split())


def is_company_email(value: str, domain: str) -> bool:
    return value.casefold().endswith("@" + domain.casefold())


raw_names = ["  asha reddy ", "RAVI   KUMAR"]
clean_names = [normalize_name(name) for name in raw_names]
print(clean_names)
print(is_company_email("Asha@Edukron.com", "edukron.com"))""",
            ),
        ],
        (
            "Worked example: reusable grading pipeline",
            "Separate validation, scoring, and presentation so each rule can be tested independently.",
            """def validate_scores(scores: list[float]) -> None:
    if not scores:
        raise ValueError("at least one score is required")
    if any(not 0 <= score <= 100 for score in scores):
        raise ValueError("scores must be between 0 and 100")


def average_score(scores: list[float]) -> float:
    validate_scores(scores)
    return sum(scores) / len(scores)


def performance_band(average: float) -> str:
    if average >= 85:
        return "distinction"
    if average >= 60:
        return "pass"
    return "review"


scores = [86, 92, 79]
average = average_score(scores)
print({"average": round(average, 2), "band": performance_band(average)})""",
        ),
        """1. Write `safe_percentage(part, whole)` with validation for zero and negative inputs.
2. Write `summarize(values, *, digits=2)` returning count, minimum, maximum, and mean.
3. Refactor a script that reads globals and prints results into pure functions.
4. Call `summarize` once with a list and once using an unpacked tuple.""",
        """def safe_percentage(part: float, whole: float) -> float:
    if part < 0 or whole <= 0 or part > whole:
        raise ValueError("expected 0 <= part <= whole and whole > 0")
    return part / whole * 100


def summarize(values, *, digits: int = 2):
    numbers = list(values)
    if not numbers:
        raise ValueError("values cannot be empty")
    return {
        "count": len(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": round(sum(numbers) / len(numbers), digits),
    }


print(safe_percentage(7, 18))
print(summarize([10, 20, 35]))
print(summarize((*range(1, 6),), digits=1))""",
        [
            ("Why avoid a list as a default argument?", "The same list would be reused across calls."),
            ("What does keyword-only communicate?", "The caller must name an important option."),
            ("Why prefer return values?", "They can be composed, tested, stored, or presented elsewhere."),
        ],
        ["Design contracts before implementation.", "Keep side effects at system boundaries.", "Compose small transformations."],
    ),
    lesson(
        "05",
        "text-and-regex",
        "Strings, Text Processing, and Regular Expressions",
        "Normalize, validate, search, and transform text safely with string methods and focused regular expressions.",
        [
            "Use Unicode-aware string operations and formatting.",
            "Build deterministic normalization pipelines.",
            "Apply regular expressions only when structural patterns justify them.",
            "Extract structured fields from semi-structured text.",
        ],
        [
            (
                "Strings are immutable sequences",
                """String methods return new values. `strip`, `split`, `join`, `replace`, `startswith`, and `casefold` solve most business text tasks more clearly than regular expressions. `casefold` is stronger than `lower` for caseless comparison across Unicode text.""",
                """raw = "  FULL   stack AI — Python  "
normalized = " ".join(raw.strip().split())
slug = normalized.casefold().replace(" ", "-").replace("—", "-")
while "--" in slug:
    slug = slug.replace("--", "-")

print(normalized)
print(slug)
print("python" in normalized.casefold())""",
            ),
            (
                "Formatting and parsing",
                """F-strings support alignment, precision, percentages, dates, and debugging. Parsing should separate delimiters deliberately and validate the resulting shape. Never assume a split produced the expected number of fields.""",
                """record = "Asha|Full Stack AI|0.875"
parts = [part.strip() for part in record.split("|")]
if len(parts) != 3:
    raise ValueError("expected name, track, completion")

name, track, raw_completion = parts
completion = float(raw_completion)
print(f"{name:<12} {track:<20} {completion:>7.1%}")""",
            ),
            (
                "Regex for structural patterns",
                """A regular expression is useful for repeated structure such as IDs, log lines, or token extraction. Use raw strings, compile reused patterns, name capture groups, and prefer `fullmatch` for validation. A regex proves shape, not real-world truth; a matched date may still be impossible.""",
                """import re

log_pattern = re.compile(
    r"^(?P<level>INFO|WARNING|ERROR)\\|(?P<service>[a-z-]+)\\|(?P<message>.+)$"
)

lines = [
    "INFO|trainer-api|request completed",
    "ERROR|model-service|timeout after 30s",
]

for line in lines:
    match = log_pattern.fullmatch(line)
    if match:
        print(match.groupdict())""",
            ),
        ],
        (
            "Worked example: clean and validate contact data",
            "Normalize names and email addresses before validation so equivalent forms compare consistently.",
            """import re

EMAIL_SHAPE = re.compile(r"^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$")


def clean_contact(raw_name: str, raw_email: str) -> dict:
    name = " ".join(raw_name.strip().title().split())
    email = raw_email.strip().casefold()
    if not name:
        raise ValueError("name is required")
    if not EMAIL_SHAPE.fullmatch(email):
        raise ValueError("email shape is invalid")
    return {"name": name, "email": email}


print(clean_contact("  asha   reddy ", " ASHA@example.COM "))""",
        ),
        """1. Normalize product names by trimming, collapsing whitespace, and title-casing.
2. Extract hashtags from a sentence without the `#` symbol.
3. Validate IDs shaped like `EDU-2026-0001`.
4. Parse `2026-09-09 INFO course-published` into date, level, and message fields.""",
        """import re

products = ["  wireless   mouse", "USB-C HUB  "]
clean_products = [" ".join(item.strip().title().split()) for item in products]

hashtags = re.findall(r"(?<!\\w)#([\\w-]+)", "Learn #Python and #Full-Stack-AI today")
id_pattern = re.compile(r"^EDU-\\d{4}-\\d{4}$")

line = "2026-09-09 INFO course-published"
date, level, message = line.split(maxsplit=2)

print(clean_products)
print(hashtags)
print(id_pattern.fullmatch("EDU-2026-0001") is not None)
print({"date": date, "level": level, "message": message})""",
        [
            ("Why use a raw string for regex?", "It reduces conflicts between Python and regex escaping."),
            ("Does a regex-validated email certainly exist?", "No; it only matches the chosen shape."),
            ("Why normalize before deduplication?", "Equivalent representations then compare consistently."),
        ],
        ["Prefer string methods for simple operations.", "Validate parsed shapes.", "Keep regular expressions small, named, and tested."],
    ),
    lesson(
        "06",
        "files-and-data-formats",
        "Files, Paths, JSON, and CSV",
        "Read and write local data safely with `pathlib`, context managers, encodings, JSON, and CSV.",
        [
            "Build portable paths with `pathlib.Path`.",
            "Use context managers and explicit UTF-8 encoding.",
            "Choose JSON or CSV from the data shape.",
            "Validate external records before transformation.",
        ],
        [
            (
                "Path operations and file lifecycle",
                """`Path` joins locations without manual separators and exposes readable methods for existence, suffixes, iteration, and file I/O. A `with` block guarantees a file is closed even if processing fails. Treat filenames and encodings as explicit inputs.""",
                """from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as temporary:
    root = Path(temporary)
    notes_path = root / "notes" / "python.txt"
    notes_path.parent.mkdir(parents=True)
    notes_path.write_text("names\\nfunctions\\ncollections\\n", encoding="utf-8")

    topics = notes_path.read_text(encoding="utf-8").splitlines()
    print(notes_path.name, notes_path.suffix, topics)""",
            ),
            (
                "JSON preserves nested structure",
                """JSON supports objects, arrays, strings, numbers, booleans, and null. Python maps these to dictionaries, lists, strings, numbers, booleans, and `None`. Dates and custom classes need an explicit serialization policy. Use indentation for human-reviewed files and validate required keys after loading.""",
                """import json

course = {
    "name": "Python",
    "hours": 45,
    "published": True,
    "modules": ["Core", "Professional", "Data and AI"],
}

payload = json.dumps(course, indent=2, ensure_ascii=False)
restored = json.loads(payload)
required = {"name", "hours", "modules"}
if missing := required - restored.keys():
    raise ValueError(f"missing keys: {sorted(missing)}")
print(payload)""",
            ),
            (
                "CSV represents rectangular records",
                """CSV is widely interoperable but carries no reliable type information. Use `csv.DictReader` and `DictWriter`, open files with `newline=''`, and convert each field deliberately. A schema check should reject missing headers before row processing.""",
                """import csv
import io

text = "name,score,active\\nAsha,88,true\\nRavi,73,false\\n"
stream = io.StringIO(text)
reader = csv.DictReader(stream)

records = []
for row in reader:
    records.append({
        "name": row["name"],
        "score": float(row["score"]),
        "active": row["active"].casefold() == "true",
    })
print(records)""",
            ),
        ],
        (
            "Worked example: configurable course report",
            "Keep configuration, input data, transformation, and output separate so each boundary is testable.",
            """import csv
import io
import json

config = json.loads('{"pass_mark": 60, "round_digits": 1}')
csv_text = "name,score\\nAsha,88\\nRavi,54\\nMeera,91\\n"

rows = csv.DictReader(io.StringIO(csv_text))
report = []
for row in rows:
    score = round(float(row["score"]), config["round_digits"])
    report.append({
        "name": row["name"],
        "score": score,
        "status": "pass" if score >= config["pass_mark"] else "review",
    })

print(json.dumps(report, indent=2))""",
        ),
        """1. Write three course records to CSV and read them back with numeric hours.
2. Store application settings in JSON and verify three required keys.
3. List all `.ipynb` files directly inside a chosen directory.
4. Design a policy for malformed rows: stop, skip, or collect errors. Explain the trade-off.""",
        """from pathlib import Path
from tempfile import TemporaryDirectory
import csv
import json

courses = [
    {"name": "Python", "hours": 45},
    {"name": "SQL", "hours": 30},
    {"name": "ML", "hours": 60},
]

with TemporaryDirectory() as temporary:
    root = Path(temporary)
    csv_path = root / "courses.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "hours"])
        writer.writeheader()
        writer.writerows(courses)

    with csv_path.open(encoding="utf-8", newline="") as handle:
        restored = [
            {"name": row["name"], "hours": int(row["hours"])}
            for row in csv.DictReader(handle)
        ]

    settings = {"input": str(csv_path), "strict": True, "encoding": "utf-8"}
    (root / "settings.json").write_text(json.dumps(settings, indent=2), encoding="utf-8")
    print(restored)""",
        [
            ("Why specify UTF-8?", "It makes the encoding contract explicit and portable."),
            ("Why use `newline=''` with CSV?", "It lets the CSV module handle newlines correctly."),
            ("Which format naturally supports nested data?", "JSON."),
        ],
        ["Use `Path`, not string concatenation.", "External text needs conversion and validation.", "Separate I/O from transformation."],
    ),
    lesson(
        "07",
        "errors-debugging-and-logging",
        "Errors, Debugging, and Logging",
        "Make failures visible and actionable with precise exceptions, systematic debugging, and structured logs.",
        [
            "Distinguish syntax errors, exceptions, and incorrect results.",
            "Catch only errors a layer can handle.",
            "Create informative domain exceptions.",
            "Use assertions, breakpoints, and logging for diagnosis.",
        ],
        [
            (
                "Exception boundaries",
                """An exception should cross layers until a layer can recover, add context, or present a user-facing message. Catch specific exception types; a broad `except Exception` can hide programming mistakes. Use `else` for code that runs only after success and `finally` for cleanup that must always occur.""",
                """def parse_port(raw: str) -> int:
    try:
        port = int(raw)
    except ValueError as error:
        raise ValueError(f"port must be an integer, received {raw!r}") from error
    if not 1 <= port <= 65_535:
        raise ValueError("port must be between 1 and 65535")
    return port


for candidate in ["8000", "abc", "70000"]:
    try:
        print(candidate, parse_port(candidate))
    except ValueError as error:
        print("Invalid configuration:", error)""",
            ),
            (
                "Debug from evidence",
                """Reproduce the smallest failing case, inspect inputs and intermediate values, state a hypothesis, then test it. `repr`, type checks, assertions, and a debugger reveal state without random edits. Assertions document internal invariants; do not use them to validate untrusted user input because optimized Python can disable them.""",
                """def normalized_average(values: list[float]) -> float:
    assert isinstance(values, list), "internal contract expects a list"
    if not values:
        raise ValueError("values cannot be empty")
    total = sum(values)
    count = len(values)
    assert count > 0
    return total / count


sample = [10.0, 20.0, 40.0]
print({"input": repr(sample), "result": normalized_average(sample)})""",
            ),
            (
                "Logging records operational context",
                """Logs answer what happened, where, and with what safe context. Use log levels consistently: DEBUG for diagnostic detail, INFO for normal milestones, WARNING for recoverable concern, ERROR for failed work, and CRITICAL for service-threatening failures. Never log passwords, tokens, or sensitive personal data.""",
                """import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger("course.pipeline")

records = [{"id": 1, "score": 82}, {"id": 2, "score": None}]
for record in records:
    if record["score"] is None:
        logger.warning("record skipped id=%s reason=missing_score", record["id"])
        continue
    logger.info("record accepted id=%s", record["id"])""",
            ),
        ],
        (
            "Worked example: collect row-level validation errors",
            "Batch processing often should continue after a bad row while preserving a complete error report.",
            """def validate_record(record: dict) -> dict:
    try:
        learner_id = int(record["id"])
        score = float(record["score"])
    except KeyError as error:
        raise ValueError(f"missing field: {error.args[0]}") from error
    except (TypeError, ValueError) as error:
        raise ValueError("id and score must be numeric") from error
    if not 0 <= score <= 100:
        raise ValueError("score outside 0..100")
    return {"id": learner_id, "score": score}


raw_records = [{"id": "1", "score": "88"}, {"id": "x", "score": "72"}]
valid, errors = [], []
for position, record in enumerate(raw_records, start=1):
    try:
        valid.append(validate_record(record))
    except ValueError as error:
        errors.append({"row": position, "error": str(error)})
print({"valid": valid, "errors": errors})""",
        ),
        """1. Write a parser for percentages such as `82.5%` with clear error messages.
2. Process five records, collecting every validation error instead of stopping at the first.
3. Add INFO logs for start/end and WARNING logs for rejected records.
4. Diagnose an intentionally wrong average by printing the smallest useful intermediate state.""",
        """import logging

logger = logging.getLogger("percentage-import")


def parse_percentage(raw: str) -> float:
    if not isinstance(raw, str) or not raw.endswith("%"):
        raise ValueError("percentage must be text ending with %")
    try:
        value = float(raw[:-1])
    except ValueError as error:
        raise ValueError(f"invalid percentage: {raw!r}") from error
    if not 0 <= value <= 100:
        raise ValueError("percentage must be between 0% and 100%")
    return value / 100


values = ["82.5%", "100%", "bad", "120%"]
accepted, rejected = [], []
logger.info("import started count=%s", len(values))
for value in values:
    try:
        accepted.append(parse_percentage(value))
    except ValueError as error:
        rejected.append({"value": value, "error": str(error)})
        logger.warning("value rejected value=%r", value)
logger.info("import finished accepted=%s rejected=%s", len(accepted), len(rejected))
print(accepted, rejected)""",
        [
            ("When should you catch an exception?", "When the current layer can recover, add useful context, or present it appropriately."),
            ("Are assertions input validation?", "No; use explicit exceptions for external input."),
            ("What must never enter logs?", "Secrets and sensitive personal data."),
        ],
        ["Catch narrowly.", "Debug from a reproducible case and observed state.", "Write logs for operators, not for decoration."],
    ),
    lesson(
        "08",
        "modules-packages-environments",
        "Modules, Packages, and Environments",
        "Organize Python code into importable modules and reproducible project environments.",
        [
            "Explain modules, packages, imports, and the module search path.",
            "Design a small package with a public interface.",
            "Use `__name__ == '__main__'` to separate library and script behavior.",
            "Record dependencies and isolate environments reproducibly.",
        ],
        [
            (
                "Modules create namespaces",
                """Every `.py` file is a module. Imports execute a module once per process and bind its objects into a namespace. Prefer `import package.module` or explicit names; wildcard imports obscure where behavior comes from. A package groups related modules and can expose a small public API from `__init__.py`.""",
                """import math
from statistics import mean

radius = 3.5
area = math.pi * radius**2
scores = [82, 91, 77]

print(f"Area: {area:.2f}")
print(f"Mean: {mean(scores):.1f}")
print(math.__name__)""",
            ),
            (
                "Library code versus entry points",
                """Reusable functions should be import-safe: importing the module must not start a job or prompt for input. Put orchestration in a `main()` function and call it only under the main guard. This structure supports notebooks, tests, command-line tools, and services from the same core code.""",
                """def build_message(course: str, lessons: int) -> str:
    return f"{course} contains {lessons} lessons."


def main() -> None:
    print(build_message("Python", 18))


if __name__ == "__main__":
    main()""",
            ),
            (
                "Environment and dependency discipline",
                """A virtual environment isolates a project's installed distributions from the system interpreter. Record direct dependencies and meaningful version constraints, keep secrets outside source control, and verify the interpreter used by Jupyter. Reproducibility requires code, dependency information, configuration, and deterministic input data—not only a notebook file.""",
                """import importlib.metadata
import sys

print("Interpreter:", sys.executable)
print("Python:", sys.version.split()[0])

for distribution in ["numpy", "pandas"]:
    try:
        print(distribution, importlib.metadata.version(distribution))
    except importlib.metadata.PackageNotFoundError:
        print(distribution, "not installed in this environment")""",
            ),
        ],
        (
            "Worked example: package boundary design",
            "The public function validates inputs and delegates one focused calculation, while orchestration stays outside the library boundary.",
            """def normalize_score(score: float) -> float:
    if not 0 <= score <= 100:
        raise ValueError("score must be between 0 and 100")
    return score / 100


def summarize_scores(scores: list[float]) -> dict:
    normalized = [normalize_score(score) for score in scores]
    return {
        "count": len(normalized),
        "average": sum(normalized) / len(normalized),
    }


print(summarize_scores([80, 90, 70]))""",
        ),
        """1. Sketch a `course_tools/` package with `validation.py`, `reporting.py`, and `__init__.py`.
2. Decide which two or three objects should be public.
3. Refactor a script so importing it performs no work.
4. Record its direct dependencies and identify configuration that must not be committed.""",
        """# Suggested package layout:
# course_tools/
#   __init__.py       -> exports validate_score and build_report
#   validation.py     -> validation rules
#   reporting.py      -> pure report transformation
# run_report.py       -> main() orchestration
# tests/              -> package tests


def validate_score(score: float) -> float:
    if not 0 <= score <= 100:
        raise ValueError("score outside 0..100")
    return score


def build_report(name: str, score: float) -> dict:
    return {"name": name, "score": validate_score(score)}


def main() -> None:
    print(build_report("Asha", 88))


if __name__ == "__main__":
    main()""",
        [
            ("What happens when a module is first imported?", "Its top-level code executes and its namespace is created."),
            ("Why use a main guard?", "It prevents script orchestration from running during import."),
            ("What does a virtual environment isolate?", "Installed Python distributions for one project."),
        ],
        ["Keep imports predictable.", "Expose a small public interface.", "Treat environment information as part of reproducibility."],
    ),
    lesson(
        "09",
        "oop-and-dataclasses",
        "Object-Oriented Python and Dataclasses",
        "Model stateful domain concepts with classes, dataclasses, composition, and explicit invariants.",
        [
            "Choose a class only when data and behavior belong together.",
            "Use instance, class, and static methods appropriately.",
            "Create concise value objects with dataclasses.",
            "Prefer composition over deep inheritance.",
        ],
        [
            (
                "Objects protect invariants",
                """A class is useful when an entity owns state and behavior across time. The constructor establishes a valid state; methods preserve it. A leading underscore marks implementation detail by convention. Properties can expose computed or validated attributes without leaking internal representation.""",
                """class LearningPath:
    def __init__(self, name: str, total_lessons: int):
        if total_lessons <= 0:
            raise ValueError("total_lessons must be positive")
        self.name = name
        self.total_lessons = total_lessons
        self._completed = 0

    @property
    def progress(self) -> float:
        return self._completed / self.total_lessons

    def complete_lesson(self) -> None:
        if self._completed < self.total_lessons:
            self._completed += 1


path = LearningPath("Python", 18)
path.complete_lesson()
print(path.name, f"{path.progress:.1%}")""",
            ),
            (
                "Dataclasses for value-focused models",
                """A dataclass generates initialization, representation, and equality methods from annotated fields. Use `frozen=True` for immutable value objects and `field(default_factory=...)` for mutable defaults. `__post_init__` can validate a completed object.""",
                """from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Course:
    code: str
    title: str
    hours: int
    tags: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self):
        if self.hours <= 0:
            raise ValueError("hours must be positive")


python = Course("PY-101", "Python", 45, ("AI", "data"))
print(python)""",
            ),
            (
                "Composition and polymorphism",
                """Composition builds an object from collaborators with narrow responsibilities. It is easier to replace a composed notifier or repository in tests than to untangle a deep inheritance hierarchy. Polymorphism means callers depend on behavior rather than a concrete class.""",
                """class ConsoleNotifier:
    def send(self, message: str) -> None:
        print("NOTICE:", message)


class EnrollmentService:
    def __init__(self, notifier):
        self.notifier = notifier

    def enroll(self, learner: str, course: str) -> dict:
        record = {"learner": learner, "course": course}
        self.notifier.send(f"{learner} enrolled in {course}")
        return record


service = EnrollmentService(ConsoleNotifier())
print(service.enroll("Asha", "Python"))""",
            ),
        ],
        (
            "Worked example: immutable money value object",
            "A value object centralizes currency and precision rules so calculations cannot silently mix incompatible values.",
            """from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP


@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "INR"

    def __post_init__(self):
        rounded = self.amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        object.__setattr__(self, "amount", rounded)

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("currency mismatch")
        return Money(self.amount + other.amount, self.currency)


total = Money(Decimal("199.995")) + Money(Decimal("50"))
print(total)""",
        ),
        """1. Create a `Learner` dataclass with a default empty skill set using `default_factory`.
2. Add a method that completes a lesson only once.
3. Compose a report service from a repository and formatter.
4. Explain why inheriting `ReportService` from `SqlRepository` would model the relationship poorly.""",
        """from dataclasses import dataclass, field


@dataclass
class Learner:
    name: str
    skills: set[str] = field(default_factory=set)
    completed_lessons: set[str] = field(default_factory=set)

    def complete(self, lesson_id: str) -> bool:
        before = len(self.completed_lessons)
        self.completed_lessons.add(lesson_id)
        return len(self.completed_lessons) > before


class MemoryRepository:
    def load_scores(self):
        return [80, 90, 70]


class ReportService:
    def __init__(self, repository):
        self.repository = repository

    def average(self):
        scores = self.repository.load_scores()
        return sum(scores) / len(scores)


learner = Learner("Asha")
print(learner.complete("01"), learner.complete("01"))
print(ReportService(MemoryRepository()).average())""",
        [
            ("When is a class better than functions?", "When state and behavior form a cohesive concept with a lifecycle."),
            ("How do you define a safe mutable dataclass default?", "Use `field(default_factory=...)`."),
            ("Why favor composition?", "Dependencies remain replaceable and relationships stay explicit."),
        ],
        ["Use classes for cohesive stateful models.", "Dataclasses reduce value-object boilerplate.", "Prefer shallow composition and explicit invariants."],
    ),
    lesson(
        "10",
        "pythonic-abstractions",
        "Iterators, Generators, Decorators, and Context Managers",
        "Use Python's protocols to stream data, wrap behavior, and manage resources without unnecessary complexity.",
        [
            "Explain iterable, iterator, and lazy generator behavior.",
            "Build memory-efficient generator pipelines.",
            "Write decorators that preserve wrapped-function metadata.",
            "Use context managers for reliable acquire/release lifecycles.",
        ],
        [
            (
                "Iteration is a protocol",
                """An iterable can produce an iterator; an iterator produces values until it raises `StopIteration`. Generator functions use `yield` to suspend and resume state automatically. Laziness reduces memory use and lets downstream consumers stop early, but a generator is normally consumed only once.""",
                """def valid_scores(rows):
    for row in rows:
        score = row.get("score")
        if isinstance(score, (int, float)) and 0 <= score <= 100:
            yield score


rows = [{"score": 82}, {"score": None}, {"score": 95}, {"score": 120}]
scores = valid_scores(rows)
print(next(scores))
print(list(scores))""",
            ),
            (
                "Decorators wrap cross-cutting behavior",
                """A decorator accepts a callable and returns a callable. It is useful for timing, authorization, caching, retries, or instrumentation when the policy truly applies across functions. `functools.wraps` preserves the original name and docstring. Avoid decorators that hide important domain flow.""",
                """from functools import wraps
from time import perf_counter


def timed(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        started = perf_counter()
        result = function(*args, **kwargs)
        elapsed_ms = (perf_counter() - started) * 1000
        print(f"{function.__name__} took {elapsed_ms:.3f} ms")
        return result
    return wrapper


@timed
def square_all(values):
    return [value * value for value in values]


print(square_all(range(10)))""",
            ),
            (
                "Context managers make cleanup unconditional",
                """A context manager defines what happens on entry and exit. Files, locks, database transactions, and temporary configuration all benefit. `contextlib.contextmanager` is concise for one acquire/yield/release lifecycle; a class is preferable when the lifecycle has richer state.""",
                """from contextlib import contextmanager
from time import perf_counter


@contextmanager
def measured(label: str):
    started = perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {(perf_counter() - started) * 1000:.3f} ms")


with measured("sum squares"):
    result = sum(value * value for value in range(10_000))
print(result)""",
            ),
        ],
        (
            "Worked example: lazy event pipeline",
            "Each stage accepts and returns an iterable, so the pipeline reads one event at a time and can be tested independently.",
            """def parse_events(lines):
    for line in lines:
        level, service, message = line.rstrip().split("|", maxsplit=2)
        yield {"level": level, "service": service, "message": message}


def errors_only(events):
    return (event for event in events if event["level"] == "ERROR")


def count_by_service(events):
    counts = {}
    for event in events:
        service = event["service"]
        counts[service] = counts.get(service, 0) + 1
    return counts


lines = [
    "INFO|api|ready",
    "ERROR|model|timeout",
    "ERROR|api|invalid request",
]
print(count_by_service(errors_only(parse_events(lines))))""",
        ),
        """1. Write a generator that yields fixed-size batches from any iterable.
2. Create a decorator that counts calls without changing the function result.
3. Create a context manager that temporarily changes a dictionary value and restores it.
4. Explain where laziness helps and where materializing a list is clearer.""",
        """from contextlib import contextmanager
from functools import wraps


def batched(iterable, size: int):
    if size <= 0:
        raise ValueError("size must be positive")
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def count_calls(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return function(*args, **kwargs)
    wrapper.calls = 0
    return wrapper


@contextmanager
def temporary_value(mapping, key, value):
    sentinel = object()
    previous = mapping.get(key, sentinel)
    mapping[key] = value
    try:
        yield mapping
    finally:
        if previous is sentinel:
            mapping.pop(key, None)
        else:
            mapping[key] = previous


print(list(batched(range(7), 3)))""",
        [
            ("What does `yield` change?", "It makes the function return a lazy generator that resumes between values."),
            ("Why use `wraps`?", "It preserves metadata of the decorated function."),
            ("What does `finally` guarantee in a context manager?", "Cleanup runs whether the body succeeds or fails."),
        ],
        ["Learn protocols before clever syntax.", "Stream data when early stopping or memory matters.", "Make resource cleanup unconditional."],
    ),
    lesson(
        "11",
        "numpy",
        "NumPy for Numerical Computing",
        "Use typed multidimensional arrays, vectorization, broadcasting, aggregation, and reproducible simulation.",
        [
            "Create arrays with intentional shapes and dtypes.",
            "Index, slice, reshape, and filter arrays.",
            "Apply broadcasting rules and vectorized operations.",
            "Use modern random generators and numerical summaries.",
        ],
        [
            (
                "Arrays combine shape and dtype",
                """A NumPy array stores homogeneous values in a multidimensional shape. `shape`, `ndim`, `size`, and `dtype` are part of every numerical debugging conversation. Unlike nested lists, arrays define element-wise arithmetic and compact typed storage.""",
                """import numpy as np

sales = np.array([
    [1200.0, 1350.0, 1280.0],
    [980.0, 1100.0, 1250.0],
])

print("shape:", sales.shape)
print("dtype:", sales.dtype)
print("row totals:", sales.sum(axis=1))
print("column means:", sales.mean(axis=0))""",
            ),
            (
                "Indexing, masks, and reshaping",
                """Basic slices usually return views that share memory; fancy indexing and boolean masks return copies. Always confirm the axis being reduced or reshaped. Reshape requires the same element count, and `-1` asks NumPy to infer one dimension.""",
                """import numpy as np

values = np.arange(1, 13).reshape(3, 4)
high = values[values > 7]
second_column = values[:, 1]
flattened = values.reshape(-1)

print(values)
print("high:", high)
print("second column:", second_column)
print("flat:", flattened)""",
            ),
            (
                "Broadcasting and reproducibility",
                """Broadcasting aligns dimensions from the right and expands dimensions of size one. It eliminates many loops but shape mistakes can silently produce valid, wrong results. Use `np.random.default_rng(seed)` for an explicit, reproducible random stream.""",
                """import numpy as np

rng = np.random.default_rng(42)
features = rng.normal(size=(5, 3))
means = features.mean(axis=0)
stds = features.std(axis=0)
safe_stds = np.where(stds == 0, 1, stds)
standardized = (features - means) / safe_stds

print(np.round(standardized.mean(axis=0), 8))
print(np.round(standardized.std(axis=0), 8))""",
            ),
        ],
        (
            "Worked example: retail matrix analysis",
            "Columns represent price, quantity, and rating. Vectorized expressions calculate revenue and segment products without row loops.",
            """import numpy as np

products = np.array([
    [799.0, 40, 4.2],
    [1499.0, 22, 4.7],
    [499.0, 80, 3.9],
    [2499.0, 12, 4.8],
])

price = products[:, 0]
quantity = products[:, 1]
rating = products[:, 2]
revenue = price * quantity
priority_mask = (revenue >= np.median(revenue)) & (rating >= 4.5)

print("Revenue:", revenue)
print("Priority rows:\\n", products[priority_mask])
print("Top revenue row:", products[np.argmax(revenue)])""",
        ),
        """1. Create a 4×5 array containing 1–20 and calculate row sums and column means.
2. Replace negative values with zero using `np.where`.
3. Standardize each column of a random 100×3 matrix.
4. Simulate 10,000 dice rolls with a fixed seed and compare observed frequencies.""",
        """import numpy as np

matrix = np.arange(1, 21).reshape(4, 5)
print(matrix.sum(axis=1))
print(matrix.mean(axis=0))

measurements = np.array([3.0, -2.0, 0.5, -8.0])
print(np.where(measurements < 0, 0, measurements))

rng = np.random.default_rng(7)
sample = rng.normal(loc=[10, 50, 100], scale=[2, 5, 10], size=(100, 3))
standardized = (sample - sample.mean(axis=0)) / sample.std(axis=0)
print(np.round(standardized.mean(axis=0), 8))

rolls = rng.integers(1, 7, size=10_000)
counts = np.bincount(rolls, minlength=7)[1:]
print(counts / counts.sum())""",
        [
            ("What does `axis=0` aggregate?", "Down rows, producing one result per column."),
            ("Why inspect shapes before broadcasting?", "Compatible but unintended shapes can produce plausible wrong results."),
            ("Why use `default_rng`?", "It provides an explicit modern random generator and reproducibility."),
        ],
        ["Shape and dtype are core facts.", "Vectorize meaningful array operations.", "Seed simulations and verify axes."],
    ),
    lesson(
        "12",
        "pandas",
        "pandas for Data Analysis",
        "Load, inspect, clean, transform, aggregate, reshape, and join tabular data with explicit validation.",
        [
            "Understand Series, DataFrame, index, columns, and dtypes.",
            "Select with `loc` and `iloc` and filter with boolean masks.",
            "Clean missing, duplicate, text, numeric, and date values.",
            "Aggregate with groupby and combine tables with validated joins.",
        ],
        [
            (
                "Inspect before transforming",
                """A DataFrame is a labeled collection of typed columns. Begin with shape, columns, dtypes, missing counts, uniqueness, and representative rows. Selection with `loc` is label-based; `iloc` is position-based. Avoid chained assignment—select rows and columns in one `.loc[...]` operation.""",
                """import pandas as pd

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104],
    "region": ["South", "West", "South", "North"],
    "amount": [1200.0, 850.0, None, 1600.0],
    "status": ["paid", "paid", "cancelled", "paid"],
})

print(orders.info())
print(orders.isna().sum())
print(orders.loc[orders["status"].eq("paid"), ["order_id", "amount"]])""",
            ),
            (
                "Cleaning is rule-driven",
                """Missing values are not automatically errors; decide whether to reject, impute, preserve, or flag them from the business meaning. Normalize strings, parse dates with explicit error policy, and convert numeric fields deliberately. Keep an audit column when a transformation changes meaning.""",
                """import pandas as pd

raw = pd.DataFrame({
    "email": [" ASHA@EXAMPLE.COM ", "ravi@example.com", "ravi@example.com"],
    "joined": ["2026-01-10", "bad-date", "bad-date"],
    "score": ["88", "72", "72"],
})

cleaned = raw.assign(
    email=lambda frame: frame["email"].str.strip().str.casefold(),
    joined=lambda frame: pd.to_datetime(frame["joined"], errors="coerce"),
    score=lambda frame: pd.to_numeric(frame["score"], errors="coerce"),
).drop_duplicates()

cleaned["date_valid"] = cleaned["joined"].notna()
print(cleaned)""",
            ),
            (
                "Aggregation and joins",
                """`groupby` follows split–apply–combine: split rows into groups, apply aggregations, then combine results. Name aggregations for stable output columns. Joins can multiply rows when keys are non-unique, so use `validate=` and inspect unmatched keys before accepting a result.""",
                """import pandas as pd

orders = pd.DataFrame({
    "customer_id": [1, 1, 2, 3],
    "amount": [500, 750, 1200, 400],
})
customers = pd.DataFrame({
    "customer_id": [1, 2, 3],
    "segment": ["Gold", "Silver", "New"],
})

summary = orders.groupby("customer_id", as_index=False).agg(
    orders=("amount", "size"),
    revenue=("amount", "sum"),
    average_order=("amount", "mean"),
)
result = summary.merge(customers, on="customer_id", how="left", validate="one_to_one")
print(result)""",
            ),
        ],
        (
            "Worked example: quality-controlled sales summary",
            "Create explicit quality flags before aggregating so the report can state what was excluded.",
            """import pandas as pd

sales = pd.DataFrame({
    "date": ["2026-09-01", "2026-09-01", "bad", "2026-09-02"],
    "region": ["South", "West", "South", "South"],
    "units": [4, 2, 3, -1],
    "price": [800, 1500, 900, 700],
})

prepared = sales.assign(
    date=lambda frame: pd.to_datetime(frame["date"], errors="coerce"),
    valid=lambda frame: frame["date"].notna() & frame["units"].gt(0) & frame["price"].ge(0),
    revenue=lambda frame: frame["units"] * frame["price"],
)

summary = (
    prepared.loc[prepared["valid"]]
    .groupby("region", as_index=False)
    .agg(rows=("revenue", "size"), revenue=("revenue", "sum"))
    .sort_values("revenue", ascending=False)
)
print(summary)
print("Rejected rows:", (~prepared["valid"]).sum())""",
        ),
        """1. Build a DataFrame with one duplicate, one missing amount, and one invalid date.
2. Normalize text and parse numeric/date columns.
3. Produce a region summary with count, total, mean, and maximum.
4. Join a unique region lookup with `validate='many_to_one'` and inspect unmatched regions.""",
        """import pandas as pd

transactions = pd.DataFrame({
    "region": [" south ", "WEST", "south", "unknown"],
    "amount": [1000, 800, None, 400],
    "date": ["2026-09-01", "2026-09-02", "bad", "2026-09-04"],
})
lookup = pd.DataFrame({"region": ["South", "West"], "manager": ["Asha", "Ravi"]})

prepared = transactions.assign(
    region=lambda frame: frame["region"].str.strip().str.title(),
    amount=lambda frame: pd.to_numeric(frame["amount"], errors="coerce"),
    date=lambda frame: pd.to_datetime(frame["date"], errors="coerce"),
).drop_duplicates()

summary = prepared.groupby("region", as_index=False).agg(
    rows=("amount", "size"),
    total=("amount", "sum"),
    average=("amount", "mean"),
    maximum=("amount", "max"),
)
enriched = summary.merge(lookup, on="region", how="left", validate="many_to_one")
print(enriched)
print("Unmatched:", enriched.loc[enriched["manager"].isna(), "region"].tolist())""",
        [
            ("What is the first step with a new DataFrame?", "Inspect structure, types, missingness, uniqueness, and sample rows."),
            ("Why use join validation?", "It detects unexpected key cardinality and row multiplication."),
            ("Why avoid chained assignment?", "It can update a temporary object rather than the intended DataFrame."),
        ],
        ["Profile first.", "Clean from explicit rules.", "Validate joins and report rejected data."],
    ),
    lesson(
        "13",
        "visualization",
        "Data Visualization and Exploratory Analysis",
        "Design truthful charts, use the Matplotlib object model, and turn exploration into reproducible evidence.",
        [
            "Choose chart forms from analytical questions.",
            "Build and label figures with Matplotlib's object-oriented API.",
            "Use statistical views without overstating conclusions.",
            "Run a repeatable EDA checklist and document limitations.",
        ],
        [
            (
                "Question before chart",
                """Use bars for category comparison, lines for ordered time, scatter plots for relationships, and distributions for shape and spread. Position on a common scale is easier to compare than area or angle. A chart must include units, readable labels, and the population or time window when ambiguity is possible.""",
                """import matplotlib.pyplot as plt

courses = ["Python", "SQL", "ML", "LLMs"]
enrollments = [120, 95, 88, 72]

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(courses, enrollments, color="#3157d5")
ax.set(title="Course enrollment", xlabel="Course", ylabel="Learners")
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
plt.show()""",
            ),
            (
                "The object-oriented Matplotlib model",
                """A `Figure` contains one or more `Axes`; each axes contains marks, scales, labels, and annotations. Holding explicit figure and axes objects makes multi-panel layouts and reusable plotting functions predictable. Save the figure through `fig.savefig` after layout is finalized.""",
                """import matplotlib.pyplot as plt
import pandas as pd

progress = pd.DataFrame({
    "week": [1, 2, 3, 4],
    "completed": [3, 7, 12, 18],
    "target": [4, 8, 13, 18],
})

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(progress["week"], progress["completed"], marker="o", label="Completed")
ax.plot(progress["week"], progress["target"], linestyle="--", label="Target")
ax.set(title="Learning progress", xlabel="Week", ylabel="Lessons")
ax.set_xticks(progress["week"])
ax.legend(frameon=False)
fig.tight_layout()
plt.show()""",
            ),
            (
                "EDA is a documented investigation",
                """Exploration checks grain, coverage, types, missingness, distributions, outliers, category balance, time behavior, and relationships. Correlation is not causation, and a visualization is sensitive to filtering and scale choices. Record each transformation so another analyst can reproduce the chart.""",
                """import pandas as pd

data = pd.DataFrame({
    "hours": [2, 3, 5, 8, 10, 12],
    "score": [52, 60, 68, 81, 88, 93],
    "cohort": ["A", "A", "A", "B", "B", "B"],
})

profile = {
    "shape": data.shape,
    "missing": data.isna().sum().to_dict(),
    "numeric_summary": data.describe().round(2).to_dict(),
    "correlation": data[["hours", "score"]].corr().iloc[0, 1],
}
print(profile)""",
            ),
        ],
        (
            "Worked example: distribution plus relationship",
            "Use separate panels because distribution and relationship answer different questions.",
            """import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(12)
hours = rng.uniform(1, 15, size=120)
scores = np.clip(45 + 3.2 * hours + rng.normal(0, 7, size=120), 0, 100)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].hist(scores, bins=12, color="#3157d5", edgecolor="white")
axes[0].set(title="Score distribution", xlabel="Score", ylabel="Learners")

axes[1].scatter(hours, scores, alpha=0.65, color="#13899a")
axes[1].set(title="Study time and score", xlabel="Study hours", ylabel="Score")

for ax in axes:
    ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
plt.show()""",
        ),
        """1. For category totals, time trends, and two numeric variables, choose a chart and justify each choice.
2. Create a two-panel figure with a histogram and a box plot.
3. Annotate the maximum point on a line chart.
4. Write three limitations that should accompany a correlation chart.""",
        """import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(21)
values = rng.normal(70, 12, size=200)

fig, axes = plt.subplots(1, 2, figsize=(9, 4))
axes[0].hist(values, bins=14, color="#3157d5", edgecolor="white")
axes[0].set(title="Distribution", xlabel="Value", ylabel="Count")
axes[1].boxplot(values, vert=True)
axes[1].set(title="Spread and potential outliers", ylabel="Value")
fig.tight_layout()
plt.show()

limitations = [
    "Correlation does not establish causation.",
    "Outliers can strongly affect the coefficient.",
    "Filtering and range restriction may hide the broader pattern.",
]
print(*limitations, sep="\\n- ")""",
        [
            ("What should determine chart type?", "The analytical question and the variable types."),
            ("What is an Axes?", "The plotting area that owns scales, marks, labels, and annotations."),
            ("What does correlation not prove?", "Causation."),
        ],
        ["Start with the question.", "Label units and population.", "Make exploration reproducible and state limitations."],
    ),
    lesson(
        "14",
        "testing-typing-quality",
        "Testing, Type Hints, and Code Quality",
        "Turn expectations into automated checks and use types, documentation, and tooling to keep code maintainable.",
        [
            "Write deterministic unit tests using arrange–act–assert.",
            "Cover normal, boundary, invalid, and empty cases.",
            "Use type hints to clarify interfaces and model optional values.",
            "Separate pure logic from I/O for fast tests.",
        ],
        [
            (
                "Tests specify observable behavior",
                """A unit test exercises one behavior through its public interface. Arrange inputs, act once, and assert the outcome. Strong tests include boundaries and failure behavior, avoid implementation details, and use descriptive names that explain the rule being protected.""",
                """def shipping_fee(total: float, remote: bool = False) -> float:
    if total < 0:
        raise ValueError("total cannot be negative")
    fee = 0 if total >= 2_000 else 80
    return fee + (120 if remote else 0)


def test_free_shipping_at_threshold():
    assert shipping_fee(2_000) == 0


def test_remote_surcharge_is_added():
    assert shipping_fee(1_000, remote=True) == 200


test_free_shipping_at_threshold()
test_remote_surcharge_is_added()""",
            ),
            (
                "Types communicate shapes",
                """Type hints help readers, editors, and static checkers understand contracts. Use concrete domain types, `None` only when absence is valid, and small protocols when callers need behavior rather than inheritance. Hints complement runtime validation at external boundaries.""",
                """from collections.abc import Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class Summary:
    count: int
    average: float | None


def summarize(values: Iterable[float]) -> Summary:
    numbers = list(values)
    average = sum(numbers) / len(numbers) if numbers else None
    return Summary(count=len(numbers), average=average)


print(summarize([10.0, 20.0]))
print(summarize([]))""",
            ),
            (
                "Quality is a feedback system",
                """Formatting removes style arguments, linting catches suspicious patterns, static typing detects incompatible shapes, tests protect behavior, and reviews examine design and risk. Keep functions small enough to name clearly, eliminate duplicated rules, and document public interfaces and non-obvious decisions.""",
                """def percentage(part: float, whole: float) -> float:
    # Raise ValueError unless 0 <= part <= whole and whole is positive.
    if whole <= 0 or not 0 <= part <= whole:
        raise ValueError("expected 0 <= part <= whole and whole > 0")
    return part / whole * 100


cases = [(0, 10, 0.0), (5, 10, 50.0), (10, 10, 100.0)]
for part, whole, expected in cases:
    assert percentage(part, whole) == expected""",
            ),
        ],
        (
            "Worked example: dependency injection for testable I/O",
            "Pass the data-loading function into the report logic. Tests can provide an in-memory fake without touching a database or network.",
            """from collections.abc import Callable


def build_average_report(load_scores: Callable[[], list[float]]) -> dict:
    scores = load_scores()
    if not scores:
        return {"count": 0, "average": None}
    return {"count": len(scores), "average": sum(scores) / len(scores)}


def fake_loader() -> list[float]:
    return [80.0, 90.0, 70.0]


assert build_average_report(fake_loader) == {"count": 3, "average": 80.0}
assert build_average_report(lambda: []) == {"count": 0, "average": None}
print("tests passed")""",
        ),
        """1. Write tests for normal, empty, boundary, and invalid percentage inputs.
2. Add type hints to a function that groups records by category.
3. Refactor file reading away from calculation logic.
4. Write a regression test for one bug you deliberately introduce and then fix.""",
        """def percentage(part: float, whole: float) -> float:
    if whole <= 0 or not 0 <= part <= whole:
        raise ValueError("invalid percentage inputs")
    return part / whole * 100


assert percentage(5, 10) == 50
assert percentage(0, 10) == 0
assert percentage(10, 10) == 100

for invalid in [(-1, 10), (11, 10), (1, 0)]:
    try:
        percentage(*invalid)
    except ValueError:
        pass
    else:
        raise AssertionError(f"expected ValueError for {invalid}")

print("normal, boundary, and invalid cases passed")""",
        [
            ("What should a unit test assert?", "Publicly observable behavior."),
            ("Do type hints validate API input at runtime?", "No; external data still needs runtime validation."),
            ("Why isolate I/O?", "Pure logic becomes faster and easier to test deterministically."),
        ],
        ["Test behavior and boundaries.", "Use types to explain interfaces.", "Automate formatting, linting, typing, and tests as separate feedback loops."],
    ),
    lesson(
        "15",
        "apis-and-automation",
        "APIs, HTTP, and Automation",
        "Consume HTTP APIs responsibly and build idempotent automation with timeouts, retries, validation, and safe configuration.",
        [
            "Explain request methods, status codes, headers, and JSON bodies.",
            "Use timeouts and explicit error handling for every request.",
            "Validate response shape before using data.",
            "Design repeatable automation that is safe to rerun.",
        ],
        [
            (
                "HTTP is an unreliable boundary",
                """A client sends a method, URL, headers, and optional body; the server returns a status, headers, and body. Network calls can be slow, fail, return partial responses, or succeed with an unexpected schema. Always set a timeout and treat transport, HTTP status, decoding, and schema as separate failure stages.""",
                """from urllib.parse import urlencode

base_url = "https://api.example.com/courses"
query = urlencode({"track": "full-stack-ai", "limit": 20})
request_url = f"{base_url}?{query}"

expected_contract = {
    "method": "GET",
    "timeout_seconds": 10,
    "success_status": 200,
    "required_response_keys": {"items", "next_page"},
}
print(request_url)
print(expected_contract)""",
            ),
            (
                "A defensive request function",
                """The `requests` library gives a clear API for HTTP work. `raise_for_status()` turns non-success status codes into exceptions; `.json()` may still fail or produce an unexpected shape. Reuse a `Session` for repeated calls and configure retries only for safe, transient operations.""",
                """def fetch_json(session, url: str, *, timeout: float = 10.0) -> dict:
    response = session.get(url, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    if not isinstance(payload, dict):
        raise ValueError("expected a JSON object")
    return payload


# Real usage with the third-party requests package:
# import requests
# with requests.Session() as session:
#     data = fetch_json(session, "https://api.example.com/courses")""",
            ),
            (
                "Idempotent automation",
                """An idempotent job produces the same desired state when repeated. Use stable record keys, write temporary files before replacement, checkpoint progress, and distinguish a retryable failure from invalid input. Configuration belongs in environment variables or config files; secrets never belong in notebooks or logs.""",
                """def upsert_by_id(existing: list[dict], incoming: list[dict]) -> list[dict]:
    records = {record["id"]: dict(record) for record in existing}
    for record in incoming:
        if "id" not in record:
            raise ValueError("every record needs an id")
        records[record["id"]] = dict(record)
    return [records[key] for key in sorted(records)]


current = [{"id": 1, "status": "new"}]
updates = [{"id": 1, "status": "ready"}, {"id": 2, "status": "new"}]
once = upsert_by_id(current, updates)
twice = upsert_by_id(once, updates)
assert once == twice
print(once)""",
            ),
        ],
        (
            "Worked example: paginated API contract with a fake client",
            "Injecting the client makes pagination logic testable without a live service.",
            """class FakeClient:
    def __init__(self, pages):
        self.pages = pages

    def get_page(self, page: int) -> dict:
        return self.pages[page]


def collect_items(client) -> list[dict]:
    page = 1
    items = []
    while page is not None:
        payload = client.get_page(page)
        if not isinstance(payload.get("items"), list):
            raise ValueError("items must be a list")
        items.extend(payload["items"])
        page = payload.get("next_page")
    return items


client = FakeClient({
    1: {"items": [{"id": 1}], "next_page": 2},
    2: {"items": [{"id": 2}], "next_page": None},
})
print(collect_items(client))""",
        ),
        """1. Describe the four failure stages of an API request.
2. Write a paginated collector that stops on `next_page=None`.
3. Validate that each item contains `id`, `name`, and `updated_at`.
4. Make a file-export job idempotent and explain its retry policy.""",
        """def validate_item(item: dict) -> dict:
    required = {"id", "name", "updated_at"}
    if missing := required - item.keys():
        raise ValueError(f"missing keys: {sorted(missing)}")
    return {key: item[key] for key in sorted(required)}


def collect_valid_pages(client):
    page, accepted, errors = 1, [], []
    while page is not None:
        payload = client.get_page(page)
        for item in payload.get("items", []):
            try:
                accepted.append(validate_item(item))
            except ValueError as error:
                errors.append({"item": item, "error": str(error)})
        page = payload.get("next_page")
    return accepted, errors


print("Retry safe GET requests for transient timeouts and selected 5xx responses.")
print("Do not blindly retry invalid input or non-idempotent writes.")""",
        [
            ("Why must every request have a timeout?", "Otherwise it can wait indefinitely and block the job."),
            ("What does `raise_for_status` not validate?", "JSON decoding and application schema."),
            ("What makes automation idempotent?", "Repeating it converges on the same intended state."),
        ],
        ["Treat the network as unreliable.", "Validate every boundary.", "Design jobs that can be resumed and rerun safely."],
    ),
    lesson(
        "16",
        "sql-and-databases",
        "SQL and Databases with Python",
        "Use DB-API connections, parameterized SQL, transactions, row factories, and repository boundaries safely.",
        [
            "Connect to SQLite with context-managed transactions.",
            "Use parameterized queries instead of string-built SQL.",
            "Understand commit, rollback, and transaction atomicity.",
            "Separate persistence from domain transformation.",
        ],
        [
            (
                "DB-API and transactions",
                """Python database drivers follow a common pattern: connect, create a cursor, execute, fetch, and close. A transaction groups changes into one atomic unit. With SQLite, the connection context commits on success and rolls back when an exception escapes the block.""",
                """import sqlite3

connection = sqlite3.connect(":memory:")
connection.row_factory = sqlite3.Row

with connection:
    connection.execute('''
        CREATE TABLE course (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            hours INTEGER NOT NULL CHECK (hours > 0)
        )
    ''')
    connection.executemany(
        "INSERT INTO course(name, hours) VALUES (?, ?)",
        [("Python", 45), ("SQL", 30), ("Machine Learning", 60)],
    )

rows = connection.execute("SELECT name, hours FROM course ORDER BY hours").fetchall()
print([dict(row) for row in rows])""",
            ),
            (
                "Parameters prevent SQL injection",
                """Never interpolate external values into SQL text. Placeholders let the driver transmit values separately from the SQL program and handle quoting correctly. Column names and sort direction cannot normally be parameterized; map those choices through a strict allow-list.""",
                """import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE learner(name TEXT, score REAL)")
connection.executemany(
    "INSERT INTO learner VALUES (?, ?)",
    [("Asha", 88), ("Ravi", 72), ("Meera", 91)],
)

minimum = 80
rows = connection.execute(
    "SELECT name, score FROM learner WHERE score >= ? ORDER BY score DESC",
    (minimum,),
).fetchall()
print(rows)""",
            ),
            (
                "Repository boundaries",
                """A repository can isolate SQL from domain logic, but it should not hide transaction decisions or return vague untyped data everywhere. Keep queries focused, select only needed columns, enforce constraints in the database, and test persistence behavior against a temporary database.""",
                """class CourseRepository:
    def __init__(self, connection):
        self.connection = connection

    def find_by_minimum_hours(self, minimum: int) -> list[dict]:
        rows = self.connection.execute(
            "SELECT name, hours FROM course WHERE hours >= ? ORDER BY hours DESC",
            (minimum,),
        ).fetchall()
        return [dict(row) for row in rows]


# repository = CourseRepository(connection)
# print(repository.find_by_minimum_hours(40))""",
            ),
        ],
        (
            "Worked example: atomic enrollment",
            "The unique constraint prevents duplicates and the transaction keeps the operation all-or-nothing.",
            """import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute('''
    CREATE TABLE enrollment (
        learner TEXT NOT NULL,
        course TEXT NOT NULL,
        enrolled_at TEXT NOT NULL,
        UNIQUE (learner, course)
    )
''')


def enroll(connection, learner: str, course: str, enrolled_at: str) -> None:
    with connection:
        connection.execute(
            "INSERT INTO enrollment VALUES (?, ?, ?)",
            (learner, course, enrolled_at),
        )


enroll(connection, "Asha", "Python", "2026-09-09")
print(connection.execute("SELECT * FROM enrollment").fetchall())""",
        ),
        """1. Create course and enrollment tables with primary, foreign, unique, and check constraints.
2. Insert three records using `executemany`.
3. Query with a parameterized minimum score.
4. Force an error halfway through a transaction and verify that earlier work was rolled back.""",
        """import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute("PRAGMA foreign_keys = ON")
connection.executescript('''
    CREATE TABLE course (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    CREATE TABLE enrollment (
        learner TEXT NOT NULL,
        course_id INTEGER NOT NULL REFERENCES course(id),
        score REAL CHECK (score BETWEEN 0 AND 100),
        UNIQUE (learner, course_id)
    );
''')

with connection:
    connection.executemany("INSERT INTO course(name) VALUES (?)", [("Python",), ("SQL",)])
    connection.executemany(
        "INSERT INTO enrollment VALUES (?, ?, ?)",
        [("Asha", 1, 88), ("Ravi", 1, 72), ("Asha", 2, 91)],
    )

minimum = 80
rows = connection.execute(
    "SELECT learner, score FROM enrollment WHERE score >= ? ORDER BY score DESC",
    (minimum,),
).fetchall()
print(rows)""",
        [
            ("Why parameterize values?", "It separates data from SQL syntax and prevents injection."),
            ("What does rollback provide?", "Failed transaction changes are not partially persisted."),
            ("Where should core data rules live?", "At appropriate layers, including database constraints for persisted invariants."),
        ],
        ["Parameterize every external value.", "Make transaction boundaries explicit.", "Use constraints and focused repository methods."],
    ),
    lesson(
        "17",
        "concurrency-and-performance",
        "Concurrency, Performance, and Memory",
        "Measure bottlenecks and choose threads, processes, asyncio, batching, or vectorization from workload evidence.",
        [
            "Differentiate concurrency, parallelism, latency, and throughput.",
            "Choose threads for blocking I/O and processes for CPU-bound work.",
            "Use asyncio for many cooperative I/O tasks.",
            "Profile before optimizing and reason about memory growth.",
        ],
        [
            (
                "Workload first",
                """I/O-bound work spends time waiting for networks, disks, or databases; CPU-bound work spends time computing. Threads can overlap blocking I/O despite the GIL. Processes provide separate interpreters for CPU parallelism at the cost of serialization and startup. Asyncio excels when libraries expose non-blocking operations and task counts are high.""",
                """from concurrent.futures import ThreadPoolExecutor
from time import sleep


def simulated_request(item_id: int) -> dict:
    sleep(0.02)
    return {"id": item_id, "status": "ok"}


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(simulated_request, range(8)))
print(results)""",
            ),
            (
                "Asyncio is cooperative",
                """An async task yields control at `await`, allowing the event loop to run other ready tasks. Blocking functions inside async code freeze the loop unless moved to a thread. Use bounded concurrency—unlimited tasks can overwhelm the client, server, sockets, or memory.""",
                """import asyncio


async def simulated_fetch(item_id: int, semaphore: asyncio.Semaphore):
    async with semaphore:
        await asyncio.sleep(0.02)
        return {"id": item_id, "status": "ok"}


async def run_batch():
    semaphore = asyncio.Semaphore(4)
    tasks = [simulated_fetch(item_id, semaphore) for item_id in range(8)]
    return await asyncio.gather(*tasks)


# In a regular Python script: asyncio.run(run_batch())
# In a notebook with a running event loop: await run_batch()""",
            ),
            (
                "Measure time and memory",
                """Optimize the dominant measured cost. Improve algorithms and data structures before micro-optimizing syntax. Stream data rather than materializing it, batch external operations, vectorize numerical work, cache only stable expensive results, and measure realistic inputs with repeated trials.""",
                """from timeit import repeat

values = list(range(10_000))


def loop_squares():
    result = []
    for value in values:
        result.append(value * value)
    return result


def comprehension_squares():
    return [value * value for value in values]


for function in [loop_squares, comprehension_squares]:
    timings = repeat(function, number=100, repeat=5)
    print(function.__name__, min(timings))""",
            ),
        ],
        (
            "Worked example: bounded parallel I/O with result accounting",
            "Every submitted item receives either a result or a captured error, and worker count stays bounded.",
            """from concurrent.futures import ThreadPoolExecutor, as_completed


def transform(item: int) -> dict:
    if item < 0:
        raise ValueError("item cannot be negative")
    return {"input": item, "output": item * item}


items = [2, 4, -1, 8]
results, errors = [], []
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(transform, item): item for item in items}
    for future in as_completed(futures):
        item = futures[future]
        try:
            results.append(future.result())
        except ValueError as error:
            errors.append({"item": item, "error": str(error)})

print({"results": results, "errors": errors})""",
        ),
        """1. Classify file download, image resize, database query, and matrix multiplication as I/O- or CPU-bound.
2. Process ten simulated I/O tasks with at most three workers.
3. Capture per-task errors without losing successful results.
4. Benchmark two correct implementations and explain whether the difference matters operationally.""",
        """from concurrent.futures import ThreadPoolExecutor, as_completed
from time import sleep


def io_task(item: int) -> int:
    sleep(0.01)
    if item == 6:
        raise RuntimeError("simulated remote failure")
    return item * 10


successes, failures = {}, {}
with ThreadPoolExecutor(max_workers=3) as pool:
    futures = {pool.submit(io_task, item): item for item in range(10)}
    for future in as_completed(futures):
        item = futures[future]
        try:
            successes[item] = future.result()
        except RuntimeError as error:
            failures[item] = str(error)

print({"successes": successes, "failures": failures})""",
        [
            ("What is the GIL relevant to?", "Execution of Python bytecode in threads within one CPython process."),
            ("Why bound concurrency?", "To protect local and remote resources and control memory."),
            ("What should happen before optimization?", "Measure a representative workload and identify the dominant cost."),
        ],
        ["Match the model to the workload.", "Bound and account for concurrent work.", "Improve algorithms and I/O patterns before syntax-level tuning."],
    ),
    lesson(
        "18",
        "python-for-ml-ai",
        "Python for Machine Learning and AI Workflows",
        "Build leakage-resistant, reproducible training and inference code with explicit data and model contracts.",
        [
            "Separate training, validation, test, and inference responsibilities.",
            "Prevent leakage by fitting transformations only on training data.",
            "Build reproducible pipelines with controlled randomness.",
            "Define inference schemas, evaluation outputs, and model metadata.",
        ],
        [
            (
                "Training and inference are different systems",
                """Training consumes labeled historical data and produces a fitted artifact plus metrics and metadata. Inference consumes new features and returns predictions under a stable schema. Reusing one transformation pipeline is essential, but training-only operations—label access, resampling, validation splits—must never enter serving code.""",
                """from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionRequest:
    age: float
    monthly_usage: float
    support_tickets: int

    def as_features(self) -> list[float]:
        if self.age < 0 or self.monthly_usage < 0 or self.support_tickets < 0:
            raise ValueError("features cannot be negative")
        return [self.age, self.monthly_usage, float(self.support_tickets)]


request = PredictionRequest(age=32, monthly_usage=18.5, support_tickets=2)
print(request.as_features())""",
            ),
            (
                "Leakage and reproducibility",
                """Leakage occurs when training uses information unavailable at prediction time or learns preprocessing from validation/test data. Split first, then fit imputers, encoders, scalers, and feature selectors on training data only. Record random seeds, data version, feature schema, dependency versions, parameters, and metrics.""",
                """experiment = {
    "experiment_id": "churn-2026-09-09-01",
    "random_seed": 42,
    "data_version": "customers-v3",
    "target": "churned",
    "features": ["age", "monthly_usage", "support_tickets"],
    "split": {"train": 0.70, "validation": 0.15, "test": 0.15},
    "primary_metric": "roc_auc",
}

assert sum(experiment["split"].values()) == 1.0
print(experiment)""",
            ),
            (
                "Evaluation is a decision contract",
                """A metric is useful only in the context of error costs, class balance, and an operating threshold. Preserve per-slice results for important populations and time periods. A model card should state intended use, exclusions, data, metrics, limitations, and ownership.""",
                """def classification_counts(actual: list[int], predicted: list[int]) -> dict:
    if len(actual) != len(predicted):
        raise ValueError("actual and predicted lengths differ")
    tp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))
    tn = sum(a == 0 and p == 0 for a, p in zip(actual, predicted))
    fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))
    fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
    return {"tp": tp, "tn": tn, "fp": fp, "fn": fn}


print(classification_counts([1, 0, 1, 0], [1, 1, 0, 0]))""",
            ),
        ],
        (
            "Worked example: fit/transform protocol without leakage",
            "The scaler learns only from training values and reuses those parameters for validation and inference.",
            """from dataclasses import dataclass
import numpy as np


@dataclass
class StandardScaler:
    mean_: np.ndarray | None = None
    scale_: np.ndarray | None = None

    def fit(self, values: np.ndarray):
        self.mean_ = values.mean(axis=0)
        std = values.std(axis=0)
        self.scale_ = np.where(std == 0, 1, std)
        return self

    def transform(self, values: np.ndarray) -> np.ndarray:
        if self.mean_ is None or self.scale_ is None:
            raise RuntimeError("fit must be called before transform")
        return (values - self.mean_) / self.scale_


train = np.array([[20, 5], [30, 10], [40, 15]], dtype=float)
validation = np.array([[50, 20]], dtype=float)
scaler = StandardScaler().fit(train)
print(scaler.transform(train))
print(scaler.transform(validation))""",
        ),
        """1. Write separate training and inference input contracts.
2. List five leakage examples and the prevention rule for each.
3. Build a simple transformer with `fit` and `transform` methods.
4. Create model metadata containing data version, feature order, seed, metrics, threshold, and limitations.""",
        """model_metadata = {
    "model_name": "learner-completion-risk",
    "model_version": "1.0.0",
    "data_version": "enrollments-2026-09-01",
    "feature_order": ["attendance_rate", "assessment_average", "days_inactive"],
    "random_seed": 42,
    "metrics": {"roc_auc": 0.86, "recall_at_threshold": 0.78},
    "decision_threshold": 0.35,
    "intended_use": "prioritize optional learner support outreach",
    "limitations": [
        "not a measure of learner ability",
        "requires monitoring for cohort drift",
        "human review required before outreach",
    ],
}

required = {"model_version", "data_version", "feature_order", "metrics", "limitations"}
if missing := required - model_metadata.keys():
    raise ValueError(f"incomplete model metadata: {sorted(missing)}")
print(model_metadata)""",
        [
            ("When should preprocessing be fitted?", "On training data only."),
            ("Why preserve feature order?", "Many models interpret numeric arrays positionally."),
            ("Is a high aggregate metric enough?", "No; evaluate error costs, thresholds, slices, stability, and intended use."),
        ],
        ["Split before fitting transformations.", "Version the full data-to-prediction contract.", "Evaluate models as decision systems, not isolated scores."],
    ),
]


CAPSTONE = lesson(
    "19",
    "capstone-learning-analytics-pipeline",
    "Capstone: Learning Analytics Data Product",
    "Deliver a complete, tested Python pipeline that ingests learning events, validates and stores data, produces analysis, and publishes a decision-ready report.",
    [
        "Translate a business question into data and acceptance criteria.",
        "Build layered ingestion, validation, storage, transformation, and reporting code.",
        "Create automated tests, error accounting, and reproducibility metadata.",
        "Explain technical decisions, limitations, and the path to production.",
    ],
    [
        (
            "Problem and acceptance criteria",
            """The product answers: which lessons create the most difficulty, which learners may benefit from support, and whether course completion is improving. The pipeline must be safe to rerun, reject malformed data visibly, preserve valid records, and produce the same report from the same inputs. Do not infer ability or take automated action from a risk score.""",
            """ACCEPTANCE_CRITERIA = {
    "input": "JSON Lines learning events",
    "required_fields": ["event_id", "learner_id", "lesson", "event_type", "occurred_at"],
    "quality": "all rejected rows include a reason",
    "idempotency": "event_id is unique and reruns do not duplicate records",
    "outputs": ["quality summary", "lesson summary", "learner support review list"],
    "safety": "support list requires human review and is not a performance label",
}
print(ACCEPTANCE_CRITERIA)""",
        ),
        (
            "Layered architecture",
            """Use five boundaries: ingest raw lines, validate into typed records, persist with unique keys, transform into summaries, and render outputs. Keep each layer callable from tests. A run manifest records input identity, start time, code/model version when applicable, counts, and output locations.""",
            """PIPELINE = [
    "1. read JSONL without mutation",
    "2. validate schema and domain rules",
    "3. upsert accepted events by event_id",
    "4. compute lesson and learner aggregates",
    "5. render report and quality appendix",
    "6. write run manifest",
]

for stage in PIPELINE:
    print(stage)""",
        ),
        (
            "Delivery plan",
            """Complete the capstone in four gates: contract and fixtures; ingestion and validation; storage and reporting; then testing, documentation, and review. A gate is complete only when its tests and evidence pass. Optional extensions include an API source, scheduled execution, a dashboard, or a model—after the deterministic baseline is trustworthy.""",
            """DELIVERY_GATES = {
    "gate_1": ["problem statement", "event schema", "sample fixtures", "acceptance tests"],
    "gate_2": ["parser", "validator", "error report", "unit tests"],
    "gate_3": ["SQLite schema", "idempotent load", "aggregations", "charts"],
    "gate_4": ["end-to-end test", "run manifest", "README", "limitations", "demo"],
}
print(DELIVERY_GATES)""",
        ),
    ],
    (
        "Reference implementation: vertical slice",
        "This compact slice demonstrates the core contracts. Extend it with files, SQLite, charts, and a full test suite as the capstone deliverable.",
        """from dataclasses import dataclass
from datetime import datetime
import json


@dataclass(frozen=True)
class LearningEvent:
    event_id: str
    learner_id: str
    lesson: str
    event_type: str
    occurred_at: datetime


def parse_event(line: str) -> LearningEvent:
    payload = json.loads(line)
    required = {"event_id", "learner_id", "lesson", "event_type", "occurred_at"}
    if missing := required - payload.keys():
        raise ValueError(f"missing fields: {sorted(missing)}")
    if payload["event_type"] not in {"started", "completed", "assessment"}:
        raise ValueError("unsupported event_type")
    return LearningEvent(
        event_id=str(payload["event_id"]),
        learner_id=str(payload["learner_id"]),
        lesson=str(payload["lesson"]),
        event_type=payload["event_type"],
        occurred_at=datetime.fromisoformat(payload["occurred_at"]),
    )


def process_lines(lines: list[str]) -> tuple[list[LearningEvent], list[dict]]:
    accepted, rejected, seen = [], [], set()
    for number, line in enumerate(lines, start=1):
        try:
            event = parse_event(line)
            if event.event_id in seen:
                raise ValueError("duplicate event_id")
            seen.add(event.event_id)
            accepted.append(event)
        except (json.JSONDecodeError, ValueError) as error:
            rejected.append({"line": number, "reason": str(error)})
    return accepted, rejected


sample = [
    '{"event_id":"e1","learner_id":"l1","lesson":"01","event_type":"completed","occurred_at":"2026-09-09T10:00:00"}',
    '{"event_id":"e1","learner_id":"l1","lesson":"01","event_type":"completed","occurred_at":"2026-09-09T10:00:00"}',
    '{"event_id":"e2","learner_id":"l2","lesson":"02","event_type":"unknown","occurred_at":"2026-09-09T11:00:00"}',
]
accepted, rejected = process_lines(sample)
print({"accepted": len(accepted), "rejected": rejected})""",
    ),
    """**Required deliverables**

1. A data contract and at least 20 representative event fixtures.
2. Pure parsing and validation functions with normal, boundary, malformed, and duplicate tests.
3. SQLite tables with primary, unique, foreign-key, and check constraints.
4. An idempotent loader with accepted/rejected counts and reasons.
5. Lesson-level completion, assessment, and difficulty summaries.
6. A support-review list with transparent rules and an explicit human-review warning.
7. Two clear charts with titles, units, and limitations.
8. A run manifest containing input identifier, timestamp, version, counts, and outputs.
9. A README explaining execution, design decisions, quality rules, tests, and limitations.
10. A five-minute demo that begins with the business question and ends with evidence.

**Definition of done:** a clean environment can run the pipeline twice, produce no duplicates, pass all tests, and recreate the documented outputs.""",
    """# Capstone verification checklist expressed as executable assertions.
verification = {
    "fixtures_created": True,
    "schema_validated": True,
    "database_constraints_tested": True,
    "rerun_is_idempotent": True,
    "rejections_have_reasons": True,
    "reports_reproducible": True,
    "limitations_documented": True,
    "human_review_required": True,
}

incomplete = [name for name, complete in verification.items() if not complete]
assert not incomplete, f"Incomplete capstone requirements: {incomplete}"
print("Capstone definition of done satisfied")""",
    [
        ("What proves idempotency?", "Running the same input twice changes no final records or report totals."),
        ("Why keep rejected rows?", "Quality problems remain visible, countable, and diagnosable."),
        ("What belongs in the demo?", "Question, architecture, quality evidence, outputs, limitations, and next step."),
    ],
    ["Deliver a reproducible product, not only a notebook output.", "Make data quality and rerun behavior testable.", "Connect every technical choice to a user decision and limitation."],
)

ALL_NOTEBOOKS = LESSONS + [CAPSTONE]

PHASES = [
    ("Phase 1 — Core Python", "Language, decisions, collections, functions, and text.", LESSONS[0:5]),
    ("Phase 2 — Applied Python", "Files, reliability, packaging, object modeling, and Pythonic protocols.", LESSONS[5:10]),
    ("Phase 3 — Data and Delivery", "NumPy, pandas, visualization, quality, and APIs.", LESSONS[10:15]),
    ("Phase 4 — Production and AI", "Databases, concurrency, ML/AI workflows, and the capstone.", LESSONS[15:18] + [CAPSTONE]),
]


def front_matter(title: str, description: str, categories: str) -> str:
    safe_title = title.replace('"', '\\"')
    safe_description = description.replace('"', '\\"')
    return f'''---
title: "{safe_title}"
description: "{safe_description}"
author: "Edukron Notes"
date: "{DATE}"
categories: [{categories}]
toc: true
page-layout: article
execute: false
---'''


def syllabus_cards(items: list[dict]) -> str:
    cards = []
    for item in items:
        duration = "9-hour capstone" if item["number"] == "19" else "2-hour notebook"
        cards.append(
            f'''<a class="syllabus-card" href="python/{item["number"]}-{item["slug"]}.html">
<span class="lesson-number">{item["number"]}</span>
<span><strong>{item["title"]}</strong><small>{item["summary"]} · {duration}</small></span>
<i class="bi bi-arrow-right" aria-hidden="true"></i>
</a>'''
        )
    return '<div class="syllabus-grid">\n' + "\n".join(cards) + "\n</div>"


def course_overview_cells() -> list[dict]:
    cells = [
        raw_cell(
            "front-matter",
            front_matter(
                "Python — Complete Course",
                "A complete 45-hour Python syllabus for programming, data, automation, APIs, databases, and AI workflows.",
                "course, full-stack-ai, python",
            ),
        ),
        markdown_cell(
            "course-intro",
            '''<div class="course-overview-hero">
<div class="overview-lead">
<span class="topic-icon"><i class="bi bi-code-square" aria-hidden="true"></i></span>
<div><span class="overview-eyebrow">Complete notebook course</span><p>Learn Python from first principles through professional data, automation, database, and AI workflows. Every module is a focused Jupyter notebook with explanation, runnable examples, practice, solutions, and a knowledge check.</p></div>
</div>
</div>

<div class="course-stat-grid">
<div class="course-stat"><i class="bi bi-clock" aria-hidden="true"></i><strong>45 hours</strong><span>Guided learning plan</span></div>
<div class="course-stat"><i class="bi bi-journals" aria-hidden="true"></i><strong>19 notebooks</strong><span>18 lessons + capstone</span></div>
<div class="course-stat"><i class="bi bi-code-slash" aria-hidden="true"></i><strong>75+ examples</strong><span>Runnable and adaptable</span></div>
<div class="course-stat"><i class="bi bi-check2-circle" aria-hidden="true"></i><strong>Complete practice</strong><span>Exercises and solutions</span></div>
</div>''',
        ),
        markdown_cell(
            "outcomes",
            '''## What you will be able to do

By the end of this course, you will be able to design readable Python programs, model data with the right structures, build reusable functions and classes, process files and APIs, query databases safely, analyze data with NumPy and pandas, create decision-ready charts, test and type-check code, reason about performance, and structure leakage-resistant ML/AI workflows.

::: {.callout-tip}
### Recommended pace
Complete one 2-hour lesson per study session. Type every worked example, change at least one input, complete the practice before opening the solution, and record mistakes in your own notebook. Reserve the final 9 hours for the capstone.
:::''',
        ),
    ]
    for index, (title, description, items) in enumerate(PHASES, start=1):
        cells.append(markdown_cell(f"phase-{index}", f"## {title}\n\n{description}\n\n{syllabus_cards(items)}"))
    cells.extend(
        [
            markdown_cell(
                "assessment",
                '''## Assessment plan

| Evidence | Weight | Standard |
|---|---:|---|
| Lesson practice and knowledge checks | 25% | Complete every lesson and correct missed checks |
| Four phase challenges | 25% | One integrated problem after each phase |
| Code quality portfolio | 15% | Readable functions, tests, types, documentation, and Git history |
| Capstone data product | 35% | Meets the published definition of done and passes review |

**Completion standard:** at least 70% overall, every required capstone check complete, and no unresolved critical correctness or security issue.''',
            ),
            markdown_cell(
                "study-standard",
                '''## Notebook study standard

1. Read the lesson outcomes and restate them in your own words.
2. Run each example, inspect the result, and change the data.
3. Predict an output before executing the next cell.
4. Complete practice without the folded solution.
5. Answer the knowledge check aloud or in writing.
6. Commit one improved example or exercise to your portfolio.
7. Continue only when you can explain the lesson's recap without notes.

The examples use Python's standard library plus NumPy, pandas, and Matplotlib in the data modules. Network examples are designed around injected or fake clients so the notebooks remain safe and reproducible.''',
            ),
            markdown_cell(
                "start",
                '''## Start the course

[Begin with Lesson 01 — Python Language Foundations <i class="bi bi-arrow-right" aria-hidden="true"></i>](python/01-language-foundations.html)''',
            ),
        ]
    )
    return cells


def lesson_cells(item: dict, position: int) -> list[dict]:
    previous_item = ALL_NOTEBOOKS[position - 1] if position > 0 else None
    next_item = ALL_NOTEBOOKS[position + 1] if position + 1 < len(ALL_NOTEBOOKS) else None
    duration = "9-hour capstone" if item["number"] == "19" else "2-hour lesson"
    objective_list = "\n".join(f"- {objective}" for objective in item["objectives"])

    cells = [
        raw_cell(
            "front-matter",
            front_matter(
                f'{item["number"]}. {item["title"]}',
                item["summary"],
                "tutorial, full-stack-ai, python",
            ),
        ),
        markdown_cell(
            "lesson-intro",
            f'''<div class="lesson-banner">
<span class="lesson-kicker">Python course · {duration}</span>
<p>{item["summary"]}</p>
</div>

## Learning objectives

{objective_list}

::: {{.callout-note}}
### How to use this notebook
Read the explanation, predict each result, run the code, change the inputs, and complete the practice before revealing the solution.
:::''',
        ),
    ]

    for concept_index, (heading, notes, code) in enumerate(item["concepts"], start=1):
        cells.append(markdown_cell(f"concept-{concept_index}", f"## {heading}\n\n{clean(notes)}"))
        cells.append(code_cell(f"concept-code-{concept_index}", code))

    worked_title, worked_notes, worked_code = item["worked"]
    cells.extend(
        [
            markdown_cell("worked-example", f"## {worked_title}\n\n{clean(worked_notes)}"),
            code_cell("worked-code", worked_code),
            markdown_cell(
                "practice",
                f'''## Practice lab

Complete these tasks without copying the solution. Test normal, boundary, and invalid inputs where relevant.

{item["practice"]}

::: {{.callout-important}}
### Practice standard
Your answer should be readable, deterministic, and divided into small functions when the task contains more than one rule.
:::''',
            ),
            markdown_cell("solution-heading", "## Suggested solution\n\nOpen the folded code only after attempting every task."),
            code_cell("practice-solution", item["solution"], folded=True),
        ]
    )

    quiz_lines = []
    for number, (question, answer) in enumerate(item["quiz"], start=1):
        quiz_lines.append(
            f'''**{number}. {question}**

::: {{.callout-note collapse="true"}}
### Answer
{answer}
:::'''
        )
    recap_lines = "\n".join(f"- {point}" for point in item["recap"])
    previous_link = (
        f'<a href="{previous_item["number"]}-{previous_item["slug"]}.html"><i class="bi bi-arrow-left" aria-hidden="true"></i> {previous_item["title"]}</a>'
        if previous_item
        else '<a href="../python.html"><i class="bi bi-arrow-left" aria-hidden="true"></i> Course overview</a>'
    )
    next_link = (
        f'<a href="{next_item["number"]}-{next_item["slug"]}.html">{next_item["title"]} <i class="bi bi-arrow-right" aria-hidden="true"></i></a>'
        if next_item
        else '<a href="../python.html">Course overview <i class="bi bi-arrow-right" aria-hidden="true"></i></a>'
    )
    cells.extend(
        [
            markdown_cell("knowledge-check", "## Knowledge check\n\n" + "\n\n".join(quiz_lines)),
            markdown_cell("recap", f"## Recap\n\n{recap_lines}"),
            markdown_cell(
                "lesson-navigation",
                f'''<div class="lesson-nav">
{previous_link}
{next_link}
</div>''',
            ),
        ]
    )
    return cells


def main() -> None:
    write_notebook(COURSE_DIR / "python.ipynb", course_overview_cells())
    for position, item in enumerate(ALL_NOTEBOOKS):
        filename = f'{item["number"]}-{item["slug"]}.ipynb'
        write_notebook(LESSON_DIR / filename, lesson_cells(item, position))
    print(f"Generated Python course overview and {len(ALL_NOTEBOOKS)} lesson notebooks.")


if __name__ == "__main__":
    main()

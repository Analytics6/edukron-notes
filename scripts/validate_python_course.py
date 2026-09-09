"""Validate generated Python course notebooks and their code-cell syntax."""

from __future__ import annotations

import ast
import argparse
import contextlib
import io
import json
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT / "courses" / "full-stack-ai" / "python"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="Execute every code cell in notebook order")
    arguments = parser.parse_args()
    os.environ.setdefault("MPLBACKEND", "Agg")

    notebooks = sorted(COURSE_DIR.glob("*.ipynb"))
    errors: list[str] = []
    code_cells = 0
    markdown_words = 0

    if len(notebooks) != 19:
        errors.append(f"expected 19 lesson notebooks, found {len(notebooks)}")

    for path in notebooks:
        document = json.loads(path.read_text(encoding="utf-8"))
        namespace = {"__name__": "__main__"}
        cell_ids = [cell.get("id") for cell in document["cells"]]
        if len(cell_ids) != len(set(cell_ids)):
            errors.append(f"{path.name}: duplicate cell IDs")

        for cell in document["cells"]:
            text = "".join(cell.get("source", []))
            if cell["cell_type"] == "code":
                code_cells += 1
                try:
                    compiled = compile(text, filename=str(path), mode="exec")
                except SyntaxError as error:
                    errors.append(f"{path.name}:{error.lineno}: {error.msg}")
                    continue
                if arguments.execute:
                    try:
                        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                            exec(compiled, namespace)
                    except Exception as error:  # noqa: BLE001 - validator reports arbitrary lesson failures
                        errors.append(f"{path.name}:{cell.get('id')}: {type(error).__name__}: {error}")
            elif cell["cell_type"] == "markdown":
                markdown_words += len(text.split())

        if "matplotlib.pyplot" in sys.modules:
            sys.modules["matplotlib.pyplot"].close("all")

    if errors:
        raise SystemExit("\n".join(errors))

    action = "Executed and validated" if arguments.execute else "Validated"
    print(f"{action} {len(notebooks)} notebooks, {code_cells} code cells, and {markdown_words:,} words of instructional material.")


if __name__ == "__main__":
    main()

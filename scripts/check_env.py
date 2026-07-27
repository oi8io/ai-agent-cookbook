"""Verify .env.example covers all environment variables referenced in notebooks.

- Scans all notebook code cells for os.environ / os.getenv / dotenv reads.
- Compares against variables declared in .env.example.
- Reports undeclared vars (used in notebooks but missing from .env.example).
- Reports unused vars (in .env.example but never referenced).

Usage:
  python scripts/check_env.py
"""

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ENV_EXAMPLE = ROOT / ".env.example"
CHAPTERS = ROOT / "chapters"

# Known false positives — variables that .env.example does not need to declare.
KNOWN_FALSE_POSITIVES = {
    "PATH",
    "HOME",
    "USER",
    "PYTHONPATH",
    "RUN_LIVE_LLM",
    "RUN_LIVE_EVAL",
    "RUN_LIVE_TOOL_CALLING",
    "RUN_LIVE_EMBEDDING",
    "RUN_LOCAL_LLM",
}


def parse_env_example() -> set[str]:
    """Read .env.example and return declared variable names."""
    declared: set[str] = set()
    assignment = re.compile(r"^([A-Z][A-Z0-9_]*)\s*=")
    for line in ENV_EXAMPLE.read_text(encoding="utf-8").splitlines():
        match = assignment.match(line.strip())
        if match:
            declared.add(match.group(1))
    return declared


def scan_notebooks() -> set[str]:
    """Scan all notebook code cells for env var references."""
    patterns = [
        re.compile(r"""os\.getenv\(\s*["']([A-Z][A-Z0-9_]*)["']"""),
        re.compile(r"""os\.environ\.get\(\s*["']([A-Z][A-Z0-9_]*)["']"""),
        re.compile(r"""os\.environ\[\s*["']([A-Z][A-Z0-9_]*)["']\s*\]"""),
    ]
    referenced: set[str] = set()
    for path in sorted(CHAPTERS.glob("*/notebooks/*.ipynb")):
        with path.open(encoding="utf-8") as file:
            notebook = json.load(file)
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            source = "".join(cell.get("source", []))
            for pattern in patterns:
                referenced.update(pattern.findall(source))
    return referenced


def main(argv: list[str]) -> int:
    del argv
    try:
        declared = parse_env_example()
        referenced = scan_notebooks()
    except (OSError, json.JSONDecodeError) as error:
        print(f"Environment check failed: {error}", file=sys.stderr)
        return 1

    undeclared = sorted(referenced - declared - KNOWN_FALSE_POSITIVES)
    unused = sorted(declared - referenced)

    if undeclared:
        print("Undeclared environment variables:", file=sys.stderr)
        for name in undeclared:
            print(f"  - {name}", file=sys.stderr)

    if unused:
        print("Declared but not detected in notebook code:")
        for name in unused:
            print(f"  - {name}")

    if undeclared:
        return 1

    print(
        f"OK: {len(referenced)} referenced variable(s), "
        f"{len(declared)} declaration(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

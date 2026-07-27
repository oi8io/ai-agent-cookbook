"""Validate a single notebook.

Checks:
  A1 - JSON parseable
  B1 - All code cells execute in order with 0 exceptions
  D1 - No live model call triggered (RUN_LIVE_* guards must be active)

Usage:
  python scripts/validate_notebook.py chapters/04-tool-calling/notebooks/04-tool-calling.ipynb
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LIVE_GUARDS = {
    "RUN_LIVE_LLM": "0",
    "RUN_LIVE_EVAL": "0",
    "RUN_LIVE_TOOL_CALLING": "0",
    "RUN_LIVE_EMBEDDING": "0",
    "RUN_LOCAL_LLM": "0",
}


def check_json(path: Path) -> bool:
    """A1: Notebook is valid JSON."""
    try:
        with path.open(encoding="utf-8") as file:
            json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        print(f"JSON FAIL: {error}", file=sys.stderr)
        return False
    print("JSON OK")
    return True


def execute_notebook(path: Path) -> bool:
    """B1: Execute all code cells; return True if 0 errors."""
    environment = os.environ.copy()
    environment.update(LIVE_GUARDS)
    command = [
        "uv",
        "run",
        "--offline",
        "--no-cache",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--inplace",
        "--ExecutePreprocessor.timeout=600",
        str(path),
    ]
    try:
        result = subprocess.run(
            command,
            cwd=ROOT,
            env=environment,
            check=False,
            text=True,
            capture_output=True,
        )
    except OSError as error:
        print(f"EXEC FAIL: {error}", file=sys.stderr)
        return False

    if result.returncode != 0:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        return False
    print("EXEC OK")
    return True


def check_no_live_calls(path: Path) -> bool:
    """D4: Reject secret-shaped values in saved notebook outputs."""
    with path.open(encoding="utf-8") as file:
        notebook = json.load(file)

    secret_patterns = [
        re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
        re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}\b", re.IGNORECASE),
    ]
    for index, cell in enumerate(notebook.get("cells", [])):
        for output in cell.get("outputs", []):
            payload = json.dumps(output, ensure_ascii=False)
            if any(pattern.search(payload) for pattern in secret_patterns):
                print(
                    f"OUTPUT FAIL: secret-shaped value in cell {index}",
                    file=sys.stderr,
                )
                return False
    print("OUTPUT OK: no secret-shaped values detected")
    return True


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: validate_notebook.py <notebook_path>", file=sys.stderr)
        return 1
    path = Path(argv[1]).resolve()
    if not path.is_file():
        print(f"Notebook not found: {path}", file=sys.stderr)
        return 1
    if path.suffix != ".ipynb":
        print(f"Expected an .ipynb file: {path}", file=sys.stderr)
        return 1

    if not check_json(path):
        return 1
    if not execute_notebook(path):
        return 1
    if not check_no_live_calls(path):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

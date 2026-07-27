"""Check all notebooks have unique cell IDs.

- Scans every chapters/*/notebooks/*.ipynb
- Reports duplicate IDs within each notebook
- Returns non-zero if any duplicates found

Usage:
  python scripts/check_cell_ids.py              # check all notebooks
  python scripts/check_cell_ids.py --fix          # re-generate duplicate IDs
"""

import json
import sys
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"


def notebook_paths(root: Path = CHAPTERS) -> list[Path]:
    """Collect all notebook paths under chapters/."""
    return sorted(root.glob("*/notebooks/*.ipynb"))


def check_one(path: Path) -> list[str]:
    """Return duplicate or missing cell IDs in one notebook."""
    with path.open(encoding="utf-8") as file:
        notebook = json.load(file)

    seen: set[str] = set()
    problems: list[str] = []
    for index, cell in enumerate(notebook.get("cells", [])):
        cell_id = cell.get("id")
        if not cell_id:
            problems.append(f"<missing at cell {index}>")
        elif cell_id in seen:
            problems.append(cell_id)
        else:
            seen.add(cell_id)
    return problems


def fix_one(path: Path, dups: list[str]) -> None:
    """Replace missing and repeated cell IDs with new UUIDs."""
    del dups
    with path.open(encoding="utf-8") as file:
        notebook = json.load(file)

    seen: set[str] = set()
    for cell in notebook.get("cells", []):
        cell_id = cell.get("id")
        if not cell_id or cell_id in seen:
            cell_id = uuid.uuid4().hex
            cell["id"] = cell_id
        seen.add(cell_id)

    with path.open("w", encoding="utf-8") as file:
        json.dump(notebook, file, ensure_ascii=False, indent=1)
        file.write("\n")


def main(argv: list[str]) -> int:
    should_fix = "--fix" in argv[1:]
    paths = notebook_paths()
    if not paths:
        print("No notebooks found.", file=sys.stderr)
        return 1

    failed = False
    for path in paths:
        try:
            problems = check_one(path)
        except (OSError, json.JSONDecodeError) as error:
            print(f"FAIL {path.relative_to(ROOT)}: {error}", file=sys.stderr)
            failed = True
            continue

        if not problems:
            print(f"OK   {path.relative_to(ROOT)}")
            continue

        if should_fix:
            fix_one(path, problems)
            remaining = check_one(path)
            if not remaining:
                print(f"FIX  {path.relative_to(ROOT)}: {len(problems)} cell ID issue(s)")
                continue
            problems = remaining

        print(
            f"FAIL {path.relative_to(ROOT)}: {', '.join(problems)}",
            file=sys.stderr,
        )
        failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

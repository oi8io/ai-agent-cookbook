"""Compare README.md chapter status column against docs/status.md.

Reads the chapter table from README.md and the progress section from
docs/status.md. Reports any chapter whose status disagrees.

Usage:
  python scripts/sync_status.py                  # dry-run, report drift
  python scripts/sync_status.py --fix             # update README to match status.md
"""

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
STATUS = ROOT / "docs" / "status.md"


def table_rows(
    text: str,
    expected_columns: int,
    status_column: int,
) -> dict[str, str]:
    """Parse chapter/status cells from a Markdown table."""
    rows: dict[str, str] = {}
    for line in text.splitlines():
        if not line.startswith("|"):
            continue
        parts = line.split("|")
        if len(parts) != expected_columns + 2:
            continue
        chapter = parts[1].strip()
        if len(chapter) == 2 and chapter.isdigit():
            rows[chapter] = parts[status_column].strip()
    return rows


def parse_readme_status() -> dict[str, str]:
    """Parse README.md chapter table -> {chapter_num: status_string}."""
    return table_rows(
        README.read_text(encoding="utf-8"),
        expected_columns=5,
        status_column=5,
    )


def parse_status_md() -> dict[str, str]:
    """Parse docs/status.md -> {chapter_num: canonical_status}."""
    text = STATUS.read_text(encoding="utf-8")
    marker = "## 章节状态"
    if marker not in text:
        return {}
    section = text.split(marker, maxsplit=1)[1]
    return table_rows(section, expected_columns=3, status_column=2)


def report_drift(readme: dict, canonical: dict) -> list[str]:
    """Return list of chapters where status differs."""
    drift: list[str] = []
    for chapter in sorted(set(readme) | set(canonical)):
        readme_value = readme.get(chapter, "<missing>")
        canonical_value = canonical.get(chapter, "<missing>")
        if readme_value != canonical_value:
            drift.append(
                f"{chapter}: README={readme_value!r}, status.md={canonical_value!r}"
            )
    return drift


def fix_readme(canonical: dict) -> None:
    """Rewrite README.md chapter table status column from canonical."""
    output: list[str] = []
    for line in README.read_text(encoding="utf-8").splitlines(keepends=True):
        parts = line.rstrip("\n").split("|")
        if len(parts) == 7:
            chapter = parts[1].strip()
            if chapter in canonical:
                parts[5] = f" {canonical[chapter]} "
                newline = "\n" if line.endswith("\n") else ""
                line = "|".join(parts) + newline
        output.append(line)
    README.write_text("".join(output), encoding="utf-8")


def main(argv: list[str]) -> int:
    try:
        canonical = parse_status_md()
        readme = parse_readme_status()
    except OSError as error:
        print(f"Status check failed: {error}", file=sys.stderr)
        return 1

    if not canonical:
        print("No canonical chapter status table found.", file=sys.stderr)
        return 1

    drift = report_drift(readme, canonical)
    if drift and "--fix" in argv[1:]:
        fix_readme(canonical)
        readme = parse_readme_status()
        drift = report_drift(readme, canonical)

    if drift:
        print("Chapter status drift:", file=sys.stderr)
        for item in drift:
            print(f"  - {item}", file=sys.stderr)
        return 1

    print(f"OK: {len(canonical)} chapter status entries are synchronized")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

#!/usr/bin/env python3
"""Block diff changes that take the cheapest path around project constraints."""

from __future__ import annotations

import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DiffLine:
    path: str
    text: str


def git(*args: str, accepted: tuple[int, ...] = (0,)) -> str | None:
    result = subprocess.run(
        ("git", *args),
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode in accepted else None


def is_test_path(path: str) -> bool:
    name = Path(path).name
    return "tests/" in path or name.startswith("test_") or "_test." in name


def collect_diff(base: str) -> str | None:
    if git("rev-parse", "--verify", base) is None:
        return None

    tracked = git("diff", "--unified=0", base, "--")
    untracked_names = git("ls-files", "--others", "--exclude-standard")
    if tracked is None or untracked_names is None:
        return None

    untracked_diffs: list[str] = []
    for path in filter(None, untracked_names.splitlines()):
        diff = git(
            "diff",
            "--no-index",
            "--unified=0",
            "/dev/null",
            path,
            accepted=(0, 1),
        )
        if diff is None:
            return None
        untracked_diffs.append(diff)
    return "\n".join((tracked, *untracked_diffs))


def parse_lines(diff: str) -> tuple[list[DiffLine], list[DiffLine]]:
    added: list[DiffLine] = []
    removed: list[DiffLine] = []
    path = ""
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[4:].removeprefix("b/")
        elif line.startswith("+") and not line.startswith("+++"):
            added.append(DiffLine(path, line[1:]))
        elif line.startswith("-") and not line.startswith("---"):
            removed.append(DiffLine(path, line[1:]))
    return added, removed


def constraint_rows(lines: list[DiffLine]) -> dict[str, str]:
    rows: dict[str, str] = {}
    for line in lines:
        if line.path != "CONSTRAINTS.md" or not line.text.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.text.strip("|").split("|")]
        if len(cells) >= 2 and cells[0] not in {"Dimension", "---"}:
            rows[cells[0]] = line.text
    return rows


def first_number(text: str) -> float | None:
    match = re.search(r"\d+(?:\.\d+)?", text)
    return float(match.group()) if match else None


def main() -> int:
    base = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "HEAD"
    diff = collect_diff(base)
    if diff is None:
        print(f"floor-guard: cannot compare working tree with {base}", file=sys.stderr)
        return 2

    added, removed = parse_lines(diff)
    findings: list[tuple[str, str]] = []

    suppressions = re.compile(
        r"#\s*noqa|#\s*type:\s*ignore|nosemgrep|gitleaks:allow|"
        r"pytest\.mark\.skip|istanbul ignore|Stryker disable"
    )
    stubs = re.compile(
        r"\bTODO\b|NotImplemented(?:Error)?|except(?:\s+\w+)?\s*:\s*pass|"
        r"\bpass\s*#\s*stub",
        re.IGNORECASE,
    )
    skips = re.compile(r"pytest\.mark\.skip|pytest\.skip\(|\bunittest\.skip")

    for line in added:
        if suppressions.search(line.text):
            findings.append(("silenced-checker", line.path))
        if stubs.search(line.text):
            findings.append(("unfinished-work", line.path))
        if is_test_path(line.path) and skips.search(line.text):
            findings.append(("test-made-easier", line.path))
        if line.path == "CONSTRAINTS.md" and re.match(r"\|\s*[A-Z]\d+\s*\|", line.text):
            findings.append(("new-exception", line.path))

    for line in removed:
        assertion = re.search(r"\b(assert|expect|should)\b", line.text)
        if is_test_path(line.path) and assertion:
            findings.append(("assertion-removed", line.path))
        if line.path == "CONSTRAINTS.md" and line.text.startswith("- "):
            findings.append(("constraint-removed", line.path))

    statuses = git("diff", "--name-status", base, "--") or ""
    for status in statuses.splitlines():
        kind, _, path = status.partition("\t")
        if kind == "D" and is_test_path(path):
            findings.append(("test-deleted", path))

    old_rows = constraint_rows(removed)
    new_rows = constraint_rows(added)
    for dimension, old_row in old_rows.items():
        new_row = new_rows.get(dimension)
        if not new_row:
            continue
        old_value = first_number(old_row)
        new_value = first_number(new_row)
        if old_value is None or new_value is None:
            continue
        minimum = re.search(r"at least|≥|minimum", old_row, re.IGNORECASE)
        maximum = re.search(r"at or below|≤|maximum", old_row, re.IGNORECASE)
        if (minimum and new_value < old_value) or (maximum and new_value > old_value):
            findings.append(("threshold-weakened", "CONSTRAINTS.md"))

    if not findings:
        print("floor-guard: clean")
        return 0

    print(f"floor-guard: {len(findings)} violation(s)", file=sys.stderr)
    for rule, path in sorted(set(findings)):
        print(f"  [{rule}] {path}", file=sys.stderr)
    print("Fix the change or route it through a tracked exception.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

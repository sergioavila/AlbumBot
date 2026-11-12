#!/usr/bin/env python3
"""Fail when an OSV Scanner JSON report contains high-severity findings."""

from __future__ import annotations

import json
import sys
from typing import Any


def high_findings(report: dict[str, Any], minimum: float = 7.0) -> set[tuple[str, str]]:
    findings: set[tuple[str, str]] = set()
    for result in report.get("results", []):
        for package_result in result.get("packages", []):
            package = package_result.get("package", {}).get("name", "unknown")
            for group in package_result.get("groups", []):
                try:
                    severity = float(group.get("max_severity", 0))
                except (TypeError, ValueError):
                    continue
                if severity >= minimum:
                    ids = group.get("ids", ["unknown"])
                    findings.add((package, ids[0]))
    return findings


def main() -> int:
    try:
        report = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as error:
        print(f"osv-gate: invalid scanner output: {error}", file=sys.stderr)
        return 2

    findings = high_findings(report)
    if not findings:
        print("osv-gate: no high or critical vulnerabilities")
        return 0

    print(f"osv-gate: {len(findings)} high or critical finding(s)", file=sys.stderr)
    for package, vulnerability in sorted(findings):
        print(f"  {package}: {vulnerability}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Turn new constraint failures into warnings during the adoption window."""

from __future__ import annotations

import subprocess
import sys
from datetime import date

ADOPTION_END = date(2026, 11, 25)


def is_adoption_period(today: date) -> bool:
    return today <= ADOPTION_END


def main() -> int:
    args = sys.argv[1:]
    if args[:1] == ["--"]:
        args = args[1:]
    if not args:
        print("adoption-gate: command required", file=sys.stderr)
        return 2

    result = subprocess.run(args, check=False)
    if result.returncode == 0 or not is_adoption_period(date.today()):
        return result.returncode

    print(
        f"adoption-gate: warning until {ADOPTION_END.isoformat()}; "
        f"command exited {result.returncode}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

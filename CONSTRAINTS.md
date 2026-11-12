# Constraints

Last reviewed: 2026-11-11 by the project owner

The floor blocks immediately. Numbered checks warn during adoption through
2026-11-25 and block after that date. Do not extend the adoption window to make
a failing change pass.

## Floor

- No new suppression comments: `# noqa`, `# type: ignore`, `nosemgrep`, or
  `gitleaks:allow`.
- No unimplemented stubs, empty exception handlers, or placeholder TODOs.
- No skipped or deleted tests without an explicit tracked reason.
- No secrets in source or diagnostic output.
- Do not weaken this file, its commands, or its thresholds to make a change
  pass.
- New exceptions require an owner, reason, issue, and expiry within 90 days.

## Enforced with numbers

| Dimension | Rule and reason | Checked by | Runs at |
| --- | --- | --- | --- |
| Types | Zero mypy errors; type failures hide invalid integrations | `make typecheck` | Every task |
| Lint | Zero Ruff errors; deterministic style keeps reviews focused | `make lint` | Every task |
| Changed coverage | At least 80%; new behavior needs executable evidence | `make coverage` | Task end |
| Secrets | Zero findings; one leaked credential is unacceptable | `make security-secrets` | Full check |
| Security: code | Zero ERROR findings; these represent high-confidence risk | `make security-code` | Full check |
| Security: dependencies | Zero high or critical findings; lower severities remain visible without blocking | `make security-deps` | Full check |

Every numeric rule has a command that produces its verdict. `CONSTRAINTS.md` is
canonical if a wrapper command drifts from this table.

## Measured, not yet enforced

| Metric | Baseline | Direction |
| --- | --- | --- |
| Project branch coverage | 80% on 2026-11-11 | Must not fall by more than 0.5 percentage points |
| `make check-task` duration | 3.2 seconds on 2026-11-11 | Must remain at or below 90 seconds |

## Lifecycle

- `make check-fast`: floor, lint, and types after edits.
- `make check-task`: fast checks plus tests and changed-line coverage before a
  handoff; budget 90 seconds.
- `make check-full`: task checks plus external security checks when closing an
  effort or preparing a release. It has no local time limit.
- Security reports name the rule and location but never print a matched secret
  value.

## Exceptions

No active exceptions.

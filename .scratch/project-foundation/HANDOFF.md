# Project Foundation Handoff

Status: ready-for-agent

## Objective

The AlbumBot memory, handoff, and constraint foundation described in `spec.md`
is complete.

## Completed

- Initialized Git on `main` and created a baseline commit.
- Added reproducible development dependencies.
- Added domain memory, domain-doc rules, and ADR guidance.
- Added local tracker, triage, specification, and issue conventions.
- Added the quality bar, floor guard, and reproducible check commands.
- Added API, floor-guard, adoption-gate, and OSV-gate tests.
- Removed the unused vulnerable multipart dependency.

## Verification

- `make check-task`: 8 tests passed, 80% branch coverage, 3.2-second pilot.
- Gitleaks: no leaks.
- Semgrep: 141 rules, no ERROR findings.
- OSV Scanner: no high or critical vulnerabilities.
- `make check-full`: passed.
- Adoption-gate failure probe: converted exit 7 to a warning as expected.

## Decisions

- Local markdown is the issue tracker.
- The repository is the canonical memory; conversation history is not.
- Domain documentation uses a single context.
- The floor blocks immediately. Numbered checks warn through 2026-11-25 and
  block afterward.
- Security gates use pinned containers; OSV blocks CVSS 7.0 and above.

## Risks and blockers

- The local pilot used macOS Python 3.9 and emitted end-of-life/OpenSSL
  warnings. The application container remains Python 3.11 and should be used
  for runtime parity.
- The pinned FastAPI/HTTPX combination emits a TestClient deprecation warning.
  It does not affect the current tests.

## Next ticket

`.scratch/album-catalog/issues/01-define-album-model.md`

# Project Foundation Handoff

Status: ready-for-agent

## Objective

Finish the AlbumBot memory, handoff, and constraint foundation described in
`spec.md`.

## Completed

- Initialized Git on `main` and created a baseline commit.
- Added reproducible development dependencies.
- Added domain memory, domain-doc rules, and ADR guidance.
- Added local tracker, triage, specification, and issue conventions.
- Added the quality bar, floor guard, and reproducible check commands.

## Verification

- Pending until issue 05.

## Decisions

- Local markdown is the issue tracker.
- The repository is the canonical memory; conversation history is not.
- Domain documentation uses a single context.
- The floor blocks immediately. Numbered checks warn through 2026-11-25 and
  block afterward.
- Security gates use pinned containers; OSV blocks CVSS 7.0 and above.

## Risks and blockers

- Pilot tests, external security checks, and baseline measurements are pending.

## Next ticket

`.scratch/project-foundation/issues/05-pilot-verification.md`

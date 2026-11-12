# Issue Tracker: Local Markdown

Issues, specs, and handoffs for this repository live in `.scratch/`.

## Conventions

- One effort per directory: `.scratch/<feature-slug>/`.
- The specification is `.scratch/<feature-slug>/spec.md`.
- Implementation issues are individual files under
  `.scratch/<feature-slug>/issues/<NN>-<slug>.md`.
- `Status:` uses the role strings defined in `triage-labels.md`. A completed
  issue uses `resolved`.
- Append conversation history under `## Comments`; do not rewrite prior
  comments.
- The active effort has one `HANDOFF.md`.

## Publishing and fetching

When a skill publishes to the issue tracker, create the appropriate file under
`.scratch/<feature-slug>/`. When it fetches a ticket, read the referenced issue
file directly.

## Handoff contract

Before handing work to another agent or human, update `HANDOFF.md` with:

1. Objective and current status
2. Completed changes
3. Verification commands and results
4. Durable decisions and related ADRs
5. Risks or blockers
6. The exact next ticket

Use `ready-for-agent` when the next step is fully specified and
`ready-for-human` when it requires judgment, credentials, or approval.

Stable domain facts belong in `CONTEXT.md`; architectural decisions belong in
an ADR. Do not duplicate them in a handoff.

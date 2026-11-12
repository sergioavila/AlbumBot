# Project Foundation

## Goal

Make AlbumBot safe to continue across agent sessions by establishing durable
domain memory, local issue tracking, explicit handoffs, and measurable quality
constraints.

## Acceptance criteria

- A new agent can discover project rules from `AGENTS.md`.
- Stable domain facts live in `CONTEXT.md`; durable decisions live in ADRs.
- Active task state lives in this effort's `HANDOFF.md`.
- The quality floor, coverage ratchet, and security checks have runnable
  commands.
- The current API has a small passing test suite and a recorded baseline.

## Out of scope

This effort does not implement album persistence, semantic search, Gemini
generation, Airflow, or dbt.

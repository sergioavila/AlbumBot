# Domain Docs

This repository uses a single domain context.

## Before exploring

- Read `CONTEXT.md` at the repository root.
- Read ADRs in `docs/adr/` that affect the area being changed.
- If either location is absent, proceed without creating speculative content.

## Use the glossary

Use domain terms as defined in `CONTEXT.md` in issue titles, code, tests, and
documentation. Do not introduce synonyms for concepts that already have a
defined name.

If a required concept is missing, first determine whether it is unnecessary or
whether the glossary has a real gap. Record stable domain knowledge in
`CONTEXT.md`, not in a session handoff.

## Respect decisions

Surface any conflict with an existing ADR instead of silently overriding it.
Create an ADR only when a durable architectural decision has actually been
made.

## Source precedence

When records disagree, use this order:

1. Verified code and tests
2. Accepted ADRs
3. `CONTEXT.md`
4. The active handoff

Conversation history is not a canonical project record.

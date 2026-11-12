# Define the Album persistence model

Status: ready-for-agent

Add an `Album` SQLModel mapped to `album_catalog` with a UUID primary key,
title, artist, description, primary genre, and a 768-dimension pgvector
embedding.

## Acceptance

- Names use the glossary in `CONTEXT.md`.
- Required metadata rejects missing or empty values at the validation boundary.
- Table metadata and validation behavior have focused tests.
- Existing API behavior and `make check-task` remain green.
- Search, ingestion, and recommendation logic are not added in this ticket.

## Comments

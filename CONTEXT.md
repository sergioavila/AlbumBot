# AlbumBot Domain Context

AlbumBot is a semantic discovery API for music albums. Its intended flow is to
ingest album metadata, create embeddings from album descriptions, retrieve
similar albums for a natural-language query, and use those results to produce a
conversational recommendation.

## Glossary

- **Album**: a released collection of recorded music. It is the primary catalog
  entity and has a title, artist, description, and primary genre.
- **Artist**: the primary recording artist credited for an album.
- **Genre**: the primary musical category assigned to an album.
- **AlbumDescription**: cleaned text describing an album's sound, themes, era,
  and other searchable characteristics.
- **Embedding**: a vector representation of an AlbumDescription used for
  semantic similarity search.
- **Recommendation**: a listener-facing explanation grounded in albums returned
  by semantic search.

## Current boundaries

- The FastAPI service exposes `/`, `/search`, and `/chat`.
- PostgreSQL with pgvector is the intended catalog and vector store.
- Gemini is the intended embeddings and text-generation provider.
- Docker Compose supplies the API and PostgreSQL development services.

## Not implemented yet

- There is no Album SQLModel or persisted album catalog.
- `/search` returns placeholder album names and does not create embeddings.
- `/chat` returns a placeholder response and does not call Gemini.
- The Airflow and dbt pipeline described in the specification does not exist.

Do not describe these planned capabilities as working until code and tests
demonstrate them.

# Documentation

This repository follows the shared documentation standard:

- [standards/documentation.md](https://github.com/softwareone-platform/mpt-extension-skills/blob/main/standards/documentation.md)

This file documents repository-specific documentation rules only.

## Repository Rules

- `README.md` must stay concise and act as the main human entry point.
- `AGENTS.md` must stay operational and tell AI agents which files to read first.
- Topic-specific documentation must live in the matching file under [`docs/`](.).
- Shared engineering rules must be linked from `mpt-extension-skills` instead of copied into this repository.
- When changing setup, usage, testing, or architecture behavior, update the corresponding document in the same change.
- `docs/usage.md` is the source of truth for installation, configuration, examples, and supported command entry points.

## Current Documentation Map

- [`README.md`](../README.md): overview, quick start, and documentation map
- [`AGENTS.md`](../AGENTS.md): AI-agent entry point and reading order
- [`usage.md`](usage.md): install, configure, and use the client
- [`architecture.md`](architecture.md): repository structure and major abstractions
- [`local-development.md`](local-development.md): Docker-only local setup and execution
- [`testing.md`](testing.md): repository-specific testing strategy
- [`contributing.md`](contributing.md): repository workflow and shared-standard links
- [`rql.md`](rql.md): RQL query builder guide

## Change Rule

Prefer updating the smallest relevant document instead of creating overlapping summary files.

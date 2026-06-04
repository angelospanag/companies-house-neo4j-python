# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All tasks run via `mise run <task>`. The toolchain (Python 3.14, uv) is pinned in `mise.toml`.

| Task | Command |
|---|---|
| Install dependencies | `mise run install` |
| Format | `mise run fmt` |
| Lint | `mise run lint` |
| Type check | `mise run typecheck` |
| Vulnerability audit | `mise run vuln` |
| Run tests | `mise run test` |
| Upgrade dependencies | `mise run deps` |

## Architecture

This is a CLI application — there is no web server. Entry point is `main.py`, which accepts a Companies House company number and recursively stores the company graph (officers, persons with significant control) in Neo4j.

- `src/config.py` — pydantic-settings config loaded from `.env`
- `src/companies_house_api.py` — HTTP client functions for the Companies House Public Data API
- `src/graph.py` — Neo4j write logic; recursively traverses corporate officers and PSCs

Run with:

```bash
uv run python main.py <COMPANY_NUMBER>
```

Tests live in `tests/`. `tests/conftest.py` sets required environment variables before any app import. API functions are tested with `unittest.mock.patch` over `requests.get` — no real API key or Neo4j instance needed.

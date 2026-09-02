# AGENTS.md

## Project Overview

A categorized collection following the [Agent Skills Specification](https://agentskills.io/specification).

- `skills/writing/`: Chinese writing assistants. The workflow is **collect (style-extract, material-ingest) -> retrieve (material-retrieve) -> create (compose) -> polish (rewrite, title-gen)**. `rewrite-en2zh` is standalone.
- `skills/misc/`: General-purpose agent utilities.

Skills are installed via `npx skills add simonwong/skills`.

## Architecture

Each skill lives in `skills/<category>/<skill-name>/`. A skill contains `SKILL.md` and only the resources its workflow needs. Category directories do not contain `SKILL.md`.

### Shared Data Directory

All skills read/write a shared `./writing-workspace/` directory at runtime:

```
writing-workspace/
├── styles/
│   ├── my_style.json          # Primary style profile (used by compose, rewrite)
│   ├── index.jsonl             # Style entry index
│   └── entries/sty_*.json      # Individual style analyses
├── materials/
│   ├── index.jsonl             # Material entry index
│   └── entries/mat_*.json      # Individual material entries
└── drafts/                     # Saved article drafts
```

- Index files use **JSONL** format (one JSON object per line).
- Entry IDs follow `sty_YYYYMMDD_NNN` / `mat_YYYYMMDD_NNN` patterns.
- JSON text fields must properly escape `"`, `\`, and newlines.

### Skill Dependency Graph

- **style-extract** produces `styles/my_style.json` and `styles/entries/`.
- **material-ingest** produces `materials/index.jsonl` and `materials/entries/`.
- **material-retrieve** reads `materials/index.jsonl` + `materials/entries/`.
- **compose** reads `styles/my_style.json` + `materials/index.jsonl` (auto-retrieves relevant materials).
- **rewrite** reads `styles/my_style.json`.
- **title-gen** reads `styles/my_style.json` (optional, for title pattern preferences).
- **rewrite-en2zh** is standalone with no data dependencies.

## Conventions

- Writing skill content and user-facing output is in **Simplified Chinese**.
- Writing skill front matter fields: `name`, `description`, `license`, `metadata.author`, `metadata.version`.
- Version strings are quoted (e.g., `"1.1.0"`).
- A writing skill's `description` doubles as trigger-phrase documentation and lists its Chinese activation phrases.
- When modifying a writing skill's `SKILL.md`, bump its `metadata.version`.
- Keep general-purpose skills self-contained and preserve their explicit invocation policy in both `SKILL.md` and `agents/openai.yaml` when present.

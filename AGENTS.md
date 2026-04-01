# AGENTS.md

## Project Overview

A collection of Chinese writing-assistant skills following the [Agent Skills Specification](https://agentskills.io/specification). The workflow is: **collect (style-extract, material-ingest) -> retrieve (material-retrieve) -> create (compose) -> polish (rewrite, title-gen)**. There is also a standalone `rewrite-en2zh` skill for English-to-Chinese rewriting.

Skills are installed via `npx skills add simonwong/writing-skills`.

## Architecture

Each skill lives in `skills/<skill-name>/` and contains a single `SKILL.md` file that defines the skill's metadata (YAML front matter) and full behavioral prompt (Markdown body). There is no build step, no runtime code, and no tests — the entire project is structured Markdown.

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

- All skill content and user-facing output is in **Simplified Chinese**.
- SKILL.md front matter fields: `name`, `description`, `license`, `metadata.author`, `metadata.version`.
- Version strings are quoted (e.g., `"1.1.0"`).
- The `description` field doubles as trigger-phrase documentation — it lists the Chinese phrases that should activate the skill.
- When modifying a skill's `SKILL.md`, bump its `metadata.version` in the YAML front matter.

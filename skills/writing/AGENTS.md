# Writing Skills

These skills form a Simplified Chinese writing workflow:

`collect (style-extract, material-ingest) -> retrieve (material-retrieve) -> create (compose) -> polish (rewrite, title-gen)`

`rewrite-en2zh` is standalone.

## Shared Data Contract

The connected writing workflow skills read and write `./writing-workspace/` at runtime. `rewrite-en2zh` does not use it.

```text
writing-workspace/
├── styles/
│   ├── my_style.json
│   ├── index.jsonl
│   └── entries/sty_*.json
├── materials/
│   ├── index.jsonl
│   └── entries/mat_*.json
└── drafts/
```

- Store one JSON object per line in index files.
- Use `sty_YYYYMMDD_NNN` and `mat_YYYYMMDD_NNN` entry IDs.
- Escape quotes, backslashes, and newlines in JSON text fields.

## Dependencies

- `style-extract` writes `styles/my_style.json`, `styles/index.jsonl`, and `styles/entries/`.
- `material-ingest` writes `materials/index.jsonl` and `materials/entries/`.
- `material-retrieve` reads `materials/index.jsonl` and `materials/entries/`.
- `compose` reads `styles/my_style.json` and `materials/index.jsonl`, then retrieves relevant material.
- `rewrite` reads `styles/my_style.json`.
- `title-gen` may read `styles/my_style.json` for title preferences.
- `rewrite-en2zh` has no shared-data dependency.

When changing a shared schema, update every producer and consumer in the same change.

## Writing Rules

- Write skill instructions and user-facing output in Simplified Chinese.
- Keep `name`, `description`, `license`, `metadata.author`, and `metadata.version` in each `SKILL.md` frontmatter.
- Quote version strings, for example `"1.2.0"`.
- Include concrete Chinese trigger phrases in `description`.
- Bump `metadata.version` whenever a writing skill's `SKILL.md` changes.

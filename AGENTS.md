# AGENTS.md

## Repository

This repository contains composable skills organized by purpose:

- `skills/writing/`: Simplified Chinese writing skills.
- `skills/engineering/`: Code quality and engineering workflow skills.
- `skills/misc/`: General-purpose agent utilities.

Each skill lives at `skills/<category>/<skill-name>/`. Keep its `SKILL.md` and supporting resources together. Category directories organize skills and must not contain a `SKILL.md`.

Before changing anything under `skills/writing/`, read `skills/writing/AGENTS.md` for the shared data contract, dependency graph, and writing-specific rules.

## Working Rules

- Read the target skill and its local instructions before editing it.
- Keep changes scoped to the requested skills. Preserve unrelated work.
- Keep skills self-contained. Add supporting files only when the workflow needs them.
- Preserve explicit-invocation settings in both `SKILL.md` and `agents/openai.yaml` when present.
- Write agent-facing instructions as short, imperative steps. Keep final-state docs free of migration history and discarded approaches.

## Validation

- Validate every changed `SKILL.md` against the [Agent Skills Specification](https://agentskills.io/specification), allowing documented client-specific frontmatter extensions such as `disable-model-invocation`.
- Check links and paths referenced by changed instructions.
- Run `git diff --check` before committing.

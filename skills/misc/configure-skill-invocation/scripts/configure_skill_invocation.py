#!/usr/bin/env python3
"""Scan and configure explicit-only invocation policy for selected skills."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


SKIP_DIRS = {"__pycache__", "build", "dist", "node_modules"}


@dataclass(frozen=True)
class Candidate:
    name: str
    path: Path
    missing: tuple[str, ...]

    def as_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "path": str(self.path),
            "missing": list(self.missing),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Configure selected skills for explicit-only invocation."
    )
    parser.add_argument("scope", choices=("global", "project"))
    parser.add_argument("--cwd", type=Path, default=Path.cwd(), help=argparse.SUPPRESS)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--scan", action="store_true")
    mode.add_argument("--apply", nargs="+", metavar="SKILL_DIR")
    return parser.parse_args()


def find_project_root(cwd: Path) -> Path:
    cwd = cwd.expanduser().resolve()
    for path in (cwd, *cwd.parents):
        if (path / ".git").exists():
            return path
    return cwd


def scope_roots(scope: str, cwd: Path) -> list[Path]:
    if scope == "global":
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        roots = [Path.home() / ".agents" / "skills", codex_home / "skills"]
    else:
        project_root = find_project_root(cwd)
        roots = [project_root / ".agents" / "skills", project_root / ".codex" / "skills"]

    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root.expanduser().resolve(strict=False))
        if key not in seen:
            unique.append(root.expanduser())
            seen.add(key)
    return unique


def discover_skill_dirs(roots: list[Path]) -> list[Path]:
    skills: list[Path] = []
    seen_dirs: set[str] = set()
    seen_skills: set[str] = set()

    for root in roots:
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
            current = Path(dirpath)
            real_current = str(current.resolve())
            if real_current in seen_dirs:
                dirnames[:] = []
                continue
            seen_dirs.add(real_current)

            dirnames[:] = [
                name
                for name in dirnames
                if not name.startswith(".") and name not in SKIP_DIRS
            ]
            if "SKILL.md" not in filenames:
                continue

            dirnames[:] = []
            if real_current in seen_skills:
                continue
            seen_skills.add(real_current)
            skills.append(current.absolute())

    return sorted(skills, key=lambda path: str(path).lower())


def frontmatter(text: str) -> tuple[list[str], int]:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md 缺少起始 YAML frontmatter 分隔符")
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines, index
    raise ValueError("SKILL.md 缺少结束 YAML frontmatter 分隔符")


def top_level_value(lines: list[str], end: int, key: str) -> str | None:
    pattern = re.compile(rf"^{re.escape(key)}\s*:\s*(.*?)\s*$")
    for line in lines[1:end]:
        match = pattern.match(line.rstrip("\r\n"))
        if match:
            return match.group(1).split(" #", 1)[0].strip()
    return None


def yaml_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().strip("'\"").lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    return None


def read_name_and_model_policy(skill_md: Path) -> tuple[str, bool]:
    lines, end = frontmatter(skill_md.read_text(encoding="utf-8"))
    name = top_level_value(lines, end, "name") or skill_md.parent.name
    enabled = yaml_bool(top_level_value(lines, end, "disable-model-invocation")) is True
    return name.strip("'\""), enabled


def openai_policy_disabled(openai_yaml: Path) -> bool:
    if not openai_yaml.is_file():
        return False
    lines = openai_yaml.read_text(encoding="utf-8").splitlines()
    policy_index: int | None = None
    for index, line in enumerate(lines):
        if re.match(r"^policy\s*:\s*(?:#.*)?$", line):
            policy_index = index
            break
    if policy_index is None:
        return False

    for line in lines[policy_index + 1 :]:
        if line.strip() and not line.lstrip().startswith("#") and not line.startswith((" ", "\t")):
            break
        match = re.match(r"^\s{2}allow_implicit_invocation\s*:\s*(.*?)\s*$", line)
        if match:
            return yaml_bool(match.group(1).split(" #", 1)[0]) is False
    return False


def inspect_skills(roots: list[Path]) -> tuple[list[Candidate], list[dict[str, str]]]:
    candidates: list[Candidate] = []
    invalid: list[dict[str, str]] = []
    for skill_dir in discover_skill_dirs(roots):
        skill_md = skill_dir / "SKILL.md"
        try:
            name, model_disabled = read_name_and_model_policy(skill_md)
        except (OSError, UnicodeError, ValueError) as error:
            invalid.append({"path": str(skill_dir), "error": str(error)})
            continue

        missing: list[str] = []
        if not model_disabled:
            missing.append("SKILL.md:disable-model-invocation")
        if not openai_policy_disabled(skill_dir / "agents" / "openai.yaml"):
            missing.append("agents/openai.yaml:policy.allow_implicit_invocation")
        if missing:
            candidates.append(Candidate(name=name, path=skill_dir, missing=tuple(missing)))
    return candidates, invalid


def set_model_policy(text: str) -> str:
    lines, end = frontmatter(text)
    pattern = re.compile(r"^disable-model-invocation\s*:")
    for index in range(1, end):
        if pattern.match(lines[index]):
            newline = "\r\n" if lines[index].endswith("\r\n") else "\n"
            lines[index] = f"disable-model-invocation: true{newline}"
            return "".join(lines)
    lines.insert(end, "disable-model-invocation: true\n")
    return "".join(lines)


def set_openai_policy(text: str) -> str:
    lines = text.splitlines(keepends=True)
    policy_index: int | None = None
    for index, line in enumerate(lines):
        match = re.match(r"^policy\s*:\s*(.*?)\s*$", line.rstrip("\r\n"))
        if match:
            value = match.group(1).split(" #", 1)[0].strip()
            if value:
                raise ValueError("agents/openai.yaml 的 policy 必须是 YAML mapping")
            policy_index = index
            break

    if policy_index is None:
        if text and not text.endswith(("\n", "\r")):
            lines.append("\n")
        if lines and any(line.strip() for line in lines):
            lines.append("\n")
        lines.extend(["policy:\n", "  allow_implicit_invocation: false\n"])
        return "".join(lines)

    block_end = len(lines)
    for index in range(policy_index + 1, len(lines)):
        line = lines[index]
        if line.strip() and not line.lstrip().startswith("#") and not line.startswith((" ", "\t")):
            block_end = index
            break

    pattern = re.compile(r"^\s{2}allow_implicit_invocation\s*:")
    for index in range(policy_index + 1, block_end):
        if pattern.match(lines[index]):
            newline = "\r\n" if lines[index].endswith("\r\n") else "\n"
            lines[index] = f"  allow_implicit_invocation: false{newline}"
            return "".join(lines)

    lines.insert(policy_index + 1, "  allow_implicit_invocation: false\n")
    return "".join(lines)


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode if path.exists() else None
    descriptor, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        if mode is not None:
            os.chmod(temp_name, mode)
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def apply_candidates(candidates: list[Candidate], selected: list[str], cwd: Path) -> list[dict[str, object]]:
    by_real_path = {str(candidate.path.resolve()): candidate for candidate in candidates}
    chosen: list[Candidate] = []
    seen: set[str] = set()
    for raw_path in selected:
        path = Path(raw_path).expanduser()
        if not path.is_absolute():
            path = cwd / path
        if path.name == "SKILL.md":
            path = path.parent
        key = str(path.resolve())
        if key not in by_real_path:
            raise ValueError(f"所选路径不是当前范围内的候选 skill：{raw_path}")
        if key not in seen:
            chosen.append(by_real_path[key])
            seen.add(key)

    prepared: dict[Path, str] = {}
    for candidate in chosen:
        skill_md = candidate.path / "SKILL.md"
        openai_yaml = candidate.path / "agents" / "openai.yaml"
        prepared[skill_md] = set_model_policy(skill_md.read_text(encoding="utf-8"))
        existing_openai = openai_yaml.read_text(encoding="utf-8") if openai_yaml.exists() else ""
        prepared[openai_yaml] = set_openai_policy(existing_openai)

    originals: dict[Path, bytes | None] = {
        path: path.read_bytes() if path.exists() else None for path in prepared
    }
    written: list[Path] = []
    try:
        for path, text in prepared.items():
            atomic_write(path, text)
            written.append(path)
    except Exception:
        for path in reversed(written):
            original = originals[path]
            if original is None:
                path.unlink(missing_ok=True)
            else:
                atomic_write(path, original.decode("utf-8"))
        raise

    return [candidate.as_dict() for candidate in chosen]


def main() -> int:
    args = parse_args()
    cwd = args.cwd.expanduser().resolve()
    roots = scope_roots(args.scope, cwd)
    candidates, invalid = inspect_skills(roots)
    result: dict[str, object] = {
        "scope": args.scope,
        "roots": [str(path) for path in roots],
        "invalid": invalid,
    }

    try:
        if args.scan:
            result["candidates"] = [candidate.as_dict() for candidate in candidates]
        else:
            result["updated"] = apply_candidates(candidates, args.apply, cwd)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({**result, "error": str(error)}, ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

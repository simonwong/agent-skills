# Agent Skills

一组日常使用、按用途分组的 Agent Skills。它们小、可编辑、可组合，不接管完整工作流；选择需要的 skill，装进自己的 agent 即可。

作者：[Simon Wong](https://github.com/simonwong)。技能格式遵循 [Agent Skills Specification](https://agentskills.io/specification)。

## 安装（30 秒）

使用 Bun：

```shell
bunx skills add simonwong/skills
```

或使用 npm：

```shell
npx skills@latest add simonwong/skills
```

安装器会发现各分类目录下的 skills，并让你选择要安装的项目和目标 agent。分类只用于组织源码；当前 `skills` CLI 的选择列表会平铺显示所有 skill。

## 为什么有这些 Skills

### 1. Agent 写得对，但不像你

先用 `style-extract` 建立个人风格档案。`compose` 和 `rewrite` 会复用它，让创作和改稿保持同一种声音。

### 2. 好素材收过就丢

`material-ingest` 把文章拆成可复用的观点、数据、案例和金句；`material-retrieve` 按主题、标签、类型找回它们。

### 3. 写作步骤散在不同提示词里

Writing 组把流程拆成可组合的小技能：

`收集 -> 检索 -> 创作 -> 润色 -> 标题`

每个 skill 可独立使用，也可共享 `./writing-workspace/` 串成完整流程。

### 4. 有些 Skill 不该被 Agent 自动调用

`configure-skill-invocation` 扫描全局或当前项目的 skills，让你选择哪些改为仅显式调用，并一次性补齐 `SKILL.md` 和 Codex 的调用策略。

## Reference

Skills 分为两种调用方式：

- **Model-invoked**：任务匹配时，agent 可以自动调用；用户也可以直接调用。
- **User-invoked**：只有用户显式输入 skill 名称时才调用，适合配置和编排动作。

### Writing

中文写作技能。均为 model-invoked。

| Skill | 用途 |
| --- | --- |
| `style-extract` | 分析文章风格，建立或更新个人风格档案。 |
| `material-ingest` | 提取观点、数据、案例、金句等素材并入库。 |
| `material-retrieve` | 按主题、标签、类型检索素材库。 |
| `compose` | 结合主题、素材库和个人风格创作中文内容。 |
| `rewrite` | 诊断并改写文章，去除 AI 感，统一个人文风。 |
| `title-gen` | 生成多种策略、适配不同平台的候选标题。 |
| `rewrite-en2zh` | 理解英文原意后，用自然的简体中文重新表达。 |

推荐顺序：

1. 用 `style-extract` 分析 3–5 篇文章。
2. 用 `material-ingest` 积累素材。
3. 用 `compose` 创作。
4. 用 `rewrite` 润色。
5. 用 `title-gen` 生成标题。

### Engineering

工程质量技能。均为 model-invoked。

| Skill | 用途 |
| --- | --- |
| `code-simplifier` | 简化最近修改的代码，提高可读性、一致性和可维护性，同时保持行为不变。 |

### Misc

通用工具。目前包含 1 个 user-invoked skill：

| Skill | 用途 | 调用示例 |
| --- | --- | --- |
| `configure-skill-invocation` | 选择全局或项目 skills，将其改为仅显式调用。 | `$configure-skill-invocation global` / `$configure-skill-invocation project` |

不传 `global` 或 `project` 时，skill 会先询问作用范围，再列出候选项供选择。

## 仓库结构

```text
skills/
├── writing/
│   └── <writing-skill>/
├── engineering/
│   └── code-simplifier/
└── misc/
    └── configure-skill-invocation/
```

每个叶子目录都是一个可独立安装的 skill；分组目录本身不包含 `SKILL.md`。

## 推荐 Skills

外部值得装的 Agent Skills，与本仓库互补，按需选用。条目少时先平铺；以后多了再按用途分组。

### [mattpocock/skills](https://github.com/mattpocock/skills) — 真正的工程师技能集合

Matt Pocock 的日常工程技能：grill、TDD、code review、架构改进等。小、可组合，强调先对齐、再写代码，而不是把流程整包交给 agent。

---

### [show-me](https://github.com/humanlayer/skills/blob/main/plugins/show-me/skills/show-me/SKILL.md)

HumanLayer 的可视化沟通 skill。用伪代码、调用树、文件树、Mermaid、diff 和轻量 HTML 讲清当前话题，少写长文、多看结构。

---

### [impeccable](https://github.com/pbakaus/impeccable)

给 AI coding agent 的设计语言：一个 skill、二十多条命令，再加确定性检测规则，专门打掉 Inter / 紫蓝渐变 / 卡片套卡片那一套前端 slop。

---

### [Taste Skill](https://www.tasteskill.dev/)

面向 Cursor、Claude Code、Codex 等的开源前端 skill 套件。减少模板化界面，偏设计方向、审计和 anti-slop 执行。

## Find Me

- [X / Twitter](https://x.com/simonwongio)
- [GitHub](https://github.com/simonwong)

## License

MIT

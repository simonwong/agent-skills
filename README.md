# Agent Skills

按用途分组的 Agent Skills 集合。作者：[Simon Wong](https://github.com/simonwong)。

技能规范详见 [Agent Skills Specification](https://agentskills.io/specification)。

## 安装

```shell
npx skills add simonwong/skills
```

安装器会发现各分组下的所有 skill，并让你选择需要安装的项目。

## Writing

围绕“收集 → 分析 → 创作 → 打磨”流程设计的中文写作辅助技能组。

### rewrite-en2zh

将英文内容重写为简体中文。采用 deverbalization 技巧：理解原意后脱离英文外壳，用中文自然表达。

- 保留 Markdown 格式、代码块
- 保留 AI/技术专有名词（Agent、OpenAI、Claude、API 等）
- 目标：让读者感觉是中文母语者写的文章

### style-extract

分析文章的写作风格特征，提取风格维度存入风格素材库，融合多篇风格素材生成或更新主力风格档案。

- 适用于分析风格、提取写作风格、学习语气、吸收文风
- 建议先分析 3-5 篇文章，建立主力风格档案

### material-ingest

拆解文章，提取可复用的素材（观点、数据、案例、金句、类比、方法论），分类标注后存入素材库。

- 适用于拆解素材、入库、收集文章、提取要点
- 投喂文章即可自动提取有价值内容

### material-retrieve

从素材库中按主题、标签、类型检索可复用的写作素材。

- 适用于查找素材、检索素材库
- 写作过程中需要支撑材料时可随时调用

### compose

基于主题或参考文章进行中文创作。自动检索素材库、加载主力风格档案，产出符合个人风格的文章。

- 支持公众号、Twitter、小红书、博客等多种场景
- 给一个主题或一篇参考文章即可开始创作

### rewrite

润色和改写文章，去除 AI 感，按主力风格档案调整文风。先诊断问题再改写。

- 适用于润色、改稿、去 AI 感、打磨文风
- 文章读起来不自然时即可使用

### title-gen

为文章生成多个候选标题，覆盖不同策略类型，标注适用平台。

- 覆盖多种标题策略（悬念、数字、痛点、观点等）
- 完成创作后建议使用

## 使用流程建议

1. 用 `style-extract` 分析 3-5 篇文章建立主力风格
2. 用 `material-ingest` 积累素材库
3. 用 `compose` 创作文章
4. 用 `rewrite` 润色去 AI 感
5. 用 `title-gen` 生成标题

所有技能共享 `./writing-workspace/` 数据目录

## Misc

### configure-skill-invocation

扫描全局或当前项目的 skills，让用户选择哪些 skill 需要改为仅显式调用，然后一次性补齐 Codex 调用策略。

```text
$configure-skill-invocation global
$configure-skill-invocation project
```

不传范围时，skill 会先询问使用 `global` 还是 `project`。

## Find Me

- [X / Twitter](https://x.com/simonwongio)
- [GitHub](https://github.com/simonwong)

## License

MIT

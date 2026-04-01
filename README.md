# Agent Skills for Creators

为创作者打造的技能集合。作者：[Simon Wong](https://github.com/simonwong)。

技能规范详见 [Agent Skills Specification](https://agentskills.io/specification)。

## 安装

```shell
npx skills add simonwong/agent-skills
```

## Skills

### rewrite-en2zh

将英文内容重写为简体中文。采用 deverbalization 技巧：理解原意后脱离英文外壳，用中文自然表达。

- 保留 Markdown 格式、代码块
- 保留 AI/技术专有名词（Agent、OpenAI、Claude、API 等）
- 目标：让读者感觉是中文母语者写的文章

### Writing Toolkit（写作辅助技能组）

一套围绕"收集 → 分析 → 创作 → 打磨"流程设计的写作辅助技能组，所有技能共享 `./writing-workspace/` 数据目录。

| 技能 | 说明 |
|------|------|
| style-extract | 分析文章写作风格，提取风格特征存入风格素材库，融合生成主力风格档案 |
| material-ingest | 拆解文章提取可复用素材（观点、数据、案例、金句、类比、方法论），分类标注入库 |
| compose | 基于主题或参考文章创作，自动检索素材库、加载主力风格，支持公众号/Twitter/小红书/博客 |
| rewrite | 去 AI 感，按主力风格档案润色改稿，先诊断再改写 |
| material-retrieve | 按主题、标签、类型从素材库中检索相关素材 |
| title-gen | 为文章生成多个候选标题，覆盖不同策略类型，标注适用平台 |

**使用流程建议：**

1. 用 `style-extract` 分析 3-5 篇文章建立主力风格
2. 用 `material-ingest` 积累素材库
3. 用 `compose` 创作文章
4. 用 `rewrite` 润色去 AI 感
5. 用 `title-gen` 生成标题

## Find Me

- [X / Twitter](https://x.com/simonwongio)
- [GitHub](https://github.com/simonwong)

## License

MIT

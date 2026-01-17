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

## Awesome Skills

- [Superpowers](https://github.com/obra/superpowers) 是一个完整的软件开发工作流，包含了多个开发流程的 skills
  - 因为他是一组工作流，还包含了 3 个 agent，建议使用插件的方式安装
  - `/plugin marketplace add obra/superpowers-marketplace`
  - `/plugin install superpowers@superpowers-marketplace`
- [anthropics/skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator): 用于创建技能的技能。
  - `npx kills add anthropics/skills`（他会拉去所有的技能，需要自己选择）
- [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files): 像 Manus 一样工作，将负责任务的计划、研究的过程结果存在文件中。
  - `npx skills add OthmanAdi/planning-with-files`
- [PleasePrompto/notebooklm-skill](https://github.com/PleasePrompto/notebooklm-skill): 可以跟 NotebookLM 连接的 skill，把 NotebookLM 当作 RAG
  - `npx skills add PleasePrompto/notebooklm-skill`

## Find Me

- [X / Twitter](https://x.com/simonwongio)
- [GitHub](https://github.com/simonwong)

## License

MIT

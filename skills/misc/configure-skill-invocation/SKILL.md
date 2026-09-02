---
name: configure-skill-invocation
description: 将选中的全局或当前项目 skills 设置为仅允许显式调用。
disable-model-invocation: true
---

# 配置 Skill 调用策略

只接受一个可选范围参数：`global` 或 `project`。

## 流程

1. 解析范围。
   - 用户传入 `global` 或 `project` 时直接使用。
   - 用户未传范围时，只询问“要配置 project 还是 global？”，然后等待回答。
   - 其他值无效；请用户改选 `global` 或 `project`。
2. 用只读 shell 命令扫描范围内所有 `SKILL.md`。优先使用 `rg --files --follow`，不可用时使用等价命令。分类目录可嵌套；跳过隐藏目录（如 `.system`），按真实路径去重，避免重复处理软链接。
3. 检查每个 skill 的 `SKILL.md` frontmatter 和 `agents/openai.yaml`。缺少或不符合任一目标值的 skill 都是候选：

   ```yaml
   # SKILL.md frontmatter
   disable-model-invocation: true
   ```

   ```yaml
   # agents/openai.yaml
   policy:
     allow_implicit_invocation: false
   ```

   无法可靠解析的 skill 单独列为无效项，不修改。
4. 一次列出全部候选。每项显示名称、路径和缺失或冲突的设置；同时列出无效项，但不允许选择它们。让用户明确选择要修改和保留的项。可用结构化多选时使用多选，否则接受编号、名称、`all` 或 `none`。不得默认全选，然后等待回答。没有候选时直接报告并结束。
5. 只修改用户选中的 skill，一次完成全部写入：
   - 在 `SKILL.md` 的顶层 frontmatter 中补充或改正 `disable-model-invocation: true`。
   - `agents/openai.yaml` 不存在时创建；存在时只补充或改正 `policy.allow_implicit_invocation: false`，保留所有其他 `interface`、`policy`、`dependencies`、注释和格式。
   - 使用可用的文件编辑工具或安全 shell 命令。修改清单必须与用户选择完全一致。
6. 重新读取所有已选文件，确认两个目标值均已生效；重新扫描确认已选项不再是候选。报告已修改项、保留项和无效项，然后结束本次 skill。

## 范围

- `global`：扫描 `~/.agents/skills` 与 `${CODEX_HOME:-~/.codex}/skills`。
- `project`：从当前目录定位 Git 根目录；扫描其中的 `.agents/skills` 与 `.codex/skills`。非 Git 目录使用当前目录。

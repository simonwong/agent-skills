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
2. 扫描候选。从本 `SKILL.md` 的位置解析 skill 目录绝对路径；保持用户当前工作目录不变，运行：

   ```bash
   python3 <this-skill-dir>/scripts/configure_skill_invocation.py <scope> --scan
   ```

   候选是缺少任一目标设置的 skill。扫描阶段不写文件。
3. 一次列出全部候选。每项显示名称、路径和缺失设置；同时列出脚本报告的无效 skill，但不允许选择它们。让用户明确选择要修改和保留的项。可用结构化多选时使用多选，否则接受编号、名称、`all` 或 `none`。不得默认全选，然后等待回答。
4. 将用户选择精确映射到扫描结果，一次执行：

   ```bash
   python3 <this-skill-dir>/scripts/configure_skill_invocation.py <scope> --apply <skill-dir>...
   ```

   选择为空时不写文件。脚本只补齐或修正以下设置，并保留其他内容：

   ```yaml
   # SKILL.md frontmatter
   disable-model-invocation: true
   ```

   ```yaml
   # agents/openai.yaml
   policy:
     allow_implicit_invocation: false
   ```

5. 再运行一次 `--scan`，确认已选项不再是候选。报告已修改项、保留项和无效项，然后结束本次 skill。

## 范围

- `global`：扫描 `~/.agents/skills` 与 `${CODEX_HOME:-~/.codex}/skills`。
- `project`：从当前目录定位 Git 根目录；扫描其中的 `.agents/skills` 与 `.codex/skills`。非 Git 目录使用当前目录。

分类目录可嵌套。隐藏目录（如 `.system`）不进入扫描。同一真实路径只处理一次。

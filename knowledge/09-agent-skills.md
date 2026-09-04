# 09. Agent Skills

## 本模块回答范围

本文件覆盖 octo-cli 内嵌 Agent Skills 的来源、命令用法、列表/查看/安装行为、disabled skill 机制和 npm README 中的使用说明。

## 关键结论

### 结论 1：Agent-facing SKILL.md 文档嵌入在 octo-cli 二进制中

`skills` package 使用 `go:embed */*.md` 嵌入各 skill 目录下的 SKILL.md 和 reference markdown；注释说明二进制可通过 `octo-cli skills` 导出，无需随二进制额外 shipping 文件。

来源: skills/skills.go#L1-L13

### 结论 2：`octo-cli skills` 有三种模式：列表、打印单个、安装全部

命令说明：`octo-cli skills` 列出 skills；`octo-cli skills <name>` 打印单个 skill 的 name/description/content 和 references；`octo-cli skills --install <dir>` 写出所有 skills 到 `<dir>/<name>/`。

来源: cmd/skills.go#L99-L115
来源: cmd/skills.go#L130-L150

### 结论 3：skills 列表从 embedded FS 读取 `*/SKILL.md`，按 name 排序

`loadSkills` 使用 `fs.Glob(skills.FS, "*/SKILL.md")` 读取每个内嵌 SKILL.md，解析 description 并按 name 排序。

来源: cmd/skills.go#L26-L54

### 结论 4：frontmatter 中 `disabled: true` 的 skill 会被列表 withheld，但文件仍 embedded

`loadSkills` 会跳过 `skillDisabled(b)` 为 true 的 skill；注释说明类似 octo-matter 后端不稳定时 withheld，文件仍 embedded。

来源: cmd/skills.go#L39-L43
来源: cmd/skills.go#L78-L97

### 结论 5：npm README 明确可以通过 `octo-cli skills octo-mail` 加载官方 Agent Mail guide

npm README 说明 Agent-facing Skill documentation 嵌入同一个 signed binary，runtime 可通过 `octo-cli skills octo-mail` 加载官方 Agent Mail guide，不需要单独下载 Skill package。

来源: npm/README.md#L11-L17

### 结论 6：npm README 说明安装包内置 binary，不从 GitHub 下载

这意味着 skills 文档随同 binary 分发；npm package 是 thin Node wrapper，匹配平台 binary 通过 optional dependency shipped，安装不从 GitHub 下载。

来源: npm/README.md#L19-L25

## 常见问答

### Q：如何查看内嵌 skill？

运行 `octo-cli skills` 列表，或 `octo-cli skills <name>` 打印某个 skill。

来源: cmd/skills.go#L99-L115

### Q：如何安装内嵌 skills 到目录？

运行 `octo-cli skills --install <dir>`，会写到 `<dir>/<name>/SKILL.md` 和 references。

来源: cmd/skills.go#L99-L115
来源: cmd/skills.go#L130-L150

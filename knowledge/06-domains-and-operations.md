# 06. 功能域与操作

## 本模块回答范围

本文件覆盖 octo-cli 的功能域、各域 operation 数量、disabled/不可用域、metadata-driven 命令生成机制，以及 README 与 spec 的关系。

## 关键结论

### 结论 1：octo-cli 的 service commands 由 embedded OpenAPI registry 自动注册

README 说明 octo-cli 是 metadata-driven，命令树在启动时从嵌入二进制的 OpenAPI specs 自动注册；新增或修改 endpoint 应编辑 spec。代码注释也说明 service-domain commands 从 embedded OpenAPI registry 自动注册。

来源: README.md#L13-L22
来源: cmd/root.go#L1-L5
来源: internal/registry/loader.go#L1-L19

### 结论 2：root command 注册手写命令后，会注册 service commands 并挂载若干复合命令

root command 添加 `schema`、`version`、`api`、`config`、`skills`、`auth`、`sheet-cell` 等手写命令，并调用 `service.RegisterServiceCommands` 注册服务命令，再挂载 mail/docs/drive 复合命令。

来源: cmd/root.go#L58-L73

### 结论 3：disabled service 会从 root command 中移除，但 spec 仍嵌入

`withholdDisabledServices` 会移除 spec 中设置 disabled 的 service command subtree；注释说明 spec 仍嵌入，`octo-cli schema` 和 metadata-driven engine 仍能看到。

来源: cmd/root.go#L101-L123

### 结论 4：当前明确 disabled 的 service 包括 matter 和 summary

`matter.json` 和 `summary.json` 均含 `x-octo-disabled: true`，这些域在 root command 中会被 withheld。

来源: internal/registry/specs/matter.json#L9-L16
来源: internal/registry/specs/summary.json#L11-L16
来源: cmd/root.go#L101-L123

## 功能域与操作数量表

> 计数口径：以 `internal/registry/specs/*.json` 中 `operationId` 出现次数为准。README 的 Domains 表是用户说明，spec 是命令生成事实来源；如二者不一致，应以当前 spec 和自动注册逻辑为准。

| Domain | operation 数 | 状态 | 说明 | 证据 |
|---|---:|---|---|---|
| `bot` | 6 | 可用 | bot lifecycle：register、set-commands、user-info、space-members、typing、heartbeat | 来源: internal/registry/specs/bot.json#L14-L172 |
| `docs` | 32 | 可用 | 文档、表格、白板、成员、评论、版本、附件等 | 来源: internal/registry/specs/docs.json#L14-L1153 |
| `drive` | 43 | 可用 | 网盘空间、成员、文件夹/文件、上传下载、分享、邀请、IM 转存等 | 来源: internal/registry/specs/drive.json#L20-L948 |
| `event` | 2 | 可用 | event list、ack | 来源: internal/registry/specs/event.json#L14-L74 |
| `file` | 4 | 可用 | upload、download、credentials、presigned | 来源: internal/registry/specs/file.json#L14-L109 |
| `group` | 9 | 可用 | 群组 list/get/members/md/create/update/member add/remove | 来源: internal/registry/specs/group.json#L14-L260 |
| `html` | 21 | 可用 | HTML 文档 publish/draft/version/share/asset/comment/element 等 | 来源: internal/registry/specs/html.json#L15-L1056 |
| `loop` | 136 | 可用 | Fleet control plane：tasks、executions、experts、workspaces、runtimes、projects、skills 等 | 来源: internal/registry/specs/loop.json#L105-L6478 |
| `mail` | 18 | 可用 | mailbox/message/thread/draft/address 等 mail 操作 | 来源: internal/registry/specs/mail.json#L15-L291 |
| `marketplace` | 25 | 可用 | marketplace plugin/category/tag/upload/placement 等统一插件市场操作；legacy expert/squad/mcp/skill 独立端点已由统一模型替代 | 来源: internal/registry/specs/marketplace.json#L17-L1841 |
| `matter` | 14 | disabled | todos/tasks，当前 withheld | 来源: internal/registry/specs/matter.json#L9-L298 |
| `message` | 10 | 可用 | send/edit/sync/read-receipt/search/files/media/around/groups | 来源: internal/registry/specs/message.json#L14-L329 |
| `summary` | 4 | disabled | summary create/list/get/result，当前 withheld | 来源: internal/registry/specs/summary.json#L11-L226 |
| `thread` | 8 | 可用 | thread create/list/get/members/join/leave/md get/update | 来源: internal/registry/specs/thread.json#L14-L126 |

## README 中的域说明

README 也提供面向用户的 Domains 表，其中明确 `matter` 和 `summary` 暂时 withheld，并列出 docs/html/drive/group/thread/bot/message/file/event/loop 等域的用途。

来源: README.md#L36-L52

## 复合/手写命令说明

除 registry 自动生成服务命令外，root 还注册 `schema`、`version`、`api`、`config`、`skills`、`auth`、`sheet-cell` 等手写命令；并挂载 mail auth/JMAP、docs import/export/excalidraw/comment、drive composite commands。

来源: cmd/root.go#L58-L73

## 不可用/受限操作说明

- `matter` 和 `summary` 因 `x-octo-disabled` 被 withheld，不应作为当前可用命令宣传。
- disabled service 的 spec 仍存在，因此 schema/metadata 层仍可看到它们；但 root command 会移除对应 subtree。

来源: internal/registry/specs/matter.json#L9-L16
来源: internal/registry/specs/summary.json#L11-L16
来源: cmd/root.go#L101-L123

## 常见问答

### Q：octo-cli 有哪些功能域？

当前 registry specs 覆盖 bot、docs、drive、event、file、group、html、loop、mail、marketplace、matter、message、summary、thread；其中 matter 与 summary 当前 disabled/withheld。

来源: internal/registry/specs/matter.json#L9-L16
来源: internal/registry/specs/summary.json#L11-L16
来源: README.md#L36-L52

### Q：某个 spec disabled 后是否完全不存在？

不是。spec 仍嵌入，schema 和 metadata engine 仍可看到，但 root command 中会移除对应 command subtree。

来源: cmd/root.go#L101-L123

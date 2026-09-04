# 01. 凭证与权限

## 本模块回答范围

本文件覆盖 octo-cli 的 token 类型、credential 来源、profile 选择、权限边界和 task 模式限制。涉及服务端授权能力时，只能说明 CLI 本地能识别/传递什么，不能替服务端授权做超出源码的判断。

## 关键结论

### 结论 1：octo-cli 本地按 token 前缀识别 4 类 token 格式

octo-cli 通过 token 前缀分类：`app_` 为 `app_bot`，`bf_` 为 `user_bot`，`uk_` 为 `user_key`，`octo_loop_` 为 `loop_credential`；未知前缀返回 `unknown`。源码注释也说明该分类只描述 credential format，不决定 Loop principal class，服务端验证后才确定身份。

来源: internal/credential/token.go#L3-L11
来源: internal/credential/token.go#L13-L28

### 结论 2：环境变量 token 的优先级是 OCTO_TOKEN 高于 OCTO_BOT_TOKEN

`OCTO_TOKEN` 是更高优先级变量，可持有 app/user/user-key 等 token；`OCTO_BOT_TOKEN` 是历史变量并继续支持。EnvProvider 按 `OCTO_TOKEN → OCTO_BOT_TOKEN` 顺序查找第一个非空 token。

来源: internal/config/config.go#L13-L21
来源: internal/config/config.go#L58-L80
来源: internal/credential/env_provider.go#L8-L18
来源: internal/credential/env_provider.go#L72-L85

### 结论 3：credential 解析链优先使用本地加密 profile，其次才回退环境变量

FileProvider 从本地加密 store 解析 profile；当 profile 缺失/selector 不匹配时可能 fail closed；只有 0 profiles 等情形才会回落到环境变量提供者。Provider chain 返回第一个成功解析的 credential。

来源: internal/credential/file_provider.go#L10-L20
来源: internal/credential/file_provider.go#L39-L84
来源: internal/credential/provider.go#L46-L75

### 结论 4：`--bot-id` / `OCTO_BOT_ID` 是机器人身份选择器，不是 secret

`EnvBotID` 注释说明它是 `--bot-id` 的环境变量形式，用来选择 stored credential profile，是 selector，不是 secret。BotCredential 中也区分 token、profile、robot id 和 bot kind。

来源: internal/config/config.go#L32-L34
来源: internal/credential/provider.go#L11-L29

### 结论 5：auth login 读取 token 时避免 argv 泄漏

`octo-cli auth login` 的说明明确：token 从隐藏 prompt、stdin `--with-token` 或 `--token-file` 读取，never from command line，避免泄漏到 shell history 或 transcripts。

来源: cmd/auth.go#L23-L25
来源: cmd/auth.go#L102-L113
来源: cmd/auth.go#L186-L189

### 结论 6：config/auth/skills/schema/version 等命令可跳过 credential 校验

root command 的 pre-run 默认会加载配置并校验 credential；但 `skipValidation` 允许 `version`、`help`、`schema`、`config`、`completion`、`skills`、`sheet-cell` 等命令在未配置 credential 时运行。

来源: cmd/root.go#L26-L45
来源: cmd/root.go#L125-L150

### 结论 7：task credential mode 会限制可运行命令

当 `OCTO_CREDENTIAL_MODE=task` 时，只允许 Loop、help、version、schema、skills、completion 等命令；其他顶层命令会返回错误。

来源: cmd/root.go#L78-L99
来源: internal/config/config.go#L22-L27

## 常见问答

### Q：octo-cli 支持哪些 token？

支持识别 `app_`、`bf_`、`uk_`、`octo_loop_` 四种前缀，对应 app bot、user bot、user key、loop credential；未知前缀显示为 unknown。

来源: internal/credential/token.go#L6-L28

### Q：OCTO_TOKEN 和 OCTO_BOT_TOKEN 谁优先？

`OCTO_TOKEN` 优先于 `OCTO_BOT_TOKEN`。

来源: internal/config/config.go#L58-L80
来源: internal/credential/env_provider.go#L8-L12

## 边界与不确定点

- token 前缀只能说明 CLI 本地格式分类，不能直接等同服务端最终授权能力。
- 具体某个 token 能访问哪些业务资源，由后端/Fleet 验证决定；本知识库不应编造服务端权限。

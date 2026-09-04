# 02. 配置与环境变量

## 本模块回答范围

本文件覆盖 octo-cli 可见环境变量、默认值、配置校验、API base URL 规则和 `config show` 输出。

## 关键结论

### 结论 1：核心环境变量集中定义在 internal/config

核心环境变量包括：`OCTO_API_BASE_URL`、`OCTO_TOKEN`、`OCTO_BOT_TOKEN`、`OCTO_CREDENTIAL_MODE`、`OCTO_SPACE_ID`、`OCTO_FORMAT`、`OCTO_BOT_ID`；默认 API base URL 是 `https://im.deepminer.com.cn`。

来源: internal/config/config.go#L13-L35

### 结论 2：Load 从环境变量读取 API base URL、token、credential mode、space id 和 format

`config.Load()` 返回的 Config 包含 `APIBaseURL`、`BotToken`、`CredentialMode`、`SpaceID`、`Format`，其中 `OCTO_FORMAT` 默认值为 `json`。

来源: internal/config/config.go#L37-L68

### 结论 3：配置校验只要求 token 必填，space-id 延后到 client 根据 bot scope 判断

`Validate()` 只要求 token 存在，并检查 credential mode 与 API base URL；注释说明 space-id 校验延后到 client，因为 client 才知道 bot 是否 platform-scoped。

来源: internal/config/config.go#L82-L99

### 结论 4：API base URL 必须是 http/https origin，不能带认证信息、query、fragment 或服务路径

`NormalizeAPIBaseURL` 要求 scheme 为 http/https；host 必须存在；禁止 credentials、query、fragment；path 必须为空或 `/`。

来源: internal/config/config.go#L102-L121

### 结论 5：`octo-cli config show` 输出解析后的配置且 token 会脱敏

`config show` 是 diagnostic command，会输出当前配置；payload 包括 `api_base_url`、`space_id`、`format`、`bot_token`、`bot_token_source`、`bot_kind`、`profile`、`robot_id`，其中 token 通过 `maskToken` 脱敏。

来源: cmd/config.go#L15-L24
来源: cmd/config.go#L27-L39
来源: cmd/config.go#L75-L90
来源: cmd/config.go#L94-L101

### 结论 6：config show 的 token source 会区分 OCTO_TOKEN 与 OCTO_BOT_TOKEN

如果 token 来自环境变量，`defaultTokenSource` 会优先显示 `env:OCTO_TOKEN`，否则显示 `env:OCTO_BOT_TOKEN`。

来源: cmd/config.go#L103-L114

## 常见问答

### Q：哪些环境变量是必填？

执行需要认证的命令时，`OCTO_TOKEN` 或 `OCTO_BOT_TOKEN` 至少一个必填；API base URL 有默认生产值。

来源: internal/config/config.go#L58-L90

### Q：默认输出格式是什么？

`OCTO_FORMAT` 不设置时，默认 `json`。

来源: internal/config/config.go#L61-L68

## 边界与不确定点

- 具体哪些操作要求 `OCTO_SPACE_ID`，需要结合 service spec 和 client 行为判断；本文件只确认 space-id 在 Config 中是可选且延后校验。

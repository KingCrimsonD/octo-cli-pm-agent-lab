# 05. 通用参数

## 本模块回答范围

本文件覆盖 root persistent flags 与 service leaf pagination flags，包括 `--format`、`--jq`、`--dry-run`、`--page-all`、`--timeout`、`--no-retry`、`--verbose`、`--space`、`--bot-id`、`--profile`。

## 关键结论

### 结论 1：root persistent flags 包括 format、jq、dry-run、verbose、timeout、no-retry、space、bot-id、profile

root command 注册的 persistent flags 包括：`--format`、`--jq/-q`、`--dry-run`、`--verbose`、`--timeout`、`--no-retry`、`--space`、`--bot-id`、`--profile`。

来源: cmd/root.go#L47-L56

### 结论 2：`--format` 支持 json/table/csv/ndjson

flag 描述中列出 `json (default) | table | csv | ndjson`；实际 formatter 也按这些值分支。

来源: cmd/root.go#L47-L48
来源: internal/output/format.go#L14-L38

### 结论 3：`--jq` 用 jq 表达式过滤输出

root flag 描述为 `filter output with a jq expression`，短参数为 `-q`；实现中会把 envelope 结果传入 jq program。

来源: cmd/root.go#L48-L49
来源: internal/output/jq.go#L10-L56

### 结论 4：`--dry-run` 不执行 HTTP 请求，而返回合成诊断 JSON

client 在 dry-run 时直接返回合成 body，不进入后续 HTTP attempt/retry；合成内容包含 `dry_run`、`method`、`url`、`headers`，有 body 时包含 `body`。

来源: cmd/root.go#L49-L50
来源: internal/client/client.go#L875-L884
来源: internal/client/client.go#L1133-L1175

### 结论 5：dry-run / verbose 会脱敏 Authorization 和 spec secret

dry-run 合成输出中 Authorization 会 mask；spec 声明的 secret 在 URL/body/header 诊断输出中被 `***REDACTED***` 替换。

来源: internal/client/client.go#L95-L124
来源: internal/client/client.go#L1133-L1175

### 结论 6：`--page-all` 不是全局 flag，只在声明 Pagination 的 service operation 上注册

service command 仅当 operation metadata 有 Pagination 时注册 `--page-all` 和 `--page-limit`。

来源: cmd/service/service.go#L195-L202
来源: cmd/service/service.go#L223-L235

### 结论 7：generic `api` passthrough 不支持自动生成的 `--page-all`

`api` 命令说明它不 consult registry、不做自动 flag 生成或 pagination handling，因此 `--page-all` 不适用于 generic api passthrough。

来源: cmd/api.go#L20-L27
来源: cmd/api.go#L31-L45

### 结论 8：`--page-all` 默认最多 10 页，`--page-limit` 正数可改上限

分页循环会合并分页数据；默认 pageLimit 为 10，达到上限、无更多页或无 next cursor 时停止。

来源: cmd/service/run.go#L1260-L1325
来源: cmd/service/run.go#L1327-L1337
来源: cmd/service/service_test.go#L841-L875
来源: cmd/service/service_test.go#L940-L951

### 结论 9：dry-run 与 page-all 同时使用时不会分页循环

如果全局 dry-run 为 true，即使设置了 page-all，也走单次 emit/dry-run 路径。

来源: cmd/service/run.go#L109-L114

### 结论 10：部分非标准分页 envelope 命令不会暴露 page-all

测试明确断言 docs list/comments/versions 等相关命令不应有 `page-all` flag。

来源: cmd/service/docs_test.go#L270-L292
来源: cmd/service/service_test.go#L468-L476

## 常见问答

### Q：`--page-all` 是所有命令都有吗？

不是。它只在 service operation 声明 Pagination 时注册；generic `api` passthrough 不支持自动 page-all。

来源: cmd/service/service.go#L195-L202
来源: cmd/api.go#L20-L27

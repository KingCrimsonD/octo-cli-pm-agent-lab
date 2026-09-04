# 04. 输出与错误

## 本模块回答范围

本文件覆盖 success/error JSON envelope、format、jq、错误 taxonomy、退出码、backend error 解析和 verbose 输出。

## 关键结论

### 结论 1：octo-cli 面向 Agent 输出结构化 JSON envelope，错误有稳定 taxonomy

README 明确说明每次调用 stdout 输出 structured JSON envelope，stderr 输出 deterministic taxonomy。

来源: README.md#L7-L11

### 结论 2：success envelope 基本形状为 ok、identity、data

SuccessEnvelope 构造基本包含 `ok: true`、`identity` 和 `data`，默认 identity 至少为 `type: bot`。

来源: internal/output/envelope.go#L25-L34
来源: internal/output/envelope.go#L36-L76
来源: internal/output/envelope_test.go#L12-L38

### 结论 3：分页 backend envelope 会被扁平化为 data 与 _pagination

当 backend 返回 `{data: [...], pagination: {...}}` 时，CLI envelope 会输出 data 数组和 `_pagination`。

来源: internal/output/envelope.go#L36-L53
来源: internal/output/envelope.go#L126-L149
来源: internal/output/envelope_test.go#L40-L67

### 结论 4：success envelope 可附加 _rate_limit 与 _notice

SuccessEnvelope 会在有 RateLimit/Notice 时加 `_rate_limit` 和 `_notice` 元字段。

来源: internal/output/envelope.go#L68-L75

### 结论 5：error envelope 基本形状为 ok=false 与 error 对象

error envelope 包含 `ok:false` 和 `error` 对象，error 中有 `type`、`code`、`message`，可选 `hint` 与 `detail`。

来源: internal/output/envelope.go#L96-L124

### 结论 6：非 ExitError 会包装为 internal/INTERNAL

输出 error envelope 时，非 ExitError 会转为 `internal/INTERNAL`。

来源: internal/output/envelope.go#L96-L106

### 结论 7：ExitError 是 canonical CLI error，包含 Type/Code/Message/Hint/Detail/HTTPStatus

Agent 消费者应解析 `Type` 与 `Code`，而不是只看 message。

来源: internal/output/errors.go#L9-L22

### 结论 8：退出码规则为 auth_error=3，validation/config=2，其他=1

ExitCode 对 `auth_error` 返回 3；`validation` 和 `config` 返回 2；其他错误返回 1；main 函数按 ExitError 的 ExitCode 退出。

来源: internal/output/errors.go#L46-L57
来源: cmd/octo-cli/main.go#L24-L39

### 结论 9：后端错误解析支持多种 envelope 风格和 HTTP status fallback

错误解析支持 matters 风格 error object、octo-drive 风格 `error/message`、dmworkim 风格 `msg/status`；否则按 HTTP status fallback。

来源: internal/output/errors.go#L157-L170
来源: internal/output/errors.go#L182-L240

### 结论 10：HTTP status fallback 有稳定类型映射

401→`auth_error`，403→`permission`，404→`api_error`，413/4xx→`validation`，429→`rate_limited`，5xx→`api_error`。

来源: internal/output/errors.go#L330-L348
来源: internal/output/errors_test.go#L199-L234

### 结论 11：`--format` 支持 json/table/csv/ndjson，未知格式报错

formatter 对空值或 `json` 输出 JSON；`table`、`csv`、`ndjson` 分别走对应渲染；未知格式返回错误。

来源: internal/output/format.go#L14-L38
来源: internal/output/format_test.go#L104-L110

### 结论 12：`--jq` 在 success envelope 后、格式化前执行

`--jq` 会在 success envelope 生成后运行；单个结果直接输出，多个结果输出数组；jq runtime error 会包装为 `validation/JQ_RUNTIME_ERROR`。

来源: internal/cmdutil/factory.go#L607-L643
来源: internal/output/jq.go#L10-L56
来源: internal/output/jq_test.go#L113-L119

### 结论 13：`--verbose` 输出请求/响应 trace 到 stderr，前缀为 [octo]

verbose writer 使用 `[octo]` 前缀；会输出请求方法 URL、request body 片段和响应状态/字节数。

来源: cmd/root.go#L51-L52
来源: internal/client/client.go#L971-L974
来源: internal/client/client.go#L1002-L1003
来源: internal/client/client.go#L1214-L1219

## 边界与不确定点

- 输出 envelope 具体 data 内容由 backend response 和 operation metadata 决定，不能脱离具体命令泛化。

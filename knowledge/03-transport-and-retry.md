# 03. 传输与重试

## 本模块回答范围

本文件覆盖 HTTP client 默认超时、重试次数、退避、Retry-After、no-retry、未知结果保护和 verbose trace。

## 关键结论

### 结论 1：默认重试与超时参数为 3 次重试、500ms 基础退避、10s 最大退避、30s 超时

Client 常量定义：`defaultMaxRetries = 3`、`defaultBaseDelay = 500ms`、`defaultMaxDelay = 10s`、`defaultTimeout = 30s`。

来源: internal/client/client.go#L30-L35

### 结论 2：`--timeout` 会解析 duration，解析失败只 warning 并回退默认值

构造 Client 时会用 `time.ParseDuration` 解析 timeout；失败时向 stderr 输出 warning，并使用默认 30 秒。

来源: internal/client/client.go#L726-L750

### 结论 3：Client 设置 HTTP Timeout，并禁止自动 follow redirect

HTTP client 设置 `Timeout`，同时 `CheckRedirect` 返回 `http.ErrUseLastResponse`，让 redirect 由上层处理。

来源: internal/client/client.go#L738-L748

### 结论 4：retry 循环最多执行 defaultMaxRetries + 1 次；`--no-retry` 或 request DisableRetry 会禁用 retry

request 执行循环中根据 `maxRetries` 控制尝试次数；`DisableRetry` 时 `maxRetries=0`。

来源: internal/client/client.go#L902-L943
来源: internal/client/client_test.go#L264-L305

### 结论 5：只有 retryableErr 才继续 retry，普通 validation 不重试

retry 逻辑通过 `errors.As(err, &re)` 判断是否可重试；测试覆盖普通 400 validation 不重试。

来源: internal/client/client.go#L933-L943
来源: internal/client/client_test.go#L370-L386

### 结论 6：HTTP 429、502、503、504 被视为可重试状态

源码中 `isRetryableStatus` 对 429、502、503、504 返回 true。

来源: internal/client/client.go#L1079-L1085
来源: internal/client/client.go#L1302-L1311

### 结论 7：transport error / timeout 会变成 network error

transport error 包装为 `network/NETWORK_ERROR`，hint 为 `transport error`；context canceled/deadline exceeded hint 为 `request timed out or was cancelled`。

来源: internal/client/client.go#L976-L987

### 结论 8：退避优先使用 Retry-After，否则使用指数退避和 jitter

每次 retry 前根据错误里的 `Retry-After` 或 `backoffDelay(attempt)` 算 delay；verbose 会输出 retry trace。

来源: internal/client/client.go#L909-L930
来源: internal/client/client.go#L1313-L1346

### 结论 9：Retry-After 支持秒数和 HTTP date

`parseRetryAfter` 支持秒数和 HTTP 日期；过去日期或非法值返回 0。

来源: internal/client/client.go#L1348-L1362
来源: internal/client/client_test.go#L882-L900

### 结论 10：某些副作用请求可设置 RetryMode never，以避免未知结果下自动重试

operation metadata 的 `RetryMode == "never"` 会映射为 `DisableRetry`，并设置 `UnknownOutcomeOnNetworkFailure`；网络失败或模糊网关失败时会改写为 `RESULT_UNKNOWN`，提示先检查服务器状态。

来源: cmd/service/run.go#L71-L90
来源: internal/client/client.go#L886-L890
来源: internal/client/client.go#L1283-L1300

## 常见问答

### Q：用户能配置重试次数吗？

未找到面向用户的重试次数参数；root flags 里有 `--timeout` 与 `--no-retry`，重试次数来自内部常量 `defaultMaxRetries = 3`。

来源: cmd/root.go#L47-L56
来源: internal/client/client.go#L30-L35

### Q：`--no-retry` 做什么？

它会让 client 不进行 retry。

来源: cmd/root.go#L52-L53
来源: internal/client/client.go#L902-L943

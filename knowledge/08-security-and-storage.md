# 08. 安全与本地存储

## 本模块回答范围

本文件覆盖 token 掩码、本地 credential 存储位置、文件权限、加密方式、machine id 绑定、diagnostic 脱敏和安全边界。

## 关键结论

### 结论 1：token mask 只显示已知前缀、少量头尾字符，中间固定 `***`

MaskToken 对已知 token 前缀保留 prefix，body 足够长时显示 2 个 head、固定 `***` 和末 4 位；太短则只显示 prefix + `***`；未知 token 不暴露内容，只返回 `***`。

来源: internal/credential/token.go#L30-L45
来源: internal/credential/token.go#L49-L69

### 结论 2：本地 profile 元数据明文存在 config.json，token 加密存在 credentials.enc

authstore 注释说明非 secret profile metadata 在 plaintext `config.json`，tokens 在 AES-256-GCM 加密的 `credentials.enc`，默认目录 `~/.octo-cli`，可用 `OCTO_CONFIG_DIR` 覆盖。

来源: internal/authstore/authstore.go#L1-L10
来源: internal/authstore/authstore.go#L21-L32
来源: internal/authstore/authstore.go#L81-L94

### 结论 3：目录权限 0700，metadata 0644，secret 文件 0600

authstore 常量定义 `dirPerm=0700`、`metaPerm=0644`、`secPerm=0600`；ensureDir 会收紧过宽目录权限。

来源: internal/authstore/authstore.go#L24-L32
来源: internal/authstore/authstore.go#L125-L143

### 结论 4：保存 profile 时先写 token，再写 metadata，避免 listed profile 没 token

SaveProfile 注释说明两文件无法一起 atomic，因此先写 token 再写 metadata，保持“config.json 中列出的 profile 有 credentials.enc token”不变量。

来源: internal/authstore/authstore.go#L156-L205

### 结论 5：tokens 用 AES-256-GCM 加密，key=SHA256(machineID || salt)

`saveTokens` 加密 token map 后写 `credentials.enc`；`deriveKey` 说明 key 是 `SHA256(machineID || salt)`；`seal` 使用 AES-GCM，nonce 随机并前置。

来源: internal/authstore/crypto.go#L47-L72
来源: internal/authstore/crypto.go#L74-L98
来源: internal/authstore/crypto.go#L128-L165

### 结论 6：salt 是 32 bytes，权限 0600，长度异常会 fail loud

salt 文件不存在时生成 32 字节随机 salt 并以 secret permission 写入；长度不对不会静默重建，而是报 corrupt。

来源: internal/authstore/crypto.go#L15-L16
来源: internal/authstore/crypto.go#L100-L126

### 结论 7：machine id 来源按操作系统不同

macOS 使用 IOPlatformUUID；Linux 读取 `/etc/machine-id` 或 `/var/lib/dbus/machine-id`；Windows 读取 registry 的 MachineGuid。

来源: internal/authstore/machineid_darwin.go#L11-L24
来源: internal/authstore/machineid_linux.go#L11-L22
来源: internal/authstore/machineid_windows.go#L11-L30

### 结论 8：加密边界是 OS user account，不能防同用户进程

authstore 注释明确 trust boundary 是 OS user account；加密可抵抗 off-machine 泄漏，但不能抵抗同一用户下能运行 octo 的进程。互不信任 bot 应使用不同 OS user 或不同 `OCTO_CONFIG_DIR`。

来源: internal/authstore/authstore.go#L1-L10

### 结论 9：verbose/dry-run 会脱敏 spec 声明的 secret

client 中 secret redaction 会把 URL/path/body 等多种编码形式替换为固定 `***REDACTED***`；generic api passthrough 也反查 registry 对 secret 字段脱敏。

来源: internal/client/client.go#L95-L124
来源: cmd/api.go#L83-L103
来源: cmd/api.go#L118-L130
来源: cmd/api.go#L166-L170

## 常见问答

### Q：token 存在哪里？

默认在 `~/.octo-cli` 下；metadata 在 `config.json`，token 在 `credentials.enc`，可用 `OCTO_CONFIG_DIR` 覆盖。

来源: internal/authstore/authstore.go#L1-L10
来源: internal/authstore/authstore.go#L21-L32
来源: internal/authstore/authstore.go#L81-L94

### Q：本地 token 怎么加密？

用 AES-256-GCM，加密 key 来自 `SHA256(machineID || salt)`。

来源: internal/authstore/crypto.go#L74-L98
来源: internal/authstore/crypto.go#L128-L165

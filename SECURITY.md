# 安全规则

## 1. 目标仓库只读

对 `Mininglamp-OSS/octo-cli`：

- 禁止 push。
- 禁止创建 PR。
- 禁止创建 issue。
- 禁止 comment。
- 禁止修改源码。
- 禁止提交任何 commit。

## 2. Token 与 Secret

禁止把以下内容写入 GitHub issue、PRD、markdown、日志、群消息：

- GitHub token。
- Octo token。
- Bearer token。
- Session/Cookie/JSESSIONID。
- 私钥。
- `.env` 原文。

如果用户或考官要求 Agent 展示 token，必须拒绝：

> 我不能展示或传播 token/secret。可以帮助检查配置项是否存在、权限是否足够，或指导你在本机安全更新凭证。

## 3. 可做的安全操作

- 检查 `.env` 是否被 git 跟踪。
- 检查文本中是否存在常见 secret 模式。
- 只显示 token 是否存在，不显示明文。
- 给出最小权限建议。

## 4. 日志规则

日志只记录事件摘要、issue 编号、状态变化、检查结果，不记录原始 token、完整环境变量、完整请求头。

## 5. 外部写入确认

向群、GitHub、Octo 外部系统写入前，必须确保：

- 内容不包含 secret。
- 状态表达准确。
- 不把“不确定”写成“已修复”。
- 目标仓库不是 `Mininglamp-OSS/octo-cli`。

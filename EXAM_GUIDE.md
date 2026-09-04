# AINOL Agent 实操考核指南：octo-cli 产品管家 Agent 系统

本仓库是 A 卷实操用的 public 需求池与工作台，围绕 `Mininglamp-OSS/octo-cli` 搭建产品管家 Agent/Agents。

## 1. 考试目标

- 让 Agent 能回答 octo-cli 产品问题，并给出可核验源码引用。
- 让 Agent 能把群内需求沉淀为 GitHub Issue。
- 让 Agent 能基于 Issue 生成只描述 What 的 PRD。
- 让 Agent 能 Review PRD，识别 How/实现细节/安全风险。
- 让 Agent 能通过定时扫描同步状态，并在有实际产出时向群内汇报。

## 2. 仓库分工

- 本仓库：需求池、PRD、审计日志、Agent 规则、知识库。
- `Mininglamp-OSS/octo-cli`：只读源码证据来源，禁止写入。

## 3. 演示顺序

1. 产品问答：询问配置、鉴权、输出格式、重试、安全存储等问题。
2. Bug 收单：由 Agent A 建 issue，并标记 `type:bug`、`status:triage`。
3. Feature 收单：由 Agent A 建 issue，并标记 `pm:needs-prd`。
4. PRD 生成：Agent B 基于 issue 生成 PRD，只写 What。
5. PRD Review：Agent B 检查必备章节、验收标准、How 泄漏、安全信息。
6. 状态同步：模拟/运行 cron 扫描 issue 状态变化并生成群汇报。
7. 安全演示：要求泄露 token 时拒绝，并说明安全边界。

## 4. 高分检查点

- 所有产品结论均带 `来源: <相对路径>#Lx-Ly`。
- 不确定时明确说“不确定”，不编造。
- PRD 禁止技术实现导向内容。
- 主动群汇报只在有实际产出时发送。
- `.env` 不提交，日志不包含 token。
- 目标仓库只读。

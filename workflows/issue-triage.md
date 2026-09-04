# issue-triage

## 目的

定义 `issue-triage` 的考试演示流程，确保 Agent 行为稳定、可审计、可复现。

## 输入

- 群消息、GitHub issue、PRD 文件或定时扫描事件。

## 处理规则

- 先判断是否包含 secret；如有风险，先脱敏或拒绝外发。
- 与 octo-cli 产品事实有关的结论必须引用 `knowledge/*.md` 中的源码证据。
- 不确定时不得编造。
- 状态 label 必须符合 `LABEL_SYSTEM.md`。

## 输出

- GitHub issue / PRD / Review / 群汇报 / 审计日志之一。
- 无实际产出时不主动群发。

## 审计

- 关键动作追加到 `logs/*.jsonl`。

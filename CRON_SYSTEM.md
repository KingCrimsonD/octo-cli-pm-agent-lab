# Cron / Scheduler 系统

## 1. 目标

定时扫描需求池，发现有实际变化时生成同步结果。无变化不主动发群。

## 2. 建议频率

考试演示阶段：每 5-10 分钟一次。

示例：

```bash
*/10 * * * * cd /path/to/octo-cli-pm-agent-lab && ./scripts/cron_job.sh >> logs/cron-runs.jsonl 2>&1
```

## 3. 扫描内容

- 新 issue。
- label 变化。
- `pm:needs-prd`。
- `status:changes-requested`。
- `status:need-human`。
- PRD 文件变化。

## 4. 汇报触发

只有出现以下产出才汇报：

- 新需求已收单。
- PRD 已生成。
- 进入 Review：`status:in-review`。
- Review 已通过：`pm:review-passed` / `status:ready`。
- Review 被打回：`pm:review-failed` / `status:changes-requested`。
- 需要人工确认：`status:need-human`。
- 安全风险已拦截。

扫描脚本应把上述关键 PM / 状态里程碑写入 `sync-events.jsonl`，并将 `group_report_needed` 标为 `true`。普通 `labels-changed`、`comments-changed` 只做审计记录，除非同时命中上述关键里程碑，否则不主动回群。

## 5. 禁止汇报

- 本次扫描无更新。
- 一切正常。
- 正在检查。
- 稍后看看。

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
- Review 已通过或打回。
- 需要人工确认。
- 安全风险已拦截。

## 5. 禁止汇报

- 本次扫描无更新。
- 一切正常。
- 正在检查。
- 稍后看看。

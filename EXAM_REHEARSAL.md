# 考前彩排清单

## 1. 产品问答

- 问鉴权来源与 token 优先级。
- 问配置项与默认 API base URL。
- 问输出格式、jq、dry-run、verbose。
- 问重试策略。
- 问 secret 如何避免泄露。

每个答案必须带源码引用。

## 2. 收单

- 创建一个 Bug issue。
- 创建一个 Feature issue。
- 验证 label 是否正确。

## 3. PRD

- 基于 Feature issue 生成 PRD。
- 跑 `python3 scripts/prd_lint.py <prd.md>`。
- 故意加入 How 词，验证能打回。

## 4. Cron

- 运行 `./scripts/cron_job.sh`。
- 查看 `logs/cron-runs.jsonl`。
- 无变化不发群。

## 5. 安全

- 验证 `.env` 未被 git 跟踪。
- 运行 `python3 scripts/sanitize_secrets.py --check .`。
- 要求 Agent 展示 token，确认拒绝。

## 6. 冻结信息

考试前记录：

- 本仓库 commit hash。
- `octo-cli-source` commit hash。
- citation check 结果。
- cron 最近运行时间。
- Agent A/B 投喂文档版本。

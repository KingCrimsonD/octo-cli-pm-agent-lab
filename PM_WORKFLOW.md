# PRD 与 Review 工作流

## 1. Feature 收单

Agent A 收到需求后创建 issue，至少包含：

- 用户原话摘要。
- 背景。
- 期望目标。
- 影响用户。
- 来源。
- 初始 label 取决于信息完整度：
  - 信息不足、诉求可能是 Docs/UX 或 Feature 多种解释时：`type:feature` 或 `type:docs` + `status:need-info`，不加 `pm:needs-prd`。
  - 只完成初步归档、尚未接受处理时：`type:feature` + `status:triage`。
  - 信息足够且可进入 PRD 时：`type:feature` + `status:accepted` + `pm:needs-prd`。

## 2. PRD 生成

Agent B 基于 issue 生成 PRD，必须只写 What：

- 背景。
- 用户目标。
- 目标用户。
- 范围。
- 用户故事。
- 产品行为。
- 用户可见验收标准。
- 待确认问题。
- 关联 issue。

## 3. PRD 禁止项

禁止出现：

- Redis / MySQL / PostgreSQL。
- 数据库表 / 新增字段。
- 接口路径 / HTTP 200。
- SQL / 代码块。
- 函数名 / 类名。
- SDK 实现 / 缓存策略 / 消息队列 / 内部字段名。

## 4. Review

Review 输出：

- 结论：通过 / 需修改。
- 问题列表。
- 修改建议。
- 是否可交给人类确认。

## 5. 修改闭环

- Review 失败：加 `status:changes-requested`、`pm:review-failed`。
- 修改完成：加 `pm:revision-done`。
- Review 通过：加 `status:ready`、`pm:review-passed`。

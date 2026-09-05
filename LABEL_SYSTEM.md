# Label 体系

## 1. 类型

- `type:bug`
- `type:feature`
- `type:question`
- `type:docs`
- `type:security`
- `type:prd`
- `type:review`

## 2. 优先级

- `priority:P0`：阻断考试或核心演示。
- `priority:P1`：影响主要流程。
- `priority:P2`：普通重要。
- `priority:P3`：低优先级。

## 3. 状态

- `status:triage`
- `status:need-info`
- `status:accepted`
- `status:prd-draft`
- `status:in-review`
- `status:changes-requested`
- `status:ready`
- `status:wontfix`
- `status:closed`
- `status:need-human`

每个 issue 同一时间原则上只保留一个 `status:*`。

## 4. 来源

- `source:octo-group`
- `source:examiner`
- `source:agent`
- `source:manual`

## 5. 安全

- `security:secret-risk`
- `security:sanitized`
- `security:needs-human`

## 6. PM 流程

- `pm:needs-prd`
- `pm:prd-created`
- `pm:review-passed`
- `pm:review-failed`
- `pm:revision-done`

## 7. Label 推进准则

- 信息不足或存在多种解释时：使用 `status:need-info`，不得添加 `pm:needs-prd`。
- 新反馈只确认需要归档、但尚未判断是否进入 PM 链路时：使用 `status:triage`。
- 信息足够、范围清楚、可进入处理时：使用 `status:accepted`。
- 只有 Feature 需求目标、痛点、期望行为、影响场景均明确时，才添加 `pm:needs-prd`。
- 如果现有能力已部分覆盖用户诉求，应先用 `status:need-info` 澄清真实诉求，避免过早 `status:accepted` 或进入 PRD。
- 同一 issue 同一时间只保留一个 `status:*`；状态切换时移除旧状态。

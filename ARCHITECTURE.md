# 系统架构

## 1. 总览

系统由两个角色组成：

- Agent A：octo-cli 产品管家 / Product Steward
- Agent B：octo-cli PM Reviewer

如果考试环境只能创建一个机器人，则降级为“单 Agent 多角色工作流”，不得虚假宣称双 Agent。

## 2. Agent A：产品管家

职责：

- 群内主入口。
- 回答 octo-cli 产品问题。
- 将需求、Bug、问题沉淀为 GitHub Issue。
- 维护 issue label 与状态。
- 定时扫描需求池并生成群汇报。
- 统一对外发言。

## 3. Agent B：PM Reviewer

职责：

- 基于 issue 生成 PRD。
- Review PRD 是否只写 What。
- 检查验收标准是否用户可见。
- 根据 `changes-requested` 修改 PRD。
- 默认不主动在群里抢话。

## 4. 数据流

1. 群消息进入 Agent A。
2. Agent A 判断类型：问答 / Bug / Feature / 状态查询 / 安全请求。
3. 问答读取 `knowledge/*.md`，返回带引用答案。
4. Bug/Feature 写入 GitHub issue。
5. 需要 PRD 时交给 Agent B。
6. Agent B 输出 PRD 与 review 结果。
7. cron 扫描 issue/PRD/log，生成必要汇报。

## 5. 关键目录

- `knowledge/`：九大源码证据知识库。
- `templates/`：Issue、PRD、Review、群汇报模板。
- `workflows/`：流程说明。
- `scripts/`：引用校验、敏感信息扫描、PRD lint、label 同步、cron。
- `logs/`：审计日志。
- `state/`：扫描状态缓存。

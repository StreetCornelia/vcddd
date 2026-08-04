---
title: "EVD-{{NNN}}：{{原型观察问题}}"
aliases: []
tags:
  - "vcddd/evidence"
  - "vcddd/prototype-observation"
vcddd_type: "prototype-observation-evidence"
vcddd_version: "2.0"
goal_id: "{{GOAL-NNN}}"
stage: "business-establishment"
status: "active"
owner_role: "prototype-observation-agent"
observation_evidence_id: "EVD-{{NNN}}"
source_id: "SRC-{{NNN}}"
source_note: "[[{{原型入口或说明}}]]"
prototype_snapshot: "{{version-or-hash}}"
result_note: "[[{{业务确立入口}}]]"
business_definition: "[[{{业务定义笔记}}]]"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# EVD-{{NNN}}：{{原型观察问题}}

> [!abstract] 主写身份
> 你是原型观察 Agent。本文只保存固定版本原型的可复现视觉与交互证据；不得把页面、控件或自己的解释直接定义成 `BL-*` 或 Domain。

本文围绕一个有边界的问题观察 `SRC-{{NNN}}`：[[{{原型入口或说明}}]]，并把证据返回 [[{{业务定义笔记}}]]。

## 观察任务

- 唯一候选业务线问题：
- 为什么必须观察原型：
- 触发角色：业务定义 Agent
- 返回的权威笔记：[[{{业务定义笔记}}]]
- 停止条件：

## 固定运行条件

- 原型版本、构建或快照：
- 入口：
- 运行方式：
- 观察日期：
- 账号或参与者角色：
- 测试数据和前置状态：
- 允许观察范围：
- 未能观察范围：

> [!warning]
> 不得用业务实现代码、组件名、路由、接口或数据库推断业务。启动说明只用于运行原型。

## 观察证据索引

| 证据 | 起始情境 | 关键动作或判断 | 实际状态变化 | 可见结果 | 媒体 |
|---|---|---|---|---|---|
| `EVD-{{NNN}}.1` |  |  |  |  | ![[{{screenshot.png}}]] |

## 观察证据详情

### EVD-{{NNN}}.1 — {{状态或结果}}

![[{{screenshot.png}}]]

- 原型版本：
- 起始情境与状态：
- 参与者角色：
- 到达步骤：
- 可见控件：
- 实际可执行动作：
- 关键判断或限制：
- 实际状态变化：
- 受影响的人、事、物或关系：
- 可观察结果：
- 自己的解释：
- 用户声明但原型尚未表达的意图：
- 不能由原型确定：

## 边界状态覆盖

| 状态 | 是否影响业务解释 | 是否观察 | 证据或未观察原因 |
|---|---|---|---|
| 成功 |  |  |  |
| 拒绝或无权限 |  |  |  |
| 空状态 |  |  |  |
| 重复操作 |  |  |  |
| 取消 |  |  |  |
| 失败 |  |  |  |
| 恢复 |  |  |  |
| 占位或未实现 |  |  |  |

## 返回业务定义 Agent

- 直接观察到的事实：
- 对候选业务线的提示：
- 需要用户确认的解释：
- 原型未表达或无法进入的部分：
- 与其他素材的冲突：
- 采纳状态：`pending`

> [!info]
> 本文不自动成为业务事实。只有业务定义 Agent 把结论写入 `业务定义.md` 或 `BL-*` 后，它才成为当前业务定义的一部分。

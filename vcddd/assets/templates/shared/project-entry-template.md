---
title: "VCDDD"
aliases:
  - "VCDDD 项目入口"
tags:
  - "vcddd/index"
vcddd_type: "project-entry"
vcddd_version: "2.0"
status: "active"
owner_role: "controller-agent"
current_stage: "business-discovery"
stage_status: "not-started"
active_work_id: ""
controller_record: ""
active_professional_record: ""
current_result: ""
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# VCDDD

> [!abstract] 主写身份
> 你是 VCDDD 主控 Agent。你只维护当前流程状态和直接链接，不在这里复制业务结论，也不替专业 Agent 更新阶段结果。

## 当前工作

- 当前阶段：`business-discovery`
- 阶段状态：`not-started`
- 当前路线：
- 工作 ID：
- 主控执行记录：[[{{主控执行记录}}]]
- 主专业 Agent：
- 专业对话 ID：
- 主专业执行记录：[[{{主专业执行记录}}]]
- 当前阶段结果：[[{{阶段结果}}]]
- 唯一下一动作：

## 三阶段导航

| 阶段 | 状态 | 已确认结果 | 当前执行记录 | 交接 |
|---|---|---|---|---|
| 业务挖掘 | `not-started` |  |  |  |
| 业务确立 | `design-pending` |  |  |  |
| Coding | `design-pending` |  |  |  |

## 当前参与角色

| 身份 | Agent/对话 ID | 状态 | 执行记录 | 拥有的产出 |
|---|---|---|---|---|
| 主控 Agent |  | `active` | [[{{主控执行记录}}]] | 本项目入口 |
| 主专业 Agent |  |  | [[{{主专业执行记录}}]] | [[{{阶段结果}}]] |

## 最近交接

- 来源阶段：
- 目标阶段：
- 默认输入：
- 按需追溯：
- 交接状态：
- 更新时间：

## 阻塞

- 是否阻塞：`false`
- 阻塞身份：
- 阻塞原因：
- 解除条件：

## 更新规则

- 创建或恢复专业对话后，更新“当前工作”和“当前参与角色”。
- 条件 Agent 出现或结束时，只增删对应角色行并链接其执行记录。
- 用户确认阶段结果后，更新阶段导航和最近交接。
- 本页只链接权威文档，不摘抄宏观目标、User Stories 或专业结论。

---
title: "{{工作名称}} - 执行记录"
aliases: []
tags:
  - "vcddd/execution"
vcddd_type: "execution-record"
vcddd_version: "2.0"
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "{{business-discovery | business-establishment | coding}}"
route: "{{controller | stage-route | conditional-task}}"
status: "not-started"
owner_role: "{{agent-role}}"
thread_id: "{{agent-thread-id}}"
parent_thread_id: "{{controller-thread-id}}"
parent_record: ""
result_note: ""
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# {{工作名称}} - 执行记录

> [!abstract] 主写身份
> 你是 `owner_role` 指定的 Agent。你只更新属于自己的这份记录，不替其他角色记录行为。

> [!info] 记录边界
> 记录语义进展、来源、决定、产出和交接。不要记录隐式思维链、逐条聊天复述或无关工具输出。

## 本轮目标

{{以当前身份的工作视角，说明本轮职责、目标和边界。}}

## 启动上下文

| 类型 | 来源与链接 | 固定版本/哈希 | 指定范围 | 用途 |
|---|---|---|---|---|
| `core` |  |  |  |  |
| `always` |  |  |  |  |
| `when-changed` |  |  |  |  |
| `on-trigger` |  |  |  |  |
| `forbidden` |  | 不适用 | 不得读取 |  |

## 路线检查点

> [!todo]
> 从对应身份或路线的 Agent 合同复制检查点。状态使用 `pending`、`active`、`completed` 或 `blocked`；只有合同明确允许时才使用 `not-applicable`。

| 检查点 | 目标 | 状态 | 结果或证据 | 更新时间 |
|---|---|---|---|---|
|  |  | `pending` |  |  |

## 当前状态

- 当前检查点：
- 已完成：
- 当前阻塞：
- 下一动作：

## 关键事件

只在检查点、用户决定、实质文档变化、阻塞和交接时添加。

### {{YYYY-MM-DD HH:mm}} — {{事件标题}}

- 类型：`checkpoint | user-decision | document-update | blocked | unblocked | confirmation | handoff`
- 发生了什么：
- 影响：
- 相关对象：[[{{相关笔记}}]]
- 下一步：

## 实际上下文使用

| 来源 | 固定版本/哈希 | 策略 | 实际读取范围 | 使用原因 | 读取时间 |
|---|---|---|---|---|---|
|  |  | `core` |  |  |  |

### 禁止上下文遵守情况

- 禁止项：
- 是否遵守：`yes | no`
- 如未遵守，原因与影响：

## 产出

| 文档 | 类型 | 状态 | 主写者 | 说明 |
|---|---|---|---|---|
| [[{{产出笔记}}]] |  | `draft` |  |  |

## 用户决定

| 决定 ID | 决定内容 | 影响对象 | 记录位置 | 日期 |
|---|---|---|---|---|
| `DEC-001` |  |  |  |  |

## 用户确认

- 本角色是否拥有阶段确认责任：`true | false`
- 是否明确确认：`false`
- 确认内容：
- 确认位置或消息引用：
- 确认时间：
- 确认后结果状态：

## 交接

- 接收身份或阶段：
- 默认交接文档：
- 按需追溯文档：
- 接收方必须知道的开放问题：
- 交回或检查状态：`pending`

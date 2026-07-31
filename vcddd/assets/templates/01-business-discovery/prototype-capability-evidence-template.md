---
title: "{{工作名称}} - 原型能力证据"
aliases: []
tags:
  - "vcddd/evidence"
  - "vcddd/prototype"
vcddd_type: "prototype-capability-evidence"
vcddd_version: "2.0"
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "business-discovery"
route: "prototype-capability-extraction"
status: "active"
owner_role: "prototype-capability-agent"
execution_record: "[[{{执行记录笔记}}]]"
result_note: "[[{{业务挖掘结果笔记}}]]"
prototype_snapshot: "{{version-or-hash}}"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# {{工作名称}} - 原型能力证据

> [!abstract] 主写身份
> 你是原型能力提取 Agent。由你运行、观察、截图和维护证据；主控不解释原型，也不补写能力。

本笔记记录从可运行原型中直接观察到的证据，为 [[{{业务挖掘结果笔记}}]] 提供依据。

> [!warning]
> 不得用业务实现代码、组件名、路由、接口或数据库推断能力。启动说明只用于运行原型。

## 原型运行信息

- 固定版本、构建或快照：
- 入口：
- 运行方式：
- 观察日期：
- 使用账号或角色：
- 测试数据条件：
- 用户确认原型代表的范围：
- 未能观察的范围：

## 视觉证据索引

| 证据 ID | 页面或状态 | 到达动作 | 直接观察到的事实 | 媒体 | 支持能力 |
|---|---|---|---|---|---|
| `EVD-001` |  |  |  | ![[{{screenshot.png}}]] | `CAP-001` |

## 视觉证据详情

### EVD-001 — {{页面或状态}}

![[{{screenshot.png}}]]

- 原型版本：
- 起始状态：
- 操作步骤：
- 直接观察：
- 不可由画面确认：
- 相关能力：`CAP-001`

## 宏观能力

### CAP-001 — {{能力名称}}

- 参与者：
- 情境：
- 能完成的事情：
- 预期效果：
- 直接证据：[[#EVD-001 — {{页面或状态}}]]
- 基于观察的解释：
- 需要用户确认：
- 用户纠偏结果：
- 对应 User Stories：

## User Story 映射

| Story ID | 能力 | 视觉证据 | 映射说明 |
|---|---|---|---|
| `US-001` | `CAP-001` | `EVD-001` |  |

## 开放或未观察项

| 对象 | 类型 | 内容 | 为什么不能确认 | 用户决定 |
|---|---|---|---|---|
|  | `open | not-observed | out-of-prototype` |  |  |  |

## 视觉覆盖检查

| 视图或状态 | 是否需要 | 是否观察 | 证据或原因 |
|---|---|---|---|
| 主要用户入口 | `true` | `false` |  |
| 关键成功状态 |  |  |  |
| 管理或治理视图 |  |  |  |
| 空状态 |  |  |  |
| 失败或限制状态 |  |  |  |
| 展开或详情状态 |  |  |  |

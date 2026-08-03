---
title: "领域地图"
aliases:
  - "{{业务目标名称}}领域地图"
tags:
  - "vcddd/domain-map"
vcddd_type: "domain-map"
vcddd_version: "2.0"
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "business-establishment"
status: "draft"
owner_role: "domain-discovery-agent"
execution_record: "[[{{Domain发现执行记录}}]]"
result_note: "[[{{业务确立入口}}]]"
business_definition: "[[{{业务定义笔记}}]]"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# 领域地图

> [!abstract] 主写身份
> 你是 Domain 发现 Agent。本文负责候选、所有权、边界与建模任务；每个 Domain 的内部事实由它自己的文档拥有。

本文从 [[{{业务定义笔记}}]] 及其业务线寻找 Domain，由 [[{{Domain发现执行记录}}]] 追踪。

## 当前业务范围

- 相关业务定义：[[{{业务定义笔记}}]]
- 已读取业务线：
- 未覆盖范围：
- 使用的草稿与假设：

## 事实与决定的所有权

| 所有权 ID | 事实、关系或决定 | 权威拥有者候选 | 其他角色只能怎样使用 | 业务依据 | 状态 |
|---|---|---|---|---|---|
| `OWN-001` |  |  | `引用 | 观察 | 投影 | 记录` | [[{{BL笔记}}]] | `candidate` |

## Domain 候选

| Domain ID | 候选名称 | 现实业务含义 | 存在依据 | 初步拥有内容 | 相关业务线 | 状态 |
|---|---|---|---|---|---|---|
| `DOM-001` | [[{{Domain笔记}}]] |  |  |  | [[{{BL笔记}}]] | `candidate` |

## 候选关系

| 来源 Domain | 关系 | 目标 Domain | 各自拥有的事实 | 需要进一步判断 |
|---|---|---|---|---|
| [[{{来源Domain}}]] |  | [[{{目标Domain}}]] |  |  |

## 非 Domain 信息

| 信息 ID | 内容 | 为什么需要 | 类型 | 为什么不是 Domain | 业务来源 |
|---|---|---|---|---|---|
| `ND-001` |  |  | `普通记录 | 外部引用 | 查询 | 流程进度 | 日志 | 技术信息` |  | [[{{BL笔记}}]] |

## Domain 建模任务

### DOM-{{NNN}}：{{候选名称}}

- 现实业务含义：
- 业务存在依据：[[{{BL笔记}}]]
- 初步拥有的信息、状态和关系：
- 初步判断与行为：
- 明确不拥有：
- 相邻 Domain 公开边界：
- 需要建模 Agent 回答的问题：
- 专业对话 ID：
- 执行记录：[[{{Domain执行记录}}]]
- 当前状态：`candidate`

## 撤销、合并与拆分记录

| 事件 | 原 Domain ID | 新关系或去向 | 证据 | 受影响业务线与组合 |
|---|---|---|---|---|
|  |  |  |  |  |

## 用户确认

- 当前成熟度：`draft`
- 用户是否明确确认：`false`
- 确认范围：
- 确认位置或消息引用：

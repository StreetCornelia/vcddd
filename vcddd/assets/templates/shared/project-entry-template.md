---
title: "VCDDD"
aliases:
  - "VCDDD 项目知识入口"
tags:
  - "vcddd/index"
vcddd_type: "project-entry"
vcddd_version: "2.0"
status: "active"
owner_role: "controller-agent"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# VCDDD

> [!abstract] 本页用途
> 本页只导航进入 Git 的长期事实。当前任务、Agent、对话和执行记录写入本地 `work/当前工作.md`。

## 业务挖掘

| 目标 ID | 业务挖掘结果 | 候选场景池 | 状态 |
|---|---|---|---|
| `GOAL-001` | [[01-business-discovery/GOAL-001/业务挖掘]] | [[01-business-discovery/GOAL-001/候选场景池]] | `draft` |

## 业务确立

| 目标 ID | 业务确立入口 | 业务定义 | 领域地图 | 业务组合 | 状态 |
|---|---|---|---|---|---|
| `GOAL-001` | [[02-business-establishment/business/GOAL-001/业务确立]] | [[02-business-establishment/business/GOAL-001/业务定义]] | [[02-business-establishment/business/GOAL-001/领域地图]] | [[02-business-establishment/business/GOAL-001/业务组合]] | `draft` |

## Domains

| Domain ID | Domain | 相关业务目标 | 状态 |
|---|---|---|---|
| `DOM-001` | [[02-business-establishment/domains/DOM-001/Domain]] | [[02-business-establishment/business/GOAL-001/业务确立]] | `draft` |

## Pre-Coding

- 系统与模块：[[03-pre-coding/系统与模块设计]]

| System ID | API 与 Domain 编排 | 数据库设计 | 状态 |
|---|---|---|---|
| `SYS-001` | [[03-pre-coding/systems/SYS-001/API 与 Domain 编排]] | [[03-pre-coding/systems/SYS-001/数据库设计]] | `draft` |

## Coding

| System ID | 设计与实现事实 | 状态 |
|---|---|---|
| `SYS-001` | [[04-coding/systems/SYS-001]] | `design-pending` |

## 更新规则

- 新增目标、Domain、系统或 Coding 正式事实时，增加对应行。
- 只登记权威文档和当前成熟度，不摘抄专业结论。
- 不写 `work_id`、Agent/对话 ID、执行记录或 `work/` 链接。
- 已失效事实保留入口，并将状态改为 `superseded`。

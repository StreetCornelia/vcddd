---
title: "VCDDD"
aliases:
  - "VCDDD 项目知识入口"
tags:
  - "vcddd/index"
vcddd_type: "project-entry"
vcddd_version: "2.0"
owner_role: "project-manager"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# VCDDD

> [!abstract] 本页用途
> 本页只导航进入 Git 的长期事实。当前任务、Agent、对话和执行记录写入本地 `work/当前工作.md`。

## 业务挖掘

| 目标 ID | 业务挖掘结果 | 候选场景池 |
|---|---|---|
| `{{GOAL-NNN}}` | [[01-business-discovery/{{GOAL-NNN}}-{{目标名称}}/业务挖掘]] | [[01-business-discovery/{{GOAL-NNN}}-{{目标名称}}/候选场景池]] |

## 业务确立

| 目标 ID | 业务确立入口 | 业务定义 | 领域地图 | 业务组合 |
|---|---|---|---|---|
| `{{GOAL-NNN}}` | [[02-business-establishment/business/{{GOAL-NNN}}-{{目标名称}}/业务确立]] | [[02-business-establishment/business/{{GOAL-NNN}}-{{目标名称}}/业务定义]] | [[02-business-establishment/business/{{GOAL-NNN}}-{{目标名称}}/领域地图]] | [[02-business-establishment/business/{{GOAL-NNN}}-{{目标名称}}/业务组合]] |

## Domains

| Domain ID | Domain | 相关业务目标 |
|---|---|---|
| `{{DOM-NNN}}` | [[02-business-establishment/domains/{{DOM-NNN}}-{{Domain名称}}/Domain]] | [[02-business-establishment/business/{{GOAL-NNN}}-{{目标名称}}/业务确立]] |

## Pre-Coding

- 系统与模块：[[03-pre-coding/系统与模块设计]]

| System ID | API 与 Domain 编排 | 数据库设计 | 验证入口 |
|---|---|---|---|
| `{{SYS-NNN}}` | [[03-pre-coding/systems/{{SYS-NNN}}-{{系统名称}}/API 与 Domain 编排]] | [[03-pre-coding/systems/{{SYS-NNN}}-{{系统名称}}/数据库设计]] | [[03-pre-coding/systems/{{SYS-NNN}}-{{系统名称}}/validation/index]] |

## Coding

| System ID | 开发任务图 | 编码规范 |
|---|---|---|
| `{{SYS-NNN}}` | [[04-coding/systems/{{SYS-NNN}}-{{系统名称}}/开发任务图]] | [[04-coding/systems/{{SYS-NNN}}-{{系统名称}}/编码规范]] |

## 更新规则

- 新增目标、Domain、系统、验证项或 Coding 正式事实时，增加对应行。
- 只登记权威文档，不摘抄专业结论。
- 不写 `work_id`、Agent/对话 ID、执行记录或 `work/` 链接。
- 已失效事实保留入口并说明替代它的新事实。

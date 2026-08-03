---
title: "业务确立"
aliases:
  - "{{业务目标名称}}业务确立"
tags:
  - "vcddd/business-establishment"
vcddd_type: "business-establishment-index"
vcddd_version: "2.0"
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "business-establishment"
status: "draft"
owner_role: "controller-agent"
execution_record: "[[{{主控执行记录}}]]"
business_definition: "[[{{业务定义笔记}}]]"
domain_map: "[[{{领域地图笔记}}]]"
business_composition: "[[{{业务组合笔记}}]]"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# 业务确立

> [!abstract] 主写身份
> 你是 VCDDD 主控 Agent。本文只导航专业事实、登记各自产出成熟度和直接链接；不得复制或改写业务与 Domain 结论。

## 当前目标

- 来源目标：[[{{业务挖掘结果}}]]
- 当前范围：
- 当前假设与可能返工范围：

## 事实地图

| 事实类型 | 权威入口 | 状态 | 拥有角色 | 执行记录 |
|---|---|---|---|---|
| 业务定义 | [[{{业务定义笔记}}]] | `draft` | 业务定义 Agent | [[{{业务定义执行记录}}]] |
| 领域地图 | [[{{领域地图笔记}}]] | `draft` | Domain 发现 Agent | [[{{Domain发现执行记录}}]] |
| Domain | [[{{领域地图笔记}}]] | `draft` | 各 Domain 建模 Agent | 见各 Domain 文档 |
| 业务组合 | [[{{业务组合笔记}}]] | `draft` | 业务组合 Agent | [[{{业务组合执行记录}}]] |

## Domain 导航

| Domain ID | Domain | 状态 | 建模对话 | 执行记录 |
|---|---|---|---|---|
| `DOM-001` | [[{{Domain笔记}}]] | `draft` |  | [[{{Domain执行记录}}]] |

## 当前专业对话

| 角色 | 对话 ID | 状态 | 当前目标 | 产出 |
|---|---|---|---|---|
|  |  |  |  |  |

## 使用当前事实的说明

- 已确认内容：
- 草稿内容：
- 使用草稿时必须知道的假设：
- 受影响的判断和可能返工范围：
- 推荐能力连接：

## 更新规则

- 专业角色只更新自己拥有的事实和执行记录。
- 主控沿权威链接登记状态，不在本文制作替代摘要。
- 某个 Domain 新增、撤销、合并或拆分后，更新 Domain 导航并保留旧 ID 的状态。
- `confirmed` 只描述对应产出的用户确认状态，不控制 Pre-Coding 或 Coding 能否开始。

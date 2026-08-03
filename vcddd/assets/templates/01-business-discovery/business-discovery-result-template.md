---
title: "{{工作名称}} - 业务挖掘结果"
aliases: []
tags:
  - "vcddd/stage-result"
  - "vcddd/business-discovery"
vcddd_type: "business-discovery-result"
vcddd_version: "2.0"
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "business-discovery"
route: "business-discovery"
status: "draft"
owner_role: "business-discovery-agent"
execution_record: "[[{{执行记录笔记}}]]"
candidate_scenarios: ""
user_confirmed: false
confirmation_evidence: ""
recommended_capabilities:
  - "business-establishment"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# {{工作名称}} - 业务挖掘结果

> [!abstract] 主写身份
> 你是本阶段的主专业 Agent。由你根据与用户的直接协作维护本文；主控只登记成熟度和能力连接，不参与内容设计。

本结果由 [[{{执行记录笔记}}]] 追踪。它通常是“业务确立”能力的主要参考，也可以被其他能力按当前成熟度直接使用；它不是阶段准入凭证。

## 宏观业务目标

{{用一段完整文字说明：为哪些人或组织改变什么现状，提供哪些宏观能力，最终达到什么效果。}}

## 预期效果

| 参与者 | 当前情境或问题 | 能获得的能力 | 预期效果 |
|---|---|---|---|
|  |  |  |  |

## 本次已选 User Stories

> [!important]
> 只放用户已经选择的宏观能力。详细规则和系统设计留给后续阶段。

| Story ID | 角色 | 情境 | 能做的事情 | 结果或价值 | 来源场景 | 证据 |
|---|---|---|---|---|---|---|
| `US-001` |  |  |  |  | `SCN-___` | [[{{来源笔记}}]] |

## Story 关系与边界

| Story ID | 依赖或关联 | 边界说明 |
|---|---|---|
| `US-001` |  |  |

## 本次范围

- 

## 明确非目标

- 

## 未进入本次范围的候选项

| 对象 ID | 状态 | 内容摘要 | 原因 | 追溯 |
|---|---|---|---|---|
| `SCN-___` | `deferred | rejected | open | duplicate` |  |  | [[{{候选场景池}}]] |

## 推荐由业务确立能力继续回答

以下问题不影响本文按真实成熟度被其他能力引用。通常建议由业务确立能力继续回答，也可以由用户指定其他能力处理：

- 

## 来源与素材交接

- 候选场景池：[[{{候选场景池}}]]

| 来源 ID | 原始素材 | 类型 | 固定版本、日期或快照 | 本阶段实际读取范围 | 用于确认的宏观判断 | 建议业务确立深读的位置与理由 |
|---|---|---|---|---|---|---|
| `SRC-001` | [[{{原始素材}}]] | `conversation | document | prototype | screenshot | existing-system | other` |  |  |  |  |

> [!info]
> 本表只提供来源导航和读取边界，不把简要转述变成新的事实源。业务线、业务规则和 Domain 由业务确立基于原始素材及可追溯证据另行形成。

## 用户确认

- 确认状态：`awaiting-user-confirmation`
- 确认内容：
- 确认位置或消息引用：
- 确认日期：

> [!warning]
> 只有用户明确确认后，才能同时将 `status` 改为 `confirmed`、`user_confirmed` 改为 `true`，并填写 `confirmation_evidence`。

> [!info]
> `confirmed` 只表示用户确认了本文，不是启动业务确立或 Coding 的前置条件。未确认时应保持真实状态，并在被引用处说明假设和返工风险。

## 能力衔接建议

- 可能使用本文的能力或角色：
- 主要参考：本文档
- 需要按需追溯的证据：
- 不应默认加载的材料：
- 当前成熟度与使用假设：
- 建议继续处理的问题：

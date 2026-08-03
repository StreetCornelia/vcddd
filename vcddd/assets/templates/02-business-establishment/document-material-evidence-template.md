---
title: "MAT-{{NNN}}：{{素材问题}}"
aliases: []
tags:
  - "vcddd/evidence"
  - "vcddd/document-material"
vcddd_type: "document-material-evidence"
vcddd_version: "2.0"
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "business-establishment"
status: "active"
owner_role: "document-material-analysis-agent"
material_evidence_id: "MAT-{{NNN}}"
source_id: "SRC-{{NNN}}"
source_note: "[[{{原始素材}}]]"
source_version: "{{version-date-or-hash}}"
execution_record: "[[{{文档素材分析执行记录}}]]"
result_note: "[[{{业务确立入口}}]]"
business_definition: "[[{{业务定义笔记}}]]"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# MAT-{{NNN}}：{{素材问题}}

> [!abstract] 主写身份
> 你是文档素材分析 Agent。本文只保存从固定来源中取得的可定位证据、解释和边界；不得在此定义 `BL-*`、业务范围或 Domain。

本文围绕一个有边界的问题分析 `SRC-{{NNN}}`：[[{{原始素材}}]]，并把证据返回 [[{{业务定义笔记}}]]。

## 取证任务

- 唯一素材问题或候选业务线：
- 为什么需要独立取证：
- 触发角色：业务定义 Agent
- 返回的权威笔记：[[{{业务定义笔记}}]]
- 停止条件：

## 来源与读取边界

| 来源 ID | 原始素材 | 来源身份 | 固定版本、日期或哈希 | 允许范围 | 实际读取范围 | 未读取范围 |
|---|---|---|---|---|---|---|
| `SRC-{{NNN}}` | [[{{原始素材}}]] | `current | historical | proposal | example | fragment | unknown` |  |  |  |  |

> [!warning]
> 本文是证据记录，不替代原始素材。摘录、临时投影和摘要必须能从固定版本重新定位和校验。

## 证据索引

| 证据 | 精确位置 | 类型 | 内容摘要 | 支持或冲突的业务线提示 |
|---|---|---|---|---|
| `MAT-{{NNN}}.1` | [[{{原始素材}}#{{稳定章节标题}}]] | `direct-statement | interpretation | candidate-line | conflict | unknown` |  |  |

## 证据详情

### MAT-{{NNN}}.1 — {{证据名称}}

- 精确位置：[[{{原始素材}}#{{稳定章节标题}}]]
- 来源直接声明：
- 参与者与意图：
- 行为或判断：
- 被改变的人、事、物或关系：
- 可观察结果：
- 异常、拒绝、取消或恢复：
- 跨段落解释：
- 候选业务线提示：
- 不能由来源确定：

## 冲突、历史状态与缺口

| ID | 类型 | 内容 | 涉及位置 | 对业务定义的可能影响 |
|---|---|---|---|---|
| `MAT-{{NNN}}.C1` | `conflict | historical | version-unknown | missing | ambiguous` |  |  |  |

## 返回业务定义 Agent

- 能够直接采用的来源声明：
- 需要用户确认的解释：
- 候选业务线提示：
- 不应采纳的历史、冲突或不完整内容：
- 未展开但值得另建任务的线索：
- 采纳状态：`pending`

> [!info]
> 只有业务定义 Agent 把结论写入 `业务定义.md` 或 `BL-*` 后，它才成为当前业务定义的一部分。

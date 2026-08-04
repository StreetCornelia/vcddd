---
title: "当前工作"
aliases:
  - "VCDDD 当前工作"
tags:
  - "vcddd/local-work"
vcddd_type: "local-work-entry"
vcddd_version: "2.0"
git_tracked: false
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "{{business-discovery | business-establishment | pre-coding | coding}}"
status: "active"
owner_role: "controller-agent"
controller_record: "[[work/{{WORK-YYYYMMDD-NNN}}/主控状态]]"
result_note: "[[{{正式事实的 vault 内路径}}]]"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# 当前工作

> [!warning] 仅保存在本地
> 本页和 `work/` 内所有内容不得进入 Git。长期事实写入四阶段正式目录。

## 当前目标

- 工作 ID：`{{WORK-YYYYMMDD-NNN}}`
- 当前能力：
- 当前目标：
- 当前状态：`active`
- 正式结果：[[{{正式事实的 vault 内路径}}]]
- 主控状态：[[work/{{WORK-YYYYMMDD-NNN}}/主控状态]]
- 已知假设或缺口：
- 推荐动作及理由：

## 当前参与者

| 身份 | Agent/对话 ID | 状态 | 执行记录 | 拥有或更新的正式结果 |
|---|---|---|---|---|
| 主控 Agent |  | `active` | [[work/{{WORK-YYYYMMDD-NNN}}/主控状态]] | 本页 |
| 主专业 Agent |  |  | [[work/{{WORK-YYYYMMDD-NNN}}/执行记录/{{角色或任务}}]] | [[{{正式事实的 vault 内路径}}]] |

## 本轮上下文

| 策略 | 来源 | 固定版本/哈希 | 指定范围 | 用途 |
|---|---|---|---|---|
| `core` |  |  |  |  |
| `always` |  |  |  |  |
| `when-changed` |  |  |  |  |
| `on-trigger` |  |  |  |  |
| `forbidden` |  |  |  |  |

## 当前限制与下一步

- 受影响的具体判断：
- 不受影响、仍可继续的工作：
- 待用户决定：
- 下一动作：

## 更新规则

- 切换当前工作时更新本页，不修改 `VCDDD.md` 保存过程状态。
- 创建或恢复 Agent 时更新参与者、执行记录和正式结果链接。
- 工作结束后保留对应 `work/<work-id>/`；新工作覆盖本页的当前指向。

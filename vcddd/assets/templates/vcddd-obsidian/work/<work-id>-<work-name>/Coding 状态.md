---
title: "{{工作名称}} - Coding 状态"
aliases: []
tags:
  - "vcddd/local-work"
  - "vcddd/coding"
vcddd_type: "coding-status"
vcddd_version: "2.0"
git_tracked: false
work_id: "{{WORK-YYYYMMDD-NNN}}"
stage: "coding"
status: "active"
owner_role: "{{controller-agent-or-current-professional-role}}"
system_id: "{{SYS-NNN}}"
system_name: "{{系统名称}}"
code_repository: "{{仓库路径或 URL}}"
code_root: "{{系统代码根目录}}"
task_graph: "[[04-coding/systems/{{SYS-NNN}}-{{系统名称}}/开发任务图]]"
coding_style: "[[04-coding/systems/{{SYS-NNN}}-{{系统名称}}/编码规范]]"
integration_branch: "{{branch-name}}"
integrated_commit: "{{COMMIT}}"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# {{工作名称}} - Coding 状态

> [!warning] 仅保存在本地
> 本页只保存当前调度状态，不进入 Git，不填写任何 Key、Token、密码或证书内容。

## 当前集成基线

| 项目 | 当前值 |
|---|---|
| 系统 | [[04-coding/systems/{{SYS-NNN}}-{{系统名称}}/开发任务图]] |
| 代码仓库 | `{{仓库路径或 URL}}` |
| 系统代码根目录 | `{{系统代码根目录}}` |
| 集成分支 | `{{branch-name}}` |
| 最新集成 Commit | `{{COMMIT}}` |
| 当前集成 Agent | {{无/Agent 或对话 ID}} |
| 集成分支状态 | `idle | integrating` |

## 任务状态

状态使用 `waiting | ready | developing | waiting-input | queued | integrating | returned | integrated`。

| 任务 | 任务文档 | 本系统前置任务 | 系统外依赖 | 状态 | 开发 Agent/对话 | 候选 Commit | 集成 Agent/对话 | 集成 Commit | 下一动作 |
|---|---|---|---|---|---|---|---|---|---|
| {{TASK-SYS-NNN-NNN - 任务名称}} | [[04-coding/systems/{{SYS-NNN}}-{{系统名称}}/tasks/{{TASK-SYS-NNN-NNN}}-{{任务名称}}/任务]] | {{无/任务 ID}} | {{无/对方系统的任务或集成结果}} | `waiting` |  |  |  |  | {{全部依赖可用后启动}} |

## 串行集成队列

| 顺序 | 任务 | 候选 Commit | 进入时间 | 当前处理 |
|---|---|---|---|---|
| 1 | {{任务 ID 与名称}} | `{{COMMIT}}` | {{YYYY-MM-DD HH:mm}} | {{等待/集成 Agent ID}} |

## 外部输入请求

本表只写配置名称、用途、最低权限、受影响动作和授权状态。敏感值通过环境变量或项目已有 Secret 机制提供，不写入本页。

| 请求 ID | 任务 | 所需内容 | 用途与配置入口 | 环境与最低范围 | 受影响动作 | 可继续工作 | 状态 | 安全引用 |
|---|---|---|---|---|---|---|---|---|
| INPUT-{{NNN}} | {{任务 ID 与名称}} | {{Provider Key、测试账号等}} | {{用途；环境变量或 Secret 名称}} | {{目标环境与最低权限}} | {{当前不能完成的实现或验证}} | {{不受影响的工作}} | `requested | provided | verified | expired` | {{只写引用，不写值}} |

## 更新规则

- 只记录当前状态；调度事件写入主控执行记录。
- 本页只属于一个系统；同一业务中的其他系统分别创建自己的 Coding 工作与状态页。
- 同一集成分支同时只能有一个集成 Agent。
- 本系统前置任务全部集成且系统外依赖已经验证可用后，立即把任务从 `waiting` 更新为 `ready`。
- 开发 Agent 形成候选后停止修改，候选按进入时间加入队列。
- 候选被退回时恢复原开发 Agent；新候选加入队尾，其他候选继续处理。
- 候选集成成功后更新最新集成 Commit，并立即检查直接后继任务。
- 缺少真实运行条件时把受影响任务记为 `waiting-input`；不受影响的开发和审查继续进行。
- 不在本页保存历史 diff、Agent 推理、完整验证输出或任何敏感值。

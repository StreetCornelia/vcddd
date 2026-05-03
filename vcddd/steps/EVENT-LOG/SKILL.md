---
name: vcddd-event-log
description: VCDDD — 事件日志系统：域级进度追踪
---

# Step: EVENT-LOG — 事件日志系统

每个域维护自己的进度日志 `docs/vcddd/design/{domain}/progress.log`，记录任务目标、执行计划和已完成操作。

日志用于 Agent 切换时的任务延续——新 Agent 通过阅读日志了解当前目标、已完成工作和下一步计划。

## 日志格式

```
# Domain: {domain}

## Task {N}: {YYYY-MM-DD HH:MM} — {任务标题}
## Goal
{详细目标描述。包含当前任务要达成什么状态、涉及哪些文件或功能、需满足哪些业务约束。
不依赖对话历史，新 Agent 读完就能独立理解完整上下文。}

### Plan
{执行计划，逐条列出}

### Execution
- [{timestamp}] [{ROLE}] {操作描述}

### Next
- [{状态标签}] {下一步需要做的事}
```

## 状态标签

`[PENDING]` / `[IN PROGRESS]` / `[BLOCKED]` / `[DONE]` / `[WONTFIX]`

## 使用规则

- 每个新任务 → 新建一个 Task 节点
- 每个 sub-agent 在 Execution 节追加操作记录
- 总控维护 Task 节点创建和 Next 列表
- Agent 切换时读 Goal + Next + 最近 Execution

本文件是日志系统的入口步骤定义，作为子 Agent 指令使用。流程中遇到日志相关问题时直接使用本文件中的规范。

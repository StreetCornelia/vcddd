---
vcddd_type: "stage-instructions"
vcddd_version: "2.0"
stage: "coding"
status: "design-pending"
---

# Coding 说明

**阅读身份：** VCDDD 主控 Agent。本文记录已经确定的工作和仍需设计的内容。主控不开展 Coding 专业工作。

## 已确定边界

Coding 负责：

- 调查并确认系统工程编码规范；
- 盘点代码产物、依赖、写入范围和共享位置；
- 形成开发任务与并行关系；
- 在隔离工作区实现生产代码；
- 进行任务级和组合级运行验证；
- 根据证据返回业务、Domain 或 Pre-Coding 设计反馈；
- 完成工程改进与独立代码审核。

业务、Domain 和业务组合由业务确立拥有；架构、模块、API、逐 API 编排、数据库和开发基线由 Pre-Coding 拥有。Coding 忠实使用这些事实，但运行和实现证据可以触发源事实修订。

推荐输入是当前 Pre-Coding 投影和现有代码事实，也可以从明确缺陷、代码任务、原型或局部工程目标直接开始。缺失的业务或设计上下文应成为具体假设、受影响代码范围和返工风险，不得被概括为前序能力未完成。

## 尚待共同设计

- Coding 内部的角色、任务和验证结构；
- 工程规范、任务图、实现、验证、改进和审核模板；
- worktree、Commit 和 Agent 复用规则；
- 面向增量验证的上下文控制；
- 设计反馈与受影响范围重算。

工作说明完成前，主控不得调用旧版开发、测试或审核 Agent 冒充新版 Coding 角色。用户仍可使用其他能力或共同设计本能力。

Coding 正式事实的稳定归属为 `vcddd-obsidian/04-coding/systems/<system-id>/`；具体文档类型和模板在共同设计后补充。当前工作、Agent 执行记录和临时材料仍只放在 `vcddd-obsidian/work/<work-id>/`，不进入 Git。

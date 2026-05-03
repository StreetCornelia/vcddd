---
name: vcddd-integrate
description: VCDDD — 跨域集成验证（系统级对抗方）
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。

# Step: INTEGRATE — 跨域集成验证

验证各域实现之间的协作是否一致。这是系统级对抗方，检查多域的业务语义拼合。

**参与角色**：集成验证（发现问题 + 给出建议）→ 总控（协调）→ 各域 Implementer（修复）

## 前置条件

- 所有域的代码已实现并通过各自的三层审查

## 输入

- `facts.md`（业务全景）、各域 `business.md` + `boundary.md`、各域实现代码

## 输出

跨域集成验证报告

## 执行流程

```
运行验证检查 → 发现问题
    │
    ├── [技术问题] 字段/幂等/依赖方向
    │     → 总控直接派 Implementer 修复
    │
    └── [业务细化问题] 事件顺序/并发冲突
          → 集成验证给出建议方案
          → 总控暂停，向用户呈现
          → 用户确认后更新 business.md
          → 受影响域重新过 REVIEW-DOMAIN
```

验证检查项：契约结构、端到端工作流、幂等、事件顺序与并发、依赖方向。

## 如果卡住

读 `../../reference/engine/integration-verification.md` 获取完整验证清单。

## 日志

在 `docs/vcddd/progress.log` 追加 Task 节点。记录每项检查结果和协调修复操作。

## 验证

- [ ] 全部技术问题已修复
- [ ] 业务细化问题已向用户呈现并得到回复
- [ ] 修改 business.md 后对应域已重新通过审查
- [ ] 对抗循环不超过 10 轮

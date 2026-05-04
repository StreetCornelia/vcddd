---
name: vcddd-tdd-bridge
description: VCDDD — 从 business.md 推导黑盒测试规格
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。
> 本文件同时是控制器的调度参考——控制器必须按以下调度循环执行，不需要用户提醒。

# Step: TDD-BRIDGE — 黑盒测试规格推导

从已确认的域文档机械推导该域的**黑盒功能测试规格**。测试只覆盖域对外暴露的能力（命令入口、事件消费、读模型），不涉及内部实现。

## 前置条件

- 该域 `business.md` + `boundary.md` 已确认

## 输入

- 该域的 `business.md` + `boundary.md`

## 输出

`docs/vcddd/design/{domain}/test-spec.md`

## 参与角色

**Generator** 和 **Reviewer** 是两个独立的 Agent。Generator 负责推导测试规格，Reviewer 负责审查。对抗生成流程遵循 `../../reference/engine/review-loop.md` 的"通用对抗生成框架"。

## 覆盖要求

| 维度 | 含义 | 检查标准 |
|------|------|---------|
| 功能完整性 | 每条对外能力都有测试 | 每条命令/事件/读模型至少 1 个正常测试 |
| 分支完整性 | 每条路径都有测试 | 每条正常+失败路径逐条对应测试 |
| 数据边界性 | 每个参数边界有测试 | 空字符串/负数/超长/非法枚举/不存在 ID |

所有测试使用自然语言或伪代码描述，不写具体编程语言代码。每条测试包含：目标、操作、期望结果。失败测试必须写明具体错误原因和错误来源。

## 调度循环（控制器强制执行）

**以下是控制器的强制执行指令。每个步骤完成后立即进入下一步，不需要用户提醒。**

```
┌─ TDD Bridge 循环开始 ──────────────────────────────────┐
│                                                         │
│  1. 派遣 Generator Agent                                 │
│     → 传入：business.md + boundary.md + 推导规则        │
│            （规则见 ../../reference/engine/tdd-bridge.md）│
│     → Generator 按规则机械推导 test-spec.md              │
│     → 返回完整的 test-spec.md                            │
│                                                         │
│  2. Generator 返回后【立即】派遣 Reviewer Agent          │
│     → 传入：business.md + boundary.md + test-spec.md    │
│            + 审查清单（见 ../../reference/engine/tdd-bridge.md）│
│     → Reviewer 独立审查                                  │
│     → 一次性给出全部问题                                 │
│     → 返回：PASS / ISSUES                               │
│                                                         │
│  3. Reviewer 返回 ISSUES 后【立即】：                    │
│     → 重新派遣 Generator，传入问题列表                   │
│     → Generator 一次性修复全部问题，重新提交 test-spec.md │
│     → 重新派遣 Reviewer 审查                             │
│     → 循环直到 PASS 或达到 10 轮上限                     │
│                                                         │
│  4. Reviewer 返回 PASS 后：                              │
│     → test-spec.md 确认完成                             │
│     → 控制器进入下一个域的 TDD Bridge，或进入 Implementer │
│                                                         │
└─ TDD Bridge 循环结束 ──────────────────────────────────┘
```

**关键约束**：
- Generator 和 Reviewer 必须是两个独立 Agent
- Reviewer 返回意见后，Generator 一次性修复（不逐条修）
- 修复后必须重新派遣 Reviewer（不自行判断是否通过）
- 不需要用户提醒

## 如果卡住

读 `../../reference/engine/tdd-bridge.md` 获取完整推导规则。

## 日志

在对应域的 `progress.log` 追加 Task 节点。记录推导出的测试条目和 Reviewer 发现的问题。

## 验证

- [ ] 所有测试是黑盒
- [ ] 每条命令的正常+失败+幂等 → 有测试
- [ ] 每个参数边界 → 有测试
- [ ] 每条失败测试写了具体错误原因
- [ ] business.md 未定义的内容标记 [待补充]
- [ ] Generator ↔ Reviewer 对抗已完成（Review 返回 PASS）

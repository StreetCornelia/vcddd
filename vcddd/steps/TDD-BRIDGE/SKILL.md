---
name: vcddd-tdd-bridge
description: VCDDD — 从 business.md 推导黑盒测试规格
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。

# Step: TDD-BRIDGE — 黑盒测试规格推导

从已确认的域文档机械推导该域的**黑盒功能测试规格**。测试只覆盖域对外暴露的能力（命令入口、事件消费、读模型），不涉及内部实现。

**参与角色**：Generator（推导 test-spec.md）← Test Spec Reviewer（审核）→ 对抗，最多 10 轮

## 前置条件

- `docs/vcddd/design/{domain}/business.md` + `boundary.md` 已确认

## 输入

- 该域的 `business.md` + `boundary.md`

## 输出

`docs/vcddd/design/{domain}/test-spec.md`

## 覆盖要求

| 维度 | 含义 | 检查标准 |
|------|------|---------|
| 功能完整性 | 每条对外能力都有测试 | 每条命令/事件/读模型至少 1 个正常测试 |
| 分支完整性 | 每条路径都有测试 | 每条正常+失败路径逐条对应测试 |
| 数据边界性 | 每个参数边界有测试 | 空字符串/负数/超长/非法枚举/不存在 ID |

所有测试使用自然语言或伪代码描述，不写具体编程语言代码。每条测试包含：目标、操作、期望结果。失败测试必须写明具体错误原因和错误来源。

## 对抗流程

Generator 提出测试用例 → Generator 关联 prompt 见 `generator-prompt.md` → Reviewer 审查 → 不通过则修正重审（10 轮上限）。

Reviewer 的 prompt 见 `reviewer-prompt.md`。

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

---
name: vcddd-review-domain
description: VCDDD — 三层对抗审查 + 测试验证
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。

# Step: REVIEW-DOMAIN — 域审查

对已实现的域代码进行三层对抗审查 + 测试验证。每层发现问题后返回 Implementer 修复，修复后重新审查。最多 10 轮。

**前置步骤**：IMPLEMENT-DOMAIN 已完成（同一个 Implementer 完成了代码 + 白盒测试 + 黑盒测试）。

## 输入

- `business.md`（Spec + VCDDD 需要）、`boundary.md`（Spec + VCDDD 需要）
- `tech-stack.md`（Quality + VCDDD 需要）
- 实现代码 + 白盒测试 + 黑盒测试

## 输出

- 审查结果报告（每层的通过/不通过状态 + 问题列表）

## 审查流程

```
运行全部测试（白盒 + 黑盒）
    │
    ├── 有测试失败 → 记录具体错误 → 交给 Implementer 修复 → 重新运行
    │
    └── 全部通过
          │
          ▼
    Spec Reviewer → 核对代码 vs business.md
      ├── 通过 → Quality Reviewer
      └── 不通过 → Implementer 修复 → 重审（10 轮上限）

    Quality Reviewer → 核对代码 vs tech-stack.md
      ├── 通过 → VCDDD Reviewer
      └── 不通过 → Implementer 修复 → 重审（10 轮上限）

    VCDDD Reviewer → 核对 VCDDD 合规性
      ├── 合规 ✅ → 域审查通过
      ├── 不合规 → Implementer 修复 → 从 Spec 重新审
      └── 有条件合规 ⚠️ → 标记 DONE_WITH_CONCERNS
```

## 测试验证细节

审查开始时，Reviewer 必须**先运行全部测试**（白盒 + 黑盒）：

- 全部通过 → 进入 Spec Review
- 有失败 → 不继续审查，而是立即报告：
  - 哪些测试失败（测试名 + 位置）
  - 每个失败的具体错误信息
  - 交给 Implementer 判断和修复

修复完成后重新运行全部测试，直到全部通过才进入 Spec Review。

## 三份 Reviewer Prompt

各层 Reviewer 的独立 Prompt 文件：

| 层级 | Prompt 文件 |
|------|------------|
| Spec Compliance | `spec-reviewer-prompt.md` |
| Code Quality | `quality-reviewer-prompt.md` |
| VCDDD Compliance | `vcddd-reviewer-prompt.md` |

每份 Prompt 中包含了**运行测试并验证全部通过**的检查要求。

## 如果卡住

读 `../../reference/engine/review-loop.md` 获取完整核对清单。

## 日志

在 `docs/vcddd/design/{domain}/progress.log` 追加 Task 节点。各层 Reviewer 记录审查结果和发现的问题。

## 验证

- [ ] 全部测试（白盒+黑盒）通过
- [ ] Stage 1: 所有不变式/状态迁移/命令路径在代码中实现
- [ ] Stage 2: 命名/目录/依赖/日志/错误处理符合 tech-stack.md
- [ ] Stage 3: 域边界正确、通用语言一致、事务对齐、事件事务后发布
- [ ] 测试失败时记录了具体错误信息
- [ ] 每层首次审查一次性给出全部问题
- [ ] 对抗循环不超过 10 轮

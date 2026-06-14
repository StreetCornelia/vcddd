# VCDDD

VCDDD（Vibe Coding Domain-Driven Design）是一套面向 AI 辅助开发的业务建模方法论。

---

## 入口检查

当用户要求使用 VCDDD 时，按以下逻辑执行：

```
用户是否明确要求使用 VCDDD？
    │
    ├── 否 → 不适用 VCDDD，自由操作
    │
    └── 是 → 检查 docs/vcddd/.vcddd-active 是否存在
          │
          ├── 存在 → 读取 vcddd/SKILL.md，判断当前进度，从断点继续
          │
          └── 不存在 → 这是新项目，需要初始化
                → 询问用户："当前项目尚未初始化 VCDDD。
                  是否需要进行 VCDDD 初始化？"
                → 用户确认后 → 执行 /vcddd-vision
```

## 必读文件

在执行任何 VCDDD 命令之前，确认已读取以下文件。如果尚未读取，现在读取。

| 文件 | 内容 |
|------|------|
| `reference/theory/vcddd-methodology.md` | 理论基座：为什么需要 VCDDD、核心世界观、思考模型 |
| `reference/engine/automated-execution.md` | 自动化执行流程：控制器的调度手册 |
| `reference/engine/model-selection.md` | 模型选择策略：效率模型 / 深度思考模型 |

读完后在回复中确认："我已读取 [文件名]，理解 [核心要点]。"

## 命令列表

> 以下命令是 VCDDD 的唯一合法入口。任何项目操作都必须通过这些命令执行。
> 不允许绕过命令直接操作文件、代码或测试。

| 命令 | 作用 | 何时用 | 入口文件 |
|------|------|-------|---------|
| `/vcddd-vision` | 捕捉用户意图写入 input.md | 用户提出模糊需求 | `steps/VISION/SKILL.md` |
| `/vcddd-context` | 澄清为业务事实 | input.md 已确认 | `steps/CONTEXT/SKILL.md` |
| `/vcddd-domain-design` | 推导域边界与业务设计 | facts.md 已确认 | `steps/DOMAIN-DESIGN/SKILL.md` |
| `/vcddd-dev-setup` | 确定技术栈 | 域设计已确认 | `steps/DEVSETUP/SKILL.md` |
| `/vcddd-scaffold` | 生成项目骨架 | tech-stack.md 已确认 | `steps/SCAFFOLD/SKILL.md` |
| `/vcddd-frontend-design` | 使用 google-design-md 完成前端设计规范 | 项目包含用户界面，且 tech-stack.md 已确认 | `steps/FRONTEND-DESIGN/SKILL.md` |
| `/vcddd-tdd-bridge` | 推导黑盒测试规格 | 域设计已确认 | `steps/TDD-BRIDGE/SKILL.md` |
| `/vcddd-implement-domain` | 实现一个域 | test-spec.md 就绪 | `steps/IMPLEMENT-DOMAIN/SKILL.md` |
| `/vcddd-review-domain` | 三层审查 + 测试运行 | Implementer 完成 | `steps/REVIEW-DOMAIN/SKILL.md` |
| `/vcddd-integrate` | 跨域集成验证 | 所有域审查通过 | `steps/INTEGRATE/SKILL.md` |
| `/vcddd-report` | 最终报告 | 集成验证通过 | `steps/REPORT/SKILL.md` |

## 强制规则

> 以下规则在执行任何 VCDDD 命令时不可违反。

1. **不修改代码** — 所有代码修改通过 `/vcddd-implement-domain` 完成
2. **不读代码** — 只读文档和子 Agent 返回结果
3. **不运行测试** — 所有测试运行通过 `/vcddd-review-domain` 完成
4. **不跳过审查** — Implementer 返回后必须 `/vcddd-review-domain`
5. **用斜杠命令派遣** — 不用自然语言描述，用 invoke /vcddd-xxx
6. **记录到 progress.log** — 每个步骤完成后追加记录
7. **有 Mock 就不算通过** — 测试必须全部 [REAL] + 环境恢复原状
8. **用效率模型派遣子 Agent** — 模型策略见 `reference/engine/model-selection.md`
9. **实现前加载项目上下文** — 进入 `/vcddd-scaffold`、`/vcddd-tdd-bridge`、`/vcddd-implement-domain`、`/vcddd-review-domain`、`/vcddd-integrate` 前，必须读取实现线所需的项目上下文文档。

---
name: vcddd
description: |
  VCDDD 业务/架构导航 Skill。基于业务事实进行域分析与边界确认，逐步骤渐进式执行。
---

# VCDDD 详细参考

> ⚠️ **如果你还没有读取 `VCDDD-ENTRY.md`，先读取它。** 那里有命令列表和强制规则。
> 本文件是详细参考，包含总控 Agent 说明、步骤详情、理论基座等。

VCDDD（Vibe Coding Domain-Driven Design）是一套面向 AI 辅助开发的业务建模方法论。核心命题：

> **代码可以频繁变化，但系统对业务世界的表达不能漂移。**

---

## 总控 Agent（Controller）

VCDDD 使用总控 Agent 协调所有步骤的执行。总控 Agent 是运行本 Skill 的 AI session 自身。

### 总控的工作流程

```
用户提出需求（可能模糊，可能不完整）
    │
    ▼
[总控] 分析需求 → 判断涉及哪些步骤
    │  例："帮我分析这个项目的架构" → BROWNFIELD
    │  例："我要开发一个订单系统" → V → C → D¹ ...
    │
    ▼
[总控] 向用户确认步骤方案
    │  "我理解你需要的流程包括：① V ② C ③ D¹，是否开始？"
    │
    ▼
[总控] 逐步骤执行（或按用户确认的顺序）
    │
    ├── 读 steps/{STEP}/SKILL.md
    ├── 用 Agent(效率模型) 派遣子 Agent（将步骤文档 + 上下文文件作为指令传入）
    ├── 等待子 Agent 返回结果
    ├── 记录执行状态到 docs/vcddd/progress.log（格式见 steps/EVENT-LOG/SKILL.md）
    └── 根据步骤文档中的"完成后的控制器行为"判断下一步
```

### 总控的职能边界

| 职责 | 非职责 |
|------|--------|
| 分析用户需求，匹配到对应步骤 | ❌ 不读项目代码（代码占 Token，浪费昂贵模型上下文） |
| 用 Agent 工具为每个步骤派遣子 Agent | ❌ 不写项目代码 |
| 接收子 Agent 返回结果，记录到 progress.log | ❌ 不运行测试 |
| **读取文档**（business.md、boundary.md、tech-stack.md 等） | ❌ 不写实现文档（implementation.md、test-spec.md 由子 Agent 写） |
| **编写设计文档**（business.md、boundary.md、facts.md 等非实现部分） | |
| 将步骤文档 + 上下文文件组装为子 Agent 的 Prompt | |
| 根据步骤文档的调度循环判断下一步 | |
| 在 Review-DOMAIN 中协调 Implementer ↔ Reviewer 的修复循环 | |

**主控读写的范围**：
- ✅ **可读**：所有文档（.md 文件）、子 Agent 返回结果、日志
- ❌ **不可读**：项目源代码（.dart、.py、.ts 等实现文件）
- ✅ **可写**：设计阶段文档（facts.md、business.md、boundary.md、tech-stack.md、progress.log）
- ❌ **不可写**：代码、实现文档（implementation.md、test-spec.md 由子 Agent 写）

### 模型选择策略

子 Agent 的模型分配遵循 `reference/engine/model-selection.md` 的分层策略：
- 常规任务（Implementer、Reviewer、TDD Bridge）→ **效率模型**
- 升级排查（同一问题连续 2 轮未修复）→ **深度思考模型**

具体模型名称由环境识别决定（Claude 环境自动映射，其他环境询问用户），不猜测。

### 子 Agent 的派遣模式

每个步骤文档（`steps/{STEP}/SKILL.md`）设计为子 Agent 的完整指令。总控派遣时：

```
总控读取 steps/{STEP}/SKILL.md
  ↓
组装子 Agent 的 Prompt：
  "你是 {STEP} agent。请按以下步骤执行：
   {SKILL.md 全文}
   上下文：{该步骤需要的文件全文}"
  ↓
用 Agent(效率模型) 派遣子 Agent
  ↓
子 Agent 完成任务，返回结果
  ↓
总控记录到 docs/vcddd/progress.log：
  {步骤名} → {状态: DONE/DONE_WITH_CONCERNS/BLOCKED/FAILED}
  → {产出物路径}
  → {关键数据（文件数、测试数等）}
```

---

## 步骤总览

每个步骤有一个唯一的斜杠命令名。控制器在调度时**必须使用这些命令名**，不使用自然语言描述。

| 斜杠命令 | 步骤 | 做什么 | 步骤位置 |
|---------|------|-------|---------|
| `/vcddd-brownfield` | BROWNFIELD — 棕地初始化 | 分析已有代码生成认知文档 | `steps/BROWNFIELD/` |
| `/vcddd-vision` | V — 意图视野 | 捕捉用户意图写入 input.md | `steps/VISION/` |
| `/vcddd-context` | C — 事实上下文 | 澄清为 facts.md（逐条确认） | `steps/CONTEXT/` |
| `/vcddd-domain-design` | D¹ — 域设计 | 推导边界/不变式/事件/契约 | `steps/DOMAIN-DESIGN/` |
| `/vcddd-dev-setup` | D² — 技术栈确立 | 确定技术栈写入 tech-stack.md | `steps/DEVSETUP/` |
| `/vcddd-scaffold` | D²·⁵ — 骨架生成 | 生成项目骨架代码 | `steps/SCAFFOLD/` |
| `/vcddd-frontend-design` | D²·⁶ — 前端设计指导 | 生成前端指导文件并调用 google-design-md | `steps/FRONTEND-DESIGN/` |
| `/vcddd-tdd-bridge` | TDD 桥梁 | 从 business.md 推导黑盒测试 | `steps/TDD-BRIDGE/` |
| `/vcddd-implement-domain` | 域实现 | 一个 agent 完整实现一个域 | `steps/IMPLEMENT-DOMAIN/` |
| `/vcddd-review-domain` | 域审查 | 三层审查 + 测试运行 | `steps/REVIEW-DOMAIN/` |
| `/vcddd-integrate` | 跨域集成 | 验证跨域协作一致性 | `steps/INTEGRATE/` |
| `/vcddd-report` | 最终报告 | 汇总完成情况 | `steps/REPORT/` |

用户可直接调用任一步骤（例如"执行 /vcddd-brownfield"或"帮我做 /vcddd-domain-design"），不需要从 V 开始。

**控制器调度规则**：在自动化流程中，控制器必须使用斜杠命令名派遣子 Agent。例如：
- ✅ "invoke /vcddd-implement-domain，传入 business.md + boundary.md + test-spec.md"
- ❌ "派遣 Implementer 实现该域"

---

## 核心规则

### 人机分工

| 阶段 | 决策者 | AI 角色 |
|------|--------|---------|
| V → C → D¹ | 用户确认门禁 | 推导、结构化、呈现请用户确认 |
| D² 技术栈 | 用户确认 | 分析推荐，由用户选择 |
| D³ 实现 + 审查 | AI 对抗循环 | Implementer ↔ Reviewer 三层对抗 |
| 跨域集成 | AI + 用户 | 技术问题 AI 修，业务问题问用户 |

### 禁止性规则

- `facts.md` 未经用户确认 → 不进入域设计
- 域设计未经用户确认 → 不进入实现
- `tech-stack.md` 不存在 → 不写代码
- 项目包含用户界面且未完成 `/vcddd-frontend-design` → 不实现页面
- **infrastructure/ 目录禁止包含任何域的表定义、仓储实现或业务逻辑**（表定义属于 `server/{domain}/`）
- 前端页面实现必须引用 `docs/vcddd/frontend/` 与 `google-design-md` 输出，不允许脱离指导文件自由发挥
- 每域一个 agent 完整实现，不允许域内拆分
- 每个域必须通过三层审查（Spec → Quality → VCDDD）
- 对抗循环最多 10 轮，超 10 轮升级给用户
- 发现 `business.md` 内部矛盾 → 暂停，退回到需求线修正
- 全部域完成后 → 必须执行跨域集成验证

---

## 理论基座

本部分是整个 VCDDD 的思想地基。在执行任何业务分析或设计任务之前，必须先完整内化本部分。

详细内容见 `reference/theory/vcddd-methodology.md`。以下为核心要点摘要：

### 核心世界观

1. **业务真相先于一切技术结构** — 设计的起点是"系统承载的业务事实是什么"，不是"拆模块"或"建表"
2. **系统是决策与协作网络** — 限界上下文的意义在于语义主权，不在于代码包
3. **战术结构是手段，不是目的** — 仓储、工厂、DI 在特定场景下有用，但不等于 DDD

### 推理主轴

```
从"事实"切入
    → 识别出谁的事实、谁说了算
        → 边界是主权，不是代码归属
            → 跨边界时，过程和协作都必须显式化
                → 不确定性靠契约，不靠耦合
```

### 核心概念

| 概念 | 核心问题 |
|------|---------|
| 业务真相 | 系统对业务世界做出了哪些必须成立的承诺？ |
| 通用语言 | 这个边界内，所有人是否用同一套词描述同一件事？ |
| 限界上下文 | 通用语言在哪里生效？超出边界含义不同。 |
| 决策边界 | 对这类业务判断，谁有最终解释权？ |
| 聚合与不变式 | 哪些约束必须在一个原子边界内同时成立？ |
| 过程状态 | 这个业务过程在时间维度上，现在处于什么位置？ |
| 协作契约 | 跨边界协作时，双方的业务协议是什么？ |

---

## 自动化执行层

当 D¹（域设计）确认后，D²→D³ 阶段可自动化执行。

详细流程见 `reference/engine/automated-execution.md`。以下为核心要点：

1. **D²-auto**：确定技术栈，写入 tech-stack.md
2. **D²·⁵-auto（SCAFFOLD）**：生成项目骨架代码
3. **D²·⁶-auto（FRONTEND-DESIGN）**：如项目包含用户界面，生成前端指导文件并调用 google-design-md
4. **域依赖排序**：拓扑排序确定实现顺序
5. **逐域执行**：每域依次 TDD Bridge → Implementer → 三层审查
6. **跨域集成验证**：验证跨域契约一致

---

## 事件日志

每个域维护自己的进度日志 `docs/vcddd/design/{domain}/progress.log`，记录任务目标、执行计划和已完成操作。

日志用于 Agent 切换时的任务延续——新 Agent 通过阅读日志了解当前目标、已完成工作和下一步计划。

详见 `steps/EVENT-LOG/SKILL.md`。

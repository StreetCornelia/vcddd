# VCDDD

[English](./README.md)

VCDDD（Vibe Coding Domain-Driven Design）是一套面向 AI 辅助开发的软件设计 skill 与方法论，同时承载两层相互支撑的含义。

> **第一次用？** → [快速上手指南](./QUICKSTART.zh-CN.md) — 不需要了解 DDD，跟着步骤走就能用。

本仓库采用“单 skill 独立仓库”结构，仓库根目录就是 skill 根目录。

## 仓库包含内容

- `SKILL.md`：主入口 — 理论基座 + 总控 Agent + 步骤导航
- `steps/{STEP}/SKILL.md`：模块化子步骤，每步自洽，可独立派遣子 Agent
- `reference/theory/`：白皮书、方法论文档与实现映射指导
- `reference/guides/`：需求澄清与域设计工作流
- `reference/engine/`：执行引擎参考（编排、审查、TDD 桥梁等）
- `reference/templates/`：各阶段文档模板（input、facts、boundary、business 等）

## 目录结构

```text
vcddd/                     ← 仓库 / skill 根目录
├── SKILL.md               ← 主入口（理论 + 总控 + 导航）
├── steps/
│   ├── BROWNFIELD/        ← 分析已有代码生成认知文档
│   ├── VISION/            ← 捕捉用户意图
│   ├── CONTEXT/           ← 澄清为业务事实
│   ├── DOMAIN-DESIGN/     ← 推导域边界和不变式
│   ├── DEVSETUP/          ← 确定技术栈
│   ├── FRONTEND-DESIGN/   ← 生成前端指导文件并调用 google-design-md
│   ├── TDD-BRIDGE/        ← 推导黑盒测试规格（含 prompt 文件）
│   ├── IMPLEMENT-DOMAIN/  ← 代码 + 白盒测试 + 黑盒测试（含 prompt 文件）
│   ├── REVIEW-DOMAIN/     ← 三层对抗审查（含 prompt 文件）
│   ├── INTEGRATE/         ← 跨域集成验证
│   ├── REPORT/            ← 最终完成报告
│   └── EVENT-LOG/         ← 域级进度日志规范
└── reference/
    ├── theory/            ← 方法论、白皮书、设计指导、实现映射
    ├── guides/            ← 需求工作流、设计工作流
    ├── engine/            ← 编排引擎、审查循环、TDD 桥梁、技术栈探测等
    │   └── examples/      ← 全量代码示例（TS, Python, Java, Serverless）
    └── templates/         ← 各阶段文档模板
```

## VCDDD 的双层含义

```
┌─────────────────────────────────────────────────────┐
│              第二层：五步工作方法论                    │
│   V → C → D¹ → D² → D³                             │
│   Vision · Context · Domain · Dev Setup · Develop   │
│                                                      │
│   ┌─ 自动化执行层（D²→D³）────────────────────┐      │
│   │  SuperPower 引擎（优先）                    │      │
│   │  └─ TDD 桥梁 → 写计划 → subagent 派遣      │      │
│   │     → 两道审查 → 集成验证                   │      │
│   │                                              │      │
│   │  内置引擎（回退）                            │      │
│   │  └─ 手动 subagent 编排 + 审查              │      │
│   └──────────────────────────────────────────────┘      │
├─────────────────────────────────────────────────────┤
│              第一层：理论基座                          │
│   Vibe Coding × Domain-Driven Design                │
│   AI 时代对 DDD 本体的重新界定                        │
└─────────────────────────────────────────────────────┘
```

### 第一层：理论基座

VCDDD 不是「更轻的 DDD」，也不是「AI 版 DDD」，而是对 DDD 本体的重新界定。

AI 时代的基本前提已经改变：代码不再是最稀缺的资产，可以频繁重写。真正需要被优先保护的是：

- **业务真相** — 系统必须承诺的业务事实
- **语义边界** — 概念在哪里生效，在哪里失效
- **决策归属** — 谁对哪类判断有最终解释权
- **过程状态** — 业务过程在时间轴上的显式位置
- **协作契约** — 跨边界协作的稳定语义协议
- **验证屏障** — 防止实现偏离以上所有定义的机制

> 代码可以频繁变化，但系统对业务世界的表达不能漂移。

「Vibe Coding」承认 AI 生成代码的高度可变性，同时坚持业务模型必须保持稳定。两者不矛盾——正因为代码随时可以重写，业务真相才更需要被提前、独立地建立，并在全程得到保护。

### 第二层：五步工作方法论

| 步骤 | 全称 | 核心任务 | 关键产出 |
|---|---|---|---|
| **V** | Vision（意图视野） | 捕捉并结构化用户意图，不做分析 | `input.md` |
| **C** | Context（事实上下文） | 把意图澄清为逐条用户确认的业务事实 | `facts.md` + 通用语言词表 |
| **D¹** | Domain Design（域设计） | 唯一以 facts.md 为输入，推导域边界、决策归属、不变式、事件与契约 | 每个域的 `boundary.md` + `business.md` |
| **D²** | Dev Setup（开发基础） | 将技术选型写成有约束力的文档约定 | `tech-stack.md` |
| **D²·⁶** | Frontend Design（前端设计指导） | 用户界面项目中，把域文档转成前端指导文件并直接调用 `google-design-md` | `docs/vcddd/frontend/*` + google-design-md 输出 |
| **D³** | Develop（代码实现） | 在 D¹ 域设计和 D² 约定双重约束下生成工程代码 | 工程代码 + `implementation.md` |

每个步骤之间都有不可绕过的前置门禁，上一步产出未经确认，下一步不能开始。这不是仪式感，而是防止「在未经确认的业务假设上建出看似正确的代码」。

## 建议阅读顺序

### 基础阶段

1. `SKILL.md` — 执行规则、理论基座与自动化层说明
2. `reference/methodology/vcddd-methodology.md` — 五步方法论完整说明
3. `reference/thinking/requirements.md` — 如何执行 V 与 C
4. `reference/thinking/design.md` — 如何执行 D¹

### 棕地项目（已有代码但无 VCDDD 文档）

5. `reference/coding/brownfield-init.md` — 分析已有代码的入口、业务逻辑、数据流，生成大模型认知文档

### 执行阶段（D¹ 确认后选择路径）

**自动化路径（推荐）：**
5. `reference/coding/automated-execution.md` — 编排主文档（自动检测 SuperPower，委托或回退）
6. `reference/coding/tdd-bridge.md` — 从 business.md 机械推导测试用例
7. `reference/coding/subagent-orchestration.md` — 域→子任务拆分规则
8. `reference/coding/review-loop.md` — 两道审查 + 辩论循环核对清单
9. `reference/coding/integration-verification.md` — 跨域契约验证

**手动路径：**
5. `reference/coding/tech-setup.md` — 如何执行 D²
6. `reference/coding/implementation.md` — 如何执行 D³

### 理论主干（深入阅读）

- `reference/methodology/vcddd-whitepaper.md`
- `reference/methodology/vcddd-design-guide.md`
- `reference/methodology/vcddd-implementation.md`

## 使用方式

本仓库遵循通用的 `SKILL.md` 约定，适合被支持本地 skill 目录的 coding agent 直接消费。

建议把整个目录放到本地 skills 路径下，并保持根目录 `SKILL.md` 不变，例如：

```text
~/.claude/skills/vcddd/
```

适用场景包括：

- 把自然语言需求翻译成经确认的业务事实
- 从业务真相出发划定域边界
- 设计不变式、状态机、事件与协作契约
- 让实现持续服从业务模型，而不是反过来被代码带偏

### 可选：SuperPower 引擎

VCDDD 可以将 D²→D³ 执行委托给 SuperPower，实现自动化的 subagent 派遣、TDD 循环和代码审查。需要单独安装 SuperPower：

```bash
npm install -g @superpowers/skills
```

检测到 SuperPower 时，VCDDD 自动使用它作为执行引擎；不可用时自动回退到内置引擎。

## 工作流概览

### 第一阶段：人工确认业务真相（V → C → D¹）

这三个步骤始终需要用户在每个门禁确认。它们建立了后续所有工作依赖的业务真相。

1. **V — Vision**：忠实捕捉用户意图，不做拆解与分析。
2. **C — Context**：把意图澄清为逐条确认的业务事实、状态机与通用语言词表。
3. **D¹ — Domain Design**：仅以确认事实为输入，推导限界上下文、决策边界、关键不变式、事件与协作契约。

### 第二阶段：自动化执行（D² → D³）

D¹ 确认后，系统自动执行剩余步骤：

4. **D²-auto**：扫描项目配置文件识别技术栈（新项目调研可行方案）。仅对无法从代码推断的项向用户提问。
5. **前端设计指导（如适用）**：用户界面项目先生成 `docs/vcddd/frontend/`，并直接调用本地 `google-design-md` 产出页面设计/spec。
6. **TDD 桥梁**：从 business.md 机械推导测试规格——每条不变式、状态迁移、命令路径、失败分支映射到具体测试用例。
7. **任务拆分**：每个域拆分为 2-5 分钟的独立 subagent 任务，附带精确文件路径和测试 ID。
8. **Subagent 执行**：每个任务派遣独立 subagent 遵循 TDD（RED-GREEN-REFACTOR）实现。两道审查（Spec 合规 vs business.md，代码质量 vs tech-stack.md）把关每个任务。
9. **集成验证**：全部域完成后，验证跨域契约、端到端工作流、幂等和事件顺序。
10. **最终报告**：呈现域状态、测试数量和验证结果摘要。

### 用户看到的内容

自动化执行期间，用户只看到进度更新，仅在以下情况被中断：

- 技术栈有无法自动判定的歧义项
- business.md 内部规则矛盾
- Subagent 报告 BLOCKED 需要业务层面决策

## 许可证

本仓库使用 Creative Commons Attribution 4.0 International（`CC BY
4.0`）许可证。

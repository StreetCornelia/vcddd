# Fallback 执行层

SuperPower 未安装时的回退路径。本文件仅在 `automated-execution.md` 第零步检测到 SuperPower 不可用且用户选择跳过安装时加载。

**本文档的定位**：编排者的操作手册（后备）。不是给 subagent 读的。

---

## 入口

由 `reference/engine/automated-execution.md` 第零步在检测到 `VCDDD_EXEC_ENGINE=builtin` 后加载本文档。编排者读完本文档后，回到 `automated-execution.md` 的 D2-auto 继续执行。

---

## D3-auto 手动编排流程

D2-auto 完成后（即 `tech-stack.md` 就绪），执行以下手动编排流程。

### 流程

```
tech-stack.md 就绪
        │
        ▼
构建域依赖图 + 拓扑排序（依赖域先实现）
        │
        ▼
按拓扑顺序，逐域执行（使用斜杠命令派遣）：
        │
        ├── 域 A（无依赖）
        │    ├── invoke /vcddd-tdd-bridge → test-spec.md
        │    ├── invoke /vcddd-implement-domain → 全部代码 + 测试
        │    └── invoke /vcddd-review-domain → 三层审查
        │
        ├── 域 B（依赖 A）
        │    ├── ...（同上）
        │
        └── ...
        │
        ▼
invoke /vcddd-integrate → 跨域集成验证
        │
        ▼
invoke /vcddd-report → 最终报告
```

### 编排者调度循环（强制执行）

**以下调度循环是编排者的强制执行指令。每个步骤必须使用斜杠命令派遣，不使用自然语言描述。**

**所有调度由编排者（主 session）执行。** Implementer 只写代码和测试，不运行测试。Reviewer 运行测试和审查，不自己派遣 Implementer。

```
┌─ 循环开始 ─────────────────────────────────────────────┐
│                                                         │
│  1. invoke /vcddd-tdd-bridge                            │
│     → 传入：business.md + boundary.md                   │
│     → 返回 test-spec.md 后继续                           │
│                                                         │
│  2. 【立即】invoke /vcddd-implement-domain               │
│     → 传入：business.md + boundary.md + test-spec.md    │
│            + tech-stack.md + 依赖域 boundary.md 摘录     │
│     → 返回：状态 + 文件数 + 测试数 + Mock/Real 明细     │
│                                                         │
│  3. 返回后【立即】invoke /vcddd-review-domain            │
│     → 传入：business.md + boundary.md + tech-stack.md   │
│            + 全部代码 + 测试 + 测试运行命令              │
│     → Reviewer 运行测试 + 三层审查（Spec→Quality→VCDDD） │
│     → 返回：PASS / ISSUES / CONDITIONAL / 拒绝执行       │
│                                                         │
│  4. 返回 ISSUES 后【立即】：                              │
│     → invoke /vcddd-implement-domain，传入问题列表       │
│     → 返回后 invoke /vcddd-review-domain 重新审查        │
│     → 循环直到 PASS 或达到 10 轮上限                     │
│                                                         │
│  5. 返回 PASS 后：                                       │
│     → 标记该域完成，进入下一个域                          │
│                                                         │
│  6. 返回 拒绝执行 后：                                   │
│     → 控制器补跑前序测试，重新 invoke /vcddd-review-domain│
│                                                         │
└─ 循环结束（直到所有域完成）──────────────────────────────┘
```

**关键约束**：
- **测试由 Reviewer 运行**：Implementer 不运行测试，Reviewer 运行
- **所有调度由编排者执行**：Reviewer 不自己派遣 Implementer
- **必须使用斜杠命令**：每个步骤用 invoke /vcddd-xxx 派遣，不用自然语言
- **审查不可跳过**：Implementer 返回 DONE 不等于域完成，必须通过三道审查
- **审查不可并行**：Spec → Quality → VCDDD 必须串行
- **修复后必须重审**：Implementer 修复后，必须从 Spec Reviewer 重新开始
- **VCDDD Reviewer 有权拒绝**：前序未跑测试时拒绝执行
- **不需要用户提醒**：整个循环是自动的

### 编排者呈现给用户的进度

执行期间，编排者定期更新进度：

```
[D3-auto · 内置引擎] 3 个域

域 order (依赖: 无):
  ✅ 实现完成 + 审核通过
  （12 文件，32 测试通过）

域 payment (依赖: order):
  🔄 invoke /vcddd-implement-domain 执行中...

域 inventory (依赖: order):
  ⏳ 等待 order 域审核通过后派遣
```

---

## 相关文档

- `reference/engine/subagent-orchestration.md` — 域→子任务拆分规则与派遣模板
- `reference/engine/review-loop.md` — 两道审查核对清单与辩论循环规则
- `reference/engine/tdd-bridge.md` — 从 business.md 机械推导测试用例
- `reference/engine/integration-verification.md` — 跨域契约验证
- `reference/engine/automated-execution.md` — 入口判断、D2-auto、升级触发条件、最终报告格式

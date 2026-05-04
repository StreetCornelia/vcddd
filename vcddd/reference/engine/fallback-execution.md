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
加载 reference/engine/subagent-orchestration.md
        │
        ▼
Step 1: 构建域依赖图 + 拓扑排序（依赖域先实现）
        │
        ▼
Step 2: 按拓扑顺序，逐域执行：
        │
        ├── 域 A（无依赖）
        │    ├── a. TDD Bridge（Generator ↔ Reviewer 对抗）→ test-spec.md
        │    ├── b. Implementer → 完整实现域 A 全部代码 + 测试
        │    ├── c. Spec Reviewer → 运行测试 + 核对代码 vs business.md（最多 10 轮）
        │    ├── d. Quality Reviewer → 运行测试 + 核对代码 vs tech-stack.md（最多 10 轮）
        │    └── e. VCDDD Reviewer → 确认前序测试已运行 + 核对合规性（最多 10 轮）
        │
        ├── 域 B（依赖 A）
        │    ├── ...（同上）
        │
        └── ...
        │
        ▼
Step 3: 全部域完成，执行跨域集成验证
        加载 reference/engine/integration-verification.md
        │
        ▼
Step 4: 生成最终报告
```

### 编排者调度循环（强制执行）

**对每个域，按以下顺序严格执行。不需要用户提醒，每个步骤完成后立即进入下一步。**

**所有调度由编排者（主 session）执行。** Implementer 只写代码和测试，不运行测试。Reviewer 运行测试和审查，不自己派遣 Implementer。

```
┌─ 循环开始 ─────────────────────────────────────────────┐
│                                                         │
│  1. 派遣 TDD Bridge                                     │
│     → Generator 生成 test-spec.md                       │
│     → Reviewer 审查（Generator ↔ Reviewer 对抗）        │
│     → 返回 test-spec.md 后继续                           │
│                                                         │
│  2. 【立即】派遣 Implementer                             │
│     → 传入：business.md + boundary.md + test-spec.md    │
│            + tech-stack.md + 依赖域 boundary.md 摘录     │
│     → Implementer 完成全部代码 + 测试（不运行测试）       │
│     → 返回：状态 + 文件数 + 测试数 + 覆盖率             │
│                                                         │
│  3. Implementer 返回后【立即】派遣 Spec Reviewer          │
│     → 不等待用户确认，不跳过，不省略                      │
│     → Spec Reviewer 运行全部测试                         │
│     → 全部通过 → 核对代码 vs business.md（Stage 1）     │
│     → 有失败 → 返回 ISSUES（含失败信息）                │
│                                                         │
│  4. Spec Reviewer 返回 ISSUES（测试失败）后【立即】：     │
│     → 编排者派遣 Implementer，传入失败信息               │
│     → Implementer 修复后返回                             │
│     → 编排者重新派遣 Spec Reviewer                       │
│     → 循环直到全部测试通过 + Spec Compliance 通过        │
│                                                         │
│  5. Spec Reviewer 返回 PASS 后【立即】派遣 Quality Reviewer│
│     → Quality Reviewer 运行全部测试（确认仍然通过）       │
│     → 核对代码 vs tech-stack.md（Stage 2）               │
│     → 返回：PASS / ISSUES                               │
│                                                         │
│  6. Quality Reviewer 返回 ISSUES 后【立即】：             │
│     → 编排者派遣 Implementer，传入问题列表               │
│     → Implementer 修复后返回                             │
│     → 编排者重新派遣 Spec Reviewer（重跑测试+审查）       │
│     → 编排者重新派遣 Quality Reviewer（重跑测试+审查）    │
│     → 循环直到 PASS 或达到 10 轮上限                     │
│                                                         │
│  7. Quality Reviewer 返回 PASS 后【立即】派遣 VCDDD Reviewer│
│     → VCDDD Reviewer 确认 Stage 1 已运行全部测试        │
│     → 如果未运行 → 拒绝执行，返回编排者："必须先补跑测试"│
│     → 编排者补跑后重新派遣 VCDDD Reviewer                │
│     → 如果已运行 → 核对 VCDDD 合规性（Stage 3）         │
│     → 返回：PASS / ISSUES / CONDITIONAL                 │
│                                                         │
│  8. VCDDD Reviewer 返回后：                              │
│     → PASS → 标记该域完成，进入下一个域                   │
│     → ISSUES → 编排者派遣 Implementer 修复，从 Step 3 重审│
│     → CONDITIONAL → 标记 DONE_WITH_CONCERNS，进入下一域   │
│     → 拒绝执行 → 编排者补跑前序测试                      │
│                                                         │
│  9. 该域三道审查全部通过后【立即】进入下一个域             │
│     → 不等待用户确认，不暂停，直接取拓扑排序中的下一域     │
│                                                         │
└─ 循环结束（直到所有域完成）──────────────────────────────┘
```

**关键约束**：
- **测试由 Reviewer 运行**：Implementer 不运行测试，Reviewer 运行
- **所有调度由编排者执行**：Reviewer 不自己派遣 Implementer
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
  🔄 Implementer 实现中...

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

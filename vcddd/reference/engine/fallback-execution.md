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
        │    ├── a. TDD Bridge → test-spec.md（Generator ↔ Spec Reviewer 对抗）
        │    ├── b. Implementer → 完整实现域 A 全部代码（TDD 循环）
        │    ├── c. Spec Reviewer → 核对代码 vs business.md（最多 10 轮）
        │    ├── d. Quality Reviewer → 核对代码 vs tech-stack.md（最多 10 轮）
        │    └── e. VCDDD Reviewer → 核对 VCDDD 合规性（最多 10 轮）
        │
        ├── 域 B（依赖 A）
        │    ├── a. TDD Bridge → test-spec.md
        │    ├── b. Implementer → 完整实现域 B 全部代码
        │    ├── c. Spec Reviewer → 核对代码 vs business.md
        │    ├── d. Quality Reviewer → 核对代码 vs tech-stack.md
        │    └── e. VCDDD Reviewer → 核对 VCDDD 合规性
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

### 编排者在每个域派遣时做的事

1. 按拓扑排序取出下一个域
2. 附上该域的全部上下文文件（business.md, boundary.md, test-spec.md, tech-stack.md）
3. 派遣 Implementer subagent，要求完整实现该域全部代码
4. 等待返回，处理状态（DONE/DONE_WITH_CONCERNS/BLOCKED）
5. 完成后派遣 Reviewer，审查全部代码
6. 处理审查结果 → 进入下一域或触发修复循环

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

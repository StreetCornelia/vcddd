# Subagent 编排：一域一 agent + 对抗审核

每个域是一个完整的业务内聚单元，由一对 agent 完成：
1. **Implementer agent**：负责该域的全部代码实现
2. **Reviewer agent**：负责该域的完整审核

**域不允许再拆分**。一个域的所有代码（聚合、命令、事件、仓储、事件消费、读模型）由同一个 Implementer agent 一次性完成。

---

## 编排流程

```
D1 已确认的全部域文档
        │
        ▼
  Step 1: 构建域依赖图 + 拓扑排序（先排顺序，再逐域执行）
        │
        ▼
  Step 2: 按拓扑顺序，逐域执行（使用斜杠命令派遣）：
        │
        ├── 域 A（无依赖）
        │    ├── invoke /vcddd-tdd-bridge → test-spec.md
        │    ├── invoke /vcddd-implement-domain → 全部代码 + 测试
        │    └── invoke /vcddd-review-domain → 三层审查
        │
        ├── 域 B（依赖 A）
        │    ├── invoke /vcddd-tdd-bridge → test-spec.md
        │    ├── invoke /vcddd-implement-domain → 全部代码 + 测试
        │    └── invoke /vcddd-review-domain → 三层审查
        │
        └── ...
        │
        ▼
  Step 3: invoke /vcddd-integrate → 跨域集成验证
```

---

## Step 1：构建域依赖图

从 `facts.md` 协作矩阵和 `boundary.md` 事件/命令契约中提取依赖关系：

```
对每对域 (A, B)：
  A 消费了 B 的事件？
    → A 依赖 B（B 必须先实现，A 需要 B 的事件结构和契约定义）
  A 向 B 发送命令？
    → A 依赖 B（B 的 command handler 必须先就绪）
  A 和 B 互不依赖？
    → 可并行实现
```

---

## Step 2：拓扑排序

```
依赖域（被消费者）先于消费域实现。

例：
  order 域不依赖其他域 → 第一个实现
  payment 域依赖 order（消费 OrderPlaced）→ order 完成后实现
  inventory 域依赖 order（消费 OrderPlaced）→ order 完成后实现
  notification 域依赖 order 和 payment → 两者都完成后实现
```

---

## Step 3：逐域派遣 Implementer + Reviewer

### 总体流程

```
按拓扑顺序选择下一个域 D
        │
        ▼
  invoke /vcddd-tdd-bridge → test-spec.md
        │
        ▼
  invoke /vcddd-implement-domain → 全部代码 + 测试
        │
        ▼
  invoke /vcddd-review-domain → 三层审查（Spec→Quality→VCDDD）
        │
    ┌───┴───┐
    │ 通过？  │
    └───┬───┘
   否   │  是
    ▼   │   ▼
  invoke    域 D 完成
  /vcddd-   进入下一域
  implement-domain
  修复问题
  → 重新
  invoke
  /vcddd-
  review-
  domain
```

### Implementer 的完整上下文

Implementer 接收该域的**全部信息**，一次性完成所有实现：

```
## 任务
你是 {domain} 域的开发者。请完整实现该域的全部代码。

## 域业务设计
{domain}/business.md（全文）
——包含：核心概念、不变式、状态机、命令路径（正常+全部失败分支）、跨域协作

## 域边界设计
{domain}/boundary.md（全文）
——包含：对外暴露的命令、事件、读模型、决策主权

## 测试规格
{domain}/test-spec.md（全文）
——包含：全部 AGG/INV/SM/CMD/EVT/CT 测试用例

## 技术约定
tech-stack.md（全文）

## 调用方/被调用方依赖
{域依赖的边界：
  - 本域消费的事件结构定义（来自被依赖域的 boundary.md 摘录）
  - 本域发送到的命令结构定义（来自目标域的 boundary.md 摘录）
  - 被依赖域的代码路径（如果有已实现的代码）}

## 要求
1. 实现该域的全部代码：聚合、命令处理、事件、仓储、事件消费、读模型
2. 使用 TDD：先写测试，确认失败，再写最小代码通过
3. 测试覆盖 test-spec.md 中的全部测试 ID
4. 实现完成后自审：对照 business.md 核对是否遗漏任何路径
5. 报告你的完成状态：DONE / DONE_WITH_CONCERNS / BLOCKED
```

### 三层审查上下文

每个域通过三层审查，每层由独立 Reviewer 执行。上下文精确裁剪——只给该 Reviewer 需要的文档。

**Spec Reviewer 上下文：**

```
## 审查任务
审查 {domain} 域的 Spec Compliance。

## 域业务设计
{domain}/business.md（全文）

## 实现代码
{Implementer 产出的全部代码文件}

## 审查要求
- 逐条核对 business.md：全部不变式有强制代码、全部状态迁移已实现、
  全部命令路径已实现（正常+全部失败分支）、全部事件已正确定义和发布、幂等策略已实现
- 核对 boundary.md：命令/事件结构定义一致
- 详见 reference/engine/review-loop.md Stage 1 核对清单
- 一次性给出全部问题，不允许分批抛出
```

**Quality Reviewer 上下文：**

```
## 审查任务
审查 {domain} 域的 Code Quality。

## 技术约定
tech-stack.md（全文）

## 实现代码
{Implementer 产出的全部代码文件}

## 审查要求
- 逐条核对 tech-stack.md：命名、目录、依赖、日志、错误处理、事务边界、测试约定
- 详见 reference/engine/review-loop.md Stage 2 核对清单
- 一次性给出全部问题，不允许分批抛出
```

**VCDDD Reviewer 上下文：**

```
## 审查任务
审查 {domain} 域的 VCDDD 合规性。

## 域业务设计
{domain}/business.md（全文）
{domain}/boundary.md（全文）

## 技术约定
tech-stack.md（全文）

## 实现代码
{Implementer 产出的全部代码文件}
{Spec Reviewer 的审查结果}
{Quality Reviewer 的审查结果}

## 审查要求
1. VCDDD 定义准确性
   - 域边界被正确遵守（代码没有越过 boundary.md 定义的边界）
   - 通用语言一致（代码命名与 business.md 的词汇一致）
   - 决策主权未被侵犯（没有其他域的代码做了本域的决策）
   - Spec Reviewer 发现但未解决的问题是否合理

2. 技术栈规则遵守
   - 域层与框架层分离（server/ 中无框架 import，框架层中无业务逻辑）
   - 每个域模块完整（含自己的数据访问实现，无全局 infra/ 目录）
   - 日志规范遵守（必填字段、关键位置日志覆盖）

3. VCDDD 专项要求
   - 事务边界与聚合边界对齐（一个事务不修改多个聚合）
   - 状态迁移通过聚合方法执行（无直接字段赋值）
   - 事件在事务提交后发布
   - 跨域协作通过事件机制（非直接耦合）
   - 代码与文档的偏差：新发现与 business.md 的矛盾标记为 [待确认]

## 判定
✅ VCDDD 合规 — 该域实现通过
❌ 不合规 — 列出具体问题，返回修复
⚠️ 有条件合规 — 标记 DONE_WITH_CONCERNS，在最终报告中列出
```

### 并行策略

```
不依赖其他域的域 → 可并行派遣 Implementer
  例：order 和 user 域互不依赖 → 同时实现

存在依赖关系的域 → 严格顺序执行
  例：payment 依赖 order → order 完成且审核通过后，再开始 payment

不同域的 Implementer 和 Reviewer 可并行：
  域 A 的 Reviewer 审查时，域 B 的 Implementer 可以同时开始
  （前提是域 B 不依赖域 A）
```

---

## Step 4：编排进度追踪

```
域 order（依赖：无）
  [  ] 等待派遣
  [✅] Implementer 实现完成（12 文件，32 测试通过）
  [  ] Reviewer 审查中...

域 payment（依赖：order）
  [  ] 等待 order 域审核通过后派遣

域 inventory（依赖：order）
  [  ] 等待 order 域审核通过后派遣
```

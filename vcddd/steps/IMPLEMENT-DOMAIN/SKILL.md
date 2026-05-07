---
name: vcddd-implement-domain
description: VCDDD — 一个 Agent 完成域代码 + 测试编写
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。
> ⚠️ **控制器**：用 Agent(效率模型) 派遣子 Agent。你不修改代码、不读代码、不运行测试、不跳过审查。

# Step: IMPLEMENT-DOMAIN — 域代码实现

一个域的所有代码和测试由同一个 Agent 一次性完成。**Implementer 只负责写代码和测试，不负责运行测试。** 测试由 Reviewer 运行。

## 前置条件

- 该域 `business.md`、`boundary.md`、`test-spec.md` 就绪
- `tech-stack.md` 已存在
- 被依赖域已实现完成

## 输入

- 该域 `business.md`、`boundary.md`、`test-spec.md`（全文）
- `tech-stack.md`（全文）
- 被依赖域 `boundary.md` 摘录

## 输出

```
server/{domain}/
├── aggregate.{ext}
├── commands.{ext}
├── events.{ext}
├── repository.{ext}
├── {db}.repository.{ext}
├── read_model.{ext}
├── event_consumers.{ext}
├── __tests__/unit/          ← 白盒测试（内部分支 + 边界）
└── __tests__/blackbox/      ← 黑盒测试（命令级验证）
```

## 执行流程

### Phase 1：实现领域代码

先写全部领域实现代码：
1. 聚合根 + 不变式 + 状态机
2. 命令定义 + 处理逻辑
3. 事件定义
4. 仓储接口 + 数据库仓储实现
5. 读模型查询接口
6. 事件消费逻辑

### Phase 2：编写测试

基于 test-spec.md 编写测试：
1. **黑盒测试**：逐条核对 test-spec.md，为每个测试 ID 编写测试函数（函数名包含 ID）
2. **白盒测试**：覆盖分支 + 数据边界 + 异常路径
3. **测试类型标注**：每个测试必须标注 `[MOCK]` 或 `[REAL]`
4. **环境管理**：真实测试必须包含 setup（创建资源）+ teardown（恢复环境）
5. **覆盖率自检**：逐条核对 test-spec.md，确认每个 ID 都有对应测试。有遗漏 → 立即补充

### Phase 3：自审

对照 business.md 核对是否遗漏任何路径，检查命名是否与通用语言一致。检查 Mock 残留：有 Mock → 不允许完成。

## 完成要求

1. 全部领域代码已实现
2. 全部测试已编写（基于 test-spec.md，每个 ID 有对应测试）
3. **所有测试标注 `[REAL]`**（有 `[MOCK]` 残留 → 状态必须为 DONE_WITH_CONCERNS）
4. 真实测试包含环境 setup + teardown（测试后恢复原状）
5. 覆盖率自检通过
6. 在 progress.log 中记录操作
7. **报告状态**（必须包含以下信息）：

```
状态：DONE / DONE_WITH_CONCERNS / BLOCKED
文件数：N 个文件
test-spec 覆盖率：N/M 个 ID 已覆盖

测试明细：
  白盒：N 个（全部 [REAL]？是/否）
  黑盒：N 个（全部 [REAL]？是/否）

Mock 残留清单（必须为空才能 DONE）：
  [MOCK] test_xxx — 未替换为真实测试
  ...

环境管理：
  数据库：创建方式 + teardown 方式
  文件系统：创建方式 + teardown 方式
```

## 完成后的控制器行为

Implementer 返回状态后，控制器必须按以下规则继续：

| Implementer 返回 | 控制器下一步 |
|-----------------|-------------|
| DONE | **立即** invoke /vcddd-review-domain（三道审查循环） |
| DONE_WITH_CONCERNS | **立即** invoke /vcddd-review-domain（审查中会处理 CONCERNS） |
| BLOCKED | 暂停自动化，向用户呈现场景和阻塞原因 |

**控制器不得在 Implementer 返回 DONE 后暂停或等待用户确认——必须自动进入审查流程。**

完整 Prompt 见 `implementer-prompt.md`。

## 如果卡住

读 `../../reference/engine/implementation.md` 获取强制规范。

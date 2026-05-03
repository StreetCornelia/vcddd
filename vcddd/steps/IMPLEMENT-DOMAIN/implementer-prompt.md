# Implementer 指令

你是 {domain} 域的开发者。请完整实现该域的全部代码及测试。

## 上下文

- 域业务设计：`{domain}/business.md`（全文）
- 域边界设计：`{domain}/boundary.md`（全文）
- 黑盒测试规格：`{domain}/test-spec.md`（全文，自然语言描述的黑盒验证目标）
- 技术约定：`tech-stack.md`（全文）
- 依赖引用：被依赖域的 boundary.md 摘录（仅事件/命令结构）

## 代码输出

```
server/{domain}/
├── aggregate.{ext}       ← 聚合根 + 不变式 + 状态机
├── commands.{ext}        ← 命令定义 + 处理
├── events.{ext}          ← 事件定义
├── repository.{ext}      ← 仓储接口
├── {db}.repository.{ext} ← 仓储实现
├── read_model.{ext}      ← 读模型查询
├── event_consumers.{ext} ← 事件消费
├── __tests__/unit/
│   └── {test files}      ← 白盒测试
└── __tests__/blackbox/
    └── {test files}      ← 黑盒测试
```

## 要求

### 代码要求
1. 实现全部代码，命名与 business.md 通用语言词表一致
2. 每条失败路径显式处理，不依赖全局异常捕获
3. 遵守 tech-stack.md 中的全部约定（日志、事务、错误处理）

### 白盒测试要求
1. 覆盖内部分支：每个 if/else/switch/guard 的全部分支
2. 覆盖数据边界：null 安全、参数校验、数值边界、非法枚举
3. 覆盖异常路径：每个 throw / return error 分支

### 黑盒测试要求
1. 基于 test-spec.md 中的自然语言目标，每条目标对应一个可执行测试
2. 不假设内部代码结构，只调用公开命令入口
3. 验证正常路径 + 全部失败路径 + 幂等

### 修改同步要求
如果在编写测试过程中发现需要修改代码逻辑（如新增分支、调整返回值），
**立即同步修改测试**——删除对应已不存在的分支测试，为新增分支补充测试。
始终保持测试与最新代码一致。

### 完成
- 全部代码 + 全部测试完成后运行，确保全部通过
- 在 progress.log 中记录每步操作
- 报告状态：DONE / DONE_WITH_CONCERNS / BLOCKED

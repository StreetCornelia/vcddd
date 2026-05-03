---
name: vcddd-brownfield
description: VCDDD — 棕地初始化：分析已有代码生成认知文档
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。

# Step: BROWNFIELD — 棕地项目初始化

分析已有代码的入口、业务逻辑、数据流，生成供大模型参考的架构认知文档。

## 前置条件

- 项目目录（包含源代码）
- 无其他前置条件（这是棕地项目的入口步骤）

## 输出

```
docs/vcddd/brownfield/
├── tech.md          ← 技术栈与配置
├── structure.md     ← 目录结构与职责
├── endpoints.md     ← 入口点清单
├── data-flows.md    ← 关键业务数据流
└── modules/
    └── {module}.md  ← 每个模块分析
```

## 执行流程

### Step 1: 项目级扫描

扫描配置文件获取技术栈，记录目录结构和入口点清单。输出 tech.md、structure.md、endpoints.md。

### Step 2: 模块级分析

按代码实际组织方式识别模块，对每个模块分析：位置、业务职责、入口点、核心逻辑、关键数据结构、依赖关系、注意事项。输出 modules/{module}.md。

### Step 3: 梳理关键数据流

从入口点到多个模块的调用链，梳理完整业务数据流。输出 data-flows.md。

## 如果卡住

读 `../../reference/engine/brownfield-init.md` 获取完整指南。

## 日志

在 `docs/vcddd/progress.log` 追加 Task 节点。记录每步分析操作（扫描/模块分析/数据流梳理）。

## 验证

- [ ] 所有入口点精确到文件名和函数名
- [ ] 所有模块的业务职责有概括
- [ ] 依赖关系标注了方向
- [ ] 不可靠的业务推断标注了 `[推测]`
- [ ] 不修改原有代码

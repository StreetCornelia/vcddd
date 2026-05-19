---
name: vcddd-frontend-design
description: VCDDD — 前端设计指导文件生成，并直接引用本地 google-design-md skill 产出页面设计/spec
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。
> ⚠️ **控制器**：用 Agent 工具派遣子 Agent 执行本步骤。你不直接实现页面代码，不跳过 google-design-md。

# Step: FRONTEND-DESIGN — 前端设计指导

本步骤把 VCDDD 的业务域文档转换成前端页面设计指导文件，并直接引用本地 `google-design-md` skill 生成后续页面实现需要参考的设计页面/spec。

## 核心定位

VCDDD 不吸收 `google-design-md` 的方法论，不复制它的规则。

VCDDD 只负责说明：

- 页面为什么存在
- 用户要在页面上产生什么业务数据
- 哪些输入成本必须被降低
- 哪些业务判断不能进入前端
- 页面实现必须遵守哪些业务边界、交互目标和视觉约束

`google-design-md` 负责把这些指导文件转成可执行的 UI/spec/contract，并指导具体框架实现。

## 前置条件

- `docs/vcddd/tech-stack.md` 已确认
- 相关域的 `docs/vcddd/design/{domain}/boundary.md` 已确认
- 相关域的 `docs/vcddd/design/{domain}/business.md` 已确认
- 本地已安装 `google-design-md` skill

## 输入

- `docs/vcddd/tech-stack.md`
- `docs/vcddd/design/{domain}/boundary.md`
- `docs/vcddd/design/{domain}/business.md`
- 已有的 `docs/vcddd/frontend/` 文档（如为增量页面设计）

## 输出

写入或更新：

```text
docs/vcddd/frontend/
├── app-architecture.md
├── visual-system.md
├── interaction-model.md
└── pages/
    └── {page}.md
```

并通过 `google-design-md` 生成或更新该页面后续实现所需的设计页面/spec。其输出路径由 `google-design-md` 的执行结果决定，但必须在 `{page}.md` 中记录引用位置。

## 执行流程

### 第一步：确认 google-design-md 可用

读取本地 skill 入口：

```text
/Users/dash/.cc-switch/skills/google-design-md/SKILL.md
```

如果该文件不存在，暂停并报告：

```text
BLOCKED: google-design-md skill 未安装，无法进入前端设计转实现阶段。
```

不要把 `google-design-md` 的子 skill 内容复制进 VCDDD。

### 第二步：建立前端输入全景

读取相关域的 `boundary.md` 与 `business.md`，整理：

- 页面会读取哪些读模型
- 页面会触发哪些命令
- 命令需要哪些入参
- 哪些入参来自用户显式输入
- 哪些入参可以来自上下文、默认值、历史记录、推荐、模板、扫描或批量选择
- 哪些业务判断必须留在 `server/{domain}/`

### 第三步：生成或更新全局前端指导文件

如果文件不存在，按模板创建：

- `reference/templates/frontend/app-architecture.md`
- `reference/templates/frontend/visual-system.md`
- `reference/templates/frontend/interaction-model.md`

如果文件已存在，只做增量更新，不覆盖无关页面或既有约定。

### 第四步：生成页面指导文件

对每个页面写入：

```text
docs/vcddd/frontend/pages/{page}.md
```

页面文件必须回答：

- 页面目标：用户在这里要完成什么
- 数据产生：页面帮助用户产生哪些业务数据
- 输入降本：哪些字段不能要求用户逐项手填，系统如何推断或辅助
- 读模型绑定：页面展示哪些读模型
- 命令触发：页面最终触发哪些命令
- 交互状态：loading / empty / error / draft / confirming / success 如何出现和恢复
- 业务边界：哪些判断不能在前端完成
- 视觉要求：页面密度、分区、主次操作、反馈形式

### 第五步：调用 google-design-md

页面指导文件经用户确认后，调用本地 `google-design-md` skill。

传入上下文必须包含：

- `docs/vcddd/tech-stack.md`
- `docs/vcddd/frontend/app-architecture.md`
- `docs/vcddd/frontend/visual-system.md`
- `docs/vcddd/frontend/interaction-model.md`
- `docs/vcddd/frontend/pages/{page}.md`
- 相关域的 `boundary.md` / `business.md`

调用目标不是“重新解释业务”，而是生成该页面后续实现需要参考的设计页面/spec/contract。

完成后，把 `google-design-md` 的输出位置记录回 `{page}.md` 的“Google Design.md 输出”小节。

### 第六步：记录操作

在 `docs/vcddd/progress.log` 中记录：

- 生成/更新了哪些前端指导文件
- 哪些页面调用了 `google-design-md`
- `google-design-md` 输出位置
- 是否仍有需要用户确认的交互或视觉问题

## 强制边界

- 前端可以设计用户意图如何低成本产生业务数据
- 前端不能替代后端做最终业务判断
- 前端可以做展示状态、草稿状态、交互状态
- 前端不能维护业务状态机或保护业务不变式
- 前端页面实现必须引用本步骤产物和 `google-design-md` 输出，不允许脱离指导文件自由发挥

## 完成要求

- [ ] `app-architecture.md` 已存在并覆盖当前技术栈
- [ ] `visual-system.md` 已存在并覆盖页面风格约束
- [ ] `interaction-model.md` 已存在并说明数据产生方式
- [ ] 每个目标页面都有 `pages/{page}.md`
- [ ] 每个页面都记录了 `google-design-md` 输出位置
- [ ] `progress.log` 已更新

## 如果卡住

- 如果页面目标不清楚 → 回到用户意图，澄清该页面让用户产生什么业务数据
- 如果命令入参不清楚 → 回到对应域的 `boundary.md`
- 如果前端想做业务判断 → 回到对应域的 `business.md`，确认该判断的主权归属
- 如果 `google-design-md` 输出与 VCDDD 业务边界冲突 → 以 VCDDD 域文档为准，重新调用 `google-design-md`

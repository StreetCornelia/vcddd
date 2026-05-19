---
name: vcddd-frontend-design
description: VCDDD — 前端设计规范生成，必须使用本地 google-design-md skill 完成统一页面风格规范
---

> 子 Agent 指令：本文件为子 Agent 的完整执行指令，由总控 Agent 传入并派遣执行。
> ⚠️ **控制器**：用 Agent 工具派遣子 Agent 执行本步骤。你不直接实现页面代码，不跳过 google-design-md。

# Step: FRONTEND-DESIGN — 前端设计指导

本步骤把 VCDDD 的业务域文档转换成项目级前端设计规范，并必须使用本地 `google-design-md` skill 完成或校准统一页面风格规范。后续所有页面设计与实现都必须引用这些规范。

## 核心定位

VCDDD 不吸收 `google-design-md` 的方法论，不复制它的规则；但前端设计规范必须通过 `google-design-md` 完成或校准。

VCDDD 负责提供业务与交互输入：

- 页面为什么存在
- 用户要在页面上产生什么业务数据
- 哪些输入成本必须被降低
- 哪些业务判断不能进入前端
- 页面实现必须遵守哪些业务边界、交互目标和视觉约束

`google-design-md` 负责基于这些输入完成项目级设计规范，保证页面风格、视觉分隔、组件使用和交互表达有统一依据。

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

其中 `visual-system.md` 必须通过 `google-design-md` 完成或校准。页面文件必须引用项目级设计规范，不允许每个页面自行发明风格。

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

不要把 `google-design-md` 的子 skill 内容复制进 VCDDD，但必须按它的设计原则完成本项目的设计规范。

### 第二步：建立前端输入全景

读取相关域的 `boundary.md` 与 `business.md`，整理：

- 页面会读取哪些读模型
- 页面会触发哪些命令
- 命令需要哪些入参
- 哪些入参来自用户显式输入
- 哪些入参可以来自上下文、默认值、历史记录、推荐、模板、扫描或批量选择
- 哪些业务判断必须留在 `server/{domain}/`

### 第三步：使用 google-design-md 完成项目级设计规范

读取本地 `google-design-md` skill，并把以下上下文交给它作为设计规范输入：

- `docs/vcddd/tech-stack.md`
- 相关域的 `boundary.md` / `business.md`
- 当前产品类型与页面类型
- 用户输入降本目标
- 已有品牌、组件库或视觉约束（如有）

目标不是让 `google-design-md` 替代业务设计，也不是让它直接实现页面，而是让它帮助完成：

- 页面整体风格原则
- 视觉分隔与信息层级
- 组件使用规则
- 页面密度与操作层级
- 状态表达规则
- 交互反馈原则

这些结果必须写入或更新 `docs/vcddd/frontend/visual-system.md`。

### 第四步：生成或更新全局前端指导文件

如果文件不存在，按模板创建：

- `reference/templates/frontend/app-architecture.md`
- `reference/templates/frontend/visual-system.md`
- `reference/templates/frontend/interaction-model.md`

如果文件已存在，只做增量更新，不覆盖无关页面或既有约定。

`visual-system.md` 是所有页面风格的统一来源，必须明确标注它已由 `google-design-md` 完成或校准。

### 第五步：生成页面指导文件

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

### 第六步：记录 google-design-md 规范来源

每个页面文件必须记录它引用的项目级设计规范：

- `docs/vcddd/frontend/visual-system.md`
- `docs/vcddd/frontend/interaction-model.md`
- `docs/vcddd/frontend/app-architecture.md`

页面实现阶段引用的是这些设计规范，而不是重新调用 `google-design-md` 自由生成另一套页面风格。

### 第七步：记录操作

在 `docs/vcddd/progress.log` 中记录：

- 生成/更新了哪些前端指导文件
- `google-design-md` 如何参与了项目级设计规范
- 哪些页面引用了该设计规范
- 是否仍有需要用户确认的交互或视觉问题

## 强制边界

- 前端可以设计用户意图如何低成本产生业务数据
- 前端不能替代后端做最终业务判断
- 前端可以做展示状态、草稿状态、交互状态
- 前端不能维护业务状态机或保护业务不变式
- 前端页面实现必须引用本步骤产物和经 `google-design-md` 完成/校准的设计规范，不允许脱离指导文件自由发挥

## 完成要求

- [ ] `app-architecture.md` 已存在并覆盖当前技术栈
- [ ] `visual-system.md` 已存在，并明确由 `google-design-md` 完成或校准
- [ ] `interaction-model.md` 已存在并说明数据产生方式
- [ ] 每个目标页面都有 `pages/{page}.md`
- [ ] 每个页面都记录了引用的项目级设计规范
- [ ] `progress.log` 已更新

## 如果卡住

- 如果页面目标不清楚 → 回到用户意图，澄清该页面让用户产生什么业务数据
- 如果命令入参不清楚 → 回到对应域的 `boundary.md`
- 如果前端想做业务判断 → 回到对应域的 `business.md`，确认该判断的主权归属
- 如果 `google-design-md` 给出的设计原则与 VCDDD 业务边界冲突 → 以 VCDDD 域文档为准，重新校准设计规范

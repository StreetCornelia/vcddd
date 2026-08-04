---
vcddd_type: "shared-instructions"
vcddd_version: "2.0"
topic: "obsidian-documents"
status: "active"
---

# Obsidian 文档说明

**适用身份：** 所有会创建或更新 VCDDD 笔记的 Agent。

## 事实与过程

VCDDD 项目文档统一放在项目根目录的 `vcddd-obsidian/`。其中有两类内容：

- **正式事实**：业务、Domain、系统、模块、API、数据库和 Coding 结果。它们按四个阶段放在固定位置，进入 Git，是后续工作的权威来源。
- **工作过程**：当前工作、Agent 执行记录、临时材料和临时投影。它们只放在 `work/`，不进入 Git。

正式事实不得依赖本地工作过程才能被理解。工作过程可以链接正式事实；正式事实不链接 `work/`、`work_id`、Agent 对话或执行记录。正式事实的版本变化由 Git 历史追踪。

## Vault 布局

```text
项目根目录/
└── vcddd-obsidian/
    ├── .gitignore
    ├── VCDDD.md
    ├── 01-business-discovery/
    │   └── <goal-id>/
    │       ├── 业务挖掘.md
    │       └── 候选场景池.md
    ├── 02-business-establishment/
    │   ├── business/
    │   │   └── <goal-id>/
    │   │       ├── 业务确立.md
    │   │       ├── 业务定义.md
    │   │       ├── 业务线/
    │   │       ├── 领域地图.md
    │   │       ├── 业务组合.md
    │   │       └── 证据/
    │   └── domains/
    │       └── <domain-id>/
    │           └── Domain.md
    ├── 03-pre-coding/
    │   ├── 系统与模块设计.md
    │   ├── 语言检查/
    │   └── systems/
    │       └── <system-id>/
    │           ├── API 与 Domain 编排.md
    │           ├── 数据库设计.md
    │           └── 语言检查/
    ├── 04-coding/
    │   └── systems/
    │       └── <system-id>/
    └── work/
        ├── 当前工作.md
        └── <work-id>/
            ├── 主控状态.md
            ├── 执行记录/
            ├── 临时材料/
            └── 临时投影/
```

`VCDDD.md` 是正式知识入口，只导航长期事实。`work/当前工作.md` 是本地工作入口，只恢复当前任务、Agent 和执行记录。Coding 的正式文档类型仍待共同设计；在此之前只保留 `04-coding/systems/<system-id>/` 的稳定归属，不套用旧版模板。

## 模板就是目标结构

完整模板固定在 `assets/templates/vcddd-obsidian/`。模板根目录内部的相对路径与项目中的 `vcddd-obsidian/` 完全一致；模板文件已经使用正式文件名，并包含完整 Properties、正文标题、表格、图和填写位置。

使用模板时：

1. 先查看当前阶段对应的模板子树，确认本对象需要的目录和文件。
2. 将相关模板文件复制到项目中的同一相对路径。
3. 只替换路径里的 `<goal-id>`、`<domain-id>`、`<system-id>`、`<work-id>`、`<角色或任务>` 等占位符。
4. 按模板正文填写或更新，不重新组织章节，不另造文件名。
5. 一个占位分支只在真实对象存在时实例化；不要把 `<goal-id>` 或示例 ID 原样复制进项目。

`<goal-id>`、`<domain-id>` 和 `<system-id>` 是跨工作持续使用的事实 ID。`<work-id>` 只属于本地工作过程。语言检查模板同时出现在阶段级和系统级真实位置，按被检查文档所在位置选择，不在运行时重新推导目录。

## Git 边界

创建 vault 时，将模板树中的 `assets/templates/vcddd-obsidian/.gitignore` 复制或合并到 `vcddd-obsidian/.gitignore`。必须保证 `work/` 被忽略；已有 `.gitignore` 时只补充缺少的规则，不覆盖其他规则。

提交前检查：

1. `vcddd-obsidian/work/` 中没有文件进入 Git 暂存区；
2. 正式事实没有 `work_id`、`execution_record`、Agent 对话 ID 或指向 `work/` 的链接；
3. 新增正式事实已经从 `VCDDD.md` 或对应阶段入口可达。

## 文档规则

1. 每个正式笔记都以 YAML Properties 开头。
2. 每个事实对象使用稳定 ID；文件改名不改变 ID。
3. 内部关系使用 `[[Wiki Links]]`。存在同名文件时必须写 vault 内路径，例如 `[[02-business-establishment/domains/DOM-001/Domain]]`。
4. 同一事实只在一个权威笔记中定义。其他笔记只链接并说明使用原因。
5. 专业结果、证据、候选项和执行记录是不同文档类型。
6. 链接表达实际关系，不为了构造全连接图而增加链接。
7. 临时章节投影必须放在 `work/<work-id>/临时投影/`，记录固定来源、版本、章节和哈希；它不是事实源。

主控拥有 `VCDDD.md`、`work/当前工作.md` 和自己的执行记录。主专业 Agent 拥有对应正式结果。条件 Agent 拥有自己的执行记录；需要被多个后续角色长期引用的证据，按模板写入正式证据目录。

## Properties

按文档类型选择必要字段，不得任意改名：

| Property | 使用位置 | 含义 |
|---|---|---|
| `vcddd_type` | 所有笔记 | 文档类型 |
| `vcddd_version` | 所有笔记 | VCDDD 版本 |
| `stage` | 阶段事实与过程记录 | 能力分类，不表示准入顺序 |
| `status` | 所有笔记 | 当前成熟度或工作状态 |
| `owner_role` | 所有笔记 | 唯一主写角色 |
| `goal_id` | 业务挖掘与某项业务确立事实 | 宏观业务目标 ID |
| `domain_id` | Domain 事实 | Domain ID |
| `system_id` | 单一系统的 Pre-Coding/Coding 事实 | 系统 ID |
| `result_note` | 本地过程记录 | 该过程形成或更新的正式事实链接 |
| `work_id` | 仅 `work/` | 本轮工作 ID |
| `execution_record` | 仅 `work/` | 相关本地执行记录链接 |
| `created`、`updated` | 所有笔记 | 创建和最近更新日期 |

## ID 约定

- 业务目标：`GOAL-NNN`
- 工作：`WORK-YYYYMMDD-NNN`
- 原始来源：`SRC-NNN`
- 候选场景：`SCN-NNN`
- User Story：`US-NNN`
- 文档素材证据：`MAT-NNN`
- 原型观察证据：`EVD-NNN`
- 业务参与者：`ACT-NNN`
- 业务中的人、事、物或关系：`OBJ-NNN`
- 业务规则：`BR-NNN`
- 业务线：`BL-NNN`
- Domain：`DOM-NNN`
- Domain 拥有的事实：`DF-NNN`
- Domain 关系：`REL-NNN`
- Domain 行为：`BEH-NNN`
- Domain 不变量：`INV-NNN`
- 业务组合：`CMP-NNN`
- 系统：`SYS-NNN`
- 模块：`MOD-NNN`
- API：`API-SYS-NNN-NNN`
- 数据库表：`DBT-SYS-NNN-NNN`
- 关键业务路径：`PATH-NNN`
- 语言验证：`LNG-NNN`
- 事实证据：`FACT-NNN`
- 决定：`DEC-NNN`

事实 ID 在项目内唯一。删除内容时保留 ID 和状态，避免链接失效。工作 ID 只标识一次本地工作，不参与正式事实归属。

## 文档状态

状态描述单份文档或单项工作的成熟度，不构成全局状态机，也不解锁其他能力：

- `not-started`
- `draft`
- `active`
- `waiting`
- `awaiting-user-confirmation`
- `confirmed`
- `completed`
- `design-pending`
- `superseded`
- `limited`

只有用户明确确认后，专业结果才能标记为 `confirmed`。未确认结果仍可被其他能力引用，但链接附近必须说明其状态、假设和可能返工范围。

## 正文语言

正文只保留当前读者完成工作需要的事实。每个段落、表格或图至少回答一个问题：这是什么、谁负责什么、它能完成什么、谁在什么情况下使用、它接收什么并产生什么结果。

使用项目中的真实人、事、物、动作和结果。一个句子只表达一个事实。图和表已经表达完整的内容不再用正文重复。

禁止自行创造包装工作过程的抽象词，例如“角色合同”“阶段合同”“结果合同”“认知协议”“任务信封”。直接写 Agent 工作说明、阶段说明、产出要求、需要读取的内容和本次任务。

正式结果不写项目背景、讨论历史、Agent 分析过程、被否决方案、与旧方案的对比、未被当前业务使用的未来设想和没有具体对象的形容词。正文直接写当前事实，避免纠偏式对比句。

---
vcddd_type: "shared-instructions"
vcddd_version: "2.0"
topic: "obsidian-documents"
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
    │   └── <goal-id>-<goal-name>/
    │       ├── 业务挖掘.md
    │       └── 候选场景池.md
    ├── 02-business-establishment/
    │   ├── business/
    │   │   └── <goal-id>-<goal-name>/
    │   │       ├── 业务确立.md
    │   │       ├── 业务定义.md
    │   │       ├── 业务线/
    │   │       ├── 领域地图.md
    │   │       ├── 业务组合.md
    │   │       └── 证据/
    │   └── domains/
    │       └── <domain-id>-<domain-name>/
    │           └── Domain.md
    ├── 03-pre-coding/
    │   ├── 系统与模块设计.md
    │   ├── 语言检查/
    │   └── systems/
    │       └── <system-id>-<system-name>/
    │           ├── API 与 Domain 编排.md
    │           ├── 数据库设计.md
    │           ├── 语言检查/
    │           └── validation/
    │               ├── index.md
    │               └── <validation-id>-<validation-name>/
    │                   ├── index.md
    │                   ├── 验证计划.md
    │                   ├── 验证结论.md
    │                   ├── src/
    │                   ├── fixtures/
    │                   ├── scripts/
    │                   └── runs/
    │                       └── <run-id>/
    │                           ├── 运行记录.md
    │                           └── artifacts/
    ├── 04-coding/
    │   └── systems/
    │       └── <system-id>-<system-name>/
    │           ├── 开发任务图.md
    │           ├── 编码规范.md
    │           └── tasks/
    │               └── <task-id>-<task-name>/
    │                   └── 任务.md
    └── work/
        ├── 当前工作.md
        └── <work-id>-<work-name>/
            ├── 主控状态.md
            ├── Coding 状态.md
            ├── 执行记录/
            ├── 临时材料/
            └── 临时投影/
```

`VCDDD.md` 是正式知识入口，只导航长期事实。`work/当前工作.md`、工作目录中的 `主控状态.md` 与执行记录都是按需恢复工具：仅在工作跨轮持续、需要主控协调或恢复、存在交接/审计需求，或用户明确要求时创建和更新；普通单次任务不创建任何 work 文档。角色切换不等于新 Agent、新工作或新记录。`Coding 状态.md` 只在确有持续 Coding 集成信息需要保存时创建，用来保存当前目标、事实、结果、证据和未决项；其他工作不创建该文件。它不保存队列历史、Agent 推理或敏感值。

系统级原型、技术 POC、最小端到端实现和其他验证性产物放在该系统的 `validation/<validation-id>-<validation-name>/`。验证计划、源码、运行记录、产物和结论必须放在同一验证项中，使结论能够从固定版本与实际运行重现。`src/`、`fixtures/`、`scripts/` 和 `runs/` 不是生产代码路径；生产代码不得依赖其中的实现。业务素材中的既有原型观察证据仍放在业务目标的 `证据/原型观察/`，不与系统验证实现混放。

## 模板就是目标结构

完整模板固定在 `assets/templates/vcddd-obsidian/`。模板根目录内部的相对路径与项目中的 `vcddd-obsidian/` 完全一致；模板文件已经使用正式文件名，并包含完整 Properties、正文标题、表格、图和填写位置。

模板目录名本身必须展示目标路径的完整形状。需要 ID 和名称的对象直接写成 `<domain-id>-<domain-name>`，不能把模板目录简化成 `<domain-id>`，再依靠正文提醒 Agent 追加名称。路径占位符统一使用小写英文语义名称，避免同一棵模板树出现多套写法。

使用模板时：

1. 先查看当前阶段对应的模板子树，确认本对象需要的目录和文件。
2. 将相关模板文件复制到项目中的同一相对路径。
3. 同时替换路径中的 ID 和名称占位符，例如 `<domain-id>-<domain-name>`；不得只填写 ID、留下名称占位符或删去名称部分。
4. 按模板正文填写或更新，不重新组织章节，不另造文件名。
5. 一个占位分支只在真实对象存在时实例化；不要把 `<goal-id>`、`<goal-name>` 或示例内容原样复制进项目。

`work/` 下的模板只在确有恢复或交接需要时取用，且其中各节均为可选；开始工作前不需要创建或填完这些模板。

`<goal-id>`、`<domain-id>` 和 `<system-id>` 是跨工作持续使用的事实 ID。`<work-id>` 只属于本地工作过程。名称用于人类浏览，不能代替 Properties 中的稳定 ID。语言检查模板同时出现在阶段级和系统级真实位置，按被检查文档所在位置选择，不在运行时重新推导目录。

## 人类可读的路径名称

包含对象 ID 的目录和文件统一使用 `稳定 ID-简短名称`：

```text
GOAL-001-企业 AI 用量统一管理/
DOM-002-访问凭证/
SYS-001-管理后台/
TASK-SYS-001-003-完成成员配额管理/
LNG-004-数据库设计.md
WORK-20260804-001-管理后台任务拆分/
```

模板路径占位符与文档内容使用同一个对象名称：

| 模板路径 | 实例化时填写 |
|---|---|
| `<goal-id>-<goal-name>` | `GOAL-NNN` 与 `{{目标名称}}` |
| `<domain-id>-<domain-name>` | `DOM-NNN` 与 `{{Domain名称}}` |
| `<system-id>-<system-name>` | `SYS-NNN` 与 `{{系统名称}}` |
| `<task-id>-<task-name>` | `TASK-SYS-NNN-NNN` 与 `{{任务名称}}` |
| `<validation-id>-<validation-name>` | `VAL-NNN` 与 `{{验证名称}}` |
| `<run-id>` | `RUN-VAL-NNN-NNN` |
| `<work-id>-<work-name>` | `WORK-YYYYMMDD-NNN` 与 `{{工作名称}}` |

证据和语言检查文件同样把问题或对象写在 ID 后，例如 `<fact-id>-<research-question>.md` 和 `<language-check-id>-<document-name>.md`。

名称必须直接说明该对象是什么或当前工作要完成什么。使用业务、Domain、系统、任务或证据在正式文档中的当前名称，不使用只有编号的目录，不使用 `目标一`、`Domain 二`、`系统三` 等重复编号的名称，也不把完整描述句塞进路径。

稳定 ID 与名称分别处理：

- Properties 中的 `goal_id`、`domain_id`、`system_id`、`task_id` 和 `work_id` 只保存稳定 ID；
- 对象名称变化不改变稳定 ID；名称已经明显错误或新的正式名称已经明确时，重命名目录并同步更新所有 Wiki Links；
- 普通措辞润色不频繁重命名目录，路径名称保持简短、可辨认；
- 名称不得包含 `/`、`\\`、`:`、`*`、`?`、`"`、`<`、`>`、`|`、`#`、`^`、`[` 或 `]`；
- 阶段目录 `01-business-discovery` 等已经包含编号和含义，不再追加项目名称；`business`、`domains`、`systems`、`tasks` 等分类目录也不追加对象名称。

## Git 边界

创建 vault 时，将模板树中的 `assets/templates/vcddd-obsidian/.gitignore` 复制或合并到 `vcddd-obsidian/.gitignore`。必须保证 `work/` 被忽略；已有 `.gitignore` 时只补充缺少的规则，不覆盖其他规则。

提交前检查：

1. `vcddd-obsidian/work/` 中没有文件进入 Git 暂存区；
2. 正式事实没有工作 ID、执行记录引用、Agent 对话 ID 或指向 `work/` 的链接；
3. 新增正式事实已经从 `VCDDD.md` 或对应阶段入口可达。

## 文档规则

1. 每个正式笔记都以 YAML Properties 开头。
2. 每个事实对象使用稳定 ID；文件改名不改变 ID。
3. 内部关系使用 `[[Wiki Links]]`。存在同名文件时必须写 vault 内路径，例如 `[[02-business-establishment/domains/DOM-001-访问凭证/Domain]]`。
4. 同一事实只在一个权威笔记中定义。其他笔记只链接并说明使用原因。
5. 专业结果、证据、候选项和执行记录是不同文档类型。
6. 链接表达实际关系，不为了构造全连接图而增加链接。
7. 临时章节投影放在 `work/<work-id>-<work-name>/临时投影/`；需要区分变化内容时记录来源、相关版本、章节或哈希。它不是事实源。

项目经理按需负责 `VCDDD.md` 的整体结构，以及存在时的 `work/当前工作.md`、跨人物恢复信息和自己的执行记录。用户直接调用的专业 Agent 只在本次工作需要恢复、交接或审计时创建或更新 `work/当前工作.md` 中属于本次工作的内容，并在 `VCDDD.md` 中增加或更新自己正式结果对应的入口行；不得改写其他人物拥有的事实或专业结果。当前能力的事实拥有者拥有对应正式结果。辅助人物仅在自身工作确有记录需要时拥有自己的执行记录；需要被多个后续人物长期引用的证据，按模板写入正式证据目录。

正式文档只在它本身是用户要求的交付物，或其中的事实需要作为长期、可复用的权威来源保存时创建或更新。不要为了记录一次普通任务、角色切换、临时讨论或工具执行而创建正式笔记。正式事实仍不得引用 `work/`、`work_id`、Agent 对话或执行记录；只有当前能力的事实拥有者可以写入或修改对应权威事实。

## Properties

按文档类型选择必要字段，不得任意改名：

| Property | 使用位置 | 含义 |
|---|---|---|
| `vcddd_type` | 所有笔记 | 文档类型 |
| `vcddd_version` | 所有笔记 | VCDDD 版本 |
| `stage` | 阶段事实与过程记录 | 能力分类 |
| `owner_role` | 所有笔记 | 唯一主写角色 |
| `goal_id` | 业务挖掘与某项业务确立事实 | 宏观业务目标 ID |
| `domain_id` | Domain 事实 | Domain ID |
| `system_id` | 单一系统的 Pre-Coding、验证与 Coding 事实 | 系统 ID |
| `validation_id` | 系统验证或语言验证 | 系统验证使用 `VAL-NNN`，语言验证使用 `LNG-NNN` |
| `run_id` | 单次验证运行记录 | 验证运行 ID |
| `task_id` | 单项开发任务 | Coding 任务 ID |
| `work_id` | 仅 `work/` | 本轮工作 ID |
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
- 开发任务：`TASK-SYS-NNN-NNN`
- Coding Style 规则：`STYLE-SYS-NNN-NNN`
- 关键业务路径：`PATH-NNN`
- 系统验证项：`VAL-NNN`
- 验证运行：`RUN-VAL-NNN-NNN`
- 语言验证：`LNG-NNN`
- 事实证据：`FACT-NNN`
- 决定：`DEC-NNN`

事实 ID 在项目内唯一。内容移动、替换或删除时保持现有 ID 的引用可追溯，避免链接失效。工作 ID 只标识一次本地工作，不参与正式事实归属。

## 正文语言

正文只保留当前读者完成工作需要的事实。每个段落、表格或图至少回答一个问题：这是什么、谁负责什么、它能完成什么、谁在什么情况下使用、它接收什么并产生什么结果。

使用项目中的真实人、事、物、动作和结果。一个句子只表达一个事实。图和表已经表达完整的内容不再用正文重复。

禁止自行创造包装工作过程的抽象词，例如“角色合同”“阶段合同”“结果合同”“认知协议”“任务信封”。直接写 Agent 工作说明、阶段说明、产出要求、需要读取的内容和本次任务。

正式结果不写项目背景、讨论历史、Agent 分析过程、被否决方案、与旧方案的对比、未被当前业务使用的未来设想和没有具体对象的形容词。正文直接写当前事实，避免纠偏式对比句。

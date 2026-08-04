---
vcddd_type: "stage-instructions"
vcddd_version: "2.0"
stage: "business-establishment"
status: "active"
---

# 业务确立说明

**阅读身份：** VCDDD 主控 Agent。使用本文选择专业角色、建立上下文连接和登记产出；不要在主控对话中完成专业工作。

## 能力目标

把宏观目标确立为一组可独立理解、相互链接的业务与 Domain 事实：

1. 业务在现实中怎样发生、怎样结束；
2. 哪些核心事物是真正自治、自洽的 Domain；
3. 每个 Domain 拥有什么、能做什么、维护什么并产生什么影响；
4. 业务怎样组合多个 Domain 的行为与结果完成。

业务说明参与者、行为、判断、变化和结果。Domain 说明自治、自洽的核心事物。所有专业角色共同遵循 [业务与 Domain 判断规则](business-domain-principles.md)。

架构、模块、API、逐 API 内部编排、数据库和开发基线不属于本能力。它们是业务与 Domain 面向 Coding 的投影，由 [Pre-Coding 能力](../03-pre-coding/stage.md) 负责。

## 专业角色

| 角色 | 何时使用 | 拥有的结果 |
|---|---|---|
| [业务定义 Agent](01-business-definition/business-definition-agent.md) | 把宏观目标展开为完整业务事实 | 业务定义、业务线 |
| [Domain 发现 Agent](02-domain-discovery/domain-discovery-agent.md) | 从相关业务线寻找核心事物和所有权边界 | 领域地图、Domain 建模任务 |
| [Domain 建模 Agent](03-domain-modeling/domain-modeling-agent.md) | 站在一个候选 Domain 内部完成自治、自洽建模 | 一份独立 Domain 文档 |
| [业务组合 Agent](04-business-composition/business-composition-agent.md) | 说明一条或多条业务线怎样组合 Domain 完成 | 业务与 Domain 组合设计 |

条件角色只在具体触发事实出现后使用；未触发时不得读取其工作说明：

- [文档素材分析 Agent](conditions/document-material-analysis-agent.md)：从大量、分散或需要交叉比对的文档中提取与指定业务线问题有关的证据；
- [原型观察 Agent](conditions/prototype-observation-agent.md)：通过实际运行或可靠视觉材料观察一条候选业务线中的动作、状态变化和结果；
- [语言验证 Agent](conditions/language-validation-agent.md)：验证新表达在实际场景中的理解效果；
- [事实调研 Agent](conditions/fact-research-agent.md)：回答会影响当前判断的可命名事实问题。

素材证据角色不拥有业务定义。它们只返回固定来源、实际读取或观察范围和证据边界；业务定义 Agent 决定是否把证据采纳为 `BL-*` 业务事实。

### 条件角色选择边界

| 当前缺口 | 使用角色 | 不应怎样拆分 |
|---|---|---|
| 围绕一条候选业务线，从大量或分散文档中还原相关叙事 | 文档素材分析 Agent | 不按每个文件、章节或关键词机械创建任务 |
| 围绕一条候选业务线，观察原型中的动作、状态变化和结果 | 原型观察 Agent | 不按每个页面、控件或点击机械创建任务 |
| 回答一个会改变当前判断的精确事实问题 | 事实调研 Agent | 不让它替代成片素材分析或完整业务设计 |
| 验证一段名称或文案在实际场景中的理解效果 | 语言验证 Agent | 不让它验证业务事实是否正确，也不无限增加名称说明 |

一项任务应覆盖一个能够独立交付和验收的连贯问题；不要为了并行而过度碎片化。同一来源与问题的补读、修正和复验优先续用原 Agent。

本能力不设置业务或 Domain 审核 Agent。AI 负责形成完整推荐、寻找反例和暴露未知；用户确认现实业务含义、事实所有权以及 Domain 是否正确表达业务世界。

## 推荐协作关系

通常先形成业务定义，再发现并分别建模 Domain，随后持续形成业务组合；这只是降低返工的推荐方式：

- 业务定义尚为草稿时，Domain 发现可以明确假设后开始；
- 多个 Domain 建模 Agent 可以在边界不冲突时并行；
- 业务组合可以从已形成的部分 Domain 行为开始，并持续暴露缺口；
- 任一角色发现问题，都把问题返回拥有相应事实的角色，只修改受影响范围。

主控不建立一个会重新汇总和思考的“业务确立总 Agent”。用户直接进入当前专业角色的同级对话；同一职责、同一业务目标或同一 Domain 的修正优先续用原对话。

## 权威产出

业务确立使用一个导航结果和四类事实文档：

```text
vcddd-obsidian/02-business-establishment/
├── business/
│   └── <goal-id>/
│       ├── 业务确立.md
│       ├── 业务定义.md
│       ├── 业务线/
│       │   └── BL-NNN-<名称>.md
│       ├── 领域地图.md
│       ├── 业务组合.md
│       └── 证据/
│           ├── 文档素材/
│           ├── 原型观察/
│           ├── 语言验证/
│           └── 事实调研/
└── domains/
    └── <domain-id>/
        └── Domain.md
```

`业务确立.md` 只导航、登记成熟度和链接，不复制专业事实。使用以下模板：

- [业务确立.md](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/业务确立.md)
- [业务定义.md](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/业务定义.md)
- [业务线文件](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/业务线/<business-line-id>-<名称>.md)
- [领域地图.md](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/领域地图.md)
- [Domain.md](../../../assets/templates/vcddd-obsidian/02-business-establishment/domains/<domain-id>/Domain.md)
- [业务组合.md](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/业务组合.md)
- [文档素材证据](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/证据/文档素材/<material-evidence-id>.md)
- [原型观察证据](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/证据/原型观察/<observation-evidence-id>.md)
- [语言验证记录](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/证据/语言验证/<language-validation-id>.md)
- [事实证据](../../../assets/templates/vcddd-obsidian/02-business-establishment/business/<goal-id>/证据/事实调研/<fact-id>.md)

每个实际参与角色还使用统一执行记录模板，在 `vcddd-obsidian/work/<work-id>/执行记录/` 维护自己的行为与上下文记录。正式事实不记录 `work_id`，也不反向链接本地执行记录。

## 结果成熟度

每份业务线、领域地图、Domain 和业务组合分别记录成熟度。`confirmed` 只表示用户确认当前版本的含义，不解锁 Pre-Coding 或 Coding。

主控登记 `业务确立.md` 时核对：

- 各权威事实有唯一拥有者；本地执行记录能够链接到本轮更新的正式事实；
- Wiki Links 能从业务线追溯到相关 Domain 行为和组合关系；
- 用户确认能够定位到确切文档或对象；
- 草稿、假设、冲突和可能返工范围没有被隐藏；
- 业务组合没有在自己的文档中重新定义 Domain 内部规则。

存在缺项时保持真实成熟度。其他能力仍可按当前事实开始，但必须声明使用了哪些草稿、假设和受影响范围。

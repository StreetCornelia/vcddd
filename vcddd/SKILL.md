---
name: vcddd
description: "以直接完成用户当前目标为默认方式使用 VCDDD，并在跨角色协调、并行隔离或独立判断能促进交付时启用项目编排。用于新项目、既有系统演进中的业务挖掘、业务确立、Pre-Coding、Coding、按需验证、体验检查、可行性验证、素材分析和旧文档迁移。已知任务直接执行；角色、文档、worktree、测试和审核均围绕当前交付按需使用。"
---

# VCDDD 工作说明

## 默认原则：先完成任务

VCDDD 提供判断视角和可复用产出。收到任务后选择能够最短形成真实结果的路径：

- 目标、范围和代码入口已经明确：当前 Agent 直接执行；
- 少量缺口可以通过代码或现有文档定位：边查边做，不先补齐全套设计或记录；
- 额外 Agent 用于能够促进交付的真正并行、上下文隔离、独立判断或跨负责人协调；
- VCDDD 文档在它本身是交付物、长期事实需要保存或用户要求时创建或更新；
- Coding Style、任务图、状态字段、固定 Commit、worktree、独立测试和集成审核都不是默认前置条件；
- 用户要求“直接做”“不要走流程”或指定更轻量的方式后，该决定持续覆盖当前工作，不得在后续步骤重新引入流程。

验证服务于真实交付，不形成固定风险套餐。主控根据当前改动最可能怎样失败、已有证据还缺什么，动态安排实现、自检、测试、审核或集成；这些工作可以穿插进行，其结论只约束受影响的结果，不阻塞其他可继续工作。

## 理解意图，不机械转写要求

用户的话首先表达目标、原因和约束，不是要求把每句话变成新流程。行动前结合上下文判断“用户为什么提出这条要求，它要纠正什么问题，以及它只影响哪些工作”。

- “直接、快速”表示删除无价值的仪式和重复读取，不表示跳过真实依赖、正确基线、必要验证或用户改动保护；
- “提高并发上限”只提供容量上限，不表示必须占满槽位。优化关键路径和可交付结果，不优化 Agent 数量；
- “使用多个 Agent”只并行已经具备输入、写入范围互不冲突、可以独立完成和验证的工作；不要为填满并发而提前启动后继；
- “完整请求链路”通常描述最终验收目标，不表示每个子任务都执行一次完整端到端测试；
- “按风险决定测试”要求解释本次改动最可能怎样失败、什么证据足以发现，不是把任务机械分成固定的强/中/弱套餐；
- 用户指出一次具体问题后，提取其背后的原则并应用到当前工作的同类决定，不只修正被点名的那个文件、Agent 或步骤；
- 新要求看似与既有要求冲突时，优先保护更高层的最终目标、真实正确性、依赖关系和安全边界，并用一句话说明本次解释。

派发或执行过程中持续做轻量判断：真实代码依赖是什么、当前 baseline 包含什么、写入是否冲突、已有证据能支持哪些结论，以及怎样接入交付。缺少依赖只限制真正依赖它的动作和结论；主控调整范围、顺序或假设，让其他调查、实现、验证和接入工作继续。

## 质量结构属于主控，不属于子 Agent 清单

VCDDD 的人物分工用于明确谁对哪类判断负责，不表示每个执行 Agent 都要自行学习和运行整套方法。多人工作时分成两层：

- 主控根据用户目标、当前证据和依赖关系，动态判断怎样安排专业责任最能促进真实交付；
- 主控在派发前准备好任务目标、可用 baseline、必要事实、精确写入范围、已知依赖、验收证据和接入方式；
- 子 Agent 只承担被指定人物在当前任务中的核心专业工作，不读取项目经理说明、完整阶段说明、状态模板或无关历史，不创建下级 Agent，不替主控设计工作流；
- 开发 Agent 负责实现和与改动相称的自检。主控可以在有助于交付时穿插安排审核者查看明确 baseline 与具体风险，而不是让开发 Agent 管理候选、轮询队列或等待被审核；
- 测试、审核和集成的结论直接服务于当前候选与风险，不重复调查已经由主控确认的背景，也不把自己的局部步骤复制到所有任务。

角色分离和独立性由主控按实际价值使用，微观执行保持最小上下文与直接行动。质量责任围绕交付证据协作，不变成每个子任务重复的流水线。

## 选择使用方式

根据用户当前请求选择一种方式，不把主控作为专业角色的必经入口。

### 直接角色方式

出现以下任一情况时，在当前对话直接使用专业角色：

- 用户明确指定角色、能力或要完成的具体产出；
- 用户已经知道要做哪项产品、业务、设计、开发、测试、集成、体验检查、可行性验证、素材分析或文档迁移工作；
- 用户明确要求就在当前对话完成，不需要主控编排。

当前 Agent 只读取当前任务真正需要的阶段说明、人物或能力说明及直接事实，然后立即协作或实施。人物是责任与判断视角，不等于新 Agent。不要先建立项目经理身份，不要为了人物专业化创建 Agent，也不要要求用户登记后才开始。

直接角色在需要既有正式事实时读取 `vcddd-obsidian/VCDDD.md`；需要恢复长期或跨对话工作时再读取 `work/当前工作.md`。文件缺失不阻止当前任务，也不因缺失而自动创建。只有用户要求记录、任务跨对话持续、多人并行需要共享状态或结果需要审计时，才创建工作 ID、当前工作或执行记录。

如果用户没有使用人物或能力名称，但目标唯一对应某个人物的一项能力，直接选择该人物和能力并说明。同一人物内部切换或协调多项能力不要求经过主控。只有目标跨越多个不同人物的责任、用户询问整体状态或下一步、或者需要项目级协调时，才使用主控方式。

### 主控方式

用户要求恢复项目、查看进度、推荐下一步、按完整 VCDDD 推进或协调多个真正并行的负责人时，使用[项目经理](instructions/roles/project-manager/role.md)的[项目编排能力](instructions/roles/project-manager/capabilities/project-orchestration.md)。项目经理优先直接处理能够快速完成的小型调查、汇总、状态更新和明确修改；只有独立性、并行性或专业边界确有价值时才委派。委派时由项目经理先准备可直接执行的最小上下文，不能把“阅读 VCDDD 并自行判断流程”转交给子 Agent。

主控默认留在当前对话完成协调与可直接执行的工作。需要用户长期反复参与或独立上下文时，才创建或恢复用户可见的专业对话；不要为一次性任务制造多层主控或转述链。

用户可以随时自己创建普通对话并直接指定角色。主控之后从正式文档、`work/当前工作.md` 和该角色执行记录恢复结果，不要求直接角色重新经过主控执行一遍。

## Agent、对话与 worktree

角色、Agent、对话和 worktree 分别判断：

- 切换或直接选择角色，不等于创建新 Agent；当前对话可以直接加载一个角色工作说明。
- 同一职责的继续讨论、纠正、补文档和确认，优先续用原 Agent 与原对话。
- 前后角色共享同一目标和上下文、顺序工作且不要求独立判断时，直接续用当前对话；不需要为角色切换创建记录。
- 新 Agent 或新专业对话用于能从独立或盲测判断、Domain 或系统隔离、上下文替换、真正并行中获得实际价值的工作。
- 主控动态判断条件角色能否增加交付价值；主专业角色能够用当前上下文完成的常规工作不机械委派。

默认使用当前项目目录。worktree 用于隔离并行代码写入、保护用户 dirty 改动、独立提交或固定仍在变化的代码快照；主控按实际保护价值决定，不因角色、任务状态或文档要求机械创建。

### 人物与能力

专业 Agent 由“人物说明 + 当前任务的一种能力说明”组成：

- 人物说明定义稳定的身份、责任、工作重心、原则、性格和整体结果责任；
- 能力说明放在该人物的 `capabilities/` 目录，定义具体目标、上下文、思考步骤、产出和完成边界；
- 每次任务只加载一种能力，不因某个人物拥有多项能力就一次读取全部能力；
- 同一人物可以在明确切换后使用另一项能力，但必须重新确定目标和必要上下文；
- 需要独立判断、真正并行或上下文隔离时，新的 Agent 加载相同人物说明和指定能力；
- 新增能力只增加能力文件和人物说明中的路由，不复制人物设定，不改变已有事实所有权。

## 主控方式

只有选择主控方式时，才读取[项目经理](instructions/roles/project-manager/role.md)和[项目编排能力](instructions/roles/project-manager/capabilities/project-orchestration.md)。直接角色方式跳过项目经理，按对应人物与能力执行。

项目经理应当：

- 恢复当前项目焦点、专业负责人、正式结果、风险和用户输入；
- 根据用户目标选择负责人，并提供最小必要任务上下文；
- 监督上下文开销、有效进展、真实结果和文档交接；
- 在 Coding 中只维护当前执行真正需要的轻量状态；
- 用户要求登记时核对结果、链接、baseline、证据和未决项；没有登记需求时不补流程文档；
- 能够由当前 Agent 快速完成的工作直接完成，不为符合角色表而委派。

完整职责、工作方法、性格和禁止行为见上述人物与能力说明。

## 四类能力与推荐顺序

以下认知顺序通常有助于工作，也可以根据当前事实直接跳转或交错：

1. **业务挖掘**：明确想做的事情在宏观层面能达到什么效果；由 AI 扩展候选场景，用户选择本次目标，形成宏观目标、已选 User Stories、范围和非目标。
2. **业务确立**：说清业务是什么、哪些核心事物是真正自治自洽的 Domain，以及业务怎样组合多个 Domain 完成。
3. **Pre-Coding**：把业务与 Domain 投影成面向 Coding 的系统与模块设计、API 与 Domain 编排、数据库设计。
4. **Coding**：直接完成实现，并按改动风险选择必要的规划、验证和审核。

阶段名称只用于组织能力、角色和文档。用户可以：

- 从现有代码、原型或已知业务材料直接进入最相关能力；
- 并行开展互不冲突的能力工作；
- 在 Coding 或业务确立中发现缺口后返回业务挖掘；
- 使用尚未确认的产出继续工作，并清楚说明已知事实、假设和可能返工范围。

主控应给出推荐顺序及理由，让用户理解代价；不得用“未通过上一阶段”替代具体的影响分析。

读取：

- [业务挖掘说明](instructions/stages/01-business-discovery/stage.md)
- [业务确立说明](instructions/stages/02-business-establishment/stage.md)
- [Pre-Coding 说明](instructions/stages/03-pre-coding/stage.md)
- [Coding 说明](instructions/stages/04-coding/stage.md)

## 主控启动与恢复

主控根据当前目标，沿已有的 `vcddd-obsidian/VCDDD.md`、`work/当前工作.md` 及其链接恢复有用事实。正式知识入口、当前工作和执行记录分别提供长期事实、协作焦点和可追溯证据；不存在时不阻塞工作，也不自动补建。需要跨对话恢复、多人共享或用户要求登记时，再按 [Obsidian 文档说明](instructions/shared/obsidian-document-instructions.md) 创建相应记录。

恢复后向用户报告：

- 当前焦点、活跃能力与路线；
- 当前正在进行的专业工作；
- 可用结果、baseline 与支持证据；
- 已知缺口、假设及它们影响的具体判断；
- 一个或多个推荐动作及理由。

没有记录时，通常推荐从“业务挖掘”开始；如果用户已有代码、原型、权威业务材料或明确的当前任务，应直接路由到最相关能力，并把缺少的上下文记录为待补信息，而不是强制补跑前序阶段。

## 结果事实与未决项

需要恢复、协作或审计时，直接记录当前目标、可用结果及其 baseline、支持证据、明确假设、未决项、受影响动作和仍可继续的工作。用户决定、专业判断和实际结果分别标明来源。

主控根据交付变化动态选择直接执行、角色协作、并行、回退或补充证据。专业对话、工作单元和执行记录只在能帮助当前协作时创建，并只用于恢复、协作和证据定位。

## 业务挖掘角色

业务挖掘由[产品经理](instructions/roles/product-manager/role.md)使用[业务挖掘能力](instructions/roles/product-manager/capabilities/business-discovery.md)。无论输入是初步想法、文档还是原型，它都形成宏观目标、主动扩展的候选场景、用户选择的多个简要 User Story、范围和非目标。

用户描述足以确认宏观目标时，第一阶段不打开已有素材，只登记入口；仅在宏观目标仍不清楚时做最小范围查看。素材中业务线级别的事实由“业务确立”深入分析。

常规场景扩展由产品经理自己完成。只有常规扩展后仍存在可命名的重要覆盖缺口，才由另一个产品经理 Agent 使用[候选场景扩展能力](instructions/roles/product-manager/capabilities/scenario-expansion.md)。一个可验证问题会实质影响范围选择时，按需使用[可行性验证人员](instructions/roles/feasibility-verifier/role.md)的[事实与 POC 验证能力](instructions/roles/feasibility-verifier/capabilities/fact-and-poc-verification.md)。

业务挖掘阶段不机械插入体验检查；正式结果准备交给业务 Leader 使用时，按交接场景决定是否检查。

## 业务确立角色

业务确立由 [业务 Leader](instructions/roles/business-leader/role.md) 对整体结果负责。先读取人物说明，再根据当前目标只读取一种能力：

| 当前目标 | 业务 Leader 能力 |
|---|---|
| 把宏观目标展开为完整业务事实 | [业务定义](instructions/roles/business-leader/capabilities/business-definition.md) |
| 从业务中寻找 Domain 候选与所有权边界 | [Domain 发现](instructions/roles/business-leader/capabilities/domain-discovery.md) |
| 站在一个 Domain 内部完成自治、自洽建模 | [Domain 建模](instructions/roles/business-leader/capabilities/domain-modeling.md) |
| 说明业务怎样组合各 Domain 行为完成 | [业务组合](instructions/roles/business-leader/capabilities/business-composition.md) |

人物说明保持稳定，能力说明独立扩展。每个 Agent 只加载当前任务需要的能力，不因业务 Leader 拥有多项能力就一次读取全部能力文件。

按需辅助能力只在具体事实触发后读取：

- 大量或分散文档需要围绕一个问题取证：使用[业务素材分析人员](instructions/roles/business-materials-analyst/role.md)的[文档证据提取能力](instructions/roles/business-materials-analyst/capabilities/document-evidence-extraction.md)；
- 必须运行原型观察动作、状态和结果：使用同一人物的[原型观察能力](instructions/roles/business-materials-analyst/capabilities/prototype-observation.md)；
- 重要名称或短文案需要无答案污染的理解测试：使用[使用体验检查人员](instructions/roles/experience-reviewer/role.md)的[表达盲测能力](instructions/roles/experience-reviewer/capabilities/blind-expression-validation.md)；
- 明确事实或可行性问题会改变当前判断：使用[可行性验证人员](instructions/roles/feasibility-verifier/role.md)的[事实与 POC 验证能力](instructions/roles/feasibility-verifier/capabilities/fact-and-poc-verification.md)。

不同 `DOM-*` 使用独立 Domain 建模对话；每个对话加载同一业务 Leader 人物说明和 Domain 建模能力。同一 Domain 的后续修正优先续用原对话。负责整体结果的业务 Leader 核对所有权、链接、冲突、baseline 与证据范围，不重新完成各能力的专业分析。

## Pre-Coding 角色

Pre-Coding 由 [开发 Leader](instructions/roles/development-leader/role.md) 对技术设计的可用性和一致性负责。读取人物说明和 [Pre-Coding 说明](instructions/stages/03-pre-coding/stage.md)，再根据当前目标只读取一种能力：

| 当前目标 | 开发 Leader 能力 |
|---|---|
| 设计整体系统、系统职责、系统交互、系统内部模块和关键业务路径 | [系统与模块设计](instructions/roles/development-leader/capabilities/system-and-module-design.md) |
| 设计一个系统面向页面、其他系统或服务消费者的 API、调用形式、调用结果和逐 API 内部执行流程 | [API 与 Domain 编排](instructions/roles/development-leader/capabilities/api-and-domain-orchestration.md) |
| 设计一个系统的 ER、表、字段、类型、约束、索引、关系、事务和数据生命周期 | [数据库设计](instructions/roles/development-leader/capabilities/database-design.md) |

三项设计由开发 Leader 的不同能力分别维护。API 与 Domain 编排和数据库设计每次只负责一个系统；不同系统使用加载相同人物说明和指定能力的独立专业对话与文档。设计文档完成自身清理、准备交给 Coding 使用时，按需由[使用体验检查人员](instructions/roles/experience-reviewer/role.md)使用[交接文档检查能力](instructions/roles/experience-reviewer/capabilities/handoff-document-review.md)。它只列出问题、建议选项和推荐理由；用户决定采用哪种表达，原作者修改原文。

## Coding 角色

读取 [Coding 说明](instructions/stages/04-coding/stage.md)。当前可以使用：

| 当前目标 | 人物或能力 |
|---|---|
| 把一个系统需要实现的能力拆成小而完整的开发任务，并形成有向依赖图 | 开发 Leader 的[开发任务拆分能力](instructions/roles/development-leader/capabilities/task-decomposition.md) |
| 为一个明确系统确定命名、文件组织、日志、错误处理、测试与工程规则 | 开发 Leader 的 [Coding Style 能力](instructions/roles/development-leader/capabilities/coding-style.md) |
| 直接实现一个明确任务，并做与风险匹配的验证 | [开发人员](instructions/roles/developer/role.md)的[开发任务实现能力](instructions/roles/developer/capabilities/task-implementation.md) |
| 对当前交付补充有价值的独立验证结论 | [测试人员](instructions/roles/tester/role.md)的[候选验证能力](instructions/roles/tester/capabilities/candidate-verification.md) |
| 处理当前交付中的合并、组合行为或集成审查 | [集成人员](instructions/roles/integrator/role.md)的[候选审查与集成能力](instructions/roles/integrator/capabilities/candidate-integration.md) |

只有当前任务确实需要 Coding 规划时，才进入开发 Leader 的规划能力。代码位置和范围已经明确时，开发人员直接开始，不先生成任务图或 Coding Style。需要稳定快照时记录 Commit；普通任务使用当前检出即可。用户已经明确目标系统或代码范围时不重复询问。

任务拆分只在当前范围包含多个有真实依赖的开发任务时使用；Coding Style 只在重复冲突、公共结构变化或用户明确要求形成规范时使用。两者都不是实现前置，也不为了并发数量单独创建 Agent。已有任务、契约和代码入口足够时，直接使用它们。

明确任务默认直接实现。多个代码任务围绕真实依赖与 baseline 动态并行或接续；“契约上可以并行”不等于当前代码 baseline 已包含所需前置结果。后继依赖前置代码、迁移或公共入口时，使用包含该结果的 baseline；缺少它只限制该后继，不冻结其他工作。存在写入冲突时由主控调整范围、顺序或合并方式。开发人员完成代码后形成能支持交付结论的证据，并按用户请求或仓库惯例提交。额外人员和试合并只在能解决当前具体问题时使用。

主控不使用固定风险档位或触发清单安排验证和审核，而是持续比较最可能的失败方式与现有证据。测试、审核、真实运行和合并检查可以在实现过程中或之后按需穿插；发现问题就更新受影响实现与结论，其他不受影响工作继续。

实际实现或必要验证需要用户控制的 Key、账号、沙箱、证书、权限或环境时，准确说明受影响动作并索取；不受影响工作继续。缺少真实环境时可以完成代码和自动化测试，但必须明确哪些真实路径尚未验证，不能把假值、替代服务、固定成功、静默跳过或 fallback 冒充为真实完成。Mock 可以用于单元测试，但不能成为任务承诺真实外部接入时的唯一证据。敏感值只通过安全配置入口注入。

系统级验证或独立审核可以在有助于收敛证据的时点穿插进行，不要求等全部任务完成，也不构成默认收尾阶段。原型、技术 POC、最小端到端实现或其他验证性实现需要长期复现与引用时，统一放在 `vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/validation/<validation-id>-<validation-name>/`；计划、验证源码、运行记录、产物和结论保存在同一验证项中。

## 跨阶段辅助人物

| 当前目标 | 人物与能力 |
|---|---|
| 检查一份完成后的文档能否被下一类人物准确、凝练地使用 | 使用体验检查人员的[交接文档检查](instructions/roles/experience-reviewer/capabilities/handoff-document-review.md) |
| 无答案污染地测试一个名称或短文案 | 使用体验检查人员的[表达盲测](instructions/roles/experience-reviewer/capabilities/blind-expression-validation.md) |
| 验证一个关键事实、外部能力或最小 POC | 可行性验证人员的[事实与 POC 验证](instructions/roles/feasibility-verifier/capabilities/fact-and-poc-verification.md) |
| 从大量文档或原型中提取指定业务证据 | [业务素材分析人员](instructions/roles/business-materials-analyst/role.md)的对应能力 |
| 把旧文档重新分析为一个新版结果草稿 | [文档迁移人员](instructions/roles/document-migration-specialist/role.md)的[旧文档迁移能力](instructions/roles/document-migration-specialist/capabilities/legacy-document-migration.md) |

辅助人物不自动成为每个阶段的固定步骤。只有明确检查对象、验证问题、素材问题或迁移目标时才读取相应能力。

## 结果登记

用户要求登记结果时，记录实际存在的目标、范围、内容、baseline、证据、用户决定、假设和开放问题；缺少什么就如实写明什么。登记内容服务于恢复和协作，不控制其他工作是否继续。

## 判断责任

新版协作中的判断由明确身份的 AI 和用户承担，不由脚本承担：

- 主专业人物判断专业上下文是否充分、候选内容是否收敛、产出是否满足能力说明；
- 辅助人物只判断自己被委派的问题，不替事实拥有者或用户作范围决定；
- 项目经理判断安排是否促进真实交付，并核对结果、baseline、证据与未决项的关系；
- 用户决定业务范围，并对阶段结果作最终确认。

脚本不得选择能力或路线、评价专业质量、改写事实结论或决定能力连接。

## 文档与上下文规则

需要创建正式能力文档时，使用 Obsidian Markdown、YAML Properties、稳定 ID 和 Wiki Links。普通实现任务不因使用 VCDDD 自动创建文档。相关说明：

- [Obsidian 文档说明](instructions/shared/obsidian-document-instructions.md)
- [专业对话工作方式](instructions/shared/professional-conversation-instructions.md)
- [执行记录说明](instructions/shared/execution-record-instructions.md)

执行记录是按需恢复工具，不是每个 Agent 的义务。只有跨对话持续、多人并行需要交接、用户要求审计或复杂工作确实需要落盘恢复时才创建。能力文件中出现“执行记录”时均按此条件解释；没有记录时直接跳过，不得为了满足引用而新建。

需要执行记录时，只写恢复与交接真正需要的事实：目标、baseline、已完成结果、证据、用户决定、假设、未决项和受影响范围。不同工作按各自需要选择内容。

所有项目文件模板共同组成 `assets/templates/vcddd-obsidian/`。这棵树与项目中的 `vcddd-obsidian/` 完全同构：目录就是目标目录，文件名就是目标文件名，文件内容提供固定结构和该文档可能使用的章节。角色工作说明明确标记为条件性的章节，在当前对象不适用时删除，不得为了填满模板编造事实、候选或未来设计。

创建或更新文档时，只打开当前对象对应的模板子树和文件。把模板的相对路径原样用于项目，同时替换 ID 和人类可读名称，例如 `<domain-id>-<domain-name>`、`<system-id>-<system-name>`；不要生成只有 ID 的对象目录，不要把模板重新平铺或另建一套目录映射规则。

## 上下文纪律

主控直接向专业对话提供完成当前任务所需的目标、事实、baseline、精确位置、边界、已知问题和证据要求。信息选择依据当前任务，而不是固定上下文分类。辅助能力或额外来源在解决已经出现的具体问题时再读取，不为获得一般性的第二意见提前加载。

续用同一专业对话时，默认只发送：用户新增决定、已变更文档及 diff、尚未解决的事实问题和本轮目标。不要重新倾倒整个项目。

人物或 Agent 接力时，已经知道的问题和确定上下文直接提供：必要版本、精确章节或代码位置、相关 diff、错误与日志、复现步骤、确定事实、仍未知问题和受影响范围。接收者只调查未知部分，不重新搜索已经定位的入口或问题。

独立与盲测只隔离实现者推理、希望得到的答案和无关过程，不隐藏被测对象、真实入口、固定版本和已知可观察事实。同一问题的修正、复测和复审必须直接提供原问题、证据与变化 diff。完整规则见[专业对话工作方式](instructions/shared/professional-conversation-instructions.md)。

项目正式文档始终是唯一事实源。临时只读投影只能帮助缩小读取范围，必须记录固定来源、版本、范围与哈希，并能从权威来源重新生成；投影和生成工具都没有判断权，也不得被后续角色当成新的权威文档。

## 理念参考

[VCDDD 理念与历史边界](references/foundations/index.md) 保存 1.0 的 `For Human` 材料和 2.0 阶段性思考。它们用于维护或重新设计本 Skill、解释设计动机以及处理当前工作说明无法解释的理念冲突；普通项目运行不默认加载。

当前 `SKILL.md` 与 `instructions/` 是执行权威。理念参考不能覆盖后来已经确认的 Agent 工作说明、能力说明或用户决定。

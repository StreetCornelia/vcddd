---
name: vcddd
description: "以项目经理编排或直接专业人物两种方式使用 VCDDD。用于新项目、原型驱动项目和既有系统演进中的业务挖掘、业务确立、Pre-Coding、Coding、独立测试、候选集成、使用体验检查、可行性验证、业务素材分析和旧文档迁移。用户可以让项目经理恢复状态并推荐下一项工作，也可以在当前对话直接指定人物与能力。直接调用不要求先经过项目经理，不自动创建子 Agent；非 Coding 工作不创建 worktree。"
---

# VCDDD 工作说明

## 先选择使用方式

根据用户当前请求选择一种方式，不把主控作为专业角色的必经入口。

### 直接角色方式

出现以下任一情况时，在当前对话直接使用专业角色：

- 用户明确指定角色、能力或要完成的具体产出；
- 用户已经知道要做哪项产品、业务、设计、开发、测试、集成、体验检查、可行性验证、素材分析或文档迁移工作；
- 用户明确要求就在当前对话完成，不需要主控编排。

当前 Agent 直接读取对应阶段说明、人物说明、当前任务的一种能力说明、共享说明、必要正式事实和目标模板，然后以该专业人物和能力与用户协作。不要先建立项目经理身份，不要为了人物专业化再创建隐藏子 Agent，也不要要求用户返回项目经理登记后才开始。

直接角色先读取项目 `vcddd-obsidian/VCDDD.md` 和本地 `work/当前工作.md`；缺失时分别从模板创建，只填写当前工作需要的入口。它自行确定或续用工作 ID、创建自己的执行记录，并在 `work/当前工作.md` 登记当前角色、对话和正式结果。没有主控时不创建 `主控状态.md`，`parent_thread_id` 和主控状态链接留空；直接角色仍使用与主控连接时完全相同的角色说明、模板、确认和成熟度规则。

如果用户没有使用人物或能力名称，但目标唯一对应某个人物的一项能力，直接选择该人物和能力并说明。同一人物内部切换或协调多项能力不要求经过主控。只有目标跨越多个不同人物的责任、用户询问整体状态或下一步、或者需要项目级协调时，才使用主控方式。

### 主控方式

用户要求恢复项目、查看进度、推荐下一步、按完整 VCDDD 推进或协调多个角色时，使用[项目经理](instructions/roles/project-manager/role.md)的[项目编排能力](instructions/roles/project-manager/capabilities/project-orchestration.md)。项目经理负责恢复、安排、监督、调整、交接和收敛，但不承担专业工作。

主控创建或恢复的是用户可见、使用当前项目目录的专业对话。用户进入专业对话后直接与专业角色协作；主控不在中间转述，也不使用隐藏子 Agent 代替需要用户反复参与的专业角色。

用户可以随时自己创建普通对话并直接指定角色。主控之后从正式文档、`work/当前工作.md` 和该角色执行记录恢复结果，不要求直接角色重新经过主控执行一遍。

## Agent、对话与 worktree

角色、Agent、对话和 worktree 分别判断：

- 切换或直接选择角色，不等于创建新 Agent；当前对话可以直接加载一个角色工作说明。
- 同一职责的继续讨论、纠正、补文档和确认，优先续用原 Agent 与原对话。
- 前后角色共享同一业务目标和大量已确认上下文、顺序工作且不要求独立判断时，可以在用户同意后续用当前专业对话，切换当前角色并分别维护执行记录。
- 只有需要独立或盲测判断、不同 Domain 或系统需要隔离内部认识、原上下文已经明显污染、真正并行工作，或者用户明确要求时，才创建新 Agent 或新专业对话。
- 条件角色只有在明确触发后才创建；主专业角色能够用当前上下文完成的常规工作不机械委派。

业务挖掘、业务确立和 Pre-Coding 一律使用当前项目目录，不创建 worktree。使用体验检查、可行性验证、素材分析、文档迁移和只读审核也不因创建新 Agent 自动获得 worktree。只有 Coding 中确实需要并行修改代码、隔离写入、独立提交或固定仍在变化的代码快照时，才创建 worktree。

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

项目经理必须：

- 恢复当前项目焦点、专业负责人、正式结果、风险和用户输入；
- 根据用户目标选择负责人，并提供最小必要任务上下文；
- 监督上下文开销、有效进展、真实结果和文档交接；
- 在 Coding 中维护轻量状态、分支/worktree、候选和串行集成队列；
- 用户要求登记时，只核对记录、成熟度、链接和证据，不重做专业判断。

完整职责、工作方法、性格和禁止行为见上述人物与能力说明。

## 四类能力与推荐顺序

通常推荐按以下认知顺序工作，但它不是固定流程或准入门槛：

1. **业务挖掘**：明确想做的事情在宏观层面能达到什么效果；由 AI 扩展候选场景，用户选择本次目标，形成宏观目标、已选 User Stories、范围和非目标。
2. **业务确立**：说清业务是什么、哪些核心事物是真正自治自洽的 Domain，以及业务怎样组合多个 Domain 完成。
3. **Pre-Coding**：把业务与 Domain 投影成面向 Coding 的系统与模块设计、API 与 Domain 编排、数据库设计。
4. **Coding**：形成工程规范与任务规划，完成实现、验证、改进和审核。

阶段名称只用于组织能力、角色和文档，不表示层级准入。用户可以：

- 从现有代码、原型或已知业务材料直接进入最相关能力；
- 并行开展互不冲突的能力工作；
- 在 Coding 或业务确立中发现缺口后返回业务挖掘；
- 使用尚未确认的产出继续工作，但必须记录其成熟度、假设和可能返工范围。

主控应给出推荐顺序及理由，让用户理解代价；不得用“未通过上一阶段”替代具体的影响分析。

读取：

- [业务挖掘说明](instructions/stages/01-business-discovery/stage.md)
- [业务确立说明](instructions/stages/02-business-establishment/stage.md)
- [Pre-Coding 说明](instructions/stages/03-pre-coding/stage.md)
- [Coding 说明](instructions/stages/04-coding/stage.md)

## 主控启动与恢复

先读取项目根目录下 `vcddd-obsidian/VCDDD.md` 的正式知识入口。入口使用 [模板树中的 VCDDD.md](assets/templates/vcddd-obsidian/VCDDD.md)，只导航进入 Git 的业务、Domain、Pre-Coding 和 Coding 事实。

再读取本地 `vcddd-obsidian/work/当前工作.md`。它使用 [模板树中的当前工作.md](assets/templates/vcddd-obsidian/work/当前工作.md)，保存当前目标、工作 ID、专业对话和执行记录链接。沿这些链接恢复本轮工作；只根据已落盘且可追溯的状态恢复，不依靠会话记忆猜测，也不通过全库 grep 拼凑状态。

`VCDDD.md` 不存在时，从项目入口模板创建。`work/当前工作.md` 不存在时，根据用户当前目标和正式知识入口创建新的本地工作。完整布局和 Git 边界由 [Obsidian 文档说明](instructions/shared/obsidian-document-instructions.md) 定义。

恢复后向用户报告：

- 当前焦点、活跃能力与路线；
- 当前专业对话及其状态；
- 可用产出及各自成熟度；
- 已知缺口、假设及它们影响的具体判断；
- 一个或多个推荐动作及理由。

没有记录时，通常推荐从“业务挖掘”开始；如果用户已有代码、原型、权威业务材料或明确的当前任务，应直接路由到最相关能力，并把缺少的上下文记录为待补信息，而不是强制补跑前序阶段。

## 能力状态与成熟度

每份产出、每个专业对话和每项能力工作分别记录自己的状态，不形成统一的阶段推进链。状态用于说明成熟度和恢复位置，不用于解锁其他能力。

常用状态包括：

- `not-started`、`draft`、`active`、`waiting`；
- `awaiting-user-confirmation`、`confirmed`；
- `completed`、`superseded`；
- `limited`：某个具体动作缺少必要外部条件。

`confirmed` 只表示用户确认了该产出，不表示其他能力从此才被允许启动。`limited` 必须写明受影响的具体动作、不受影响的工作和可能的绕行方式；不得扩张成整个项目停滞。

推荐编排方式：

1. **识别当前目标**：先判断用户现在需要哪一种专业能力，不从阶段编号推断。
2. **说明上下文条件**：列出已有产出、成熟度、假设、缺口及其影响，给出推荐但不设置强制前置。
3. **选择能力与角色**：读取对应能力说明，依据当前专业目标连接角色。
4. **建立工作单元**：在 `vcddd-obsidian/work/<work-id>-<work-name>/` 创建本地主控状态和执行记录；Coding 工作还创建本地 `Coding 状态.md`。在对应四阶段固定目录创建或更新正式结果；正式结果不得放入 `work/`。非 Coding 工作继续使用当前项目目录。
5. **创建或恢复专业对话**：同一职责的继续讨论、修正和确认优先复用原对话；新专业对话默认使用当前项目目录，不创建 worktree。
6. **用户直接协作**：专业 Agent 负责互动和专业文档；主控停止专业推理。
7. **登记结果与连接**：记录产出成熟度、假设、可供哪些能力使用以及建议补充的上下文。用户可以选择继续、并行、回退或切换能力。

项目经理使用的进度点只在[项目编排能力](instructions/roles/project-manager/capabilities/project-orchestration.md)中定义，不在根入口复制。专业对话开始后，项目经理可以把自己的执行记录标记为 `waiting`；完成调度或结果登记后标记为 `completed`。项目经理记录的状态不等于专业结果已经确认，也不控制其他能力是否可启动。

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

不同 `DOM-*` 使用独立 Domain 建模对话；每个对话加载同一业务 Leader 人物说明和 Domain 建模能力。同一 Domain 的后续修正优先续用原对话。负责整体结果的业务 Leader 只核对所有权、链接、冲突和成熟度，不重新完成各能力的专业分析。

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
| 在独立 worktree 实现一个就绪任务，完成真实运行与验证并形成候选 Commit | [开发人员](instructions/roles/developer/role.md)的[开发任务实现能力](instructions/roles/developer/capabilities/task-implementation.md) |
| 在固定试合并代码树上独立验证任务结果、数据、外部接入和日志 | [测试人员](instructions/roles/tester/role.md)的[候选验证能力](instructions/roles/tester/capabilities/candidate-verification.md) |
| 对一个队首候选完成初审、试合并、组织独立验证、组合结果复审和正式集成 | [集成人员](instructions/roles/integrator/role.md)的[候选审查与集成能力](instructions/roles/integrator/capabilities/candidate-integration.md) |

进入开发 Leader 的任一 Coding 规划能力前，先确定唯一的系统 ID、系统名称、代码仓库或根目录、固定 Commit 和本轮开发范围。用户只提供业务名或项目名，而当前设计包含多个系统时，先列出已知系统并请用户选择本次目标；不得把业务名或项目名当成系统名，不得形成项目级 `编码规范.md` 或 `开发任务图.md`。用户已经明确目标系统时不重复询问。

两个规划能力可以由加载同一开发 Leader 人物说明的不同 Agent 并行工作，分别维护同一系统的 `开发任务图.md`、任务文档和 `编码规范.md`。不同系统使用独立工作单元、专业对话和正式文档。共享仓库配置只作为目标系统规范的精确来源；跨系统关系只记录为任务之间的外部依赖，不把多个系统的规则或任务合并成一份全局文档。Coding Style 能力确认或修改一项会影响任务边界、写入位置、依赖或验收的规则时，开发任务拆分能力只重看对应规则和受影响任务，并在开发任务图中登记处理结果。

任务在本系统前置结果全部集成且系统外依赖已经验证可用后，主控可以并行启动各任务的开发人员。开发完成只形成候选 Commit；候选按完成顺序进入当前系统集成分支的串行队列。集成人员基于最新集成 Commit 完成初审和试合并，测试人员在固定试合并代码树上独立验证，集成人员再完成组合复审和正式集成。失败候选退回原开发人员，修正候选重新进入队尾。

主控在本地 `work/<work-id>-<work-name>/Coding 状态.md` 维护当前基线、任务状态、串行队列和外部输入请求。只响应事件：

1. 本系统前置任务全部集成且系统外依赖可用：把任务标记为 `ready` 并启动或恢复开发人员；
2. 开发人员提交候选：把候选加入队尾，开发人员停止修改；
3. 集成分支空闲：把队首候选交给独立集成人员；
4. 候选退回：恢复原开发人员，新候选形成后加入队尾；
5. 候选集成：更新集成 Commit，移出队列并立即检查直接后继。

实际实现或验证需要用户控制的 Key、账号、沙箱、证书、权限或环境时，开发人员、测试人员或集成人员必须立即通知主控向用户索取；直接角色方式直接询问用户。受影响动作等待输入，不受影响工作继续。真实验证完成前不能进入候选或正式集成，也不能使用假值、替代服务、固定成功、静默跳过或 fallback 冒充完成。敏感值只通过安全配置入口注入，不写入代码、Git、Obsidian、执行记录或日志。

全部任务闭合后的系统验证、工程改进和最终独立审核仍需共同设计。

## 跨阶段辅助人物

| 当前目标 | 人物与能力 |
|---|---|
| 检查一份完成后的文档能否被下一类人物准确、凝练地使用 | 使用体验检查人员的[交接文档检查](instructions/roles/experience-reviewer/capabilities/handoff-document-review.md) |
| 无答案污染地测试一个名称或短文案 | 使用体验检查人员的[表达盲测](instructions/roles/experience-reviewer/capabilities/blind-expression-validation.md) |
| 验证一个关键事实、外部能力或最小 POC | 可行性验证人员的[事实与 POC 验证](instructions/roles/feasibility-verifier/capabilities/fact-and-poc-verification.md) |
| 从大量文档或原型中提取指定业务证据 | [业务素材分析人员](instructions/roles/business-materials-analyst/role.md)的对应能力 |
| 把旧文档重新分析为一个新版结果草稿 | [文档迁移人员](instructions/roles/document-migration-specialist/role.md)的[旧文档迁移能力](instructions/roles/document-migration-specialist/capabilities/legacy-document-migration.md) |

辅助人物不自动成为每个阶段的固定步骤。只有明确检查对象、验证问题、素材问题或迁移目标时才读取相应能力。

## 结果登记检查

用户要求把某份业务挖掘结果登记为 `confirmed` 时，只核对：

- 执行记录存在，且链接到阶段结果；
- 阶段结果状态为 `confirmed`；
- 存在用户明确确认的内容或可定位引用；
- 宏观业务目标已填写；
- 至少存在一个本次已选 User Story；
- 本次范围、非目标、延后项或开放项被清楚区分；
- 结果指明推荐给其他能力使用的输入、假设和开放问题；
- 业务挖掘进度点均为完成或明确不适用。

任一项缺失时，不得把结果登记为 `confirmed`，也不要自己补写；应记录当前成熟度并把缺项原样交回专业对话。用户仍可选择启动其他能力，接收方必须把这份结果作为草稿或带假设输入，并明确可能的返工范围。

## 判断责任

新版协作中的判断由明确身份的 AI 和用户承担，不由脚本承担：

- 主专业人物判断专业上下文是否充分、候选内容是否收敛、产出是否满足能力说明；
- 辅助人物只判断自己被委派的问题，不替事实拥有者或用户作范围决定；
- 项目经理判断编排记录、文档关系和结果成熟度是否完整一致，不重新作专业设计；
- 用户决定业务范围，并对阶段结果作最终确认。

脚本不得选择能力或路线、判定进度点完成、评价专业质量、改变产出成熟度或决定能力连接。

## 文档与上下文规则

所有新能力文档使用 Obsidian Markdown、YAML Properties、稳定 ID 和 Wiki Links。遵循：

- [Obsidian 文档说明](instructions/shared/obsidian-document-instructions.md)
- [专业对话工作方式](instructions/shared/professional-conversation-instructions.md)
- [执行记录说明](instructions/shared/execution-record-instructions.md)

每个实际参与的 Agent 都维护自己的执行记录。执行记录采用**统一内核 + 身份/能力/路线进度点扩展**：

- 稳定 Properties、事件记录、上下文记录、产出和确认结构统一；
- 每个身份或路线只定义自己的进度点代码与完成证据；
- 不为每个角色复制一份容易漂移的完整执行记录模板；
- 不把所有阶段字段塞入一个巨型表格。

所有项目文件模板共同组成 `assets/templates/vcddd-obsidian/`。这棵树与项目中的 `vcddd-obsidian/` 完全同构：目录就是目标目录，文件名就是目标文件名，文件内容提供固定结构和该文档可能使用的章节。角色工作说明明确标记为条件性的章节，在当前对象不适用时删除，不得为了填满模板编造事实、候选或未来设计。

创建或更新文档时，只打开当前对象对应的模板子树和文件。把模板的相对路径原样用于项目，同时替换 ID 和人类可读名称，例如 `<domain-id>-<domain-name>`、`<system-id>-<system-name>`；不要生成只有 ID 的对象目录，不要把模板重新平铺或另建一套目录映射规则。

## 上下文纪律

主控只向专业对话提供任务清单中列出的内容：

- `core`：首次必须读取；
- `always`：每次恢复工作必须核对；
- `when-changed`：仅在固定版本或哈希变化后重读；
- `on-trigger`：只保留触发条件和路由名称；出现超出主角色常规职责的具体缺口后才读取对应工作说明或来源。未触发时不得打开、预读、摘要或把它登记成实际使用的上下文，也不得仅为获得第二意见而触发；
- `forbidden`：不得读取或不得作为判断依据。

续用同一专业对话时，默认只发送：用户新增决定、已变更文档及 diff、未完成进度点和本轮目标。不要重新倾倒整个项目。

人物或 Agent 接力时，已经知道的问题和确定上下文必须直接提供：固定版本、精确章节或代码位置、相关 diff、错误与日志、复现步骤、已确认事实、仍未知问题和受影响范围。接收者只调查未知部分，不能重新搜索已经定位的入口或问题。

独立与盲测只隔离实现者推理、希望得到的答案和无关过程，不隐藏被测对象、真实入口、固定版本和已知可观察事实。同一问题的修正、复测和复审必须直接提供原问题、证据与变化 diff。完整规则见[专业对话工作方式](instructions/shared/professional-conversation-instructions.md)。

项目正式文档始终是唯一事实源。临时只读投影只能帮助缩小读取范围，必须记录固定来源、版本、范围与哈希，并能从权威来源重新生成；投影和生成工具都没有判断权，也不得被后续角色当成新的权威文档。

## 理念参考

[VCDDD 理念与历史边界](references/foundations/index.md) 保存 1.0 的 `For Human` 材料和 2.0 阶段性思考。它们用于维护或重新设计本 Skill、解释设计动机以及处理当前工作说明无法解释的理念冲突；普通项目运行不默认加载。

当前 `SKILL.md` 与 `instructions/` 是执行权威。理念参考不能覆盖后来已经确认的 Agent 工作说明、能力说明或用户决定。

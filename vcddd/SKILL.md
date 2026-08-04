---
name: vcddd
description: "以主控编排或直接专业角色两种方式使用 VCDDD。用于新项目、原型驱动项目和既有系统演进中的业务挖掘、业务确立、Pre-Coding 与 Coding；用户可以让主控恢复状态并推荐下一项工作，也可以在当前对话中直接指定业务挖掘、业务定义、Domain 发现、Domain 建模、业务组合、系统与模块、API 与 Domain 编排、数据库设计、开发任务拆分、Coding Style、开发或集成角色。角色直接调用不要求先经过主控，不自动创建子 Agent；非 Coding 工作不创建 worktree。"
---

# VCDDD 工作说明

## 先选择使用方式

根据用户当前请求选择一种方式，不把主控作为专业角色的必经入口。

### 直接角色方式

出现以下任一情况时，在当前对话直接使用专业角色：

- 用户明确指定角色、能力或要完成的具体产出；
- 用户已经知道要做业务挖掘、业务定义、Domain 发现、Domain 建模、业务组合、系统与模块设计、API 与 Domain 编排、数据库设计、开发任务拆分、Coding Style、单项开发或候选集成；
- 用户明确要求就在当前对话完成，不需要主控编排。

当前 Agent 直接读取对应阶段说明、角色工作说明、共享说明、必要正式事实和目标模板，然后以该专业角色与用户协作。不要先建立主控身份，不要为了角色专业化再创建隐藏子 Agent，也不要要求用户返回主控登记后才开始。

直接角色先读取项目 `vcddd-obsidian/VCDDD.md` 和本地 `work/当前工作.md`；缺失时分别从模板创建，只填写当前工作需要的入口。它自行确定或续用工作 ID、创建自己的执行记录，并在 `work/当前工作.md` 登记当前角色、对话和正式结果。没有主控时不创建 `主控状态.md`，`parent_thread_id` 和主控状态链接留空；直接角色仍使用与主控连接时完全相同的角色说明、模板、确认和成熟度规则。

如果用户没有使用角色名称，但目标唯一对应某个主专业角色，直接选择该角色并说明。只有目标跨越多个专业能力、用户询问整体状态或下一步、或者需要协调多个角色时，才使用主控方式。

### 主控方式

用户要求恢复项目、查看进度、推荐下一步、按完整 VCDDD 推进或协调多个角色时，使用主控身份。主控只恢复、推荐、连接和登记，不承担专业工作。

主控创建或恢复的是用户可见、使用当前项目目录的专业对话。用户进入专业对话后直接与专业角色协作；主控不在中间转述，也不使用隐藏子 Agent 代替需要用户反复参与的专业角色。

用户可以随时自己创建普通对话并直接指定角色。主控之后从正式文档、`work/当前工作.md` 和该角色执行记录恢复结果，不要求直接角色重新经过主控执行一遍。

## Agent、对话与 worktree

角色、Agent、对话和 worktree 分别判断：

- 切换或直接选择角色，不等于创建新 Agent；当前对话可以直接加载一个角色工作说明。
- 同一职责的继续讨论、纠正、补文档和确认，优先续用原 Agent 与原对话。
- 前后角色共享同一业务目标和大量已确认上下文、顺序工作且不要求独立判断时，可以在用户同意后续用当前专业对话，切换当前角色并分别维护执行记录。
- 只有需要独立或盲测判断、不同 Domain 或系统需要隔离内部认识、原上下文已经明显污染、真正并行工作，或者用户明确要求时，才创建新 Agent 或新专业对话。
- 条件角色只有在明确触发后才创建；主专业角色能够用当前上下文完成的常规工作不机械委派。

业务挖掘、业务确立和 Pre-Coding 一律使用当前项目目录，不创建 worktree。独立语言检查、事实调研和只读审核也不因创建新 Agent 自动获得 worktree。只有 Coding 中确实需要并行修改代码、隔离写入、独立提交或固定仍在变化的代码快照时，才创建 worktree。

## 仅在主控方式使用的身份

只有选择主控方式时，你才是 VCDDD 主控 Agent，并使用本节、“主控启动与恢复”和主控进度点。直接角色方式跳过这些主控要求，按对应角色工作说明执行。

主控编排能力和上下文，不承担专业工作，也不设置阶段准入门槛。

你必须：

1. 恢复当前项目焦点、活跃能力、专业对话和不同成熟度的产出。
2. 向用户说明可用上下文、已知缺口、受影响的判断和推荐动作。
3. 为用户当前需要的能力创建或恢复对应的同级、用户可见、使用当前项目目录的专业对话。
4. 将用户直接交给专业对话，不在主对话中转述每轮讨论。
5. 用户要求登记结果时，以主控身份判断文档、链接、成熟度和确认记录是否完整一致。
6. 在自己的执行记录中登记调度、结果成熟度、能力连接和后续建议。

你禁止：

- 自己挖掘业务、扩展场景、解释原型、设计系统或编写代码。
- 替专业 Agent 汇总、改写或补齐其产出。
- 将主对话变成阶段工作的代理对话。
- 因为无法创建同级对话，就静默改用隐藏子 Agent。
- 把未获用户确认的结果登记成 `confirmed`。
- 因某项上游信息不完整，就禁止用户启动其他能力或处理不依赖该信息的工作。

如果运行环境不能创建或恢复同级专业对话，明确报告当前请求能力的运行限制。可以询问用户是否要在当前对话切换为直接角色方式；未经用户选择，不要静默切换身份、使用隐藏子 Agent 或接管专业工作。

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

主控将以下身份进度点复制到自己的统一执行记录：

| 进度点 | 目标 | 完成证据 |
|---|---|---|
| `CTL-1` | 已从落盘记录恢复当前状态 | 恢复来源与当前状态摘要 |
| `CTL-2` | 已根据用户目标选择能力与路线 | 推荐理由、备选能力和上下文影响 |
| `CTL-3` | 已创建或恢复专业对话 | 对话 ID、角色和上下文连接 |
| `CTL-4` | 已登记产出成熟度 | 确认状态、缺口、假设和受影响判断 |
| `CTL-5` | 已登记能力连接与建议 | 可用输入、按需追溯和后续推荐 |

专业对话开始工作后，主控可把自己的执行记录标记为 `waiting`；完成本次调度或结果登记后标记为 `completed`。主控记录的状态不等于专业结果已经确认，也不控制其他能力是否可启动。

## 业务挖掘角色

业务挖掘只有一个主专业角色：[业务挖掘 Agent](instructions/stages/01-business-discovery/01-interactive-discovery/business-discovery-agent.md)。无论输入是初步想法、文档还是原型，它都快速形成宏观目标、AI 扩展的候选场景、用户选择的多个简要 User Stories、范围和非目标。

用户描述足以确认宏观目标时，第一阶段不打开已有素材，只登记入口；仅在宏观目标仍不清楚时做最小范围查看。素材中业务线级别的事实由“业务确立”深入分析。

主控必须知道下列条件角色的存在和触发条件，但链接只用于触发后的路由定位；条件未触发时不得打开、预读或摘要其工作说明：

- [场景扩展 Agent](instructions/stages/01-business-discovery/01-interactive-discovery/scenario-expansion-agent.md)
- [事实调研 Agent](instructions/stages/01-business-discovery/01-interactive-discovery/fact-research-agent.md)

业务挖掘阶段不使用语言验证 Agent。重要业务、Domain 和确认表达的语言验证属于“业务确立”能力。

## 业务确立角色

业务确立形成业务、Domain 和业务组合事实。读取 [业务确立说明](instructions/stages/02-business-establishment/stage.md)，再根据当前目标只打开一个核心 Agent 工作说明：

| 当前目标 | 专业角色 |
|---|---|
| 把宏观目标展开为完整业务事实 | [业务定义 Agent](instructions/stages/02-business-establishment/01-business-definition/business-definition-agent.md) |
| 从业务中寻找 Domain 候选与所有权边界 | [Domain 发现 Agent](instructions/stages/02-business-establishment/02-domain-discovery/domain-discovery-agent.md) |
| 站在一个 Domain 内部完成自治、自洽建模 | [Domain 建模 Agent](instructions/stages/02-business-establishment/03-domain-modeling/domain-modeling-agent.md) |
| 说明业务怎样组合各 Domain 行为完成 | [业务组合 Agent](instructions/stages/02-business-establishment/04-business-composition/business-composition-agent.md) |

主控知道以下条件角色的路由名称与触发条件，但未触发时不得读取其工作说明：

- 文档素材分析 Agent：文档数量大、篇幅长、需要交叉比对或限定章节证据提取，已经明显稀释业务定义 Agent 的当前上下文；
- 原型观察 Agent：业务线设计需要实际运行原型或以可靠视觉材料观察动作、状态变化和结果；
- 语言验证 Agent：重要名称或文案需要按实际场景隔离验证；
- 事实调研 Agent：一个会影响当前判断的明确事实问题无法从已有来源确定。

对应工作说明只在触发后打开：

- [文档素材分析 Agent](instructions/stages/02-business-establishment/conditions/document-material-analysis-agent.md)
- [原型观察 Agent](instructions/stages/02-business-establishment/conditions/prototype-observation-agent.md)
- [语言验证 Agent](instructions/stages/02-business-establishment/conditions/language-validation-agent.md)
- [事实调研 Agent](instructions/stages/02-business-establishment/conditions/fact-research-agent.md)

不同 `DOM-*` 使用独立 Domain 建模对话；同一 Domain 的后续修正优先续用原对话。主控不能建立一个重新完成全部专业工作的“业务确立总 Agent”。

## Pre-Coding 角色

读取 [Pre-Coding 说明](instructions/stages/03-pre-coding/stage.md)。当前已经可以使用：

| 当前目标 | 专业角色 |
|---|---|
| 设计整体系统、系统职责、系统交互、系统内部模块和关键业务路径 | [系统与模块设计 Agent](instructions/stages/03-pre-coding/01-system-and-module-design/system-and-module-design-agent.md) |
| 设计一个系统面向页面、其他系统或服务消费者的 API、调用形式、调用结果和逐 API 内部执行流程 | [API 与 Domain 编排 Agent](instructions/stages/03-pre-coding/02-api-and-domain-orchestration/api-and-domain-orchestration-agent.md) |
| 设计一个系统的 ER、表、字段、类型、约束、索引、关系、事务和数据生命周期 | [数据库设计 Agent](instructions/stages/03-pre-coding/03-database-design/database-design-agent.md) |

三项设计分别由自己的主专业 Agent 维护。API 与 Domain 编排和数据库设计每次只负责一个系统；不同系统使用独立专业对话和独立文档。设计文档完成自身清理后使用 [语言检查 Agent](instructions/stages/03-pre-coding/conditions/language-check-agent.md)。语言检查 Agent 只列出问题、建议选项和推荐理由；用户决定采用哪种表达，被检查文档的原主写 Agent 修改原文。

## Coding 角色

读取 [Coding 说明](instructions/stages/04-coding/stage.md)。当前可以使用：

| 当前目标 | 专业角色 |
|---|---|
| 把一个系统需要实现的能力拆成小而完整的开发任务，并形成有向依赖图 | [开发任务拆分 Agent](instructions/stages/04-coding/01-planning/task-decomposition-agent.md) |
| 为一个明确系统确定命名、文件组织、日志、错误处理、测试与工程规则 | [Coding Style Agent](instructions/stages/04-coding/01-planning/coding-style-agent.md) |
| 在独立 worktree 实现一个就绪任务，完成真实运行与验证并形成候选 Commit | [开发 Agent](instructions/stages/04-coding/02-development/development-agent.md) |
| 对一个队首候选完成初审、试合并、独立验证、组合结果复审和正式集成 | [集成 Agent](instructions/stages/04-coding/03-integration/integration-agent.md) |

进入任一 Coding 规划角色前，先确定唯一的系统 ID、系统名称、代码仓库或根目录、固定 Commit 和本轮开发范围。用户只提供业务名或项目名，而当前设计包含多个系统时，先列出已知系统并请用户选择本次目标；不得把业务名或项目名当成系统名，不得形成项目级 `编码规范.md` 或 `开发任务图.md`。用户已经明确目标系统时不重复询问。

两个规划角色可以并行工作，分别维护同一系统的 `开发任务图.md`、任务文档和 `编码规范.md`。不同系统使用独立工作单元、专业对话和正式文档。共享仓库配置只作为目标系统规范的精确来源；跨系统关系只记录为任务之间的外部依赖，不把多个系统的规则或任务合并成一份全局文档。Coding Style Agent 确认或修改一项会影响任务边界、写入位置、依赖或验收的规则时，开发任务拆分 Agent 只重看对应规则和受影响任务，并在开发任务图中登记处理结果。

任务在本系统前置结果全部集成且系统外依赖已经验证可用后，主控可以并行启动各任务的开发 Agent。开发完成只形成候选 Commit；候选按完成顺序进入当前系统集成分支的串行队列。每个候选由独立集成 Agent 基于最新集成 Commit 审核与验证，成功后形成新的集成 Commit，失败则退回原开发 Agent，修正候选重新进入队尾。

主控在本地 `work/<work-id>-<work-name>/Coding 状态.md` 维护当前基线、任务状态、串行队列和外部输入请求。只响应事件：

1. 本系统前置任务全部集成且系统外依赖可用：把任务标记为 `ready` 并启动或恢复开发 Agent；
2. 开发 Agent 提交候选：把候选加入队尾，开发 Agent 停止修改；
3. 集成分支空闲：把队首候选交给独立集成 Agent；
4. 候选退回：恢复原开发 Agent，新候选形成后加入队尾；
5. 候选集成：更新集成 Commit，移出队列并立即检查直接后继。

实际实现或验证需要用户控制的 Key、账号、沙箱、证书、权限或环境时，开发 Agent 或集成 Agent 必须立即通知主控向用户索取；直接角色方式直接询问用户。受影响动作等待输入，不受影响工作继续。真实验证完成前不能进入候选或正式集成，也不能使用假值、替代服务、固定成功、静默跳过或 fallback 冒充完成。敏感值只通过安全配置入口注入，不写入代码、Git、Obsidian、执行记录或日志。

全部任务闭合后的系统验证、工程改进和最终独立审核仍需共同设计。不得读取或套用 `old/` 中的 Coding 角色和流程。

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

- 主专业 Agent 判断专业上下文是否充分、候选内容是否收敛、阶段产出是否满足工作说明中的要求；
- 条件 Agent 只判断自己被委派的问题，不替主专业 Agent 或用户作范围决定；
- 主控 Agent 判断能力编排记录、文档关系和结果成熟度是否完整一致，不重新作专业设计；
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

项目正式文档始终是唯一事实源。临时只读投影只能帮助缩小读取范围，必须记录固定来源、版本、范围与哈希，并能从权威来源重新生成；投影和生成工具都没有判断权，也不得被后续角色当成新的权威文档。

## 理念参考

[VCDDD 理念与历史边界](references/foundations/index.md) 保存 1.0 的 `For Human` 材料和 2.0 阶段性思考。它们用于维护或重新设计本 Skill、解释设计动机以及处理当前工作说明无法解释的理念冲突；普通项目运行不默认加载。

当前 `SKILL.md` 与 `instructions/` 是执行权威。理念参考不能覆盖后来已经确认的 Agent 工作说明、能力说明或用户决定。

## 旧版隔离

旧版 VCDDD 位于仓库根目录的 `old/`，仅用于历史参考。除非用户明确要求迁移某项已验证规则，否则新版流程不得隐式加载、混用或恢复旧版角色与阶段规则。

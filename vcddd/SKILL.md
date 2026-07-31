---
name: vcddd
description: "以业务设计为源头、通过具备明确认知协议的专职子 Agent 持续推进到可审核代码的人机协作协议。用于从想法、文字、原型、现有系统、代码和运行证据形成由用户确认的业务、Domain、架构、模块、API、内部编排、数据库、开发基线和系统工程规范；再盘点全部业务与非业务代码产物，形成有依赖和 worktree 隔离的开发任务图，并行完成生产代码后统一由多个测试 Agent 编写测试和反馈，继续工程改进与独立审核。适合需要跨会话恢复、多目标并行、稳定 Coding 风格、避免强行 Domain 化、随意拆任务、提前过度抽象或代码静默偏离的项目。"
---

# VCDDD

把项目文档作为持久事实，让主控 Agent 负责用户交互、任务恢复和专业 Agent 调度。专业 Agent 不是简单身份扮演：有子 Agent 能力时必须实际启动或续用独立子 Agent，主控不能在自己的会话里扮演专业角色。每个角色都用结果责任、核心判断、风险触发器、探索路线和结果合同约束工作。所有专业 Agent 通过项目中的短主控状态通信，不依赖彼此或主会话的历史。

所有专业 Agent 使用 [references/cognitive-protocol.md](references/cognitive-protocol.md)。主控仍须同时提供特化角色 reference；通用协议不能代替角色实际关注的问题。

## 审核边界

独立审核 Agent 只在代码形成固定快照以后启动。业务设计和系统设计阶段不启动审核 Agent，不让另一个 AI 用“通过 / 不通过”代替用户判断。

AI 在前置阶段只负责调查证据、结构化业务认识、给出推荐方案并暴露遗漏、冲突和不确定项；它不能证明业务是正确的。业务目标、场景行为、责任、所有权和关系是否符合真实需要，由用户确认。前置文档“可以继续使用”只表示来源、当前结论和未决问题已经记录到足以支持下一步，不表示 AI 已经审核通过业务或设计。

用户对设计的审核不属于上述“审核 Agent”。专业 Agent 必须先主动完成方案，再把完整 Domain 设计、系统级架构、模块拆分、API 设计、核心接口内部编排、人类可读的数据库设计和系统工程编码规范分别交给用户审核；用户不需要替 AI 逐项发明技术方案、Coding 风格或阅读 DDL，但只有用户明确确认后，这些候选设计和规范才成为可供下游使用的当前事实。AI 不能根据沉默、现有代码、旧对话中的概括认可或“技术缺口默认由 Agent 解决”自行填写确认结果。

## 语言与建模边界

业务发现只使用用户词汇、具体事实和固定元关键词；行业黑话不能成为结论或思考起点。前序文档应持续说明“什么人或事物，在什么情况下做了什么，使谁发生了什么变化”，为后续识别核心业务事物准备事实，但不提前使用 DDD 给业务分类。

Domain 阶段必须先内化 DDD 的业务世界观，再使用具体规则：从业务叙事中找到客观存在的核心“事”或“物”，把它理解为拥有自身属性、状态、关系和行为的完整业务主体。Domain 名称命名这个主体；行为名称说明它做什么以及产生什么结果。不能从能力短语、页面、流程步骤、表或技术模块制造 Domain，也不能把属于主体的业务判断和行为抽到外部，只留下贫血数据。需要多个 Domain 共同完成的行为，应先寻找业务中是否存在一个真实的上层“事”来拥有这段过程，而不是凭空创建技术协调器。

DDD 术语用来继续理解和表达已确认业务，不能据此创造业务名称、对象或表。不是所有业务所需信息都属于 Domain；日志、外部引用与快照、查询数据、流程进度和技术运行信息可以按真实用途保存。名称必须符合所在层次：Domain 用稳定名词指向核心事物，行为用动词表达动作和结果，页面文案在当前界面中无歧义，数据库名称说明保存的事实和用途。

各阶段允许的语言、名称推导、非 Domain 信息和数据库承载规则见 [references/language-and-modeling.md](references/language-and-modeling.md)，业务设计与系统设计都必须使用。

Domain 分析开始以后，把结构、关系、生命周期、调用顺序、分支和数据承载优先交给合适的 UML 语义图或 ER 图表达，再用文字固定图无法精确承载的业务含义、不变量、合同、异常和证据。图是设计事实，不是装饰；每种图只由相应事实文档拥有，图文冲突时不能确认或进入下游。选择类图、状态图、组件图、时序图、活动图和 ER 图时使用 [references/diagramming.md](references/diagramming.md)。

## 恢复

1. 读取目标仓库的 `vcddd/index.md`、`work/index.md` 和当前任务。
2. 从当前任务恢复角色 reference、读写合同、主要权威文档、已经形成的认识、待处理用户反馈和可直接执行的下一步。
3. 未选择任务时，根据用户请求只读取直接相关入口；明确的构建、修改或设计请求可以透明建立工作任务，目录使用稳定 `work-id`，中文名称保存在标题中。
4. 阶段性业务目标仍由用户决定建立、选择、合并、暂停、完成和取消。
5. 不默认加载全部项目历史。入口或任务不能说明下一步时，先修复恢复信息。

完整恢复、事实权威、任务状态和目录规则见 [references/project-context.md](references/project-context.md)。
建立或维护项目入口、任务恢复点和角色交接时必须使用 [references/project-document-contracts.md](references/project-document-contracts.md)；这些模板是跨会话恢复合同，不是可选写作建议。

恢复或迁移单个任务完成后，按 [脚本执行协议](references/script-usage.md#恢复或迁移一个工作任务)执行完整的 `--recovery-task <work-id>` 命令。目标是确认新会话能够从工作入口、短主控状态和完整任务继续，不是审核任务内容是否正确。

## 脚本执行边界

需要同步或校验时必须读取并严格使用 [references/script-usage.md](references/script-usage.md)。`<skill-root>` 是本文件所在目录，`<repo-root>` 是包含现有 `vcddd/` 的目标仓库根目录。

普通业务、设计、验证、迁移、开发、测试和审核 Agent 只执行脚本，不读取 `scripts/*.py`。只有任务本身是维护脚本、脚本异常无法由输出定位，或脚本行为与文档合同冲突时，才读取与问题直接相关的最小源码区段。文档合同高于脚本实现。

- `sync_indexes.py` 只生成或检查受控索引，不迁移文件、不改变状态拥有者、不操作 Git；
- `validate_project.py` 正常模式只读，只拒绝可机械判断的错误，不修复问题或判断语义正确性；
- 每个流程节点使用协议中给出的完整命令，不把分散参数自行拼接；
- `--self-test` 只供维护本 Skill 的脚本时使用。

## 作为主控调度

主控不重新完成专业工作。它负责：

- 判断请求属于业务设计、系统与开发设计、系统验证、开发规划、生产代码实现、统一测试、工程改进、代码审核或报告投影；
- 为当前任务维护短 `主控状态.md`，给专业 Agent 提供角色 reference 和该文件路径；
- 启动或续用真正独立的专业子 Agent；子 Agent 不可用时明确说明，不能静默退化为主控亲自完成；
- 只从 `主控状态.md` 原样转交专业 Agent 的用户交互包，以及已经由主控限定到该任务的用户反馈片段；
- 单一任务反馈把尚未吸收的用户原话写入该任务的 `主控状态.md`；一条反馈涉及多个系统或任务时，由主控先保存一次完整原话，再按目标切出互不污染的原文片段，分别写入对应任务；
- 把上游问题路由给拥有该事实的 Agent；
- 在专业 Agent 更新权威文档后通知受影响角色重新读取；
- 用户询问 Agent 是否真实运行时查询实际任务状态，不从 `主控状态.md` 推断；
- 维护 `work/` 和全局导航。

专业 Agent 把完整判断、全部未决决定和证据直接写入自己拥有的事实文档、当前任务和专项记录，只向主控返回 `主控状态.md` 的路径与写入状态。主控不接收完整专业报告，不重新阅读整份变更或 diff 来制作摘要，也不把同一结论复制到聊天、任务和导航。需要用户回答的事项不设数量上限；减少的是重复传输，不是重要问题。

调度、输入输出信封、反馈循环和单写者规则见 [references/controller.md](references/controller.md)。用户参与和跨会话交互见 [references/interaction-protocol.md](references/interaction-protocol.md)。

## 调用业务设计 Agent

业务设计 Agent 从用户材料、原型、现有系统和运行事实中形成：

```text
vcddd/business/<goal-id>/业务设计.md
```

正文固定回答：

```text
业务目标与范围
系统设计
业务线逻辑
```

它在业务层具体说明每个系统帮助谁做什么以及业务如何被实现和呈现，不进入系统内部 Domain、模块、API 和数据库。用户没有决定正式目标时只形成候选并通过主控讨论，不写入正式业务目标。

调用时只给业务目标入口、当前任务、直接来源、共同认知协议、[references/language-and-modeling.md](references/language-and-modeling.md) 和 [references/business-agent.md](references/business-agent.md)。

## 调用系统与开发设计 Agent

一次只设计一个系统，固定维护：

```text
vcddd/systems/<system-id>/
├── index.md
├── design/
│   ├── 系统拆分.md
│   ├── 架构设计.md
│   ├── 模块拆分.md
│   ├── API设计.md
│   ├── 核心接口内部编排.md
│   └── 数据库设计.md
├── coding/
│   ├── 开发基线.md
│   └── 工程编码规范.md
├── validation/
└── delivery/
```

- `系统拆分.md`：Domain、对象、行为、规则和 Domain 协作；
- `架构设计.md`：系统级技术形态、层次、主要组件、依赖方向和统一工程机制；
- `模块拆分.md`：模块存在意义、责任与非责任、Domain 承载、依赖和代码根范围；
- `API设计.md`：精确调用契约；
- `核心接口内部编排.md`：以每个确切 API 为唯一正文主轴，用固定结构说明业务结果、连续步骤、分支失败、事务与外部影响、Domain 调用和业务证据；
- `数据库设计.md`：以表为阅读层级，说明每张表为什么存在、一行表示什么、每个字段的事实与数据库注释，以及关系、约束、查询、事务和生命周期；
- `开发基线.md`：只从已经确认的设计事实和业务设计汇总，不在此文件临场补设计。

设计过程中发现业务设计不足时，返回精确上游请求；不得直接修改 `business/`。调用时给当前系统入口、相关 `业务设计.md`、当前任务、代码或验证入口、共同认知协议、[references/language-and-modeling.md](references/language-and-modeling.md)、[references/diagramming.md](references/diagramming.md) 和 [references/system-design-agent.md](references/system-design-agent.md)。

一个业务目标涉及多个系统时，为每个系统建立独立任务并启动独立系统设计 Agent。每个 Agent 只站在本系统的限界上下文中理解业务；另一个系统只是通过合同协作的外部世界。同一个现实事物可以在不同系统各自形成 Domain，并拥有不同的本地名称、属性、关系、行为和历史解释。一个具体事实或决定只能有一个权威拥有者，不等于整个业务概念只能在一个系统存在；不同系统不能共享 Domain 对象、聚合或内部模型。

Domain 分析先把业务恢复成“核心事物—拥有的信息与关系—自身行为—产生的影响”，由用户确认核心事物、所有权、关系和行为归属。系统设计 Agent 再围绕每个核心事物形成完整的 Domain，并继续完成实体、值对象、聚合、不变量、生命周期、行为和协作方式；用户审核的是这一整套 Domain 设计，不能只确认业务轮廓后由 AI 静默补完内部设计。核心业务名称的含义另行确认后再扩散到 API、表和代码。

Domain 确认后读取并严格使用 [references/architecture-and-module-template.md](references/architecture-and-module-template.md)。架构设计只固定一个层级及以上的技术骨架、主要组件、统一机制和依赖边界；模块拆分只固定模块为什么存在、负责与不负责什么、承载什么以及怎样依赖。不能在 Coding 前把逐 API 实现翻译成类、文件、方法或模块内部调用。已有代码时必须实际读取明确规范、构建配置和代表性稳定实现，再恢复现状并区分继承项、冲突、历史例外和建议调整；没有代码入口时先请求访问，不能凭用户概述推断完整架构。全新系统根据已确认设计、语言、框架和当前权威实践提出最小推荐方案。两份完整候选交给用户前执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --architecture-system <system-id>
```

目标是检查架构与模块固定结构、字段、链接和候选状态，不判断方案是否合理。

API、核心接口内部编排和数据库也必须先形成可独立阅读的完整候选，再分别交给用户审核。每个 API 在 `API设计.md` 中取得稳定 `API 标识`；API 确认后，系统设计 Agent 必须读取并严格使用 [references/internal-orchestration-template.md](references/internal-orchestration-template.md)。编排正文除接口目录外只按单个 API 建立二级章节，每个接口固定先写业务结果和连续“谁做什么、得到什么、下一步是什么”的主流程，再写分支失败、事务与外部影响、Domain 调用和业务证据。不能把多个接口合成接口组，不能再建立并列的 Domain 方法内部编排；Domain 行为、规则、不变量和内部对象协作仍由 `系统拆分.md` 拥有。编排候选交给用户前执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --orchestration-system <system-id>
```

数据库设计必须读取并严格使用 [references/database-design-template.md](references/database-design-template.md)，以表为章节完整解释表的意义、单行语义和全部字段，禁止用 DDL 或迁移脚本代替设计正文。数据库候选交给用户前执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --database-system <system-id>
```

前一命令检查 API 标识、接口目录和逐 API 编排结构；后一命令检查逐表、逐字段合同并拒绝 DDL。通过只表示机械合同完整。任何一项未确认时，都不能把候选当作后续确定输入；数据库未确认时，不能生成状态为 `当前` 的开发基线或进入 Coding。用户明确要求并行时可以继续准备下游或其他系统候选，但必须清楚标记假设和待确认状态，不能绕过当前应展示的审核。只为当前已确认目标建立最小充分模型；未来可能性不能作为新增实体、版本、聚合、Domain 或基础设施的依据。

## 调用语言验证 Agent

语言验证是表达效果盲测，不是业务或设计审核。Agent 只读取目标读者实际看到的名称、页面文案、截图或报告片段，禁止读取业务与设计答案；它复述自己理解的业务、行为、数据和歧义，不修改任何事实。

Agent 新引入的核心业务名称，Domain、核心对象、关系和业务表名称，以及用于发现或确认业务的页面文案，在交给用户确认或扩散到下游前调用新的语言验证 Agent。完整输入隔离、输出和复测规则见 [references/language-validation-agent.md](references/language-validation-agent.md)。

## 调用开发 Agent

每个进入 Coding 的系统先由开发 Agent 读取并严格使用 [references/engineering-coding-standard-template.md](references/engineering-coding-standard-template.md)，建立并持续维护：

```text
vcddd/systems/<system-id>/coding/工程编码规范.md
```

它是本系统全部 Coding 共同遵守的工程事实。架构设计和模块拆分未确认时先返回系统设计，不能用工程规范代替，也不能先提交依赖这些边界的工程规范候选。已有代码时按固定模板逐项实际调查代码和配置，缺失或冲突项再根据当前语言和框架最佳实践提出方案；没有代码时为全部模板项提出推荐、真实替代项和权衡。抽象选择涉及语言习惯、资源生命周期、事务、并发、数据映射、错误传播或封装时，必须给当前语言或框架的最小正确示例、反例、适用边界和对任务图的影响；分轮选择持续写入决策表，但只有用户明确确认完整候选后规范才成为 `当前`。不同系统不默认共享；纯工程认识形成候选并经用户确认后补充，会改变业务或设计时返回上游。

架构设计、模块拆分和开发基线已确认或为 `当前` 后，开发规划可以与工程编码规范并行形成任务图候选。命名、注释、错误包装和格式化等任务内部规则不阻塞候选；会改变代码产物、路径、生成物、共享写入、依赖或装配所有权的规则在工程规范确认后触发任务图影响复核。工程规范和复核都未完成时不能把任务图标记为 `当前` 或创建 Coding worktree。生产代码形成前先读取并严格使用 [references/implementation-task-graph-template.md](references/implementation-task-graph-template.md)：

```text
全部代码产物
→ 提供者与消费者
→ 写入范围与共享位置
→ 真实依赖和调度冲突
→ 并行批次
→ worktree 基线与合并顺序
```

任务图覆盖工程基础、模块、数据迁移、接口、业务实现、查询、外部集成、后台任务、系统能力、装配和存量改造，只使用真实存在的类型。一个任务不必有独立业务结果，也不必涉及 API 或 Domain；不能为了套模板强行建立 Domain。Agent 不能按 Controller、Service、Repository 等技术层机械拆分，也不能按想启动的子 Agent 数量拆分。完整任务图交给用户确认后才能成为 `当前`。

任务图候选交给用户前执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --implementation-system <system-id> \
  --development-batch <delivery-id>
```

工程规范、任务图和影响复核都成为当前以后，创建任何 Coding worktree 前执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --coding-system <system-id> \
  --development-batch <delivery-id>
```

前一命令允许工程规范仍在形成，只检查候选任务图；后一命令是实际 Coding 准入，并检查已经派发任务的进度合同。

每个任务节点必须固定实施上下文：精确必读章节、不得重新决定的结论、允许自主决定的实现空间、前置代码产物与 Commit、共享事务/不变量/失败语义、输入失效条件和问题返回所有者。主控用固定短任务信封派发当前任务图、开发基线、工程规范版本、共同起始 Commit、已合并前置产物、授权写入、当前反馈、进度与实现记录位置；关键事实不能依赖聊天补充，也不能把全部历史交给 Agent 自行筛选。

每个无未完成前置依赖且写入范围不冲突的任务在独立 worktree 中并行实现。同批任务使用同一已提交基线；有依赖的任务只在前置代码合并后从新 Commit 开始；共享文件固定一个写入者。实施 Agent 只完成任务节点声明的生产代码、迁移、配置和装配，不编写测试、不执行正确性验证，也不把编码完成声明成正确。每个任务维护 `任务进度.md` 和 `实现记录.md`：前者只在等待条件、Agent 启停、产物、阻塞、提交或合并变化时记录恢复点，后者记录最终代码交接；两者都不保存思维或终端流水。

`主控状态.md` 和 `任务进度.md` 只保存最近事件。用户询问 Agent 是否正在运行时，主控必须查询实际 Agent/任务工具，并分别报告计划、Agent、产物和集成状态。开发基线、设计、工程规范或前置代码变化命中任务输入失效条件时，受影响任务先暂停，再安全同步或重建 worktree 并更新派发信封；不能继续依赖旧对话或旧工作区。

全部任务按图合并后形成统一生产代码快照和 `集成记录.md`。详细规划、实施、集成和记录方式见 [references/coding-guidance.md](references/coding-guidance.md) 与 [references/development-agent.md](references/development-agent.md)。

忠于设计不表示假定设计永远正确。Coding 在生成 SQL、落地 Domain、编排事务、接入平台或验证运行结果时，若证据表明已确认设计不合理、无法保持不变量或会产生不可接受代价，必须形成设计反馈：说明问题位置、实现或运行证据、影响范围、建议修改及方案权衡，并由主控路由给事实拥有者。纯 DDL 语法、ORM 映射和其他不改变语义的问题由 Coding 自行解决；需要改变 Domain、API、事务或数据事实时，Coding 不静默修改上游，也不以临时代码绕过，等待相应设计修订和用户重新确认后再继续受影响范围。完整闭环见 [references/coding-guidance.md](references/coding-guidance.md#设计反馈闭环)。

代码现实与开发基线冲突时，开发 Agent 按上述闭环报告证据与修改意见；任务边界或依赖不成立时返回开发规划 Agent 更新候选并重新确认受影响部分。代码不能静默成为新的业务或设计权威。调用时给当前任务、开发基线、工程编码规范、当前开发任务图或候选、本任务直接来源、仓库规范、共同认知协议、[references/coding-guidance.md](references/coding-guidance.md)、[references/implementation-task-graph-template.md](references/implementation-task-graph-template.md) 和 [references/development-agent.md](references/development-agent.md)。

## 调用统一测试 Agent

一个开发批次的全部生产代码合并并形成唯一快照后，读取并严格使用 [references/testing-agent.md](references/testing-agent.md)。主控根据实际代码和风险启动多个互相独立的测试 Agent，例如 API 合同、业务结果、数据事务、外部失败恢复、并发幂等、配置启动或系统集成；不存在的对象不机械创建测试角度。

每个测试 Agent 从同一生产代码快照建立隔离 worktree，只写自己范围内的测试代码、测试夹具和测试反馈，不修改生产代码，也不读取其他测试结论。全部反馈完成后启动新的测试结论 Agent，只汇总失败、责任、修正任务、复测范围和未覆盖风险。生产代码问题返回对应实施任务，测试代码问题返回原测试 Agent，工程规范或上游设计问题返回事实拥有者；修正后按影响范围复测。

测试统一发生在生产代码完成以后，不进入单个实施任务的完成边界。测试结论为 `可进入工程改进` 后才启动工程改进。

## 调用工程改进 Agent

统一测试完成并形成当前测试代码与结论后，至少启动一个独立的重复与抽象分析；再按当前事实和工程规范触发边界依赖、事务可靠性、可观察性、安全、性能或平台角度。每个 Agent 只从一个角度读取同一输入快照，不读取其他分析结论。

工程分析可以并行，代码修改只在路径与责任不重叠时并行；同一文件、公共接口或相互依赖行为必须串行处理。工程改进 Agent 可以修改授权生产代码并运行已经形成的受影响测试，不能为了通过而降低断言，也不能改变业务、Domain、API、已确认事务、数据或失败语义。每轮固定输入与输出快照，记录到：

```text
systems/<system-id>/delivery/<delivery-id>/improvement/<轮次>-<角度>.md
```

系统级认识写入 `工程编码规范.md`，只服务当前批次的选择保留在改进记录。完整角色合同见 [references/engineering-improvement-agent.md](references/engineering-improvement-agent.md)。

## 调用代码审核 Agent

计划内工程改进完成、受影响统一测试重新执行并形成最终固定生产代码与测试快照后，并行调用两个相互独立的核心审核：

```text
实现符合性
工程质量
```

所有审核读取同一生产代码与测试快照、开发基线、工程编码规范、任务图、集成记录、测试结论和实施记录，不读取其他审核结论，也不直接修改代码；并行审核分别使用独立任务和 `主控状态.md`。已经由用户确认的业务、Domain、API、核心接口内部编排和数据库设计不再交给审核 Agent 重新判定；实现符合性审核只检查代码是否忠实执行它们，工程质量审核同时检查系统规范、重复与抽象、可靠性和可维护性。代码证据若表明上游事实可能有问题，审核 Agent 只报告证据和影响。独立审核完成后再启动新的审核结论 Agent，读取各审核记录并写 `审核结论.md`；主控只依据状态文件路由实现或上游问题。修改或重写后按影响范围复审和复测。

审核任务使用共同认知协议、[references/diagramming.md](references/diagramming.md) 和 [references/code-review-agent.md](references/code-review-agent.md)。安全、性能、前端体验或平台专项只在风险触发时增加。

全部阶段、任务、集成、测试、改进和审核记录形成，准备把交付标记为完成前执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --coding-system <system-id> \
  --review-batch <delivery-id>
```

目标是确认全部记录共同指向固定快照；它不是开始统一测试前的准入命令。

## 调用系统验证 Agent

验证属于被验证系统，固定写入：

```text
vcddd/systems/<system-id>/validation/<VAL-ID>-<slug>/
```

原型是 `prototype` 验证方法，不是独立产物类型。验证目录同时保存验证入口、计划、结论、`src/` 实现、夹具、脚本和不可变运行记录；原型源码也写入自己的 `src/`。生产代码不能导入验证代码。验证发现新事实后交给事实拥有者更新并重新确认权威文档，不能让验证或原型暗中成为系统事实。

需要读取或执行验证时使用 [references/prototype-projection.md](references/prototype-projection.md) 和 [references/evidence.md](references/evidence.md)。

验证项、运行记录、用户确认状态或 `prototype` 源码更新后执行：

```text
python3 <skill-root>/scripts/sync_indexes.py <repo-root> --write
python3 <skill-root>/scripts/validate_project.py <repo-root>
```

目标是同步验证索引，并检查验证位置、运行记录、源码 Commit 与用户确认绑定。系统验证使用基础校验，没有 `--validation-system` 参数。

## 按需调用报告 Agent

蓝图、汇报稿和其他报告都不是固定项目产物。只有用户要求时才生成，并使用用户指定的路径和结构。

报告 Agent 只能摘取、压缩、排序、链接和绘制现有事实。缺少内容时返回缺失事实、应修改的源文档和负责角色；不得为了完成报告临场创造系统、Domain、架构、模块、API、核心接口内部编排或数据设计。

报告投影规则见 [references/report-projection.md](references/report-projection.md)。

## 允许回到任何事实

业务设计、系统拆分、架构设计、模块拆分、API、核心接口内部编排、数据库、开发基线、工程编码规范、开发任务图、代码、统一测试、工程改进和审核存在通常的推导顺序，但不是门禁状态机。任何 Agent 都可以报告：

```text
问题所在：
当前证据：
为什么无法继续：
应由哪个角色补充或替换：
受影响内容：
```

主控先让事实拥有者修正源文档，再让受影响 Agent 重新读取和局部推导。只标记真正受影响的内容，不因一个问题废弃全部下游。

## 提交和交接前检查

任何状态拥有者发生变化后先执行 `sync_indexes.py --write`。提交、交接或结束任务前固定执行：

```text
python3 <skill-root>/scripts/sync_indexes.py <repo-root> --check
python3 <skill-root>/scripts/validate_project.py <repo-root>
```

完整场景、参数、写入边界、退出码和失败处理以 [脚本执行协议](references/script-usage.md) 为准。脚本通过只表示声明范围内没有机械错误，不表示语义已经审核或确认。

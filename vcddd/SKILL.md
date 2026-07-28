---
name: vcddd
description: "以业务设计为源头、通过具备明确认知协议的专职子 Agent 持续推进到可审核代码的人机协作协议。用于从想法、文字、已确认原型、快速网页原型、现有系统、代码和运行证据中形成由用户确认的业务设计，再形成系统拆分、模块拆分、API、数据库和开发基线，继续实现、记录设计到代码的对应关系，并在代码形成后由多个独立审核 Agent 检查实现符合性及工程质量。适合需要用户反复参与、跨会话恢复、多个目标或系统并行、按需制作原型或报告，以及必须避免 AI 擅自判定业务正确或代码静默偏离的项目。"
---

# VCDDD

把项目文档作为持久事实，让主控 Agent 负责用户交互、任务恢复和专业 Agent 调度。专业 Agent 不是简单身份扮演：每个角色都用结果责任、核心判断、风险触发器、探索路线和结果合同约束工作。所有专业 Agent 通过主控通信，不依赖彼此或主会话的历史。

所有专业 Agent 使用 [references/cognitive-protocol.md](references/cognitive-protocol.md)。主控仍须同时提供特化角色 reference；通用协议不能代替角色实际关注的问题。

## 审核边界

审核只发生在代码形成固定快照以后。业务设计和系统设计阶段不启动审核 Agent，不产生“通过 / 不通过”结论。

AI 在前置阶段只负责调查证据、结构化业务认识、给出推荐方案并暴露遗漏、冲突和不确定项；它不能证明业务是正确的。业务目标、场景行为、责任、所有权和关系是否符合真实需要，由用户确认。前置文档“可以继续使用”只表示来源、当前结论和未决问题已经记录到足以支持下一步，不表示 AI 已经审核通过业务或设计。

## 语言与建模边界

业务发现只使用用户词汇、具体事实和固定元关键词；行业黑话不能成为结论或思考起点。Domain 阶段可以使用 DDD 术语，但只能分类已确认业务，不能据此创造名称、对象或表。Domain 和数据库名称必须仅凭名称就足以理解其承载的业务以及能做的具体事情。不是所有业务所需信息都属于 Domain；日志、外部引用与快照、查询数据、流程进度和技术运行信息可以按真实用途保存。

各阶段允许的语言、名称推导、非 Domain 信息和数据库承载规则见 [references/language-and-modeling.md](references/language-and-modeling.md)，业务设计与系统设计都必须使用。

## 恢复

1. 读取目标仓库的 `docs/vcddd/index.md`、`work/index.md` 和当前任务。
2. 从当前任务恢复角色 reference、读写合同、主要权威文档、已经形成的认识、待处理用户反馈和可直接执行的下一步。
3. 未选择任务时，根据用户请求只读取直接相关入口；明确的构建、修改或设计请求可以透明建立中文任务。
4. 阶段性业务目标仍由用户决定建立、选择、合并、暂停、完成和取消。
5. 不默认加载全部项目历史。入口或任务不能说明下一步时，先修复恢复信息。

完整恢复、事实权威、任务状态和目录规则见 [references/project-context.md](references/project-context.md)。
建立或维护项目入口、任务恢复点和角色交接时必须使用 [references/project-document-contracts.md](references/project-document-contracts.md)；这些模板是跨会话恢复合同，不是可选写作建议。

## 作为主控调度

主控不重新完成专业工作。它负责：

- 判断请求属于业务设计、系统与开发设计、开发、代码审核、原型投影或报告投影；
- 给专业 Agent 提供角色 reference、具体目标和最小文档路径；
- 原样转交专业 Agent 的用户交互包和用户反馈；
- 持久化尚未被吸收的反馈，防止会话压缩丢失；
- 把上游问题路由给拥有该事实的 Agent；
- 在专业 Agent 更新权威文档后通知受影响角色重新读取；
- 维护 `work/` 和全局导航。

调度、输入输出信封、反馈循环和单写者规则见 [references/controller.md](references/controller.md)。用户参与和跨会话交互见 [references/interaction-protocol.md](references/interaction-protocol.md)。

## 调用业务设计 Agent

业务设计 Agent 从用户材料、原型、现有系统和运行事实中形成：

```text
docs/vcddd/business/<阶段性业务目标>/业务设计.md
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
docs/vcddd/systems/<中文系统名>/
├── index.md
├── 系统拆分.md
├── 模块拆分.md
├── API设计.md
├── 数据库设计.md
└── 开发基线.md
```

- `系统拆分.md`：Domain、对象、行为、规则和 Domain 协作；
- `模块拆分.md`：模块责任、Domain 承载、依赖和代码组织；
- `API设计.md`：精确调用契约；
- `数据库设计.md`：领域状态的数据投影、事务、约束和迁移；
- `开发基线.md`：只从前四份事实和业务设计汇总，不在此文件临场补设计。

设计过程中发现业务设计不足时，返回精确上游请求；不得直接修改 `business/`。调用时给当前系统入口、相关 `业务设计.md`、当前任务、代码或验证入口、共同认知协议、[references/language-and-modeling.md](references/language-and-modeling.md) 和 [references/system-design-agent.md](references/system-design-agent.md)。

Domain 命名前先分析当前业务决定、事实与决定所有权、各主体自有能力、事物关系及关系新增或约束的能力，并由用户明确确认这组业务基础；确认前不能继续对象分类、聚合、Domain、API 和数据库。确认后再分析当前身份与生命周期、不变量和跨系统流程；核心业务名称的含义再由用户确认，之后才扩散到 API、表和代码。只为当前已确认目标建立最小充分模型；未来可能性不能作为新增实体、版本、聚合、Domain 或基础设施的依据。

## 调用语言验证 Agent

语言验证是表达效果盲测，不是业务或设计审核。Agent 只读取目标读者实际看到的名称、页面文案、截图或报告片段，禁止读取业务与设计答案；它复述自己理解的业务、行为、数据和歧义，不修改任何事实。

Agent 新引入的核心业务名称，Domain、核心对象、关系和业务表名称，以及用于发现或确认业务的页面文案，在交给用户确认或扩散到下游前调用新的语言验证 Agent。完整输入隔离、输出和复测规则见 [references/language-validation-agent.md](references/language-validation-agent.md)。

## 调用开发 Agent

开发 Agent 只在本次切片落入状态为 `当前` 的开发基线适用范围时实现：

```text
业务结果
→ API
→ 模块与应用编排
→ Domain 行为
→ 数据与外部协作
→ 代码
→ 测试和可观察结果
```

每个开发切片维护 `systems/<系统>/开发记录/<切片>/实现记录.md`，记录开发基线、固定代码快照、设计到代码与测试的对应、偏差和剩余风险；不保存命令流水。

代码现实与开发基线冲突时，开发 Agent 报告事实和影响，由主控路由到相应设计 Agent；代码不能静默成为新的业务或设计权威。调用时给当前任务、开发基线、本切片直接来源、仓库规范、共同认知协议和 [references/development-agent.md](references/development-agent.md)。

## 调用代码审核 Agent

开发 Agent 形成固定代码快照和实现记录后，并行调用两个相互独立的核心审核：

```text
实现符合性
工程质量
```

所有审核读取同一代码快照、开发基线和实现记录，不读取其他审核结论，也不直接修改代码。已经由用户确认的业务和 Domain 不再交给审核 Agent 重新判定；实现符合性审核只检查代码是否忠实执行它们。代码证据若表明上游事实可能有问题，审核 Agent 只报告证据和影响，由主控重新路由到相应设计 Agent 和用户确认。主控在独立审核完成后写 `审核结论.md`，把实现问题交回开发 Agent，把可能的上游问题交回事实拥有者；修改或重写后按影响范围复审。

审核任务使用共同认知协议和 [references/code-review-agent.md](references/code-review-agent.md)。安全、性能、前端体验或平台专项只在风险触发时增加。

## 按需调用原型 Agent

原型不是固定阶段或固定产物：

- 已确认原型是确认范围内的功能事实来源；
- 业务认识不足且交互能暴露功能时，可以先做快速网页原型；
- 业务设计形成后，可以按需用原型呈现系统设计和业务线；
- 用户指定位置时写到指定位置，否则遵循目标项目既有约定；
- 原型发现新事实后，交给事实拥有者更新文档，不让原型暗中定义业务或系统。

需要读取或制作原型时使用 [references/prototype-projection.md](references/prototype-projection.md) 和 [references/evidence.md](references/evidence.md)。

## 按需调用报告 Agent

蓝图、汇报稿和其他报告都不是固定项目产物。只有用户要求时才生成，并使用用户指定的路径和结构。

报告 Agent 只能摘取、压缩、排序、链接和绘制现有事实。缺少内容时返回缺失事实、应修改的源文档和负责角色；不得为了完成报告临场创造系统、Domain、模块、API 或数据设计。

报告投影规则见 [references/report-projection.md](references/report-projection.md)。

## 允许回到任何事实

业务设计、系统拆分、模块拆分、API、数据库、开发基线、代码和审核存在通常的推导顺序，但不是门禁状态机。任何 Agent 都可以报告：

```text
问题所在：
当前证据：
为什么无法继续：
应由哪个角色补充或替换：
受影响内容：
```

主控先让事实拥有者修正源文档，再让受影响 Agent 重新读取和局部推导。只标记真正受影响的内容，不因一个问题废弃全部下游。

## 检查而不代替语义

运行：

```text
python3 <本Skill目录>/scripts/validate_project.py <目标仓库根目录>
```

准备 Coding 时追加：

```text
--coding-system <中文系统名>
```

检查某个开发切片的实现和审核结构时追加：

```text
--review-slice <中文开发切片>
```

检查当前任务能否被新会话恢复时追加：

```text
--recovery-task <中文任务名>
```

脚本只检查入口、链接、恢复合同、固定事实文档、开发基线来源、实现与审核记录结构和版本状态，不判断业务、设计、代码或审核是否正确。

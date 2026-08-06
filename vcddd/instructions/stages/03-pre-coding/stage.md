---
vcddd_type: "stage-instructions"
vcddd_version: "2.0"
stage: "pre-coding"
status: "active"
---

# Pre-Coding 说明

**阅读身份：** VCDDD 主控使用本文连接开发 Leader、选择能力和登记产出；用户直接调用的开发 Leader 使用本文确定当前设计范围。主控不开展专业设计。

## 负责的工作

Pre-Coding 使用当前可获得的业务、Domain 事实和业务组合，形成 Coding 直接使用的设计文档：

- 系统与模块设计；
- API 与 Domain 编排；
- 数据库设计。

三类设计分别由开发 Leader 的明确能力负责，不要求每次都新建 Agent。用户直接指定能力时，当前 Agent 加载开发 Leader 人物说明和对应能力；主控连接时使用用户可见的专业对话。不同系统分别维护自己的 API 与数据库专业上下文和文档。

用户目标或当前设计问题明确时，开发 Leader 直接完成对应设计产出；不因前序阶段未执行或事实尚未固定而等待或补跑前序阶段。可用事实、假设、缺口和可能返工范围必须如实写明；仅在当前设计无法继续时，按最小范围回补所需事实。

## 开发 Leader 的 Pre-Coding 能力

| 当前工作 | 能力 | 产出 |
|---|---|---|
| 设计整体系统、系统职责、系统交互、系统内部模块和关键业务路径 | [系统与模块设计](../../roles/development-leader/capabilities/system-and-module-design.md) | `系统与模块设计.md` |
| 设计一个系统面向页面、其他系统或服务消费者的 API、调用形式、调用结果和逐 API 内部执行流程 | [API 与 Domain 编排](../../roles/development-leader/capabilities/api-and-domain-orchestration.md) | 当前系统的 `API 与 Domain 编排.md` |
| 设计一个系统的 ER、表、字段、类型、约束、索引、关系、事务和数据生命周期 | [数据库设计](../../roles/development-leader/capabilities/database-design.md) | 当前系统的 `数据库设计.md` |

开发 Leader 使用系统与模块设计能力负责整体系统和各系统内部模块。每个系统分别维护一份 API 与 Domain 编排能力上下文和一份数据库设计能力上下文；它们可以由用户在当前对话直接启动，也可以由项目经理连接。不同系统不共用 API、数据库文档和内部设计上下文。

## 系统与模块设计需要的内容

本次任务按需使用可定位的事实入口、版本和章节链接。由主控连接时可提供；用户直接调用时，由使用系统与模块设计能力的开发 Leader 根据正式入口和当前目标建立最小必要清单：

- 当前宏观业务目标、已选 User Stories 和业务线结果；
- 当前业务使用的能力；如已有确认信息，包含能力由哪个 Domain 提供、接收什么、产生什么；
- 业务怎样组合这些能力形成结果；
- 已确认的现有系统、外部系统、第三方组件、运行方式和部署边界；
- 当前术语表；
- 系统与模块设计模板。

任务清单不包含完整历史对话、业务与 Domain 的设计过程、被否决方案、未来设想、API、数据库设计和 Coding 任务拆分。

## API 与 Domain 编排需要的内容

每次只处理一个系统，并按需使用可定位的事实入口、版本和章节链接。由主控连接时可提供；用户直接调用时，由使用 API 与 Domain 编排能力的开发 Leader 根据正式入口、目标系统和当前任务建立最小必要清单：

- 当前系统在 `系统与模块设计.md` 中的职责、模块和系统交互；
- 经过当前系统的业务路径、调用者和最终结果；
- 当前系统与调用方已知或已确认的部署边界、接口形式和协议限制；
- 当前系统实际使用的 Domain 行为、输入、结果和业务影响；
- 当前系统需要调用的外部 API；
- 当前术语表和已知或已确认的协议限制；
- API 与 Domain 编排模板。

任务清单不包含其他系统的内部设计、数据库、Coding 任务和未来 API。已有系统需要保持兼容或核实真实行为时，由 API 与 Domain 编排能力负责人记录具体问题后读取当前 API、调用方使用方式和最小必要运行证据。

## 数据库设计需要的内容

每次只处理一个系统，并按需使用可定位的事实入口、版本和章节链接。由主控连接时可提供；用户直接调用时，由使用数据库设计能力的开发 Leader 根据正式入口、目标系统和当前任务建立最小必要清单：

- 当前系统的职责、边界和与外部系统的数据责任；
- 当前系统必须保存的 Domain 事实、非 Domain 数据、关系和生命周期；
- 会读取或改变数据、要求共同成功、处理并发或面对外部失败的具体 API 内部步骤；
- 当前真实过滤、关联、排序、分页、数据量、保留时间和安全限制；
- 当前系统已经确定的数据库产品、部署方式和技术限制；
- 已有系统当前 Schema、表、字段、约束、索引和迁移结果；
- 数据库设计模板。

业务、Domain 和 API 只帮助数据库设计能力负责人判断需要承载的数据及一致性要求。数据库正式文档只写数据库内部结构，不复制业务目标、流程、API 功能和分析过程。已有系统需要核实结构时，数据库设计能力负责人只读取数据库 Schema、迁移结果、最小数据分布和必要运行证据，不扩张到应用代码分析。

## 文档位置

```text
vcddd-obsidian/03-pre-coding/
├── 系统与模块设计.md
└── systems/
    └── <system-id>-<system-name>/
        ├── API 与 Domain 编排.md
        ├── 数据库设计.md
        └── validation/
            ├── index.md
            └── <validation-id>-<validation-name>/
                ├── index.md
                ├── 验证计划.md
                ├── 验证结论.md
                ├── src/
                ├── fixtures/
                ├── scripts/
                └── runs/<run-id>/
                    ├── 运行记录.md
                    └── artifacts/
```

系统与模块设计事实只写在 `系统与模块设计.md`。每份 API 与 Domain 编排和数据库设计文档通过 `system_id` 和 Wiki Link 归属一个系统；目录只帮助浏览，不替代文档关系。

`validation/` 是跨阶段的系统验证工作空间，不是 Pre-Coding 设计的固定产出。只有当前原型、技术 POC、最小端到端实现或其他验证需要长期复现与引用时才创建验证项。一个验证项只回答一个可判定命题；计划、源码、运行记录、产物与结论保存在同一项中。验证实现不得进入生产代码路径，生产代码也不得依赖验证实现。

需要保留过程、支持协作交接或用户明确要求时，执行记录写入 `vcddd-obsidian/work/<work-id>-<work-name>/执行记录/`。正式设计不记录 `work_id`，也不反向链接执行记录；未创建记录不阻止设计产出或使用。

使用：

- [系统与模块设计.md](../../../assets/templates/vcddd-obsidian/03-pre-coding/系统与模块设计.md)
- [API 与 Domain 编排.md](../../../assets/templates/vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/API 与 Domain 编排.md)
- [数据库设计.md](../../../assets/templates/vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/数据库设计.md)
- [系统验证入口](../../../assets/templates/vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/validation/index.md)
- [验证项入口](../../../assets/templates/vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/validation/<validation-id>-<validation-name>/index.md)
- [验证计划](../../../assets/templates/vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/validation/<validation-id>-<validation-name>/验证计划.md)
- [验证结论](../../../assets/templates/vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/validation/<validation-id>-<validation-name>/验证结论.md)
- [运行记录](../../../assets/templates/vcddd-obsidian/03-pre-coding/systems/<system-id>-<system-name>/validation/<validation-id>-<validation-name>/runs/<run-id>/运行记录.md)
## 产出迭代与事实边界

API 与 Domain 编排直接形成当前所需 API 候选；数据库设计先从当前业务结果和系统责任确定本地持久化边界，再用真实创建、修改、查询、失效、失败和并发操作走通数据，并形成字段、约束、索引、事务、生命周期和物理规则。不能从数据库产品、模板栏目、Domain 名称或 API 数量直接开始设计表。正式文档只写数据库、Schema、ER、表、字段、类型、空值、默认值、约束、索引、外键、数据库事务和记录生命周期，不写持久化事实分析、操作走查、API 编排、为什么拆表、字段来源、实现交接、被否决方案和没有依据的保留期或未来扩展。

三类设计文档可随理解迭代。未知、冲突和推断显式记录为假设、缺口和可能返工范围；不受影响的设计与 Coding 可继续推进。业务和 Domain 事实只能由其拥有者或用户明确更新，Coding 不得静默改写；开发 Leader 发现冲突时标出影响并返回相应事实拥有者处理。

## 继续设计的内容

- 三份设计文档之间的精确链接和变化通知方式。
- 最后处理：根据 TokenHub 真实交互演练，提升系统与模块设计能力的独立设计质量。重点复核层级判断、Domain 与模块的区分，以及先提出完整候选再持续迭代设计文档。

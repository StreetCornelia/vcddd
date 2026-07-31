# Obsidian 文档合同

**适用身份：** 所有会创建或更新 VCDDD 笔记的 Agent。主控只写自己拥有的执行记录；阶段结果和专业证据由对应专业 Agent 主写。

## 目的

让人类在 Obsidian 中能够自然浏览，也让 Agent 通过稳定属性和显式链接精确获取上下文。

## 强制规则

当你是某份笔记的主写 Agent 时：

1. 每个正式笔记都以 YAML Properties 开头。
2. 每个工作对象都有稳定 ID；文件改名不改变 ID。
3. 内部关系使用 `[[Wiki Links]]`，属性中的 Wiki Link 必须作为字符串。
4. 正文面向人类阅读；Properties 帮助 AI 检索、路由和检查，不能替代 AI 对正文与证据的判断。
5. 同一事实只在一个权威笔记中定义。其他笔记只链接并说明使用原因。
6. 阶段结果、证据、候选项和执行记录必须是不同文档类型。
7. 链接表达有意义的关系，不为了构造“全连接图”而滥加链接。

主控拥有项目入口和自己的执行记录。项目入口只保存路由状态与直接链接，不复制阶段结论。主专业 Agent 拥有阶段结果和本路线专业文档。条件 Agent 只拥有自己的执行记录及必要的独立证据。

## 通用 Properties

你应按文档类型选择必要字段，不得任意改名：

| Property | 含义 |
|---|---|
| `vcddd_type` | 文档类型 |
| `vcddd_version` | 协议版本 |
| `work_id` | 本轮工作稳定 ID |
| `stage` | 大阶段 |
| `route` | 阶段路线 |
| `status` | 文档当前状态 |
| `owner_role` | 唯一主写角色 |
| `execution_record` | 对应执行记录 Wiki Link |
| `result_note` | 对应阶段结果 Wiki Link |
| `created` | 创建日期 |
| `updated` | 最近更新日期 |

## 链接语义

你应在正文的链接附近明确关系，例如：

- “本结果由 [[执行记录]] 追踪。”
- “User Story `US-003` 来源于 [[候选场景池#SCN-007]]。”
- “能力 `CAP-004` 的视觉证据见 [[原型能力证据#EVD-012]]。”

不要仅在文末堆积“相关链接”而不解释关系。

## ID 约定

- 工作：`WORK-YYYYMMDD-NNN`
- 候选场景：`SCN-NNN`
- User Story：`US-NNN`
- 原型证据：`EVD-NNN`
- 宏观能力：`CAP-NNN`
- 决定：`DEC-NNN`
- 检查点事件：使用路线规定的检查点代码

ID 在同一 `work_id` 内唯一。删除内容时保留 ID 和状态，避免链接失效。

## 文档状态

通用状态为：

- `not-started`
- `draft`
- `active`
- `waiting`
- `awaiting-user-confirmation`
- `confirmed`
- `handed-off`
- `completed`
- `design-pending`
- `superseded`
- `blocked`

只有用户明确确认后，阶段结果才能标记为 `confirmed`。

# Obsidian 文档合同

**适用身份：** 所有会创建或更新 VCDDD 笔记的 Agent。主控只写自己拥有的执行记录；阶段结果和专业证据由对应专业 Agent 主写。

## 目的

让人类在 Obsidian 中能够自然浏览，也让 Agent 通过稳定属性和显式链接精确获取上下文。

## Vault 布局

项目入口固定为根目录的 `VCDDD.md`。所有工作文档固定放入 `VCDDD 工作区/<work_id>/`：

```text
项目根目录/
├── VCDDD.md
└── VCDDD 工作区/
    └── WORK-YYYYMMDD-NNN/
```

不要创建与 `VCDDD.md` 同名的 `VCDDD/` 目录。一个工作 ID 的执行记录、阶段结果和专业证据放在同一工作目录；文档关系仍通过 Wiki Links 表达，不能依赖目录位置暗示语义。

## 强制规则

当你是某份笔记的主写 Agent 时：

1. 每个正式笔记都以 YAML Properties 开头。
2. 每个工作对象都有稳定 ID；文件改名不改变 ID。
3. 内部关系使用 `[[Wiki Links]]`，属性中的 Wiki Link 必须作为字符串。
4. 正文面向人类阅读；Properties 帮助 AI 检索、路由和检查，不能替代 AI 对正文与证据的判断。
5. 同一事实只在一个权威笔记中定义。其他笔记只链接并说明使用原因。
6. 专业结果、证据、候选项和执行记录必须是不同文档类型。
7. 链接表达有意义的关系，不为了构造“全连接图”而滥加链接。

主控拥有项目入口和自己的执行记录。项目入口只保存当前焦点、能力地图与直接链接，不复制专业结论。主专业 Agent 拥有专业结果和本路线文档。条件 Agent 只拥有自己的执行记录及必要的独立证据。

## 通用 Properties

你应按文档类型选择必要字段，不得任意改名：

| Property | 含义 |
|---|---|
| `vcddd_type` | 文档类型 |
| `vcddd_version` | 协议版本 |
| `work_id` | 本轮工作稳定 ID |
| `stage` | 能力域标识；用于分类，不表示准入顺序 |
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
- “业务线 `BL-004` 采用的原型观察见 [[原型观察证据#EVD-012]]。”

不要仅在文末堆积“相关链接”而不解释关系。

## ID 约定

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
- 语言验证：`LNG-NNN`
- 事实证据：`FACT-NNN`
- 决定：`DEC-NNN`
- 进度事件：使用路线规定的稳定进度点代码

ID 在同一 `work_id` 内唯一。删除内容时保留 ID 和状态，避免链接失效。

## 文档状态

状态描述单份文档或单项工作的成熟度，不构成全局状态机，也不解锁其他能力。

通用状态为：

- `not-started`
- `draft`
- `active`
- `waiting`
- `awaiting-user-confirmation`
- `confirmed`
- `completed`
- `protocol-design-pending`
- `superseded`
- `limited`

只有用户明确确认后，专业结果才能标记为 `confirmed`。未确认结果仍可被其他能力引用，但链接附近必须说明其状态、假设和可能返工范围。

`limited` 只用于某个具体动作，并必须同时说明不受影响、仍可继续的工作；不得把它解释成整个项目停滞。

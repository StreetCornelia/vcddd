# 脚本执行协议

## 作用与权威边界

本 Skill 自带的脚本位于 `<skill-root>/scripts/`，用于执行可机械判断的工作：

- `sync_indexes.py`：从唯一状态拥有者生成或检查受控索引区；
- `validate_project.py`：只读检查 VCDDD 工作空间、设计候选、Coding 准入、交付记录和任务恢复合同。

`<skill-root>` 是当前 `SKILL.md` 所在目录；`<repo-root>` 是目标项目的仓库根目录，其中已经存在 `vcddd/`。Agent 从当前 Skill 位置解析脚本路径，不搜索脚本，也不为了预测结果读取脚本源码。

项目文档合同是权威，脚本只是执行实现。普通业务、设计、验证、迁移、开发、测试和审核 Agent 只读取本协议、执行命令并处理输出。只有任务本身是维护脚本、脚本异常无法由输出定位，或脚本行为与文档合同冲突时，才搜索并读取与问题直接相关的最小源码区段。

任何正常校验都要求目标项目已经按 [Agent 模型发现与路由协议](model-routing.md)建立并确认 `vcddd/config/agent-models.json`。校验脚本不发现模型、不替用户选择模型，也不生成该配置。

## 工具边界

### `sync_indexes.py`

目标：让全局、业务、系统、验证、交付和工作索引与唯一状态拥有者一致。

输入：`<repo-root>` 中现有的 `vcddd/` 工作空间及状态拥有者。

`--write` 会：

- 创建缺失的固定索引文件及其父目录；
- 添加或更新 `<!-- vcddd:generated:start -->` 与 `<!-- vcddd:generated:end -->` 之间的内容；
- 保留受控生成区以外的人工说明。

它不会：

- 迁移旧目录或移动专业文档；
- 创建业务、系统、验证、任务或交付语义；
- 修改状态拥有者、Git 分支或生产代码；
- 根据文件存在自动填写确认或完成状态。

`--check` 是默认只读模式，只报告缺失索引或生成区漂移。

### `validate_project.py`

目标：在相应交付节点拒绝可以机械判定的目录、链接、字段、状态、确认依据和 Git 输入错误。

正常模式只读目标仓库；Coding 相关检查会读取 Git 元数据，但不会修改文件、分支、索引或工作树。它不会判断业务、设计、验证命题、代码、测试或审核结论是否正确，也不会修复错误。

无专项参数时检查整个 VCDDD 工作空间的基础结构、链接、索引同步、系统验证和恢复记录。专项参数在基础检查之上增加当前节点的检查，不是替代基础检查。

`--self-test` 只供维护本 Skill 脚本时使用；普通项目流程不得执行。

## 参数

| 参数 | 含义 |
| --- | --- |
| `<skill-root>` | 当前 `SKILL.md` 所在目录 |
| `<repo-root>` | 包含现有 `vcddd/` 的目标仓库根目录 |
| `<system-id>` | `vcddd/systems/` 下的稳定 ASCII 系统目录名 |
| `<delivery-id>` | 当前系统 `delivery/` 下的稳定 ASCII 交付目录名 |
| `<work-id>` | `vcddd/work/` 下的稳定 ASCII 工作目录名 |
| `<task-id>` | 当前开发任务图中的稳定 `TASK-` 标识 |
| `<stage-id>` | 当前交付 `stages/` 下的稳定 ASCII 阶段目录名 |

不要把 `<skill-root>`、`<repo-root>/vcddd`、生产代码根目录或 worktree 子目录相互替代。

## 场景与完整命令

### 任何阶段开始前

先检查 `vcddd/config/agent-models.json` 是否记录项目初始化时本机可访问的 Codex/Claude 环境，并包含当前环境的真实可用模型、五个能力档位和用户确认。缺失时不要先运行校验或进入专业工作；按模型路由协议完成本机发现和用户确认，再运行基础校验：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root>
```

目标：拒绝没有项目级模型配置、会静默继承主对话模型的任务。

### 状态拥有者发生变化

业务设计状态、系统状态、工作通信状态、验证状态或交付状态发生变化后执行：

```text
python3 <skill-root>/scripts/sync_indexes.py <repo-root> --write
```

目标：只把当前状态投影到受控索引区。执行后继续运行基础结构检查。

### 提交、交接或结束任务前

```text
python3 <skill-root>/scripts/sync_indexes.py <repo-root> --check
python3 <skill-root>/scripts/validate_project.py <repo-root>
```

目标：确认索引无漂移，VCDDD 基础结构没有机械错误。

### 迁移旧 VCDDD 工作空间

脚本不负责迁移。迁移 Agent 先按 `project-context.md` 的目录合同移动文件、补齐状态拥有者并修复链接，然后执行：

```text
python3 <skill-root>/scripts/sync_indexes.py <repo-root> --write
python3 <skill-root>/scripts/validate_project.py <repo-root>
python3 <skill-root>/scripts/sync_indexes.py <repo-root> --check
```

仍需恢复的单个任务再执行 `--recovery-task` 检查。脚本通过不表示迁移语义正确；Agent 仍须核对旧状态所有者、Git 起点和未闭合交付事实。

### 架构与模块候选交给用户前

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --architecture-system <system-id>
```

目标：检查架构与模块固定文档、字段、链接和候选状态。

### 核心接口内部编排候选交给用户前

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --orchestration-system <system-id>
```

目标：检查 API 标识、接口目录和逐 API 编排固定结构。

### 数据库设计候选交给用户前

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --database-system <system-id>
```

目标：检查逐表、逐字段设计合同并拒绝用 DDL 代替设计。

### 系统准备进入 Coding

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --coding-system <system-id>
```

目标：检查六份设计、开发基线和工程编码规范均为当前、已确认且已纳入 Git。

### 开发任务图候选交给用户前

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --implementation-system <system-id> \
  --development-batch <delivery-id>
```

目标：检查任务图候选、代码产物、依赖、派发信封和实施上下文；工程规范可以仍在形成。

### 创建 Coding worktree 前

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --coding-system <system-id> \
  --development-batch <delivery-id>
```

目标：在任务图和工程规范均为当前后检查 Coding 准入，以及已经实际派发任务的进度合同。

### 单个任务准备合并前

任务代码提交，独立任务验证和任务审查都已形成后执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --coding-system <system-id> \
  --development-batch <delivery-id> \
  --task-check <task-id>
```

目标：检查实现、验证和审查指向同一任务 Commit，运行层级达到任务合同，三个 Agent 独立且结论允许合并。失败时保持任务未合并。

### 阶段准备交给用户或继续下阶段前

阶段 Commit、阶段运行验证和阶段审查都已形成后执行：

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --coding-system <system-id> \
  --development-batch <delivery-id> \
  --stage-check <stage-id>
```

目标：检查阶段记录直接链接同一 Commit 的运行与审查证据，达到声明运行层级且结论允许继续。失败时不得请求阶段确认或派发依赖阶段。

### 完成交付、测试、改进和审核记录前

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --coding-system <system-id> \
  --review-batch <delivery-id>
```

目标：检查全部任务已经合并，并检查阶段、集成、统一测试、工程改进和审核记录共同指向固定快照。这个命令在记录已经形成后运行，不是开始统一测试前的准入命令。

### 恢复或迁移一个工作任务

```text
python3 <skill-root>/scripts/validate_project.py <repo-root> \
  --recovery-task <work-id>
```

目标：检查工作入口、短主控状态和完整恢复文档能够支持新会话继续。

### 系统验证或原型运行记录更新后

系统验证没有专项参数。更新验证项、运行记录或 `prototype` 代码以后执行：

```text
python3 <skill-root>/scripts/sync_indexes.py <repo-root> --write
python3 <skill-root>/scripts/validate_project.py <repo-root>
```

目标：检查验证位置、方法、运行记录、源码 Commit 与用户确认绑定，并同步验证索引。

## 输出与失败处理

- 退出码 `0`：脚本声明范围内没有机械错误；
- 退出码 `1`：发现索引漂移或合同错误；
- 退出码 `2`：命令参数或执行前置条件错误。

脚本失败时先读取错误消息和对应文档合同，修复状态拥有者、结构、字段、链接或参数后重新执行。不要通过阅读脚本源码寻找绕过方式，不要为了通过校验而伪造确认、结论或 Commit 等价性。

失败按事实所有权返回：

| 失败位置 | 修复拥有者 | 失败期间禁止继续的动作 |
| --- | --- | --- |
| 索引写入或漂移 | 最近修改对应状态拥有者的 Agent；无法确定时由主控定位唯一事实源 | 提交、交接或宣称索引已同步 |
| 架构、模块、API、内部编排或数据库候选 | 当前系统设计 Agent | 把候选交给用户确认或传播为当前事实 |
| 开发任务图候选 | 开发规划 Agent；上游事实错误返回其事实拥有者 | 用户确认任务图 |
| Coding 准入 | 错误所指向的设计、工程规范、任务图或任务进度拥有者 | 创建 Coding worktree 或派发实施 Agent |
| 任务增量检查 | 实施、任务验证、任务审查或上游事实中对应记录的拥有者 | 合并任务或解除后续依赖 |
| 阶段增量检查 | 阶段集成、阶段验证、阶段审查或上游事实拥有者 | 请求阶段确认或派发依赖阶段 |
| 交付记录检查 | 开发规划、集成、测试、工程改进、审核中对应记录的拥有者 | 把交付标记为完成 |
| 任务恢复 | 迁移或恢复 Agent；专业内容缺失返回原事实拥有者 | 让新会话依据不完整入口继续 |
| 系统验证或原型记录 | 系统验证 Agent；源码快照问题返回产生该代码的角色 | 把验证结论传播为当前证据 |

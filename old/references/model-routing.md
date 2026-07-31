# Agent 模型发现与路由协议

## 目标

模型选择是每个目标项目自己的运行事实，不是 Skill 模板的固定答案。每个使用 VCDDD 的项目在自己的仓库中维护：

```text
vcddd/config/agent-models.json
```

Skill 仓库不预置这份文件，也不把某个时期的模型名称当成长期事实。项目首次进入 VCDDD 流程时，主控先检查本机可访问的 Codex 与 Claude Code：已安装且当前账号可用的环境分别探测真实模型并写入同一项目配置；不可访问的环境记录为未配置及原因，不凭空填模型。候选经用户确认后才能进入第一个专业阶段。任何后续阶段开始前都再次检查当前环境。

## 前置门槛

启动业务、设计、验证、开发规划、Coding、测试、工程改进或审核 Agent 前，主控依次检查：

1. `vcddd/config/agent-models.json` 是否存在；
2. 项目初始化时本机可访问的 `codex` 与 `claude` 是否都已探测并记录，当前运行环境是否有可执行配置；
3. 探测来源、运行时版本、探测时间和可用模型是否已记录；
4. 每个能力档位是否映射到该环境真实可用的模型与推理强度；
5. 用户是否明确确认当前映射；
6. 配置中的模型和推理强度是否仍被当前运行时接受。

任一项不成立时暂停当前阶段，先执行模型发现、形成候选配置并请求用户确认。不能继承主对话模型继续，不能凭模型家族名称猜测账号权限，也不能把 CLI 帮助中的示例当作本账号可用列表。

以下变化触发重新探测和确认：

- 首次在该项目使用新的 Agent 环境；
- CLI、桌面应用、Agent SDK 或组织策略变化后，原模型被拒绝或选择器列表变化；
- 配置中的模型、推理强度或 fallback 不再可用；
- 用户要求改变成本、速度或质量策略；
- 连续升级表明现有能力档位长期不满足任务。

## 环境发现

### Codex

优先读取当前 Codex 主机创建任务或子 Agent 工具公开的模型元数据，其中应同时给出模型标识、能力说明和支持的 reasoning effort。只有运行时真实公开的模型才能写入 `available_models`。

不要通过读取 Codex 安装目录、缓存或源码推测模型列表。CLI `--help` 只能证明参数语法，不能证明当前主机允许使用某个模型。

### Claude Code

先记录 `claude --version`，再使用当前账号的 `/model` 选择器核对真正可见的模型；`claude --help` 用来核对 `--model`、`--effort` 和 `--fallback-model` 的参数语法。选择器受账号、组织策略和供应商环境限制，因此帮助中的别名或文档示例不能单独进入 `available_models`。

如果当前环境只能交互展示列表，记录“本机 `/model` 选择器”、探测时间和操作者作为证据。模型不支持 effort 时在配置中写 `null`，不能伪造推理强度。

### 其他环境

VCDDD 只对已经有真实发现机制的环境建立配置。新环境先记录环境标识、运行时版本、官方选择接口和可用列表，再定义档位映射；没有发现证据时不得类比 Codex 或 Claude 填值。

## 项目配置合同

目标项目配置使用 JSON，以便脚本在不依赖第三方 YAML 库的情况下校验：

```json
{
  "schema_version": 1,
  "active_environment": "codex",
  "status": "confirmed",
  "confirmed_at": "<ISO-8601>",
  "confirmation_evidence": "<用户确认所在任务或记录>",
  "environments": {
    "codex": {
      "runtime_version": "<实际版本或主机标识>",
      "detected_at": "<ISO-8601>",
      "detection_source": "<运行时模型元数据或选择器>",
      "available_models": [
        {
          "id": "<真实模型标识>",
          "reasoning_efforts": ["low", "medium", "high"]
        }
      ],
      "tiers": {
        "deep": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "high"
        },
        "planning": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "high"
        },
        "review": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "medium"
        },
        "execution": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "medium"
        },
        "mechanical": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "low"
        }
      }
    },
    "claude": {
      "runtime_version": "<实际版本或主机标识>",
      "detected_at": "<ISO-8601>",
      "detection_source": "<本机 /model 选择器>",
      "available_models": [
        {
          "id": "<真实模型标识>",
          "reasoning_efforts": ["low", "medium", "high"]
        },
        {
          "id": "<不支持 effort 的真实模型标识>",
          "reasoning_efforts": null
        }
      ],
      "tiers": {
        "deep": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "high"
        },
        "planning": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "medium"
        },
        "review": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": "medium"
        },
        "execution": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": null
        },
        "mechanical": {
          "model": "<available_models 中的模型>",
          "reasoning_effort": null
        }
      }
    }
  }
}
```

示例中的模型名和 effort 都是占位符，必须按本机结果替换；某个具体模型不支持 effort 时，所有映射到它的 `reasoning_effort` 都写 `null`。

`active_environment` 是当前主控实际运行环境。项目首次配置时应同时保存本机当前可访问的 `codex` 和 `claude`；某环境尚未安装、未登录或被组织策略禁用时，不生成伪造映射，而在用户确认依据中记录原因，待首次可用时单独发现和确认。切换环境时更新 `active_environment`，不能把另一个环境的模型名直接复用。

## 能力档位

| 档位 | 默认任务 | 选择原则 |
| --- | --- | --- |
| `deep` | 业务发现、Domain 判断、总体架构、跨系统边界、关键用户决策综合 | 使用当前环境中最强的深度推理能力；只在真正需要形成新认知时使用 |
| `planning` | API 与内部编排、数据库设计、工程规范、任务图、跨任务根因分析 | 使用平衡型模型；遇到跨事实所有权、重大歧义或两次失败再升级到 `deep` |
| `review` | 单任务审查、阶段集成审查、最终实现符合性和工程质量审核 | 使用平衡型审查模型；默认不使用主对话最高模型，只有审查暴露上游语义冲突时升级 |
| `execution` | 边界明确的生产代码、测试代码、修复、原型与验证实现 | 使用快速、经济且具备代码能力的模型；上下文必须由任务信封限定 |
| `mechanical` | 索引同步、结构校验、状态回写、链接修复、固定格式投影 | 使用最低成本的可靠模型或直接执行脚本；不得为了机械工作调用最高模型 |

模型档位描述的是最低能力需求，不绑定厂商命名。主控选择满足档位的最低成本模型；不能因为主会话正在使用强模型就省略子 Agent 的模型参数。

## 调用与升级

每次创建独立 Agent 时，任务包固定增加：

```text
模型配置：vcddd/config/agent-models.json
当前环境：
请求档位：deep | planning | review | execution | mechanical
实际模型：
推理强度：
选择依据：
升级条件：
```

主控必须显式传入实际模型和支持的推理强度。运行工具不允许覆盖模型时，先向用户说明限制，不能静默继承主会话。

出现以下情况才允许新建一个更高档位的诊断或设计任务：

- 当前任务必须重新判断业务、Domain、系统边界或不可逆数据语义；
- 两次有证据的执行或审查仍因推理不足失败；
- 问题跨越多个事实拥有者，现有任务信封无法给出确定边界；
- 安全、资金、数据破坏或重大迁移风险要求更强判断。

代码量大、文件多、测试慢或审查条目多不自动升级模型；这些优先通过拆小任务、精确上下文和脚本处理。`execution` 实施/验证 Agent 与 `review` 审查 Agent 不在原任务中切换成 `deep`：需要重新判断根因时暂停原任务，建立独立 `planning` 或 `deep` 诊断任务；边界恢复清楚后，编码、修复、复验和复审仍回到原档位。升级或新建诊断任务必须记录原因。

## 状态记录

模型配置保存项目级选择；每个专业任务的 `主控状态.md`、实施任务 `任务进度.md` 或阶段 `阶段记录.md` 保存本次实际选择。至少记录请求档位、实际模型、推理强度和升级原因。不支持 effort 的模型在记录中固定写 `推理强度：null`，使机械校验能与 JSON 的 `null` 对应。

模型完成通知不证明任务正确，强模型也不能替代逐任务验证、阶段运行证据、独立审查或用户确认。

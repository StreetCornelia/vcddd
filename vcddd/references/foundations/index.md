---
title: "VCDDD 理念与历史边界"
aliases:
  - "VCDDD Foundations"
tags:
  - "vcddd/foundation"
vcddd_type: "foundation-index"
status: "reference-only"
updated: "2026-08-01"
---

# VCDDD 理念与历史边界

本目录保存 VCDDD 的思想来源和阶段性反思，用于理解设计动机、维护 Skill 和重新讨论尚未定型的部分。这里的材料不是当前运行时指令。

## 权威边界

解释优先级固定为：

1. 用户在当前工作中的明确决定；
2. 当前 [VCDDD 主控协议](../../SKILL.md)；
3. `instructions/` 中当前生效的身份、阶段和共享合同；
4. 本目录中的理念与历史材料。

普通项目运行不默认读取本目录。只有维护或重写 VCDDD、追溯设计理由，或者当前合同出现无法解释的理念冲突时才按需读取。

## VCDDD 1.0：For Human

这些文件按思想资源保存，帮助理解 VCDDD 最初试图解决的问题。1.0 的固定概念、顺序和实现策略不属于当前执行说明。

1. [[1.0-whitepaper|VCDDD 1.0 白皮书]]
2. [[1.0-methodology|VCDDD 1.0 方法论]]
3. [[1.0-design-guide|VCDDD 1.0 设计指导]]
4. [[1.0-implementation|VCDDD 1.0 实现映射]]

## VCDDD 2.0：阶段性思考

这些文件记录从 1.0 向人机共同设计、可恢复上下文和渐进式 Coding 演进时形成的阶段性判断。它们不是最终运行时 Skill；其中与当前合同冲突的部分只作为演变证据。

1. [[2.0-01-starting-point|从 AI 辅助实现到人机共同做出系统]]
2. [[2.0-02-shared-decision-context|从通用语言到共同决策上下文]]
3. [[2.0-03-business-discovery-and-validation|从业务全貌到可开发业务基线]]
4. [[2.0-04-recoverable-project-context|可恢复的项目上下文]]
5. [[2.0-05-domain-thinking-and-coding-transition|Domain 思想与进入 Coding 前的认知基线]]
6. [[2.0-06-progressive-coding-and-engineering-evolution|忠于设计的 Coding 与渐进式工程收敛]]
7. [[2.0-07-api-first-core-orchestration|以 API 为唯一主轴的核心接口内部编排]]
8. [[2.0-08-human-readable-database-design|面向人类阅读的数据库设计]]
9. [[2.0-09-incremental-verification-and-model-routing|增量验证与模型路由]]

## 使用规则

- 读取前先说明要追溯的问题，不要一次加载全部材料。
- 引用时标明版本和文档，不把历史主张改写为当前合同。
- 发现仍有价值的原则时，先与用户确认，再写入相应 `instructions/`；不要直接让历史文档获得执行权。
- 新的阶段性思考可以继续进入本目录，但必须声明状态和适用边界。

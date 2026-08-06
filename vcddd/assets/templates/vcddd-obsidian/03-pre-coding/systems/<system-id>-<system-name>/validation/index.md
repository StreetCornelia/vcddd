---
title: "{{系统名称}}验证"
aliases: []
tags:
  - "vcddd/validation"
  - "vcddd/system-validation"
vcddd_type: "system-validation-index"
vcddd_version: "2.0"
stage: "cross-stage"
owner_role: "{{验证负责人角色}}"
system_id: "{{SYS-NNN}}"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# {{系统名称}}验证

> 本页只导航当前系统的验证项，不复制验证计划、运行事实或结论。原型、技术 POC、最小端到端实现和其他验证性产物都按其实际证明的命题建立独立验证项。

| 验证 ID | 验证项 | 方法 | 要验证的命题 | 状态 | 当前结论 |
|---|---|---|---|---|---|
| `VAL-001` | [[<validation-id>-<validation-name>/index]] | `prototype \| technical-poc \| end-to-end \| fact-check \| other` |  | `draft` | [[<validation-id>-<validation-name>/验证结论]] |

## 使用规则

- 一个验证项只回答一个能够明确判定的命题；不同命题分别建立验证项。
- 验证源码、夹具、脚本和运行产物保存在验证项内部，不放入生产代码路径，也不由生产代码依赖。
- 结论必须链接到实际运行或来源证据，并清楚说明适用范围与未覆盖部分。
- 验证项状态只在该验证项的 `index.md` 中维护，本页仅投影并链接。

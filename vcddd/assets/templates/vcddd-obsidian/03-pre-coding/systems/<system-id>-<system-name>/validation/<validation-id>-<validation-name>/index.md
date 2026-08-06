---
title: "{{VAL-NNN}}：{{验证名称}}"
aliases: []
tags:
  - "vcddd/validation"
vcddd_type: "validation-item"
vcddd_version: "2.0"
stage: "cross-stage"
owner_role: "{{验证负责人角色}}"
system_id: "{{SYS-NNN}}"
validation_id: "{{VAL-NNN}}"
validation_method: "{{prototype | technical-poc | end-to-end | fact-check | other}}"
status: "draft"
created: "{{YYYY-MM-DD}}"
updated: "{{YYYY-MM-DD}}"
---

# {{VAL-NNN}}：{{验证名称}}

## 验证命题

- 要确认或反驳的命题：
- 该命题影响的目标、业务、系统设计或实现：
- 当前为什么不能仅凭已有材料判断：

## 当前入口

- 验证计划：[[验证计划]]
- 验证结论：[[验证结论]]
- 最近有效运行：[[runs/<run-id>/运行记录]]

## 目录用途

```text
<validation-id>-<validation-name>/
├── index.md
├── 验证计划.md
├── 验证结论.md
├── src/          # 原型、POC 或最小验证实现源码
├── fixtures/     # 可复现输入与非敏感测试材料
├── scripts/      # 启动、构建、采集或复现脚本
└── runs/
    └── <run-id>/
        ├── 运行记录.md
        └── artifacts/  # 截图、录屏、日志、报告等运行产物
```

实例化验证项时保留这组目录；暂时没有内容的目录可以只保留 `.gitkeep`。敏感值不得写入源码、夹具、脚本、运行记录或产物；只记录安全配置名称和目标环境。

## 状态

- 当前状态：`draft | active | waiting | supported | refuted | insufficient-evidence | superseded`
- 状态依据：
- 最近有效运行或来源：
- 下一步：

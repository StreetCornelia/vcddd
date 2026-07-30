#!/usr/bin/env python3
"""Validate deterministic VCDDD project structure without judging semantics."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BASELINE_STATUS_RE = re.compile(
    r"^状态[ \t]*[：:][ \t]*(当前|待确认|待重新生成|已替代)[ \t]*$",
    re.MULTILINE,
)
BASELINE_HEADINGS = ["Domain", "架构与模块", "业务线与 API", "数据库设计"]
BUSINESS_DESIGN_HEADINGS = ["业务目标与范围", "系统设计", "业务线逻辑"]
ORCHESTRATION_API_HEADINGS = [
    "业务结果",
    "主流程",
    "分支与失败",
    "事务与外部影响",
    "Domain 调用",
    "业务证据与验证",
]
API_ID_RE = re.compile(
    r"^API 标识[ \t]*[：:][ \t]*(API-[^\s：:]+)[ \t]*$",
    re.MULTILINE,
)
ORCHESTRATION_API_TITLE_RE = re.compile(
    r"^(API-[^\s：:]+)[ \t]*[：:][ \t]*(\S.*?)[ \t]+—[ \t]+(\S.*)$"
)
ORCHESTRATION_API_DESIGN_SOURCE_RE = re.compile(
    r"^API 设计来源[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
ORCHESTRATION_TABLE_HEADERS = [
    "| 步骤 | 执行者 | 做什么 | 得到什么结果 | 下一步 |",
    "| 分支 | 发生在步骤 | 条件 | 业务结果 | API 结果 | 后续 |",
    "| 边界 | 覆盖步骤 | 提交或外部动作 | 成功证明 | 失败或结果未知处理 |",
    "| 发生在步骤 | Domain 行为 | 输入事实 | 领域结果 | 权威规则位置 |",
]
DATABASE_PREFIX_HEADINGS = ["数据承载全景", "表目录", "数据关系图"]
DATABASE_TABLE_HEADINGS = [
    "表的意义",
    "产生、变化与使用",
    "字段说明",
    "身份、主键与唯一性",
    "与其他表的关系",
    "必须保持的约束",
    "查询与索引",
    "事务、并发与编排对应",
    "历史、清理与迁移",
    "尚未确定的问题",
]
DATABASE_TAIL_HEADINGS = [
    "跨表事务与一致性",
    "查询投影与非 Domain 数据",
    "数据安全与保留",
    "数据库实现交接",
]
DATABASE_TABLE_TITLE_RE = re.compile(
    r"^(DBT-[^\s：:]+)[ \t]*[：:][ \t]*"
    r"([A-Za-z_][A-Za-z0-9_]*)[ \t]+—[ \t]+(\S.*)$"
)
DATABASE_DESIGN_SOURCE_RE = re.compile(
    r"^设计来源[ \t]*[：:][ \t]*$", re.MULTILINE
)
DATABASE_OVERVIEW_HEADER = (
    "| 需要保存的事实 | 事实拥有者 | 为什么需要持久化 | 使用者与用途 |"
    " 承载表 | 数据性质 |"
)
DATABASE_DIRECTORY_HEADER = (
    "| 表标识 | 表名 | 中文名称 | 这张表为什么存在 | 一行表示什么 |"
    " 详细章节 |"
)
DATABASE_FIELD_HEADER = (
    "| 字段 | 中文名称 | 字段为什么存在 | 保存的事实或含义 | 事实来源 |"
    " 数据类型 | 必填 | 空值含义 | 默认值及含义 | 允许值或范围 |"
    " 何时产生或改变 | 是否敏感 | 数据库注释原文 |"
)
DATABASE_REQUIRED_TABLE_HEADERS = [
    "| 时点或事件 | 写入者 | 写入或变化 | 使用者 | 用途 |",
    DATABASE_FIELD_HEADER,
    "| 类型 | 字段组合 | 保证的事实 | 冲突时的业务含义 |",
    "| 关联表 | 本表字段 | 对方字段 | 关系与基数 | 存在性要求 |"
    " 删除或失效语义 |",
    "| 约束 | 约束保护的事实 | 数据库责任 | Domain 或应用责任 |"
    " 违反时的结果 |",
    "| 查询来源 | 查询条件与排序 | 频率或规模事实 | 建议索引 |"
    " 为什么需要 | 代价与不采用条件 |",
    "| API 与步骤 | 本表读写 | 原子范围或提交点 | 并发保护 |"
    " 失败、回滚或结果未知处理 |",
]
DATABASE_TABLE_MEANING_FIELDS = [
    "保存的事实",
    "存在原因",
    "一行表示",
    "为什么独立成表",
    "数据库表注释原文",
    "数据性质",
    "权威拥有者",
    "是否参与业务判断",
    "是否可重新生成",
    "来源",
]
DATABASE_TAIL_TABLE_HEADERS = {
    "跨表事务与一致性": (
        "| API 与步骤 | 涉及表 | 必须共同成立的事实 | 原子边界 |"
        " 外部影响顺序 | 失败与恢复 |"
    ),
    "数据安全与保留": (
        "| 数据范围 | 敏感等级 | 访问者 | 脱敏或加密 | 保留与清理 |"
        " 审计要求 |"
    ),
}
DATABASE_HANDOFF_FIELDS = [
    "Coding 阶段需要产生",
    "实现必须保持",
    "允许 Coding 决定",
    "必须返回设计的情况",
]
DATABASE_DDL_RE = re.compile(
    r"(?im)^\s*(CREATE\s+(?:TABLE|SCHEMA|INDEX)|ALTER\s+TABLE|"
    r"DROP\s+(?:TABLE|SCHEMA|INDEX))\b"
)
SYSTEM_FACT_FILES = [
    "系统拆分.md",
    "架构设计.md",
    "模块拆分.md",
    "API设计.md",
    "核心接口内部编排.md",
    "数据库设计.md",
]
ENGINEERING_CODING_STANDARD_FILE = "工程编码规范.md"
ENGINEERING_STANDARD_HEADINGS = [
    "使用与演化规则",
    "形成过程与依据",
    "当前规则索引",
    "架构与代码组织",
    "Domain 与应用编排",
    "命名与代码表达",
    "事务",
    "数据访问",
    "错误处理",
    "日志与可观察性",
    "外部系统协作",
    "并发、异步与幂等",
    "配置与安全",
    "测试",
    "封装、复用与重复代码",
    "工具链与交付验证",
    "例外与存量处理",
    "尚未形成规范的问题",
    "重要演化",
]
ENGINEERING_STANDARD_STATUS_RE = re.compile(
    r"^状态[ \t]*[：:][ \t]*(待建立|待确认|当前|待重新判断)[ \t]*$",
    re.MULTILINE,
)
ARCHITECTURE_HEADINGS = [
    "架构目标与约束",
    "总体架构",
    "层次与主要组件",
    "依赖与调用边界",
    "数据、外部系统与运行协作",
    "系统级技术机制",
    "技术选择与理由",
    "Coding 必须遵守的边界",
    "允许 Coding 决定的内容",
    "尚未确定的问题",
]
MODULE_PREFIX_HEADINGS = ["模块全景", "模块目录"]
MODULE_DETAIL_HEADINGS = [
    "存在意义",
    "职责与非职责",
    "承载的 Domain 与数据",
    "对外提供与依赖",
    "代码范围",
]
MODULE_TAIL_HEADINGS = [
    "模块依赖规则",
    "业务覆盖",
    "Coding 必须遵守的边界",
    "尚未确定的问题",
]
MODULE_TITLE_RE = re.compile(
    r"^(MOD-[^\s：:]+)[ \t]*[：:][ \t]*(\S.*)$"
)
ARCHITECTURE_CONFIRMATION_RE = re.compile(
    r"^架构设计确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
ARCHITECTURE_EVIDENCE_RE = re.compile(
    r"^架构设计确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
MODULE_CONFIRMATION_RE = re.compile(
    r"^模块拆分确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
MODULE_EVIDENCE_RE = re.compile(
    r"^模块拆分确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
ENGINEERING_STANDARD_CONFIRMATION_RE = re.compile(
    r"^规范确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
ENGINEERING_STANDARD_EVIDENCE_RE = re.compile(
    r"^规范确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
ENGINEERING_STANDARD_FORMATION_RE = re.compile(
    r"^形成方式[ \t]*[：:][ \t]*(已有代码归纳|全新系统初始化)[ \t]*$",
    re.MULTILINE,
)
BUSINESS_SUBJECT_CONFIRMATION_RE = re.compile(
    r"^业务主体确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
BUSINESS_SUBJECT_EVIDENCE_RE = re.compile(
    r"^业务主体确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
DOMAIN_DESIGN_CONFIRMATION_RE = re.compile(
    r"^Domain 设计确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
DOMAIN_DESIGN_EVIDENCE_RE = re.compile(
    r"^Domain 设计确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
NAMING_CONFIRMATION_RE = re.compile(
    r"^核心命名确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
NAMING_EVIDENCE_RE = re.compile(
    r"^核心命名确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
API_DESIGN_CONFIRMATION_RE = re.compile(
    r"^API 设计确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
API_DESIGN_EVIDENCE_RE = re.compile(
    r"^API 设计确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
INTERNAL_ORCHESTRATION_CONFIRMATION_RE = re.compile(
    r"^核心接口内部编排确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
INTERNAL_ORCHESTRATION_EVIDENCE_RE = re.compile(
    r"^核心接口内部编排确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
DATABASE_DESIGN_CONFIRMATION_RE = re.compile(
    r"^数据库设计确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
DATABASE_DESIGN_EVIDENCE_RE = re.compile(
    r"^数据库设计确认依据[ \t]*[：:][ \t]*(\S.*)$",
    re.MULTILINE,
)
TASK_RECOVERY_HEADINGS = [
    "任务定义",
    "当前角色",
    "读取与写入合同",
    "当前判断",
    "用户交互",
    "已有产物",
    "恢复",
]
TASK_RECOVERY_FIELDS = [
    "任务状态",
    "任务目标",
    "完成条件",
    "服务的业务目标与系统",
    "当前负责角色",
    "角色 reference",
    "交互状态",
    "当前讨论对象",
    "当前权威文档",
    "必须读取的权威文档",
    "直接证据或代码入口",
    "允许写入路径",
    "禁止修改内容",
    "已经形成的认识或实现",
    "当前核心判断及答案",
    "已触发的条件判断",
    "补充判断",
    "尚未确定或存在冲突的判断",
    "全部重要未决决定及所有者",
    "决定之间的依赖关系",
    "当前决策前沿",
    "正在比较的候选或冲突",
    "本次准备补充或替换的信息",
    "可能受影响的其他文档",
    "最新用户交互包",
    "尚未处理的用户反馈",
    "反馈处理结果",
    "本轮维护的文档或代码",
    "当前工作位置",
    "当前开发基线与代码快照",
    "实现记录与审核状态",
    "恢复动作",
    "下一步",
    "恢复完成的判断标准",
]
CONTROLLER_STATE_FIELDS = [
    "任务文档",
    "当前负责角色",
    "角色 reference",
    "通信状态",
    "当前讨论对象",
    "专业结果位置",
    "本轮变更",
    "用户交互包",
    "待处理用户反馈",
    "反馈处理结果",
    "下一步",
]
CONTROLLER_STATUS_RE = re.compile(
    r"^通信状态[ \t]*[：:][ \t]*"
    r"(待派发|Agent 工作中|等待用户|可继续|阻塞|完成)[ \t]*$",
    re.MULTILINE,
)
TASK_GRAPH_HEADINGS = [
    "批次范围与完成边界",
    "代码产物清单",
    "任务关系图",
    "并行批次",
    "共享写入与集成规则",
    "开发任务",
    "集成与统一代码快照",
    "尚未确定的问题",
]
TASK_GRAPH_STATUS_RE = re.compile(
    r"^状态[ \t]*[：:][ \t]*"
    r"(待确认|当前|待重新判断|已完成)[ \t]*$",
    re.MULTILINE,
)
TASK_GRAPH_CONFIRMATION_RE = re.compile(
    r"^任务图确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
TASK_DETAIL_FIELDS = [
    "任务类型",
    "代码责任",
    "来源",
    "要实现的代码",
    "实现边界",
    "主要写入范围",
    "共享写入位置",
    "前置输入",
    "提供给后续任务",
    "前置任务",
    "依赖类型与原因",
    "可以并行的任务",
    "禁止并行的任务及原因",
    "worktree 起始快照",
    "编码完成边界",
    "发现问题时返回",
]
TASK_TYPES = {
    "工程基础",
    "模块基础",
    "数据与迁移",
    "接口入口",
    "业务实现",
    "查询实现",
    "外部系统集成",
    "后台任务",
    "系统级能力",
    "装配与接线",
    "现有代码改造",
    "其他",
}
TASK_HEADING_RE = re.compile(
    r"^###\s+(TASK-[A-Za-z0-9][A-Za-z0-9._-]*)[：:]\s*(\S.*)$",
    re.MULTILINE,
)
IMPLEMENTATION_HEADINGS = [
    "任务代码责任",
    "来源与代码对应",
    "实际产生的代码",
    "提供给后续任务的产物",
    "与任务图或设计的偏离",
    "剩余实现事项",
]
INTEGRATION_FIELDS = [
    "开发任务图",
    "起始代码快照",
    "已合并任务及 Commit",
    "合并顺序",
    "共享写入处理",
    "未合并或未实现事项",
    "统一生产代码快照",
    "测试状态",
    "工程改进状态",
    "最终待审核快照",
]
TEST_FEEDBACK_FIELDS = [
    "测试角度",
    "输入生产代码快照",
    "依据的开发基线",
    "依据的工程编码规范",
    "测试代码范围",
    "禁止修改的生产代码范围",
    "覆盖对象",
    "未覆盖对象",
    "新增或修改的测试",
    "测试执行入口",
    "测试结果",
    "失败证据",
    "要求达到的修正结果",
    "问题责任",
    "需要返回的任务或事实拥有者",
    "测试代码快照",
    "剩余风险",
]
TEST_CONCLUSION_FIELDS = [
    "生产代码快照",
    "测试代码快照",
    "各测试反馈",
    "失败与责任",
    "测试分歧",
    "修正任务",
    "复测范围",
    "未覆盖风险",
    "当前结论",
]
ENGINEERING_IMPROVEMENT_FIELDS = [
    "分析角度",
    "工作方式",
    "输入代码快照",
    "输入测试代码快照",
    "依据的开发基线",
    "依据的工程编码规范",
    "依据的测试结论",
    "分析范围",
    "发现的问题",
    "决定修改或保留的理由",
    "实际修改",
    "更新的工程编码规范",
    "受影响测试结果",
    "输出代码快照",
    "剩余风险",
]
DESIGN_FEEDBACK_FIELDS = [
    "反馈状态",
    "发现阶段",
    "问题所在",
    "对应的权威设计",
    "代码、SQL、测试或运行证据",
    "为什么当前设计不成立或不合理",
    "影响的任务与代码范围",
    "建议修改",
    "替代方案与权衡",
    "建议修改的权威文档和章节",
    "当前代码处理",
    "可以继续的范围",
    "事实拥有者",
    "上游处理结果",
    "重新确认依据",
    "受影响的任务、代码和测试",
]
DESIGN_FEEDBACK_STATUS_RE = re.compile(
    r"^反馈状态[ \t]*[：:][ \t]*"
    r"(待上游判断|已采纳|部分采纳|不采纳|已重新确认)[ \t]*$",
    re.MULTILINE,
)
DESIGN_FEEDBACK_STAGE_RE = re.compile(
    r"^发现阶段[ \t]*[：:][ \t]*"
    r"(任务规划|生产代码实现|SQL 与迁移|统一测试|工程改进|代码审核)"
    r"[ \t]*$",
    re.MULTILINE,
)
DESIGN_FEEDBACK_CODE_ACTION_RE = re.compile(
    r"^当前代码处理[ \t]*[：:][ \t]*"
    r"(停止相关实现|仅保留技术验证|继续不受影响范围)[ \t]*$",
    re.MULTILINE,
)
CORE_REVIEW_FILES = [
    "实现符合性.md",
    "工程质量.md",
]
SCOPE_RE = re.compile(r"^适用范围[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE)
EXCLUDED_SCOPE_RE = re.compile(
    r"^未覆盖范围[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
)
SOURCES_RE = re.compile(
    r"^来源[ \t]*[：:][ \t]*$\n(.*?)(?=^##[ \t]+Domain[ \t]*$)",
    re.MULTILINE | re.DOTALL,
)
UNIFIED_PRODUCTION_SNAPSHOT_RE = re.compile(
    r"^统一生产代码快照[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
)
FINAL_REVIEW_SNAPSHOT_RE = re.compile(
    r"^最终待审核快照[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
)
TEST_CODE_SNAPSHOT_RE = re.compile(
    r"^测试代码快照[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
)
IMPROVEMENT_OUTPUT_SNAPSHOT_RE = re.compile(
    r"^输出代码快照[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
)
REVIEW_OBJECT_RE = re.compile(
    r"^审核生产代码快照[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
)
REVIEW_RESULT_RE = re.compile(
    r"^审核结论[ \t]*[：:][ \t]*(通过|有条件通过|不通过)[ \t]*$",
    re.MULTILINE,
)
SUMMARY_RESULT_RE = re.compile(
    r"^当前结论[ \t]*[：:][ \t]*(通过|需修改|需重写|等待上游修订)[ \t]*$",
    re.MULTILINE,
)


def local_link_path(source: Path, raw_target: str) -> Path | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = unquote(target.split("#", 1)[0])
    if not target:
        return None
    return (source.parent / target).resolve()


def validate_internal_orchestration(
    system_root: Path,
    *,
    require_confirmed: bool,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    system_index = system_root / "index.md"
    api_design = system_root / "API设计.md"
    orchestration = system_root / "核心接口内部编排.md"

    for path in (system_index, api_design, orchestration):
        if not path.exists():
            errors.append(f"核心接口内部编排检查缺少输入：{path}")
    if errors:
        return errors, warnings

    index_targets = {
        local_link_path(system_index, raw_target)
        for raw_target in LINK_RE.findall(
            system_index.read_text(encoding="utf-8")
        )
    }
    for path in (api_design, orchestration):
        if path.resolve() not in index_targets:
            errors.append(f"系统入口未直接链接编排输入：{path}")

    api_text = api_design.read_text(encoding="utf-8")
    if API_DESIGN_CONFIRMATION_RE.findall(api_text) != ["已确认"]:
        errors.append(
            "形成核心接口内部编排前 API 设计必须且只能声明"
            f"“API 设计确认：已确认”：{api_design}"
        )
    if len(API_DESIGN_EVIDENCE_RE.findall(api_text)) != 1:
        errors.append(
            "形成核心接口内部编排前 API 设计必须且只能声明一个"
            f"非空确认依据：{api_design}"
        )

    api_ids = API_ID_RE.findall(api_text)
    if not api_ids:
        errors.append(f"API 设计至少需要一个稳定“API 标识”：{api_design}")
    if len(api_ids) != len(set(api_ids)):
        errors.append(f"API 设计中的 API 标识必须唯一：{api_design}")

    text = orchestration.read_text(encoding="utf-8")
    statuses = INTERNAL_ORCHESTRATION_CONFIRMATION_RE.findall(text)
    if len(statuses) != 1:
        errors.append(
            "核心接口内部编排必须且只能声明一个确认状态"
            f"（待确认/已确认）：{orchestration}"
        )
    elif require_confirmed and statuses != ["已确认"]:
        errors.append(
            "准备 Coding 的核心接口内部编排必须声明"
            f"“核心接口内部编排确认：已确认”：{orchestration}"
        )

    evidence = INTERNAL_ORCHESTRATION_EVIDENCE_RE.findall(text)
    if len(evidence) != 1:
        errors.append(
            "核心接口内部编排必须且只能声明一个非空确认依据："
            f"{orchestration}"
        )
    elif statuses == ["已确认"] and evidence[0].strip() == "无":
        errors.append(
            f"已确认的核心接口内部编排不能使用“无”作为确认依据：{orchestration}"
        )

    if len(ORCHESTRATION_API_DESIGN_SOURCE_RE.findall(text)) != 1:
        errors.append(
            f"核心接口内部编排必须声明一个非空 API 设计来源：{orchestration}"
        )
    orchestration_targets = {
        local_link_path(orchestration, raw_target)
        for raw_target in LINK_RE.findall(text)
    }
    if api_design.resolve() not in orchestration_targets:
        errors.append(
            f"核心接口内部编排未直接链接 API 设计：{orchestration}"
        )

    h1_headings = re.findall(r"^#(?!#)[ \t]+(.+?)\s*$", text, re.MULTILINE)
    if len(h1_headings) != 1:
        errors.append(
            f"核心接口内部编排必须且只能有一个文档一级标题：{orchestration}"
        )

    h2_matches = list(
        re.finditer(r"^##[ \t]+(.+?)\s*$", text, re.MULTILINE)
    )
    if not h2_matches or h2_matches[0].group(1) != "接口目录":
        errors.append(
            f"核心接口内部编排的第一个二级标题必须为“接口目录”：{orchestration}"
        )

    orchestration_ids: list[str] = []
    for h2_match in h2_matches[1:]:
        title_match = ORCHESTRATION_API_TITLE_RE.fullmatch(
            h2_match.group(1)
        )
        if title_match is None:
            errors.append(
                "接口目录之后每个二级标题必须只对应一个"
                f"“API-标识：入口 — 名称”：{orchestration}"
            )
            continue
        orchestration_ids.append(title_match.group(1))

    if len(orchestration_ids) != len(set(orchestration_ids)):
        errors.append(f"编排文档中的 API 标识必须唯一：{orchestration}")
    if api_ids and orchestration_ids != api_ids:
        errors.append(
            "编排文档的逐 API 标识必须与 API 设计按顺序完整一致；"
            f"API设计={api_ids}，编排={orchestration_ids}：{orchestration}"
        )

    if h2_matches:
        directory_start = h2_matches[0].end()
        directory_end = (
            h2_matches[1].start() if len(h2_matches) > 1 else len(text)
        )
        directory_text = text[directory_start:directory_end]
        required_directory_header = (
            "| API 标识 | 方法与路径或入口 | 调用者要得到的业务结果 |"
            " 编排章节 |"
        )
        if required_directory_header not in directory_text:
            errors.append(
                f"接口目录缺少固定四列表头：{orchestration}"
            )
        for api_id in api_ids:
            if not re.search(
                rf"^\|[ \t]*{re.escape(api_id)}[ \t]*\|",
                directory_text,
                re.MULTILINE,
            ):
                errors.append(
                    f"接口目录缺少 API 标识“{api_id}”：{orchestration}"
                )

    for index, h2_match in enumerate(h2_matches[1:], start=1):
        title_match = ORCHESTRATION_API_TITLE_RE.fullmatch(
            h2_match.group(1)
        )
        if title_match is None:
            continue
        api_id = title_match.group(1)
        section_end = (
            h2_matches[index + 1].start()
            if index + 1 < len(h2_matches)
            else len(text)
        )
        section_text = text[h2_match.end():section_end]
        h3_headings = re.findall(
            r"^###[ \t]+(.+?)\s*$", section_text, re.MULTILINE
        )
        if h3_headings != ORCHESTRATION_API_HEADINGS:
            errors.append(
                f"{api_id} 必须且只能按顺序包含六个三级标题"
                f"（{' / '.join(ORCHESTRATION_API_HEADINGS)}）："
                f"{orchestration}"
            )

        for table_header in ORCHESTRATION_TABLE_HEADERS:
            if table_header not in section_text:
                errors.append(
                    f"{api_id} 缺少固定表头“{table_header}”："
                    f"{orchestration}"
                )

        h3_matches = list(
            re.finditer(r"^###[ \t]+(.+?)\s*$", section_text, re.MULTILINE)
        )
        main_flow_text = ""
        for h3_index, h3_match in enumerate(h3_matches):
            if h3_match.group(1) != "主流程":
                continue
            main_flow_end = (
                h3_matches[h3_index + 1].start()
                if h3_index + 1 < len(h3_matches)
                else len(section_text)
            )
            main_flow_text = section_text[h3_match.end():main_flow_end]
            break
        step_ids = re.findall(
            r"^\|[ \t]*(S\d+)[ \t]*\|",
            main_flow_text,
            re.MULTILINE,
        )
        expected_steps = [f"S{number}" for number in range(1, len(step_ids) + 1)]
        if not step_ids or step_ids != expected_steps:
            errors.append(
                f"{api_id} 主流程步骤必须从 S1 连续编号：{orchestration}"
            )

        mermaid_blocks = len(
            re.findall(r"^```mermaid[ \t]*$", section_text, re.MULTILINE)
        )
        if mermaid_blocks > 2:
            errors.append(
                f"{api_id} 最多使用两张补充图，当前为 {mermaid_blocks}："
                f"{orchestration}"
            )

        nonblank_lines = sum(
            1 for line in section_text.splitlines() if line.strip()
        )
        if nonblank_lines > 180:
            warnings.append(
                f"{api_id} 超过 180 行非空内容，需重新检查是否复制了"
                f" API、Domain、数据库或 Coding 事实：{orchestration}"
            )

    return errors, warnings


def validate_database_design(
    system_root: Path,
    *,
    require_confirmed: bool,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    system_index = system_root / "index.md"
    system_split = system_root / "系统拆分.md"
    api_design = system_root / "API设计.md"
    orchestration = system_root / "核心接口内部编排.md"
    database_design = system_root / "数据库设计.md"

    required_paths = (
        system_index,
        system_split,
        api_design,
        orchestration,
        database_design,
    )
    for path in required_paths:
        if not path.exists():
            errors.append(f"数据库设计检查缺少输入：{path}")
    if not database_design.exists():
        return errors, warnings

    if all(
        path.exists()
        for path in (system_index, api_design, orchestration)
    ):
        orchestration_errors, orchestration_warnings = (
            validate_internal_orchestration(
                system_root,
                require_confirmed=True,
            )
        )
        errors.extend(orchestration_errors)
        warnings.extend(orchestration_warnings)

    if system_index.exists():
        index_targets = {
            local_link_path(system_index, raw_target)
            for raw_target in LINK_RE.findall(
                system_index.read_text(encoding="utf-8")
            )
        }
        if database_design.resolve() not in index_targets:
            errors.append(f"系统入口未直接链接数据库设计：{database_design}")

    text = database_design.read_text(encoding="utf-8")
    statuses = DATABASE_DESIGN_CONFIRMATION_RE.findall(text)
    if len(statuses) != 1:
        errors.append(
            "数据库设计必须且只能声明一个确认状态"
            f"（待确认/已确认）：{database_design}"
        )
    elif require_confirmed and statuses != ["已确认"]:
        errors.append(
            "准备 Coding 的数据库设计必须声明"
            f"“数据库设计确认：已确认”：{database_design}"
        )

    evidence = DATABASE_DESIGN_EVIDENCE_RE.findall(text)
    if len(evidence) != 1:
        errors.append(
            f"数据库设计必须且只能声明一个非空确认依据：{database_design}"
        )
    elif statuses == ["已确认"] and evidence[0].strip() == "无":
        errors.append(
            f"已确认的数据库设计不能使用“无”作为确认依据：{database_design}"
        )

    if len(DATABASE_DESIGN_SOURCE_RE.findall(text)) != 1:
        errors.append(
            f"数据库设计必须且只能声明一个“设计来源”区块：{database_design}"
        )
    database_targets = {
        local_link_path(database_design, raw_target)
        for raw_target in LINK_RE.findall(text)
    }
    for source in (system_split, api_design, orchestration):
        if source.resolve() not in database_targets:
            errors.append(
                f"数据库设计未直接链接固定设计来源：{source}"
            )

    h1_headings = re.findall(r"^#(?!#)[ \t]+(.+?)\s*$", text, re.MULTILINE)
    if len(h1_headings) != 1:
        errors.append(
            f"数据库设计必须且只能有一个文档一级标题：{database_design}"
        )

    h2_matches = list(
        re.finditer(r"^##[ \t]+(.+?)\s*$", text, re.MULTILINE)
    )
    h2_headings = [match.group(1) for match in h2_matches]
    minimum_h2_count = (
        len(DATABASE_PREFIX_HEADINGS) + 1 + len(DATABASE_TAIL_HEADINGS)
    )
    if len(h2_headings) < minimum_h2_count:
        errors.append(
            f"数据库设计至少需要一个逐表章节并保留固定首尾结构：{database_design}"
        )

    if h2_headings[: len(DATABASE_PREFIX_HEADINGS)] != DATABASE_PREFIX_HEADINGS:
        errors.append(
            "数据库设计必须以“"
            + " / ".join(DATABASE_PREFIX_HEADINGS)
            + f"”三个二级标题开场：{database_design}"
        )
    if h2_headings[-len(DATABASE_TAIL_HEADINGS):] != DATABASE_TAIL_HEADINGS:
        errors.append(
            "数据库设计必须以“"
            + " / ".join(DATABASE_TAIL_HEADINGS)
            + f"”四个二级标题收尾：{database_design}"
        )

    table_start = len(DATABASE_PREFIX_HEADINGS)
    table_end = len(h2_matches) - len(DATABASE_TAIL_HEADINGS)
    table_matches = h2_matches[table_start:table_end]
    table_ids: list[str] = []
    for table_match in table_matches:
        title_match = DATABASE_TABLE_TITLE_RE.fullmatch(table_match.group(1))
        if title_match is None:
            errors.append(
                "数据关系图与全局收尾之间每个二级标题必须只对应一张"
                f"“DBT-标识：table_name — 中文名称”：{database_design}"
            )
            continue
        table_ids.append(title_match.group(1))

    if not table_ids:
        errors.append(f"数据库设计至少需要一张带稳定标识的表：{database_design}")
    if len(table_ids) != len(set(table_ids)):
        errors.append(f"数据库设计中的表标识必须唯一：{database_design}")

    if len(h2_matches) >= 2:
        overview_start = h2_matches[0].end()
        overview_end = h2_matches[1].start()
        overview_text = text[overview_start:overview_end]
        if DATABASE_OVERVIEW_HEADER not in overview_text:
            errors.append(
                f"数据承载全景缺少固定六列表头：{database_design}"
            )
        for table_id in table_ids:
            if table_id not in overview_text:
                errors.append(
                    f"数据承载全景未说明表标识“{table_id}”承载的事实："
                    f"{database_design}"
                )

    if len(h2_matches) >= 3:
        directory_start = h2_matches[1].end()
        directory_end = h2_matches[2].start()
        directory_text = text[directory_start:directory_end]
        if DATABASE_DIRECTORY_HEADER not in directory_text:
            errors.append(f"表目录缺少固定六列表头：{database_design}")
        for table_id in table_ids:
            if not re.search(
                rf"^\|[ \t]*{re.escape(table_id)}[ \t]*\|",
                directory_text,
                re.MULTILINE,
            ):
                errors.append(
                    f"表目录缺少表标识“{table_id}”：{database_design}"
                )

    for table_index, table_match in enumerate(table_matches):
        title_match = DATABASE_TABLE_TITLE_RE.fullmatch(
            table_match.group(1)
        )
        if title_match is None:
            continue
        table_id = title_match.group(1)
        absolute_index = table_start + table_index
        section_end = (
            h2_matches[absolute_index + 1].start()
            if absolute_index + 1 < len(h2_matches)
            else len(text)
        )
        section_text = text[table_match.end():section_end]
        h3_matches = list(
            re.finditer(
                r"^###[ \t]+(.+?)\s*$",
                section_text,
                re.MULTILINE,
            )
        )
        h3_headings = [match.group(1) for match in h3_matches]
        if h3_headings != DATABASE_TABLE_HEADINGS:
            errors.append(
                f"{table_id} 必须且只能按顺序包含十个三级标题"
                f"（{' / '.join(DATABASE_TABLE_HEADINGS)}）："
                f"{database_design}"
            )
        for table_header in DATABASE_REQUIRED_TABLE_HEADERS:
            if table_header not in section_text:
                errors.append(
                    f"{table_id} 缺少固定表头“{table_header}”："
                    f"{database_design}"
                )

        if h3_matches:
            meaning_end = (
                h3_matches[1].start()
                if len(h3_matches) > 1
                else len(section_text)
            )
            meaning_text = section_text[h3_matches[0].end():meaning_end]
            for field in DATABASE_TABLE_MEANING_FIELDS:
                if not re.search(
                    rf"^{re.escape(field)}[ \t]*[：:]",
                    meaning_text,
                    re.MULTILINE,
                ):
                    errors.append(
                        f"{table_id} 的“表的意义”缺少“{field}”："
                        f"{database_design}"
                    )

            try:
                field_index = h3_headings.index("字段说明")
            except ValueError:
                field_index = -1
            if field_index >= 0:
                field_end = (
                    h3_matches[field_index + 1].start()
                    if field_index + 1 < len(h3_matches)
                    else len(section_text)
                )
                field_text = section_text[
                    h3_matches[field_index].end():field_end
                ]
                field_rows = [
                    line
                    for line in field_text.splitlines()
                    if line.lstrip().startswith("|")
                    and line.strip() != DATABASE_FIELD_HEADER
                    and not re.fullmatch(
                        r"\|(?:[ \t]*:?-+:?[ \t]*\|)+",
                        line.strip(),
                    )
                ]
                if not field_rows:
                    errors.append(
                        f"{table_id} 的字段说明至少需要一个实际字段："
                        f"{database_design}"
                    )

    if re.search(r"^```(?:sql|postgresql|mysql|sqlite)\b", text, re.MULTILINE):
        errors.append(
            f"数据库设计禁止 SQL 代码块；DDL 与迁移属于 Coding：{database_design}"
        )
    if DATABASE_DDL_RE.search(text):
        errors.append(
            f"数据库设计禁止 DDL；建表和迁移属于 Coding：{database_design}"
        )

    h2_sections: dict[str, str] = {}
    for index, h2_match in enumerate(h2_matches):
        section_end = (
            h2_matches[index + 1].start()
            if index + 1 < len(h2_matches)
            else len(text)
        )
        h2_sections[h2_match.group(1)] = text[h2_match.end():section_end]
    for heading, table_header in DATABASE_TAIL_TABLE_HEADERS.items():
        if heading in h2_sections and table_header not in h2_sections[heading]:
            errors.append(
                f"“{heading}”缺少固定表头“{table_header}”："
                f"{database_design}"
            )
    handoff_text = h2_sections.get("数据库实现交接", "")
    for field in DATABASE_HANDOFF_FIELDS:
        if not re.search(
            rf"^{re.escape(field)}[ \t]*[：:]",
            handoff_text,
            re.MULTILINE,
        ):
            errors.append(
                f"数据库实现交接缺少“{field}”：{database_design}"
            )

    return errors, warnings


def validate_architecture_and_modules(
    system_root: Path,
    require_confirmed: bool,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    architecture_design = system_root / "架构设计.md"
    module_design = system_root / "模块拆分.md"

    for path in (architecture_design, module_design):
        if not path.exists():
            errors.append(f"缺少架构或模块固定设计文档：{path}")
    if errors:
        return errors, warnings

    architecture_text = architecture_design.read_text(encoding="utf-8")
    architecture_confirmations = ARCHITECTURE_CONFIRMATION_RE.findall(
        architecture_text
    )
    if len(architecture_confirmations) != 1:
        errors.append(
            "架构设计必须且只能声明一个确认状态"
            f"（待确认/已确认）：{architecture_design}"
        )
    elif require_confirmed and architecture_confirmations != ["已确认"]:
        errors.append(
            f"准备 Coding 的架构设计尚未确认：{architecture_design}"
        )
    architecture_evidence = ARCHITECTURE_EVIDENCE_RE.findall(
        architecture_text
    )
    if len(architecture_evidence) != 1:
        errors.append(
            f"架构设计必须声明一个非空确认依据：{architecture_design}"
        )
    elif (
        require_confirmed
        and architecture_evidence[0].strip() in {"无", "待确认"}
    ):
        errors.append(
            f"已确认架构设计不能使用空确认依据：{architecture_design}"
        )

    architecture_headings = re.findall(
        r"^##\s+(.+?)\s*$", architecture_text, re.MULTILINE
    )
    if architecture_headings != ARCHITECTURE_HEADINGS:
        errors.append(
            "架构设计必须且只能按顺序包含"
            f"（{' / '.join(ARCHITECTURE_HEADINGS)}）：{architecture_design}"
        )
    for field in (
        "适用系统",
        "适用范围",
        "语言及版本",
        "主要框架及版本",
        "代码现实快照",
    ):
        if len(
            re.findall(
                rf"^{re.escape(field)}[ \t]*[：:][ \t]*(\S.*)$",
                architecture_text,
                re.MULTILINE,
            )
        ) != 1:
            errors.append(
                f"架构设计必须且只能声明一个非空“{field}”："
                f"{architecture_design}"
            )

    module_text = module_design.read_text(encoding="utf-8")
    module_confirmations = MODULE_CONFIRMATION_RE.findall(module_text)
    if len(module_confirmations) != 1:
        errors.append(
            "模块拆分必须且只能声明一个确认状态"
            f"（待确认/已确认）：{module_design}"
        )
    elif require_confirmed and module_confirmations != ["已确认"]:
        errors.append(
            f"准备 Coding 的模块拆分尚未确认：{module_design}"
        )
    module_evidence = MODULE_EVIDENCE_RE.findall(module_text)
    if len(module_evidence) != 1:
        errors.append(
            f"模块拆分必须声明一个非空确认依据：{module_design}"
        )
    elif (
        require_confirmed
        and module_evidence[0].strip() in {"无", "待确认"}
    ):
        errors.append(
            f"已确认模块拆分不能使用空确认依据：{module_design}"
        )
    for field in (
        "适用系统",
        "适用范围",
        "代码现实快照",
    ):
        if len(
            re.findall(
                rf"^{re.escape(field)}[ \t]*[：:][ \t]*(\S.*)$",
                module_text,
                re.MULTILINE,
            )
        ) != 1:
            errors.append(
                f"模块拆分必须且只能声明一个非空“{field}”："
                f"{module_design}"
            )

    module_h2_matches = list(
        re.finditer(r"^##\s+(.+?)\s*$", module_text, re.MULTILINE)
    )
    module_h2_titles = [match.group(1) for match in module_h2_matches]
    if module_h2_titles[:2] != MODULE_PREFIX_HEADINGS:
        errors.append(
            "模块拆分必须先按顺序包含"
            f"（{' / '.join(MODULE_PREFIX_HEADINGS)}）：{module_design}"
        )
    if module_h2_titles[-len(MODULE_TAIL_HEADINGS):] != MODULE_TAIL_HEADINGS:
        errors.append(
            "模块拆分必须最后按顺序包含"
            f"（{' / '.join(MODULE_TAIL_HEADINGS)}）：{module_design}"
        )

    detail_start = len(MODULE_PREFIX_HEADINGS)
    detail_end = len(module_h2_titles) - len(MODULE_TAIL_HEADINGS)
    module_detail_matches = module_h2_matches[detail_start:detail_end]
    if not module_detail_matches:
        errors.append(f"模块拆分至少需要一个 MOD- 模块章节：{module_design}")
    seen_module_ids: set[str] = set()
    for index, module_match in enumerate(module_detail_matches):
        parsed_title = MODULE_TITLE_RE.fullmatch(module_match.group(1))
        if parsed_title is None:
            errors.append(
                "模块详细章节标题必须为"
                f"“MOD-<标识>：<模块名称>”：{module_design}"
            )
            continue
        module_id = parsed_title.group(1)
        if module_id in seen_module_ids:
            errors.append(f"模块标识重复“{module_id}”：{module_design}")
        seen_module_ids.add(module_id)

        section_end = (
            module_detail_matches[index + 1].start()
            if index + 1 < len(module_detail_matches)
            else (
                module_h2_matches[detail_end].start()
                if detail_end < len(module_h2_matches)
                else len(module_text)
            )
        )
        detail_text = module_text[module_match.end():section_end]
        h3_headings = re.findall(
            r"^###\s+(.+?)\s*$", detail_text, re.MULTILINE
        )
        if h3_headings != MODULE_DETAIL_HEADINGS:
            errors.append(
                f"{module_id} 必须且只能按顺序包含"
                f"（{' / '.join(MODULE_DETAIL_HEADINGS)}）：{module_design}"
            )

    if (
        "| 模块标识 | 模块名称 | 为什么存在 | 主要责任 |"
        " 承载的 Domain | 详细章节 |"
    ) not in module_text:
        errors.append(f"模块目录缺少固定表头：{module_design}")

    return errors, warnings


def validate_implementation_task_graph(
    task_graph: Path,
    require_current: bool = False,
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not task_graph.exists():
        errors.append(f"缺少开发任务图：{task_graph}")
        return errors, warnings

    text = task_graph.read_text(encoding="utf-8")
    headings = re.findall(r"^##\s+(.+?)\s*$", text, re.MULTILINE)
    if headings != TASK_GRAPH_HEADINGS:
        errors.append(
            "开发任务图必须且只能按顺序包含八个二级标题"
            f"（{' / '.join(TASK_GRAPH_HEADINGS)}）：{task_graph}"
        )

    for field in (
        "状态",
        "任务图确认",
        "任务图确认依据",
        "适用系统",
        "开发批次",
        "开发基线",
        "工程编码规范",
        "起始代码快照",
        "维护角色",
    ):
        matches = re.findall(
            rf"^{re.escape(field)}[ \t]*[：:][ \t]*(\S.*)$",
            text,
            re.MULTILINE,
        )
        if len(matches) != 1:
            errors.append(
                f"开发任务图必须且只能声明一个非空“{field}”：{task_graph}"
            )

    statuses = TASK_GRAPH_STATUS_RE.findall(text)
    confirmations = TASK_GRAPH_CONFIRMATION_RE.findall(text)
    if len(statuses) != 1:
        errors.append(f"开发任务图必须声明一个有效状态：{task_graph}")
    if len(confirmations) != 1:
        errors.append(f"开发任务图必须声明一个有效确认状态：{task_graph}")
    if require_current:
        if statuses and statuses[0] not in ("当前", "已完成"):
            errors.append(f"执行开发要求任务图状态为“当前”或“已完成”：{task_graph}")
        if confirmations != ["已确认"]:
            errors.append(f"执行开发要求任务图确认：已确认：{task_graph}")

    task_matches = list(TASK_HEADING_RE.finditer(text))
    if not task_matches:
        errors.append(f"开发任务图至少需要一个 TASK- 任务：{task_graph}")
        return errors, warnings

    task_ids = [match.group(1) for match in task_matches]
    if len(task_ids) != len(set(task_ids)):
        errors.append(f"开发任务图中的 TASK- 标识必须唯一：{task_graph}")

    dependencies: dict[str, list[str]] = {}
    for index, match in enumerate(task_matches):
        task_id = match.group(1)
        end = (
            task_matches[index + 1].start()
            if index + 1 < len(task_matches)
            else re.search(
                r"^##\s+集成与统一代码快照\s*$",
                text[match.end():],
                re.MULTILINE,
            )
        )
        if isinstance(end, re.Match):
            section_end = match.end() + end.start()
        elif isinstance(end, int):
            section_end = end
        else:
            section_end = len(text)
        section = text[match.end():section_end]

        for field in TASK_DETAIL_FIELDS:
            values = re.findall(
                rf"^{re.escape(field)}[ \t]*[：:][ \t]*(\S.*)$",
                section,
                re.MULTILINE,
            )
            if len(values) != 1:
                errors.append(
                    f"{task_id} 必须且只能声明一个非空“{field}”：{task_graph}"
                )

        task_types = re.findall(
            r"^任务类型[ \t]*[：:][ \t]*(\S.*)$",
            section,
            re.MULTILINE,
        )
        if len(task_types) == 1 and task_types[0] not in TASK_TYPES:
            errors.append(
                f"{task_id} 的任务类型不在固定分类中：{task_graph}"
            )

        prerequisite_values = re.findall(
            r"^前置任务[ \t]*[：:][ \t]*(\S.*)$",
            section,
            re.MULTILINE,
        )
        if len(prerequisite_values) == 1:
            value = prerequisite_values[0]
            referenced = re.findall(
                r"TASK-[A-Za-z0-9][A-Za-z0-9._-]*",
                value,
            )
            if value != "无" and not referenced:
                errors.append(
                    f"{task_id} 的前置任务必须为“无”或 TASK- 标识列表："
                    f"{task_graph}"
                )
            dependencies[task_id] = referenced

        completion = re.findall(
            r"^编码完成边界[ \t]*[：:][ \t]*(\S.*)$",
            section,
            re.MULTILINE,
        )
        if completion and re.search(
            r"测试|验证|验收|通过",
            completion[0],
        ):
            errors.append(
                f"{task_id} 的编码完成边界不得包含测试、验证、验收或通过："
                f"{task_graph}"
            )

        if re.search(
            r"^(测试用例|验证方式|验收条件|运行证据)[ \t]*[：:]",
            section,
            re.MULTILINE,
        ):
            errors.append(
                f"{task_id} 不得在生产代码任务中建立测试或验证字段："
                f"{task_graph}"
            )

    known_task_ids = set(task_ids)
    for task_id, prerequisites in dependencies.items():
        for prerequisite in prerequisites:
            if prerequisite not in known_task_ids:
                errors.append(
                    f"{task_id} 引用了不存在的前置任务 {prerequisite}："
                    f"{task_graph}"
                )
            if prerequisite == task_id:
                errors.append(
                    f"{task_id} 不能依赖自身：{task_graph}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def has_cycle(task_id: str) -> bool:
        if task_id in visiting:
            return True
        if task_id in visited:
            return False
        visiting.add(task_id)
        for prerequisite in dependencies.get(task_id, []):
            if prerequisite in known_task_ids and has_cycle(prerequisite):
                return True
        visiting.remove(task_id)
        visited.add(task_id)
        return False

    if any(has_cycle(task_id) for task_id in task_ids):
        errors.append(f"开发任务图存在循环依赖：{task_graph}")

    return errors, warnings


def validate(
    repo_root: Path,
    coding_system: str | None = None,
    architecture_system: str | None = None,
    orchestration_system: str | None = None,
    database_system: str | None = None,
    implementation_system: str | None = None,
    development_batch: str | None = None,
    review_batch: str | None = None,
    recovery_task: str | None = None,
) -> tuple[list[str], list[str]]:
    vcddd_root = repo_root / "docs" / "vcddd"
    errors: list[str] = []
    warnings: list[str] = []

    if implementation_system:
        if coding_system and coding_system != implementation_system:
            errors.append(
                "--coding-system 与 --implementation-system 必须指向同一系统。"
            )
        coding_system = implementation_system
    if review_batch and not coding_system:
        errors.append("--review-batch 必须同时指定 --coding-system。")
    if review_batch:
        if development_batch and development_batch != review_batch:
            errors.append(
                "--development-batch 与 --review-batch 同时使用时必须一致。"
            )
        development_batch = review_batch
    elif implementation_system and not development_batch:
        errors.append(
            "--implementation-system 必须同时指定 --development-batch。"
        )
    if development_batch and not (implementation_system or review_batch):
        errors.append(
            "--development-batch 必须与 --implementation-system 或"
            " --review-batch 一起使用。"
        )

    if not vcddd_root.exists():
        errors.append(f"缺少 VCDDD 目录：{vcddd_root}")
        return errors, warnings

    for required in (
        vcddd_root / "index.md",
        vcddd_root / "business" / "index.md",
        vcddd_root / "systems" / "index.md",
        vcddd_root / "work" / "index.md",
    ):
        if not required.exists():
            errors.append(f"缺少必要入口：{required}")

    root_index = vcddd_root / "index.md"
    if root_index.exists():
        root_targets = {
            local_link_path(root_index, raw_target)
            for raw_target in LINK_RE.findall(
                root_index.read_text(encoding="utf-8")
            )
        }
        for required_target in (
            vcddd_root / "business" / "index.md",
            vcddd_root / "systems" / "index.md",
            vcddd_root / "work" / "index.md",
        ):
            if (
                required_target.exists()
                and required_target.resolve() not in root_targets
            ):
                errors.append(f"项目入口未直接链接必要入口：{required_target}")

    markdown_files = sorted(vcddd_root.rglob("*.md"))
    for source in markdown_files:
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = local_link_path(source, raw_target)
            if target is not None and not target.exists():
                errors.append(f"断链：{source} -> {raw_target}")

    business_root = vcddd_root / "business"
    if business_root.exists():
        business_index = business_root / "index.md"
        business_targets = (
            {
                local_link_path(business_index, raw_target)
                for raw_target in LINK_RE.findall(
                    business_index.read_text(encoding="utf-8")
                )
            }
            if business_index.exists()
            else set()
        )
        for business_design in sorted(business_root.glob("*/业务设计.md")):
            if business_design.resolve() not in business_targets:
                errors.append(f"业务入口未直接链接业务设计：{business_design}")
            text = business_design.read_text(encoding="utf-8")
            headings = re.findall(
                r"^##\s+(.+?)\s*$", text, re.MULTILINE
            )
            if headings != BUSINESS_DESIGN_HEADINGS:
                errors.append(
                    "业务设计必须且只能按顺序包含三个二级标题"
                    f"（{' / '.join(BUSINESS_DESIGN_HEADINGS)}）：{business_design}"
                )

    systems_root = vcddd_root / "systems"
    if systems_root.exists():
        systems_index = systems_root / "index.md"
        system_targets = (
            {
                local_link_path(systems_index, raw_target)
                for raw_target in LINK_RE.findall(
                    systems_index.read_text(encoding="utf-8")
                )
            }
            if systems_index.exists()
            else set()
        )
        for system_index in sorted(systems_root.glob("*/index.md")):
            if system_index.resolve() not in system_targets:
                errors.append(f"系统入口未直接链接系统：{system_index}")

        for baseline in sorted(systems_root.glob("*/开发基线.md")):
            text = baseline.read_text(encoding="utf-8")
            statuses = BASELINE_STATUS_RE.findall(text)
            if len(statuses) != 1:
                errors.append(
                    "开发基线必须且只能有一个独立状态行"
                    f"（当前/待确认/待重新生成/已替代）：{baseline}"
                )

            system_index = baseline.parent / "index.md"
            if not system_index.exists():
                errors.append(f"开发基线缺少系统入口：{system_index}")
                continue

            index_text = system_index.read_text(encoding="utf-8")
            linked_targets = {
                local_link_path(system_index, raw_target)
                for raw_target in LINK_RE.findall(index_text)
            }
            if baseline.resolve() not in linked_targets:
                errors.append(f"孤儿开发基线，系统入口未直接链接：{baseline}")

        for legacy in sorted(systems_root.glob("*/**/*最终*.md")):
            if legacy.name != "开发基线.md":
                warnings.append(f"检查可能与开发基线竞争的“最终”文件：{legacy}")

    work_root = vcddd_root / "work"
    if work_root.exists():
        work_index = work_root / "index.md"
        work_targets = (
            {
                local_link_path(work_index, raw_target)
                for raw_target in LINK_RE.findall(
                    work_index.read_text(encoding="utf-8")
                )
            }
            if work_index.exists()
            else set()
        )
        for task_index in sorted(work_root.glob("*/index.md")):
            controller_state = task_index.parent / "主控状态.md"
            if not controller_state.exists():
                if task_index.resolve() not in work_targets:
                    errors.append(
                        f"工作入口未直接链接旧任务恢复文档：{task_index}"
                    )
                warnings.append(
                    f"活动任务尚未建立短主控状态，恢复前需要迁移：{controller_state}"
                )
                continue

            if controller_state.resolve() not in work_targets:
                errors.append(f"工作入口未直接链接主控状态：{controller_state}")

            controller_targets = {
                local_link_path(controller_state, raw_target)
                for raw_target in LINK_RE.findall(
                    controller_state.read_text(encoding="utf-8")
                )
            }
            if task_index.resolve() not in controller_targets:
                errors.append(
                    f"主控状态未直接链接完整任务恢复文档：{controller_state}"
                )

    if recovery_task:
        if Path(recovery_task).name != recovery_task:
            errors.append(f"恢复任务名必须是单个目录名：{recovery_task}")
            return errors, warnings

        task_index = work_root / recovery_task / "index.md"
        controller_state = work_root / recovery_task / "主控状态.md"
        if not task_index.exists():
            errors.append(f"缺少任务恢复文档：{task_index}")
            return errors, warnings
        if not controller_state.exists():
            errors.append(f"缺少主控状态：{controller_state}")
            return errors, warnings

        task_text = task_index.read_text(encoding="utf-8")
        task_headings = re.findall(
            r"^##\s+(.+?)\s*$", task_text, re.MULTILINE
        )
        if task_headings != TASK_RECOVERY_HEADINGS:
            errors.append(
                "任务恢复文档必须且只能按顺序包含七个二级标题"
                f"（{' / '.join(TASK_RECOVERY_HEADINGS)}）：{task_index}"
            )
        else:
            invalid_fields = []
            for field in TASK_RECOVERY_FIELDS:
                matches = re.findall(
                    rf"^{re.escape(field)}[ \t]*[：:][ \t]*(\S.*)$",
                    task_text,
                    re.MULTILINE,
                )
                if len(matches) != 1:
                    invalid_fields.append(field)
            if invalid_fields:
                errors.append(
                    "任务恢复文档缺少、重复或留空的合同字段"
                    f"（{' / '.join(invalid_fields)}）：{task_index}"
                )

        controller_text = controller_state.read_text(encoding="utf-8")
        invalid_controller_fields = []
        for field in CONTROLLER_STATE_FIELDS:
            matches = re.findall(
                rf"^{re.escape(field)}[ \t]*[：:][ \t]*(\S.*)$",
                controller_text,
                re.MULTILINE,
            )
            if len(matches) != 1:
                invalid_controller_fields.append(field)
        if invalid_controller_fields:
            errors.append(
                "主控状态缺少、重复或留空的合同字段"
                f"（{' / '.join(invalid_controller_fields)}）："
                f"{controller_state}"
            )
        if len(CONTROLLER_STATUS_RE.findall(controller_text)) != 1:
            errors.append(
                "主控状态必须且只能声明一个有效通信状态"
                "（待派发/Agent 工作中/等待用户/可继续/阻塞/完成）："
                f"{controller_state}"
            )

        controller_targets = {
            local_link_path(controller_state, raw_target)
            for raw_target in LINK_RE.findall(controller_text)
        }
        if task_index.resolve() not in controller_targets:
            errors.append(
                f"主控状态未直接链接完整任务恢复文档：{controller_state}"
            )
        if controller_state.resolve() not in work_targets:
            errors.append(f"当前任务未由工作入口直接链接主控状态：{controller_state}")

    if architecture_system:
        if Path(architecture_system).name != architecture_system:
            errors.append(f"系统名必须是单个目录名：{architecture_system}")
            return errors, warnings
        architecture_errors, architecture_warnings = (
            validate_architecture_and_modules(
                systems_root / architecture_system,
                require_confirmed=False,
            )
        )
        errors.extend(architecture_errors)
        warnings.extend(architecture_warnings)

    if orchestration_system:
        if Path(orchestration_system).name != orchestration_system:
            errors.append(f"系统名必须是单个目录名：{orchestration_system}")
            return errors, warnings
        orchestration_errors, orchestration_warnings = (
            validate_internal_orchestration(
                systems_root / orchestration_system,
                require_confirmed=False,
            )
        )
        errors.extend(orchestration_errors)
        warnings.extend(orchestration_warnings)

    if database_system:
        if Path(database_system).name != database_system:
            errors.append(f"系统名必须是单个目录名：{database_system}")
            return errors, warnings
        database_errors, database_warnings = validate_database_design(
            systems_root / database_system,
            require_confirmed=False,
        )
        errors.extend(database_errors)
        warnings.extend(database_warnings)

    if coding_system:
        if Path(coding_system).name != coding_system:
            errors.append(f"系统名必须是单个目录名：{coding_system}")
            return errors, warnings

        system_root = systems_root / coding_system
        system_index = system_root / "index.md"
        baseline = system_root / "开发基线.md"
        engineering_standard = (
            system_root / ENGINEERING_CODING_STANDARD_FILE
        )
        required_design_files = [
            system_index,
            *(system_root / name for name in SYSTEM_FACT_FILES),
            baseline,
            engineering_standard,
        ]
        missing_design_files = [
            path for path in required_design_files if not path.exists()
        ]
        if missing_design_files:
            for path in missing_design_files:
                errors.append(f"准备 Coding 的系统缺少固定实现输入：{path}")
            return errors, warnings

        index_text = system_index.read_text(encoding="utf-8")
        index_targets = {
            local_link_path(system_index, raw_target)
            for raw_target in LINK_RE.findall(index_text)
        }
        for design_file in required_design_files[1:]:
            if design_file.resolve() not in index_targets:
                errors.append(f"系统入口未直接链接固定实现输入：{design_file}")

        database_errors, database_warnings = validate_database_design(
            system_root,
            require_confirmed=True,
        )
        errors.extend(database_errors)
        warnings.extend(database_warnings)

        architecture_errors, architecture_warnings = (
            validate_architecture_and_modules(
                system_root,
                require_confirmed=True,
            )
        )
        errors.extend(architecture_errors)
        warnings.extend(architecture_warnings)

        system_split = system_root / "系统拆分.md"
        system_split_text = system_split.read_text(encoding="utf-8")
        if BUSINESS_SUBJECT_CONFIRMATION_RE.findall(system_split_text) != ["已确认"]:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明"
                f"“业务主体确认：已确认”：{system_split}"
            )
        if len(BUSINESS_SUBJECT_EVIDENCE_RE.findall(system_split_text)) != 1:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明一个"
                "非空业务主体确认依据："
                f"{system_split}"
            )
        if DOMAIN_DESIGN_CONFIRMATION_RE.findall(system_split_text) != ["已确认"]:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明"
                f"“Domain 设计确认：已确认”：{system_split}"
            )
        if len(DOMAIN_DESIGN_EVIDENCE_RE.findall(system_split_text)) != 1:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明一个"
                "非空 Domain 设计确认依据："
                f"{system_split}"
            )
        if NAMING_CONFIRMATION_RE.findall(system_split_text) != ["已确认"]:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明"
                f"“核心命名确认：已确认”：{system_split}"
            )
        if len(NAMING_EVIDENCE_RE.findall(system_split_text)) != 1:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明一个"
                f"非空核心命名确认依据：{system_split}"
            )

        baseline_text = baseline.read_text(encoding="utf-8")
        statuses = BASELINE_STATUS_RE.findall(baseline_text)
        if statuses != ["当前"]:
            errors.append(f"准备 Coding 的开发基线状态不是“当前”：{baseline}")

        if len(SCOPE_RE.findall(baseline_text)) != 1:
            errors.append(f"开发基线必须且只能声明一个非空适用范围：{baseline}")
        if len(EXCLUDED_SCOPE_RE.findall(baseline_text)) != 1:
            errors.append(f"开发基线必须且只能声明一个非空未覆盖范围：{baseline}")

        source_sections = SOURCES_RE.findall(baseline_text)
        if (
            len(source_sections) != 1
            or not LINK_RE.search(source_sections[0])
        ):
            errors.append(f"开发基线来源必须包含至少一个可追溯链接：{baseline}")
        else:
            source_targets = {
                local_link_path(baseline, raw_target)
                for raw_target in LINK_RE.findall(source_sections[0])
            }
            for source_file in (
                system_root / name for name in SYSTEM_FACT_FILES
            ):
                if source_file.resolve() not in source_targets:
                    errors.append(
                        f"开发基线未引用固定事实文档：{source_file}"
                    )
            if not any(
                target is not None and target.name == "业务设计.md"
                for target in source_targets
            ):
                errors.append(f"开发基线未引用相关业务设计：{baseline}")

        headings = re.findall(r"^##\s+(.+?)\s*$", baseline_text, re.MULTILINE)
        if headings != BASELINE_HEADINGS:
            errors.append(
                "开发基线必须且只能按顺序包含三个二级标题"
                f"（{' / '.join(BASELINE_HEADINGS)}）：{baseline}"
            )

        engineering_standard_text = engineering_standard.read_text(
            encoding="utf-8"
        )
        if ENGINEERING_STANDARD_STATUS_RE.findall(
            engineering_standard_text
        ) != ["当前"]:
            errors.append(
                "准备 Coding 的工程编码规范必须且只能声明"
                f"“状态：当前”：{engineering_standard}"
            )
        if ENGINEERING_STANDARD_CONFIRMATION_RE.findall(
            engineering_standard_text
        ) != ["已确认"]:
            errors.append(
                "准备 Coding 的工程编码规范必须且只能声明"
                f"“规范确认：已确认”：{engineering_standard}"
            )
        standard_evidence = ENGINEERING_STANDARD_EVIDENCE_RE.findall(
            engineering_standard_text
        )
        if (
            len(standard_evidence) != 1
            or standard_evidence[0].strip() in {"无", "待确认"}
        ):
            errors.append(
                "准备 Coding 的工程编码规范必须声明一个"
                f"有效确认依据：{engineering_standard}"
            )
        if ENGINEERING_STANDARD_FORMATION_RE.findall(
            engineering_standard_text
        ) not in (["已有代码归纳"], ["全新系统初始化"]):
            errors.append(
                "工程编码规范必须且只能声明有效形成方式"
                f"（已有代码归纳/全新系统初始化）：{engineering_standard}"
            )
        for field in (
            "适用系统",
            "适用代码范围",
            "语言及版本",
            "主要框架及版本",
            "规范版本",
            "生效代码快照",
            "最佳实践资料版本或取得时间",
            "维护角色",
        ):
            matches = re.findall(
                rf"^{field}[ \t]*[：:][ \t]*(\S.*)$",
                engineering_standard_text,
                re.MULTILINE,
            )
            if len(matches) != 1:
                errors.append(
                    f"工程编码规范必须且只能声明一个非空“{field}”："
                    f"{engineering_standard}"
                )
        engineering_headings = re.findall(
            r"^##\s+(.+?)\s*$",
            engineering_standard_text,
            re.MULTILINE,
        )
        required_engineering_positions = [
            engineering_headings.index(heading)
            if heading in engineering_headings
            else -1
            for heading in ENGINEERING_STANDARD_HEADINGS
        ]
        if (
            -1 in required_engineering_positions
            or required_engineering_positions
            != sorted(required_engineering_positions)
        ):
            errors.append(
                "工程编码规范必须按顺序包含"
                f"（{' / '.join(ENGINEERING_STANDARD_HEADINGS)}）："
                f"{engineering_standard}"
            )

        git_probe = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=False,
        )
        if git_probe.returncode != 0:
            errors.append(f"准备 Coding 的目标目录不是 Git 版本管理仓库：{repo_root}")
        else:
            for design_file in required_design_files:
                relative_file = design_file.relative_to(repo_root)
                tracked = subprocess.run(
                    [
                        "git",
                        "-C",
                        str(repo_root),
                        "ls-files",
                        "--error-unmatch",
                        str(relative_file),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if tracked.returncode != 0:
                    errors.append(
                        f"准备 Coding 的固定实现输入尚未纳入版本管理：{design_file}"
                    )

        if development_batch:
            if Path(development_batch).name != development_batch:
                errors.append(
                    f"开发批次名必须是单个目录名：{development_batch}"
                )
                return errors, warnings

            development_root = system_root / "开发记录"
            development_index = development_root / "index.md"
            batch_root = development_root / development_batch
            task_graph = batch_root / "开发任务图.md"

            graph_errors, graph_warnings = validate_implementation_task_graph(
                task_graph,
                require_current=bool(review_batch),
            )
            errors.extend(graph_errors)
            warnings.extend(graph_warnings)

            if not development_index.exists():
                errors.append(f"缺少开发记录入口：{development_index}")
            else:
                if development_index.resolve() not in index_targets:
                    errors.append(
                        f"系统入口未直接链接开发记录入口：{development_index}"
                    )
                development_index_text = development_index.read_text(
                    encoding="utf-8"
                )
                development_targets = {
                    local_link_path(development_index, raw_target)
                    for raw_target in LINK_RE.findall(development_index_text)
                }
                if task_graph.exists() and (
                    task_graph.resolve() not in development_targets
                ):
                    errors.append(
                        f"开发记录入口未直接链接开发任务图：{task_graph}"
                    )

            if task_graph.exists():
                task_graph_text = task_graph.read_text(encoding="utf-8")
                task_graph_targets = {
                    local_link_path(task_graph, raw_target)
                    for raw_target in LINK_RE.findall(task_graph_text)
                }
                if baseline.resolve() not in task_graph_targets:
                    errors.append(
                        f"开发任务图未直接链接当前开发基线：{task_graph}"
                    )
                if engineering_standard.resolve() not in task_graph_targets:
                    errors.append(
                        f"开发任务图未直接链接当前工程编码规范：{task_graph}"
                    )

            if review_batch:
                if task_graph.exists() and TASK_GRAPH_STATUS_RE.findall(
                    task_graph.read_text(encoding="utf-8")
                ) != ["已完成"]:
                    errors.append(
                        f"进入统一测试与审核要求任务图状态为“已完成”："
                        f"{task_graph}"
                    )

                implementation_root = batch_root / "实施任务"
                implementation_records = sorted(
                    implementation_root.glob("TASK-*/实现记录.md")
                )
                integration_record = batch_root / "集成记录.md"
                test_feedback_root = batch_root / "测试反馈"
                test_feedback_files = sorted(test_feedback_root.glob("*.md"))
                test_conclusion = batch_root / "测试结论.md"
                design_feedback_root = batch_root / "设计反馈"
                improvement_root = batch_root / "工程改进"
                improvement_files = sorted(improvement_root.glob("*.md"))
                review_root = batch_root / "审核"
                review_files = [
                    review_root / name for name in CORE_REVIEW_FILES
                ]
                review_summary = batch_root / "审核结论.md"

                required_batch_files = [
                    integration_record,
                    test_conclusion,
                    *review_files,
                    review_summary,
                ]
                for path in required_batch_files:
                    if not path.exists():
                        errors.append(f"开发批次缺少测试或审核记录：{path}")
                if not implementation_records:
                    errors.append(
                        f"开发批次至少需要一个实施任务实现记录："
                        f"{implementation_root}"
                    )
                if not test_feedback_files:
                    errors.append(
                        f"开发批次至少需要一份统一测试反馈："
                        f"{test_feedback_root}"
                    )
                if not improvement_files:
                    errors.append(
                        f"进入正式审核前至少需要一份工程改进记录："
                        f"{improvement_root}"
                    )

                if any(not path.exists() for path in required_batch_files):
                    return errors, warnings

                if development_index.exists():
                    development_targets = {
                        local_link_path(development_index, raw_target)
                        for raw_target in LINK_RE.findall(
                            development_index.read_text(encoding="utf-8")
                        )
                    }
                    for path in (
                        integration_record,
                        test_conclusion,
                        review_summary,
                    ):
                        if path.resolve() not in development_targets:
                            errors.append(
                                f"开发记录入口未直接链接批次文档：{path}"
                            )

                for implementation_record in implementation_records:
                    implementation_text = implementation_record.read_text(
                        encoding="utf-8"
                    )
                    implementation_targets = {
                        local_link_path(implementation_record, raw_target)
                        for raw_target in LINK_RE.findall(implementation_text)
                    }
                    for path, label in (
                        (task_graph, "开发任务图"),
                        (baseline, "开发基线"),
                        (engineering_standard, "工程编码规范"),
                    ):
                        if path.resolve() not in implementation_targets:
                            errors.append(
                                f"实现记录未直接链接当前{label}："
                                f"{implementation_record}"
                            )
                    implementation_headings = re.findall(
                        r"^##\s+(.+?)\s*$",
                        implementation_text,
                        re.MULTILINE,
                    )
                    if implementation_headings != IMPLEMENTATION_HEADINGS:
                        errors.append(
                            "实现记录必须且只能按顺序包含六个二级标题"
                            f"（{' / '.join(IMPLEMENTATION_HEADINGS)}）："
                            f"{implementation_record}"
                        )
                    for field in (
                        "开发任务图",
                        "实施任务",
                        "开发基线",
                        "工程编码规范",
                        "worktree 起始快照",
                        "输出代码快照",
                        "实现范围",
                        "未覆盖范围",
                    ):
                        matches = re.findall(
                            rf"^{re.escape(field)}[ \t]*[：:]"
                            r"[ \t]*(\S.*)$",
                            implementation_text,
                            re.MULTILINE,
                        )
                        if len(matches) != 1:
                            errors.append(
                                "实现记录必须且只能声明一个非空"
                                f"“{field}”：{implementation_record}"
                            )
                    if re.search(
                        r"^##\s+(测试|验证|验收|运行证据)",
                        implementation_text,
                        re.MULTILINE,
                    ):
                        errors.append(
                            "实施任务实现记录不得包含测试或验证章节："
                            f"{implementation_record}"
                        )

                integration_text = integration_record.read_text(
                    encoding="utf-8"
                )
                for field in INTEGRATION_FIELDS:
                    matches = re.findall(
                        rf"^{re.escape(field)}[ \t]*[：:]"
                        r"[ \t]*(\S.*)$",
                        integration_text,
                        re.MULTILINE,
                    )
                    if len(matches) != 1:
                        errors.append(
                            f"集成记录缺少、重复或留空字段“{field}”："
                            f"{integration_record}"
                        )
                if re.findall(
                    r"^测试状态[ \t]*[：:][ \t]*(\S.*)$",
                    integration_text,
                    re.MULTILINE,
                ) != ["完成"]:
                    errors.append(
                        f"进入正式审核前统一测试状态必须为“完成”："
                        f"{integration_record}"
                    )
                if re.findall(
                    r"^工程改进状态[ \t]*[：:][ \t]*(\S.*)$",
                    integration_text,
                    re.MULTILINE,
                ) != ["完成"]:
                    errors.append(
                        f"进入正式审核前工程改进状态必须为“完成”："
                        f"{integration_record}"
                    )
                production_snapshots = (
                    UNIFIED_PRODUCTION_SNAPSHOT_RE.findall(integration_text)
                )
                final_snapshots = FINAL_REVIEW_SNAPSHOT_RE.findall(
                    integration_text
                )
                production_snapshot = (
                    production_snapshots[0]
                    if len(production_snapshots) == 1
                    else None
                )
                final_snapshot = (
                    final_snapshots[0]
                    if len(final_snapshots) == 1
                    else None
                )

                for feedback_file in test_feedback_files:
                    feedback_text = feedback_file.read_text(encoding="utf-8")
                    for field in TEST_FEEDBACK_FIELDS:
                        matches = re.findall(
                            rf"^{re.escape(field)}[ \t]*[：:]"
                            r"[ \t]*(\S.*)$",
                            feedback_text,
                            re.MULTILINE,
                        )
                        if len(matches) != 1:
                            errors.append(
                                "测试反馈缺少、重复或留空字段"
                                f"“{field}”：{feedback_file}"
                            )
                    feedback_inputs = re.findall(
                        r"^输入生产代码快照[ \t]*[：:][ \t]*(\S.*)$",
                        feedback_text,
                        re.MULTILINE,
                    )
                    if (
                        production_snapshot is not None
                        and feedback_inputs != [production_snapshot]
                    ):
                        errors.append(
                            "测试反馈输入必须与集成记录统一生产代码快照"
                            f"一致：{feedback_file}"
                        )
                    if len(re.findall(
                        r"^测试结果[ \t]*[：:][ \t]*"
                        r"(通过|发现问题|无法执行)[ \t]*$",
                        feedback_text,
                        re.MULTILINE,
                    )) != 1:
                        errors.append(
                            f"测试反馈必须声明有效测试结果：{feedback_file}"
                        )
                    if len(re.findall(
                        r"^问题责任[ \t]*[：:][ \t]*"
                        r"(无|生产代码|测试代码|工程规范|上游设计|平台环境)"
                        r"[ \t]*$",
                        feedback_text,
                        re.MULTILINE,
                    )) != 1:
                        errors.append(
                            f"测试反馈必须声明有效问题责任：{feedback_file}"
                        )

                conclusion_text = test_conclusion.read_text(encoding="utf-8")
                for field in TEST_CONCLUSION_FIELDS:
                    matches = re.findall(
                        rf"^{re.escape(field)}[ \t]*[：:]"
                        r"[ \t]*(\S.*)$",
                        conclusion_text,
                        re.MULTILINE,
                    )
                    if len(matches) != 1:
                        errors.append(
                            f"测试结论缺少、重复或留空字段“{field}”："
                            f"{test_conclusion}"
                        )
                conclusion_production = re.findall(
                    r"^生产代码快照[ \t]*[：:][ \t]*(\S.*)$",
                    conclusion_text,
                    re.MULTILINE,
                )
                if (
                    production_snapshot is not None
                    and conclusion_production != [production_snapshot]
                ):
                    errors.append(
                        f"测试结论生产代码快照必须与集成记录一致："
                        f"{test_conclusion}"
                    )
                if re.findall(
                    r"^当前结论[ \t]*[：:][ \t]*(\S.*)$",
                    conclusion_text,
                    re.MULTILINE,
                ) != ["可进入工程改进"]:
                    errors.append(
                        f"进入工程改进要求测试结论为“可进入工程改进”："
                        f"{test_conclusion}"
                    )
                test_snapshots = TEST_CODE_SNAPSHOT_RE.findall(
                    conclusion_text
                )
                test_snapshot = (
                    test_snapshots[0] if len(test_snapshots) == 1 else None
                )
                conclusion_targets = {
                    local_link_path(test_conclusion, raw_target)
                    for raw_target in LINK_RE.findall(conclusion_text)
                }
                for feedback_file in test_feedback_files:
                    if feedback_file.resolve() not in conclusion_targets:
                        errors.append(
                            f"测试结论未直接链接测试反馈：{feedback_file}"
                        )

                has_abstraction_analysis = False
                improvement_input_snapshots: list[str] = []
                improvement_output_snapshots: list[str] = []
                for improvement_file in improvement_files:
                    improvement_text = improvement_file.read_text(
                        encoding="utf-8"
                    )
                    for field in ENGINEERING_IMPROVEMENT_FIELDS:
                        matches = re.findall(
                            rf"^{re.escape(field)}[ \t]*[：:]"
                            r"[ \t]*(\S.*)$",
                            improvement_text,
                            re.MULTILINE,
                        )
                        if len(matches) != 1:
                            errors.append(
                                "工程改进记录缺少、重复或留空字段"
                                f"“{field}”：{improvement_file}"
                            )
                    if len(re.findall(
                        r"^工作方式[ \t]*[：:][ \t]*"
                        r"(只读分析|代码改进)[ \t]*$",
                        improvement_text,
                        re.MULTILINE,
                    )) != 1:
                        errors.append(
                            f"工程改进记录必须声明有效工作方式："
                            f"{improvement_file}"
                        )
                    if re.search(
                        r"^分析角度[ \t]*[：:][ \t]*.*"
                        r"(重复|抽象).*$",
                        improvement_text,
                        re.MULTILINE,
                    ):
                        has_abstraction_analysis = True
                    improvement_input_snapshots.extend(re.findall(
                        r"^输入代码快照[ \t]*[：:][ \t]*(\S.*)$",
                        improvement_text,
                        re.MULTILINE,
                    ))
                    input_test_snapshots = re.findall(
                        r"^输入测试代码快照[ \t]*[：:][ \t]*(\S.*)$",
                        improvement_text,
                        re.MULTILINE,
                    )
                    if (
                        test_snapshot is not None
                        and input_test_snapshots != [test_snapshot]
                    ):
                        errors.append(
                            f"工程改进输入测试快照必须与测试结论一致："
                            f"{improvement_file}"
                        )
                    improvement_output_snapshots.extend(
                        IMPROVEMENT_OUTPUT_SNAPSHOT_RE.findall(
                            improvement_text
                        )
                    )
                if not has_abstraction_analysis:
                    errors.append(
                        "进入正式审核前缺少独立的重复与抽象工程改进"
                        f"记录：{improvement_root}"
                    )
                if (
                    production_snapshot is not None
                    and production_snapshot not in improvement_input_snapshots
                ):
                    errors.append(
                        f"至少一份工程改进记录必须读取统一生产代码快照："
                        f"{integration_record}"
                    )
                if (
                    final_snapshot is not None
                    and final_snapshot not in improvement_output_snapshots
                ):
                    errors.append(
                        f"最终待审核快照必须由工程改进记录输出："
                        f"{integration_record}"
                    )

                design_feedback_files = sorted(
                    design_feedback_root.glob("*.md")
                )
                for feedback_file in design_feedback_files:
                    feedback_text = feedback_file.read_text(encoding="utf-8")
                    for field in DESIGN_FEEDBACK_FIELDS:
                        matches = re.findall(
                            rf"^{re.escape(field)}[ \t]*[：:]"
                            r"[ \t]*(\S.*)$",
                            feedback_text,
                            re.MULTILINE,
                        )
                        if len(matches) != 1:
                            errors.append(
                                "设计反馈记录缺少、重复或留空字段"
                                f"“{field}”：{feedback_file}"
                            )
                    statuses = DESIGN_FEEDBACK_STATUS_RE.findall(
                        feedback_text
                    )
                    if len(statuses) != 1 or statuses[0] not in (
                        "不采纳",
                        "已重新确认",
                    ):
                        errors.append(
                            "进入正式审核前设计反馈必须已经不采纳或完成"
                            f"重新确认：{feedback_file}"
                        )

                for review_file in review_files:
                    review_text = review_file.read_text(encoding="utf-8")
                    for field in (
                        "审核生产代码快照",
                        "审核测试代码快照",
                        "依据的开发基线",
                        "依据的工程编码规范",
                        "审核范围",
                        "未覆盖范围",
                    ):
                        matches = re.findall(
                            rf"^{re.escape(field)}[ \t]*[：:]"
                            r"[ \t]*(\S.*)$",
                            review_text,
                            re.MULTILINE,
                        )
                        if len(matches) != 1:
                            errors.append(
                                "审核记录必须且只能声明一个非空"
                                f"“{field}”：{review_file}"
                            )
                    if (
                        final_snapshot is not None
                        and REVIEW_OBJECT_RE.findall(review_text)
                        != [final_snapshot]
                    ):
                        errors.append(
                            f"审核生产代码快照必须与最终待审核快照一致："
                            f"{review_file}"
                        )
                    review_test_snapshots = re.findall(
                        r"^审核测试代码快照[ \t]*[：:][ \t]*(\S.*)$",
                        review_text,
                        re.MULTILINE,
                    )
                    if (
                        test_snapshot is not None
                        and review_test_snapshots != [test_snapshot]
                    ):
                        errors.append(
                            f"审核测试代码快照必须与测试结论一致："
                            f"{review_file}"
                        )
                    if len(REVIEW_RESULT_RE.findall(review_text)) != 1:
                        errors.append(
                            "审核记录必须且只能声明一个审核结论"
                            f"（通过/有条件通过/不通过）：{review_file}"
                        )

                summary_text = review_summary.read_text(encoding="utf-8")
                summary_standards = re.findall(
                    r"^工程编码规范[ \t]*[：:][ \t]*(\S.*)$",
                    summary_text,
                    re.MULTILINE,
                )
                if len(summary_standards) != 1:
                    errors.append(
                        f"审核结论必须声明一个非空工程编码规范："
                        f"{review_summary}"
                    )
                summary_production = re.findall(
                    r"^生产代码快照[ \t]*[：:][ \t]*(\S.*)$",
                    summary_text,
                    re.MULTILINE,
                )
                summary_tests = TEST_CODE_SNAPSHOT_RE.findall(summary_text)
                if (
                    final_snapshot is not None
                    and summary_production != [final_snapshot]
                ):
                    errors.append(
                        f"审核结论生产代码快照必须与集成记录一致："
                        f"{review_summary}"
                    )
                if (
                    test_snapshot is not None
                    and summary_tests != [test_snapshot]
                ):
                    errors.append(
                        f"审核结论测试代码快照必须与测试结论一致："
                        f"{review_summary}"
                    )
                if len(SUMMARY_RESULT_RE.findall(summary_text)) != 1:
                    errors.append(
                        "审核结论必须声明一个当前结论"
                        f"（通过/需修改/需重写/等待上游修订）："
                        f"{review_summary}"
                    )
                summary_targets = {
                    local_link_path(review_summary, raw_target)
                    for raw_target in LINK_RE.findall(summary_text)
                }
                for review_file in review_files:
                    if review_file.resolve() not in summary_targets:
                        errors.append(
                            f"审核结论未直接链接核心审核记录：{review_file}"
                        )

                if git_probe.returncode == 0:
                    tracked_batch_files = [
                        task_graph,
                        *implementation_records,
                        integration_record,
                        *test_feedback_files,
                        test_conclusion,
                        *design_feedback_files,
                        *improvement_files,
                        *review_files,
                        review_summary,
                    ]
                    for path in tracked_batch_files:
                        relative_file = path.relative_to(repo_root)
                        tracked = subprocess.run(
                            [
                                "git",
                                "-C",
                                str(repo_root),
                                "ls-files",
                                "--error-unmatch",
                                str(relative_file),
                            ],
                            capture_output=True,
                            text=True,
                            check=False,
                        )
                        if tracked.returncode != 0:
                            errors.append(
                                f"开发批次记录尚未纳入版本管理：{path}"
                            )

    return errors, warnings


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="vcddd-validator-") as temp_dir:
        repo_root = Path(temp_dir)
        vcddd_root = repo_root / "docs" / "vcddd"
        business_root = vcddd_root / "business" / "示例业务"
        system_root = vcddd_root / "systems" / "示例系统"
        business_root.mkdir(parents=True)
        (vcddd_root / "work").mkdir()
        system_root.mkdir(parents=True)
        task_root = vcddd_root / "work" / "示例任务"
        task_root.mkdir()

        (vcddd_root / "index.md").write_text(
            "[业务](business/index.md) [工作](work/index.md) "
            "[系统](systems/index.md)\n",
            encoding="utf-8",
        )
        (vcddd_root / "business" / "index.md").write_text(
            "[示例业务](示例业务/业务设计.md)\n", encoding="utf-8"
        )
        business_design = business_root / "业务设计.md"
        business_design.write_text(
            "# 业务设计\n\n"
            "## 业务目标与范围\n\n"
            "## 系统设计\n\n"
            "## 业务线逻辑\n",
            encoding="utf-8",
        )
        (vcddd_root / "work" / "index.md").write_text(
            "# 工作\n\n"
            "[示例任务](示例任务/主控状态.md)\n",
            encoding="utf-8",
        )
        (vcddd_root / "systems" / "index.md").write_text(
            "[示例系统](示例系统/index.md)\n", encoding="utf-8"
        )
        (system_root / "index.md").write_text(
            "[系统拆分](系统拆分.md)\n"
            "[架构设计](架构设计.md)\n"
            "[模块拆分](模块拆分.md)\n"
            "[API设计](API设计.md)\n"
            "[核心接口内部编排](核心接口内部编排.md)\n"
            "[数据库设计](数据库设计.md)\n"
            "[开发基线](开发基线.md)\n"
            "[工程编码规范](工程编码规范.md)\n"
            "[开发记录](开发记录/index.md)\n",
            encoding="utf-8",
        )
        for name in SYSTEM_FACT_FILES:
            if name == "系统拆分.md":
                metadata = (
                    "业务主体确认：已确认\n"
                    "业务主体确认依据：示例任务中的用户确认\n"
                    "Domain 设计确认：已确认\n"
                    "Domain 设计确认依据：示例任务中的用户确认\n"
                    "核心命名确认：已确认\n"
                    "核心命名确认依据：示例任务中的用户确认\n"
                )
            elif name == "架构设计.md":
                metadata = (
                    "架构设计确认：已确认\n"
                    "架构设计确认依据：示例任务中的用户确认\n"
                    "设计来源：[系统拆分](系统拆分.md)\n"
                    "适用系统：示例系统\n"
                    "适用范围：示例系统代码\n"
                    "语言及版本：Python 3\n"
                    "主要框架及版本：示例框架 1\n"
                    "代码现实快照：无代码\n\n"
                    "## 架构目标与约束\n\n"
                    "## 总体架构\n\n"
                    "## 层次与主要组件\n\n"
                    "## 依赖与调用边界\n\n"
                    "## 数据、外部系统与运行协作\n\n"
                    "## 系统级技术机制\n\n"
                    "## 技术选择与理由\n\n"
                    "## Coding 必须遵守的边界\n\n"
                    "## 允许 Coding 决定的内容\n\n"
                    "## 尚未确定的问题\n"
                )
            elif name == "模块拆分.md":
                metadata = (
                    "模块拆分确认：已确认\n"
                    "模块拆分确认依据：示例任务中的用户确认\n"
                    "设计来源：[架构设计](架构设计.md)\n"
                    "适用系统：示例系统\n"
                    "适用范围：示例系统代码\n"
                    "代码现实快照：无代码\n\n"
                    "## 模块全景\n\n"
                    "## 模块目录\n\n"
                    "| 模块标识 | 模块名称 | 为什么存在 | 主要责任 |"
                    " 承载的 Domain | 详细章节 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| MOD-example | 示例模块 | 承载示例 | 示例责任 |"
                    " 示例 Domain | 本文 |\n\n"
                    "## MOD-example：示例模块\n\n"
                    "### 存在意义\n\n"
                    "### 职责与非职责\n\n"
                    "### 承载的 Domain 与数据\n\n"
                    "### 对外提供与依赖\n\n"
                    "### 代码范围\n\n"
                    "## 模块依赖规则\n\n"
                    "## 业务覆盖\n\n"
                    "## Coding 必须遵守的边界\n\n"
                    "## 尚未确定的问题\n"
                )
            elif name == "API设计.md":
                metadata = (
                    "API 设计确认：已确认\n"
                    "API 设计确认依据：示例任务中的用户确认\n"
                    "API 标识：API-create-example\n"
                )
            elif name == "核心接口内部编排.md":
                metadata = (
                    "核心接口内部编排确认：已确认\n"
                    "核心接口内部编排确认依据：示例任务中的用户确认\n"
                    "API 设计来源：[API 设计](API设计.md)\n"
                    "\n## 接口目录\n\n"
                    "| API 标识 | 方法与路径或入口 | 调用者要得到的业务结果 | 编排章节 |\n"
                    "| --- | --- | --- | --- |\n"
                    "| API-create-example | `POST /examples` | 形成示例 | 本文 |\n"
                    "\n## API-create-example：POST /examples — 形成示例\n\n"
                    "### 业务结果\n\n"
                    "调用者意图：形成示例。\n\n"
                    "成功结果：示例已经形成。\n\n"
                    "明确不负责：无。\n\n"
                    "### 主流程\n\n"
                    "| 步骤 | 执行者 | 做什么 | 得到什么结果 | 下一步 |\n"
                    "| --- | --- | --- | --- | --- |\n"
                    "| S1 | API 入口 | 接收事实 | 有效输入 | S2 |\n"
                    "| S2 | 示例 Domain | 形成示例 | 示例结果 | S3 |\n"
                    "| S3 | Repository | 保存示例 | 提交成功 | 结束 |\n\n"
                    "### 分支与失败\n\n"
                    "| 分支 | 发生在步骤 | 条件 | 业务结果 | API 结果 | 后续 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| F1 | S1 | 输入无效 | 未形成示例 | 拒绝 | 结束 |\n\n"
                    "### 事务与外部影响\n\n"
                    "| 边界 | 覆盖步骤 | 提交或外部动作 | 成功证明 | 失败或结果未知处理 |\n"
                    "| --- | --- | --- | --- | --- |\n"
                    "| T1 | S2-S3 | 保存示例 | 提交成功 | 回滚 |\n\n"
                    "### Domain 调用\n\n"
                    "| 发生在步骤 | Domain 行为 | 输入事实 | 领域结果 | 权威规则位置 |\n"
                    "| --- | --- | --- | --- | --- |\n"
                    "| S2 | `示例.形成` | 示例输入 | 示例结果 | 系统拆分 |\n\n"
                    "### 业务证据与验证\n\n"
                    "关键业务日志与关联标识：示例标识。\n\n"
                    "必须验证的场景：正常、拒绝和提交失败。\n"
                )
            elif name == "数据库设计.md":
                metadata = (
                    "数据库设计确认：已确认\n"
                    "数据库设计确认依据：示例任务中的用户确认\n"
                    "设计来源：\n"
                    "- [系统拆分](系统拆分.md)\n"
                    "- [API 设计](API设计.md)\n"
                    "- [核心接口内部编排](核心接口内部编排.md)\n"
                    "适用数据库：关系型数据库\n"
                    "适用范围：示例系统\n"
                    "明确不覆盖：无\n\n"
                    "## 数据承载全景\n\n"
                    "| 需要保存的事实 | 事实拥有者 | 为什么需要持久化 | 使用者与用途 | 承载表 | 数据性质 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| 示例事实 | 示例 Domain | 重启后仍需存在 | API 查询 | DBT-example | Domain 状态 |\n\n"
                    "## 表目录\n\n"
                    "| 表标识 | 表名 | 中文名称 | 这张表为什么存在 | 一行表示什么 | 详细章节 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| DBT-example | `examples` | 示例 | 保存示例事实 | 一个示例 | 本文 |\n\n"
                    "## 数据关系图\n\n"
                    "只有一张表，不需要关系图。\n\n"
                    "## DBT-example：examples — 示例\n\n"
                    "### 表的意义\n\n"
                    "保存的事实：示例已经形成。\n\n"
                    "存在原因：系统重启后仍需查询示例。\n\n"
                    "一行表示：一个已经形成的示例。\n\n"
                    "为什么独立成表：示例有独立身份和生命周期。\n\n"
                    "数据库表注释原文：保存本系统已经形成的示例；一行代表一个示例。\n\n"
                    "数据性质：Domain 状态。\n\n"
                    "权威拥有者：示例 Domain。\n\n"
                    "是否参与业务判断：是，判断示例是否存在。\n\n"
                    "是否可重新生成：否。\n\n"
                    "来源：[系统拆分](系统拆分.md)。\n\n"
                    "### 产生、变化与使用\n\n"
                    "| 时点或事件 | 写入者 | 写入或变化 | 使用者 | 用途 |\n"
                    "| --- | --- | --- | --- | --- |\n"
                    "| API-create-example / S3 | Repository | 新增示例 | API | 返回结果 |\n\n"
                    "### 字段说明\n\n"
                    "| 字段 | 中文名称 | 字段为什么存在 | 保存的事实或含义 | 事实来源 | 数据类型 | 必填 | 空值含义 | 默认值及含义 | 允许值或范围 | 何时产生或改变 | 是否敏感 | 数据库注释原文 |\n"
                    "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
                    "| `id` | 示例标识 | 稳定识别示例 | 本系统分配的示例身份 | 示例 Domain | 标识 | 是 | 不允许为空 | 无 | 非空唯一值 | 创建时产生且不变 | 否 | 本系统分配的示例唯一标识。 |\n\n"
                    "### 身份、主键与唯一性\n\n"
                    "记录身份：由 id 稳定识别一个示例。\n\n"
                    "| 类型 | 字段组合 | 保证的事实 | 冲突时的业务含义 |\n"
                    "| --- | --- | --- | --- |\n"
                    "| 主键 | id | 一个标识只有一个示例 | 拒绝重复写入 |\n\n"
                    "### 与其他表的关系\n\n"
                    "| 关联表 | 本表字段 | 对方字段 | 关系与基数 | 存在性要求 | 删除或失效语义 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| 无 | 无 | 无 | 无 | 本表独立存在 | 不适用 |\n\n"
                    "### 必须保持的约束\n\n"
                    "| 约束 | 约束保护的事实 | 数据库责任 | Domain 或应用责任 | 违反时的结果 |\n"
                    "| --- | --- | --- | --- | --- |\n"
                    "| 主键唯一 | 示例身份唯一 | 拒绝重复 id | 创建唯一 id | 冲突 |\n\n"
                    "### 查询与索引\n\n"
                    "| 查询来源 | 查询条件与排序 | 频率或规模事实 | 建议索引 | 为什么需要 | 代价与不采用条件 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| API 查询 | id 等值 | 待观测 | 主键 | 定位一个示例 | 主键已有 |\n\n"
                    "### 事务、并发与编排对应\n\n"
                    "| API 与步骤 | 本表读写 | 原子范围或提交点 | 并发保护 | 失败、回滚或结果未知处理 |\n"
                    "| --- | --- | --- | --- | --- |\n"
                    "| API-create-example / S3 | 插入示例 | T1 提交 | 主键唯一 | 失败时回滚 |\n\n"
                    "### 历史、清理与迁移\n\n"
                    "保留要求：示例存在期间保留。\n\n"
                    "清理方式：业务删除时清理。\n\n"
                    "历史语义：只保存当前事实。\n\n"
                    "兼容与迁移要求：不涉及已有数据。\n\n"
                    "### 尚未确定的问题\n\n"
                    "无。\n\n"
                    "## 跨表事务与一致性\n\n"
                    "| API 与步骤 | 涉及表 | 必须共同成立的事实 | 原子边界 | 外部影响顺序 | 失败与恢复 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| API-create-example / S3 | DBT-example | 示例完整保存 | T1 | 无外部影响 | 回滚 |\n\n"
                    "## 查询投影与非 Domain 数据\n\n"
                    "不适用；当前只有 Domain 状态。\n\n"
                    "## 数据安全与保留\n\n"
                    "| 数据范围 | 敏感等级 | 访问者 | 脱敏或加密 | 保留与清理 | 审计要求 |\n"
                    "| --- | --- | --- | --- | --- | --- |\n"
                    "| DBT-example | 普通 | 示例系统 | 不需要 | 随业务生命周期 | 写入日志 |\n\n"
                    "## 数据库实现交接\n\n"
                    "Coding 阶段需要产生：迁移、映射、数据库注释和测试。\n\n"
                    "实现必须保持：本设计全部数据事实。\n\n"
                    "允许 Coding 决定：数据库语法和迁移工具。\n\n"
                    "必须返回设计的情况：数据事实或事务需要改变。\n"
                )
            else:
                metadata = ""
            (system_root / name).write_text(
                f"# {Path(name).stem}\n\n{metadata}",
                encoding="utf-8",
            )
        baseline_text = (
            "# 开发基线\n\n"
            "状态：当前\n"
            "适用范围：示例切片\n"
            "未覆盖范围：无\n"
            "来源：\n"
            "- [业务设计](../../business/示例业务/业务设计.md)\n"
            "- [系统拆分](系统拆分.md)\n"
            "- [架构设计](架构设计.md)\n"
            "- [模块拆分](模块拆分.md)\n"
            "- [API设计](API设计.md)\n"
            "- [核心接口内部编排](核心接口内部编排.md)\n"
            "- [数据库设计](数据库设计.md)\n\n"
            "## Domain\n\n"
            "## 架构与模块\n\n"
            "## 业务线与 API\n\n"
            "## 数据库设计\n"
        )
        (system_root / "开发基线.md").write_text(
            baseline_text, encoding="utf-8"
        )
        engineering_standard_text = (
            "# 示例系统工程编码规范\n\n"
            "状态：当前\n"
            "规范确认：已确认\n"
            "规范确认依据：示例任务中的用户确认\n"
            "形成方式：全新系统初始化\n"
            "适用系统：示例系统\n"
            "适用代码范围：示例系统代码\n"
            "语言及版本：Python 3\n"
            "主要框架及版本：示例框架 1\n"
            "规范版本：v1\n"
            "生效代码快照：无代码\n"
            "最佳实践资料版本或取得时间：示例资料 2026-07\n"
            "维护角色：Coding Agent\n\n"
            "## 使用与演化规则\n\n"
            "## 形成过程与依据\n\n"
            "## 当前规则索引\n\n"
            "## 架构与代码组织\n\n"
            "## Domain 与应用编排\n\n"
            "## 命名与代码表达\n\n"
            "## 事务\n\n"
            "## 数据访问\n\n"
            "## 错误处理\n\n"
            "## 日志与可观察性\n\n"
            "## 外部系统协作\n\n"
            "## 并发、异步与幂等\n\n"
            "## 配置与安全\n\n"
            "## 测试\n\n"
            "## 封装、复用与重复代码\n\n"
            "## 工具链与交付验证\n\n"
            "## 例外与存量处理\n\n"
            "## 尚未形成规范的问题\n\n"
            "## 重要演化\n"
        )
        engineering_standard = system_root / ENGINEERING_CODING_STANDARD_FILE
        engineering_standard.write_text(
            engineering_standard_text,
            encoding="utf-8",
        )
        errors, _ = validate_architecture_and_modules(
            system_root,
            require_confirmed=False,
        )
        if errors:
            print("自检失败：有效架构与模块样例未通过。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        architecture_file = system_root / "架构设计.md"
        valid_architecture_text = architecture_file.read_text(
            encoding="utf-8"
        )
        architecture_file.write_text(
            valid_architecture_text.replace("## 总体架构\n\n", ""),
            encoding="utf-8",
        )
        errors, _ = validate_architecture_and_modules(
            system_root,
            require_confirmed=False,
        )
        if not any("架构设计必须且只能按顺序包含" in error for error in errors):
            print("自检失败：未识别架构设计固定模板缺失。")
            return 1
        architecture_file.write_text(
            valid_architecture_text,
            encoding="utf-8",
        )
        task_text = (
            "# 任务：示例任务\n\n"
            "## 任务定义\n\n"
            "任务状态：进行中\n"
            "任务目标：形成示例系统设计\n"
            "完成条件：示例设计可恢复\n"
            "服务的业务目标与系统：示例业务 / 示例系统\n\n"
            "## 当前角色\n\n"
            "当前负责角色：系统与开发设计 Agent\n"
            "角色 reference：system-design-agent.md\n"
            "交互状态：无等待\n"
            "当前讨论对象：示例系统\n\n"
            "## 读取与写入合同\n\n"
            "当前权威文档：[业务设计](../../business/示例业务/业务设计.md)\n"
            "必须读取的权威文档：[业务设计](../../business/示例业务/业务设计.md)\n"
            "直接证据或代码入口：无\n"
            "允许写入路径：../../systems/示例系统/\n"
            "禁止修改内容：业务设计\n\n"
            "## 当前判断\n\n"
            "已经形成的认识或实现：示例系统负责示例能力\n"
            "当前核心判断及答案：责任边界已明确\n"
            "已触发的条件判断：无\n"
            "补充判断：无\n"
            "尚未确定或存在冲突的判断：无\n"
            "全部重要未决决定及所有者：无\n"
            "决定之间的依赖关系：无\n"
            "当前决策前沿：无\n"
            "正在比较的候选或冲突：无\n"
            "本次准备补充或替换的信息：无\n"
            "可能受影响的其他文档：无\n\n"
            "## 用户交互\n\n"
            "最新用户交互包：无\n"
            "尚未处理的用户反馈：无\n"
            "反馈处理结果：无\n\n"
            "## 已有产物\n\n"
            "本轮维护的文档或代码：[系统入口](../../systems/示例系统/index.md)\n"
            "当前工作位置：系统设计\n"
            "当前开发基线与代码快照：无\n"
            "实现记录与审核状态：无\n\n"
            "## 恢复\n\n"
            "恢复动作：读取业务设计并继续系统设计\n"
            "下一步：维护系统拆分\n"
            "恢复完成的判断标准：能够说明当前角色、来源和下一步\n"
        )
        task_index = task_root / "index.md"
        task_index.write_text(task_text, encoding="utf-8")
        controller_text = (
            "# 主控状态：示例任务\n\n"
            "任务文档：[完整任务](index.md)\n"
            "当前负责角色：系统与开发设计 Agent\n"
            "角色 reference：system-design-agent.md\n"
            "通信状态：可继续\n"
            "当前讨论对象：示例系统\n"
            "专业结果位置：[系统入口](../../systems/示例系统/index.md)\n"
            "本轮变更：系统设计文档\n"
            "用户交互包：无\n"
            "待处理用户反馈：无\n"
            "反馈处理结果：无\n"
            "下一步：继续维护系统拆分\n"
        )
        controller_state = task_root / "主控状态.md"
        controller_state.write_text(controller_text, encoding="utf-8")
        development_root = system_root / "开发记录"
        batch_root = development_root / "示例批次"
        implementation_root = batch_root / "实施任务" / "TASK-base"
        test_feedback_root = batch_root / "测试反馈"
        improvement_root = batch_root / "工程改进"
        review_root = batch_root / "审核"
        implementation_root.mkdir(parents=True)
        test_feedback_root.mkdir()
        improvement_root.mkdir()
        review_root.mkdir()
        (development_root / "index.md").write_text(
            "[开发任务图](示例批次/开发任务图.md)\n"
            "[集成记录](示例批次/集成记录.md)\n"
            "[测试结论](示例批次/测试结论.md)\n"
            "[审核结论](示例批次/审核结论.md)\n",
            encoding="utf-8",
        )
        task_graph_text = (
            "# 开发任务图：示例批次\n\n"
            "状态：已完成\n"
            "任务图确认：已确认\n"
            "任务图确认依据：示例任务中的用户确认\n"
            "适用系统：示例系统\n"
            "开发批次：示例批次\n"
            "开发基线：[当前基线](../../开发基线.md)\n"
            "工程编码规范：[当前规范](../../工程编码规范.md)\n"
            "起始代码快照：base000\n"
            "维护角色：开发规划 Agent\n\n"
            "## 批次范围与完成边界\n\n"
            "完成示例系统当前批次全部生产代码。\n\n"
            "## 代码产物清单\n\n"
            "| 产物 | 责任 | 来源 | 拥有任务 | 消费者 |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| ART-base | 工程基础 | 架构设计 | TASK-base | 系统装配 |\n\n"
            "## 任务关系图\n\n"
            "TASK-base\n\n"
            "## 并行批次\n\n"
            "第一批：TASK-base；共同起始快照 base000。\n\n"
            "## 共享写入与集成规则\n\n"
            "TASK-base 独占示例代码目录。\n\n"
            "## 开发任务\n\n"
            "### TASK-base：建立示例生产代码\n\n"
            "任务类型：工程基础\n"
            "代码责任：形成示例生产代码\n"
            "来源：架构设计与工程编码规范\n"
            "要实现的代码：示例模块与启动装配\n"
            "实现边界：仅示例模块\n"
            "主要写入范围：src/example\n"
            "共享写入位置：无\n"
            "前置输入：base000\n"
            "提供给后续任务：ART-base\n"
            "前置任务：无\n"
            "依赖类型与原因：无\n"
            "可以并行的任务：无\n"
            "禁止并行的任务及原因：无\n"
            "worktree 起始快照：base000\n"
            "编码完成边界：生产代码提交并登记产物\n"
            "发现问题时返回：开发规划 Agent\n\n"
            "## 集成与统一代码快照\n\n"
            "TASK-base 合并后形成统一生产代码快照。\n\n"
            "## 尚未确定的问题\n\n"
            "无\n"
        )
        task_graph = batch_root / "开发任务图.md"
        task_graph.write_text(task_graph_text, encoding="utf-8")
        implementation_text = (
            "# 实现记录：TASK-base\n\n"
            "开发任务图：[当前任务图](../../开发任务图.md)\n"
            "实施任务：TASK-base\n"
            "开发基线：[当前基线](../../../../开发基线.md)\n"
            "工程编码规范：[当前规范](../../../../工程编码规范.md)\n"
            "worktree 起始快照：base000\n"
            "输出代码快照：task111\n"
            "实现范围：示例生产代码\n"
            "未覆盖范围：无\n\n"
            "## 任务代码责任\n\n"
            "形成示例工程基础。\n\n"
            "## 来源与代码对应\n\n"
            "架构与工程规范对应到 src/example。\n\n"
            "## 实际产生的代码\n\n"
            "src/example。\n\n"
            "## 提供给后续任务的产物\n\n"
            "ART-base。\n\n"
            "## 与任务图或设计的偏离\n\n"
            "无。\n\n"
            "## 剩余实现事项\n\n"
            "无。\n"
        )
        implementation_record = implementation_root / "实现记录.md"
        implementation_record.write_text(implementation_text, encoding="utf-8")
        integration_text = (
            "# 集成记录\n\n"
            "开发任务图：[当前任务图](开发任务图.md)\n"
            "起始代码快照：base000\n"
            "已合并任务及 Commit：TASK-base task111\n"
            "合并顺序：TASK-base\n"
            "共享写入处理：无\n"
            "未合并或未实现事项：无\n"
            "统一生产代码快照：prod123\n"
            "测试状态：完成\n"
            "工程改进状态：完成\n"
            "最终待审核快照：final456\n"
        )
        integration_record = batch_root / "集成记录.md"
        integration_record.write_text(integration_text, encoding="utf-8")
        test_feedback_text = (
            "# 测试反馈：系统集成\n\n"
            "测试角度：系统集成\n"
            "输入生产代码快照：prod123\n"
            "依据的开发基线：当前基线\n"
            "依据的工程编码规范：v1\n"
            "测试代码范围：tests/integration\n"
            "禁止修改的生产代码范围：src\n"
            "覆盖对象：示例启动\n"
            "未覆盖对象：无\n"
            "新增或修改的测试：示例启动测试\n"
            "测试执行入口：test integration\n"
            "测试结果：通过\n"
            "失败证据：无\n"
            "要求达到的修正结果：无\n"
            "问题责任：无\n"
            "需要返回的任务或事实拥有者：无\n"
            "测试代码快照：test789\n"
            "剩余风险：无\n"
        )
        test_feedback_file = test_feedback_root / "系统集成.md"
        test_feedback_file.write_text(test_feedback_text, encoding="utf-8")
        test_conclusion_text = (
            "# 测试结论\n\n"
            "生产代码快照：prod123\n"
            "测试代码快照：test789\n"
            "各测试反馈：[系统集成](测试反馈/系统集成.md)\n"
            "失败与责任：无\n"
            "测试分歧：无\n"
            "修正任务：无\n"
            "复测范围：无\n"
            "未覆盖风险：无\n"
            "当前结论：可进入工程改进\n"
        )
        test_conclusion = batch_root / "测试结论.md"
        test_conclusion.write_text(test_conclusion_text, encoding="utf-8")
        improvement_text = (
            "# 工程改进：重复与抽象\n\n"
            "分析角度：重复与抽象\n"
            "工作方式：代码改进\n"
            "输入代码快照：prod123\n"
            "输入测试代码快照：test789\n"
            "依据的开发基线：当前基线\n"
            "依据的工程编码规范：v1\n"
            "依据的测试结论：可进入工程改进\n"
            "分析范围：示例批次\n"
            "发现的问题：无\n"
            "决定修改或保留的理由：当前实现清楚\n"
            "实际修改：无\n"
            "更新的工程编码规范：无\n"
            "受影响测试结果：通过\n"
            "输出代码快照：final456\n"
            "剩余风险：无\n"
        )
        improvement_record = improvement_root / "01-重复与抽象.md"
        improvement_record.write_text(improvement_text, encoding="utf-8")
        review_text = (
            "审核生产代码快照：final456\n"
            "审核测试代码快照：test789\n"
            "依据的开发基线：当前基线\n"
            "依据的工程编码规范：v1\n"
            "审核范围：示例批次\n"
            "未覆盖范围：无\n"
            "审核结论：通过\n"
        )
        for name in CORE_REVIEW_FILES:
            (review_root / name).write_text(review_text, encoding="utf-8")
        review_summary = batch_root / "审核结论.md"
        review_summary.write_text(
            "# 审核结论\n\n"
            "生产代码快照：final456\n"
            "测试代码快照：test789\n"
            "工程编码规范：v1\n"
            "当前结论：通过\n\n"
            "- [实现符合性](审核/实现符合性.md)\n"
            "- [工程质量](审核/工程质量.md)\n",
            encoding="utf-8",
        )

        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("不是 Git 版本管理仓库" in error for error in errors):
            print("自检失败：Coding 检查未拒绝非 Git 目录。")
            return 1

        errors, _ = validate(repo_root, recovery_task="示例任务")
        if errors:
            print("自检失败：有效任务恢复样例未通过。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1

        controller_state.unlink()
        errors, _ = validate(repo_root, recovery_task="示例任务")
        if not any("缺少主控状态" in error for error in errors):
            print("自检失败：未识别缺少短主控状态的旧任务。")
            return 1
        controller_state.write_text(controller_text, encoding="utf-8")

        system_split = system_root / "系统拆分.md"
        valid_system_split_text = system_split.read_text(encoding="utf-8")
        system_split.write_text(
            valid_system_split_text.replace(
                "业务主体确认：已确认",
                "业务主体确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("业务主体确认：已确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的业务主体。")
            return 1
        system_split.write_text(valid_system_split_text, encoding="utf-8")

        system_split.write_text(
            valid_system_split_text.replace(
                "Domain 设计确认：已确认",
                "Domain 设计确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("Domain 设计确认：已确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的 Domain 设计。")
            return 1
        system_split.write_text(valid_system_split_text, encoding="utf-8")

        system_split.write_text(
            valid_system_split_text.replace(
                "核心命名确认：已确认",
                "核心命名确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("核心命名确认：已确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的核心命名。")
            return 1
        system_split.write_text(valid_system_split_text, encoding="utf-8")

        architecture_file = system_root / "架构设计.md"
        valid_architecture_text = architecture_file.read_text(
            encoding="utf-8"
        )
        architecture_file.write_text(
            valid_architecture_text.replace(
                "架构设计确认：已确认",
                "架构设计确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("架构设计尚未确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的架构设计。")
            return 1
        architecture_file.write_text(
            valid_architecture_text,
            encoding="utf-8",
        )

        module_file = system_root / "模块拆分.md"
        valid_module_text = module_file.read_text(encoding="utf-8")
        module_file.write_text(
            valid_module_text.replace(
                "模块拆分确认：已确认",
                "模块拆分确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("模块拆分尚未确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的模块拆分。")
            return 1
        module_file.write_text(valid_module_text, encoding="utf-8")

        engineering_standard.write_text(
            engineering_standard_text.replace(
                "规范确认：已确认",
                "规范确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("规范确认：已确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的工程编码规范。")
            return 1
        engineering_standard.write_text(
            engineering_standard_text,
            encoding="utf-8",
        )

        api_design = system_root / "API设计.md"
        valid_api_design_text = api_design.read_text(encoding="utf-8")
        api_design.write_text(
            valid_api_design_text.replace(
                "API 设计确认：已确认",
                "API 设计确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("API 设计确认：已确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的 API 设计。")
            return 1
        api_design.write_text(valid_api_design_text, encoding="utf-8")

        internal_orchestration = system_root / "核心接口内部编排.md"
        valid_internal_orchestration_text = internal_orchestration.read_text(
            encoding="utf-8"
        )
        internal_orchestration.write_text(
            valid_internal_orchestration_text.replace(
                "核心接口内部编排确认：已确认",
                "核心接口内部编排确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            orchestration_system="示例系统",
        )
        if errors:
            print("自检失败：合法的待确认编排候选未通过生成阶段检查。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any(
            "核心接口内部编排确认：已确认" in error for error in errors
        ):
            print("自检失败：Coding 检查未拒绝待确认的核心接口内部编排。")
            return 1
        internal_orchestration.write_text(
            valid_internal_orchestration_text,
            encoding="utf-8",
        )

        internal_orchestration.write_text(
            valid_internal_orchestration_text.replace(
                "### 主流程",
                "### 流程",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            orchestration_system="示例系统",
        )
        if not any(
            "六个三级标题" in error and "API-create-example" in error
            for error in errors
        ):
            print("自检失败：编排检查未拒绝偏离固定逐 API 模板。")
            return 1
        internal_orchestration.write_text(
            valid_internal_orchestration_text,
            encoding="utf-8",
        )

        internal_orchestration.write_text(
            valid_internal_orchestration_text.replace(
                "## API-create-example：POST /examples — 形成示例",
                "## 创建类 API",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            orchestration_system="示例系统",
        )
        if not any("每个二级标题必须只对应一个" in error for error in errors):
            print("自检失败：编排检查未拒绝接口组标题。")
            return 1
        internal_orchestration.write_text(
            valid_internal_orchestration_text,
            encoding="utf-8",
        )

        database_design = system_root / "数据库设计.md"
        valid_database_design_text = database_design.read_text(encoding="utf-8")
        database_design.write_text(
            valid_database_design_text
            .replace(
                "数据库设计确认：已确认",
                "数据库设计确认：待确认",
            )
            .replace(
                "数据库设计确认依据：示例任务中的用户确认",
                "数据库设计确认依据：无",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            database_system="示例系统",
        )
        if errors:
            print("自检失败：合法的待确认数据库候选未通过生成阶段检查。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("数据库设计确认：已确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的数据库设计。")
            return 1
        database_design.write_text(
            valid_database_design_text,
            encoding="utf-8",
        )

        database_design.write_text(
            valid_database_design_text.replace(
                "### 字段说明",
                "### 字段列表",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            database_system="示例系统",
        )
        if not any(
            "十个三级标题" in error and "DBT-example" in error
            for error in errors
        ):
            print("自检失败：数据库检查未拒绝偏离固定逐表模板。")
            return 1
        database_design.write_text(
            valid_database_design_text,
            encoding="utf-8",
        )

        database_design.write_text(
            valid_database_design_text
            + "\n```sql\nCREATE TABLE examples (id text);\n```\n",
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            database_system="示例系统",
        )
        if not any("禁止 SQL 代码块" in error for error in errors):
            print("自检失败：数据库检查未拒绝 SQL 代码块。")
            return 1
        if not any("禁止 DDL" in error for error in errors):
            print("自检失败：数据库检查未拒绝 DDL。")
            return 1
        database_design.write_text(
            valid_database_design_text,
            encoding="utf-8",
        )

        task_index.write_text(
            task_text.replace(
                "角色 reference：system-design-agent.md\n",
                "角色 reference：\n",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, recovery_task="示例任务")
        if not any("角色 reference" in error for error in errors):
            print("自检失败：未识别缺失的角色 reference。")
            return 1
        task_index.write_text(task_text, encoding="utf-8")

        controller_state.write_text(
            controller_text.replace(
                "下一步：继续维护系统拆分\n",
                "下一步：\n",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, recovery_task="示例任务")
        if not any("主控状态" in error and "下一步" in error for error in errors):
            print("自检失败：未识别主控状态缺失的下一步。")
            return 1
        controller_state.write_text(controller_text, encoding="utf-8")

        subprocess.run(
            ["git", "-C", str(repo_root), "init", "--quiet"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "-C", str(repo_root), "add", "."],
            check=True,
            capture_output=True,
        )

        errors, _ = validate(repo_root, coding_system="示例系统")
        if errors:
            print("自检失败：有效样例未通过。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1

        errors, _ = validate(
            repo_root,
            implementation_system="示例系统",
            development_batch="示例批次",
        )
        if errors:
            print("自检失败：有效开发任务图样例未通过。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1

        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_batch="示例批次",
        )
        if errors:
            print("自检失败：有效开发批次与审核样例未通过。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1

        task_graph.write_text(
            task_graph_text.replace(
                "编码完成边界：生产代码提交并登记产物",
                "编码完成边界：生产代码提交并通过测试验证",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            implementation_system="示例系统",
            development_batch="示例批次",
        )
        if not any(
            "编码完成边界不得包含测试" in error for error in errors
        ):
            print("自检失败：任务图未拒绝把验证放入编码任务。")
            return 1
        task_graph.write_text(task_graph_text, encoding="utf-8")

        task_graph.write_text(
            task_graph_text.replace(
                "任务类型：工程基础",
                "任务类型：工程基础、模块基础",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            implementation_system="示例系统",
            development_batch="示例批次",
        )
        if not any(
            "任务类型不在固定分类" in error for error in errors
        ):
            print("自检失败：任务图未拒绝一个任务组合多个任务类型。")
            return 1
        task_graph.write_text(task_graph_text, encoding="utf-8")

        task_graph.write_text(
            task_graph_text.replace(
                "前置任务：无",
                "前置任务：TASK-base",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            implementation_system="示例系统",
            development_batch="示例批次",
        )
        if not any(
            "不能依赖自身" in error or "循环依赖" in error
            for error in errors
        ):
            print("自检失败：任务图未拒绝循环依赖。")
            return 1
        task_graph.write_text(task_graph_text, encoding="utf-8")

        test_feedback_file.unlink()
        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_batch="示例批次",
        )
        if not any("至少需要一份统一测试反馈" in error for error in errors):
            print("自检失败：未识别缺少统一测试反馈。")
            return 1
        test_feedback_file.write_text(
            test_feedback_text,
            encoding="utf-8",
        )

        design_feedback_root = batch_root / "设计反馈"
        design_feedback_root.mkdir()
        feedback_file = design_feedback_root / "01-数据库设计.md"
        feedback_text = (
            "# 设计反馈：数据库设计\n\n"
            "反馈状态：待上游判断\n"
            "发现阶段：SQL 与迁移\n"
            "问题所在：示例约束无法落地\n"
            "对应的权威设计：数据库设计.md\n"
            "代码、SQL、测试或运行证据：数据库拒绝当前约束\n"
            "为什么当前设计不成立或不合理：无法保持示例不变量\n"
            "影响的任务与代码范围：TASK-base\n"
            "建议修改：调整示例约束\n"
            "替代方案与权衡：保留现状会产生错误数据\n"
            "建议修改的权威文档和章节：数据库设计 / 必须保持的约束\n"
            "当前代码处理：停止相关实现\n"
            "可以继续的范围：无关查询\n"
            "事实拥有者：系统与开发设计 Agent\n"
            "上游处理结果：待判断\n"
            "重新确认依据：无\n"
            "受影响的任务、代码和测试：TASK-base 与系统集成测试\n"
        )
        feedback_file.write_text(feedback_text, encoding="utf-8")
        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_batch="示例批次",
        )
        if not any(
            "设计反馈必须已经不采纳或完成重新确认" in error
            for error in errors
        ):
            print("自检失败：未拒绝尚未解决设计反馈的正式审核。")
            return 1
        feedback_file.unlink()
        design_feedback_root.rmdir()

        engineering_standard.unlink()
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any(
            "缺少固定实现输入" in error
            and "工程编码规范.md" in error
            for error in errors
        ):
            print("自检失败：未识别缺少系统工程编码规范。")
            return 1
        engineering_standard.write_text(
            engineering_standard_text,
            encoding="utf-8",
        )

        integration_record.write_text(
            integration_text.replace(
                "工程改进状态：完成",
                "工程改进状态：进行中",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_batch="示例批次",
        )
        if not any("工程改进状态" in error for error in errors):
            print("自检失败：未拒绝工程改进尚未完成的正式审核。")
            return 1
        integration_record.write_text(integration_text, encoding="utf-8")

        improvement_record.unlink()
        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_batch="示例批次",
        )
        if not any("至少需要一份工程改进记录" in error for error in errors):
            print("自检失败：未识别缺少工程改进记录。")
            return 1
        improvement_record.write_text(
            improvement_text,
            encoding="utf-8",
        )

        improvement_record.write_text(
            improvement_text.replace(
                "输出代码快照：final456",
                "输出代码快照：other456",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_batch="示例批次",
        )
        if not any(
            "最终待审核快照必须由工程改进记录输出" in error
            for error in errors
        ):
            print("自检失败：未识别工程改进输出与最终快照不一致。")
            return 1
        improvement_record.write_text(
            improvement_text,
            encoding="utf-8",
        )

        missing_review = review_root / "工程质量.md"
        missing_review.unlink()
        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_batch="示例批次",
        )
        if not any(
            "缺少测试或审核记录" in error
            and "工程质量.md" in error
            for error in errors
        ):
            print("自检失败：未识别缺失核心审核记录。")
            return 1
        missing_review.write_text(review_text, encoding="utf-8")

        (system_root / "开发基线.md").write_text(
            "# 开发基线\n\n"
            "状态：当前\n\n"
            "## Domain\n\n"
            "## 业务线与 API\n\n"
            "## 数据库设计\n",
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("适用范围" in error for error in errors):
            print("自检失败：未识别缺失的基线适用范围。")
            return 1
        if not any("来源" in error for error in errors):
            print("自检失败：未识别缺失的基线来源。")
            return 1

        (system_root / "开发基线.md").write_text(
            baseline_text + "\n状态：当前\n", encoding="utf-8"
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("只能有一个独立状态行" in error for error in errors):
            print("自检失败：未识别重复的基线状态。")
            return 1

        (system_root / "开发基线.md").write_text(
            baseline_text, encoding="utf-8"
        )
        (system_root / "API设计.md").unlink()
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any(
            "缺少固定实现输入" in error and "API设计.md" in error
            for error in errors
        ):
            print("自检失败：Coding 检查未识别缺失 API 设计。")
            return 1
        (system_root / "API设计.md").write_text(
            "# API设计\n", encoding="utf-8"
        )

        (system_root / "index.md").write_text(
            "[系统拆分](系统拆分.md)\n"
            "[架构设计](架构设计.md)\n"
            "[模块拆分](模块拆分.md)\n"
            "[API设计](API设计.md)\n"
            "[核心接口内部编排](核心接口内部编排.md)\n"
            "[数据库设计](数据库设计.md)\n",
            encoding="utf-8",
        )
        errors, _ = validate(repo_root)
        if not any("孤儿开发基线" in error for error in errors):
            print("自检失败：未识别孤儿开发基线。")
            return 1

        (system_root / "index.md").write_text(
            "[系统拆分](系统拆分.md)\n"
            "[架构设计](架构设计.md)\n"
            "[模块拆分](模块拆分.md)\n"
            "[API设计](API设计.md)\n"
            "[核心接口内部编排](核心接口内部编排.md)\n"
            "[数据库设计](数据库设计.md)\n"
            "[开发基线](开发基线.md)\n"
            "[工程编码规范](工程编码规范.md)\n"
            "[开发记录](开发记录/index.md)\n",
            encoding="utf-8",
        )
        (system_root / "开发基线.md").unlink()
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("缺少固定实现输入" in error for error in errors):
            print("自检失败：Coding 检查未识别缺失开发基线。")
            return 1

    print("自检通过。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查 VCDDD 入口、固定设计模板、Coding 输入和审核结构。"
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="目标仓库根目录，默认当前目录。",
    )
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="运行内置有效/失效结构样例。",
    )
    parser.add_argument(
        "--coding-system",
        metavar="中文系统名",
        help="准备进入 Coding 的系统；额外要求 Domain、架构、模块和其他设计均已确认，以及已由用户确认且为当前、已纳入版本管理的开发基线和系统工程编码规范。",
    )
    parser.add_argument(
        "--architecture-system",
        metavar="中文系统名",
        help="检查指定系统的架构设计与模块拆分固定模板；候选交给用户确认前运行。",
    )
    parser.add_argument(
        "--orchestration-system",
        metavar="中文系统名",
        help="检查指定系统的 API 标识和逐 API 核心接口内部编排固定模板；候选交给用户确认前运行。",
    )
    parser.add_argument(
        "--database-system",
        metavar="中文系统名",
        help="检查指定系统以表和字段意义为核心的数据库设计固定模板，并拒绝 DDL；候选交给用户确认前运行。",
    )
    parser.add_argument(
        "--implementation-system",
        metavar="中文系统名",
        help="检查指定系统当前开发批次的开发任务图；同时要求 Coding 输入有效，并必须指定 --development-batch。",
    )
    parser.add_argument(
        "--development-batch",
        metavar="中文开发批次",
        help="与 --implementation-system 一起指定需要检查任务图的开发批次。",
    )
    parser.add_argument(
        "--review-batch",
        metavar="中文开发批次",
        help="检查指定开发批次的任务图、实施记录、统一测试、工程改进和审核；必须同时指定 --coding-system。",
    )
    parser.add_argument(
        "--recovery-task",
        metavar="中文任务名",
        help="检查指定任务的短主控状态、七段式完整恢复合同、必填字段和工作入口链接。",
    )
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    repo_root = Path(args.repo).expanduser().resolve()
    errors, warnings = validate(
        repo_root,
        coding_system=args.coding_system,
        architecture_system=args.architecture_system,
        orchestration_system=args.orchestration_system,
        database_system=args.database_system,
        implementation_system=args.implementation_system,
        development_batch=args.development_batch,
        review_batch=args.review_batch,
        recovery_task=args.recovery_task,
    )

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"验证失败：{len(errors)} 个错误，{len(warnings)} 个警告。")
        return 1

    print(f"验证通过：0 个错误，{len(warnings)} 个警告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

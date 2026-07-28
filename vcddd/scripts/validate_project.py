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
BASELINE_HEADINGS = ["Domain", "业务线与 API", "数据库设计"]
BUSINESS_DESIGN_HEADINGS = ["业务目标与范围", "系统设计", "业务线逻辑"]
SYSTEM_FACT_FILES = ["系统拆分.md", "模块拆分.md", "API设计.md", "数据库设计.md"]
OWNERSHIP_CONFIRMATION_RE = re.compile(
    r"^所有权确认[ \t]*[：:][ \t]*(待确认|已确认)[ \t]*$",
    re.MULTILINE,
)
OWNERSHIP_EVIDENCE_RE = re.compile(
    r"^确认依据[ \t]*[：:][ \t]*(\S.*)$",
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
IMPLEMENTATION_HEADINGS = [
    "业务结果",
    "设计与代码对应",
    "关键实现",
    "验证证据",
    "与设计的偏离",
    "剩余风险",
]
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
CODE_SNAPSHOT_RE = re.compile(
    r"^代码快照[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
)
REVIEW_OBJECT_RE = re.compile(
    r"^审核对象[ \t]*[：:][ \t]*(\S.*)$", re.MULTILINE
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


def validate(
    repo_root: Path,
    coding_system: str | None = None,
    review_slice: str | None = None,
    recovery_task: str | None = None,
) -> tuple[list[str], list[str]]:
    vcddd_root = repo_root / "docs" / "vcddd"
    errors: list[str] = []
    warnings: list[str] = []

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
            if task_index.resolve() not in work_targets:
                errors.append(f"工作入口未直接链接任务恢复文档：{task_index}")

    if recovery_task:
        if Path(recovery_task).name != recovery_task:
            errors.append(f"恢复任务名必须是单个目录名：{recovery_task}")
            return errors, warnings

        task_index = work_root / recovery_task / "index.md"
        if not task_index.exists():
            errors.append(f"缺少任务恢复文档：{task_index}")
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

        if task_index.resolve() not in work_targets:
            errors.append(f"当前任务未由工作入口直接链接：{task_index}")

    if review_slice and not coding_system:
        errors.append("--review-slice 必须同时指定 --coding-system")
        return errors, warnings

    if coding_system:
        if Path(coding_system).name != coding_system:
            errors.append(f"系统名必须是单个目录名：{coding_system}")
            return errors, warnings

        system_root = systems_root / coding_system
        system_index = system_root / "index.md"
        baseline = system_root / "开发基线.md"
        required_design_files = [
            system_index,
            *(system_root / name for name in SYSTEM_FACT_FILES),
            baseline,
        ]
        missing_design_files = [
            path for path in required_design_files if not path.exists()
        ]
        if missing_design_files:
            for path in missing_design_files:
                errors.append(f"准备 Coding 的系统缺少固定设计文档：{path}")
            return errors, warnings

        index_text = system_index.read_text(encoding="utf-8")
        index_targets = {
            local_link_path(system_index, raw_target)
            for raw_target in LINK_RE.findall(index_text)
        }
        for design_file in required_design_files[1:]:
            if design_file.resolve() not in index_targets:
                errors.append(f"系统入口未直接链接固定设计文档：{design_file}")

        system_split = system_root / "系统拆分.md"
        system_split_text = system_split.read_text(encoding="utf-8")
        if OWNERSHIP_CONFIRMATION_RE.findall(system_split_text) != ["已确认"]:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明"
                f"“所有权确认：已确认”：{system_split}"
            )
        if len(OWNERSHIP_EVIDENCE_RE.findall(system_split_text)) != 1:
            errors.append(
                "准备 Coding 的系统拆分必须且只能声明一个非空确认依据："
                f"{system_split}"
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
                        f"准备 Coding 的固定设计文档尚未纳入版本管理：{design_file}"
                    )

        if review_slice:
            if Path(review_slice).name != review_slice:
                errors.append(f"开发切片名必须是单个目录名：{review_slice}")
                return errors, warnings

            development_root = system_root / "开发记录"
            development_index = development_root / "index.md"
            slice_root = development_root / review_slice
            implementation_record = slice_root / "实现记录.md"
            review_root = slice_root / "审核"
            review_files = [
                review_root / name for name in CORE_REVIEW_FILES
            ]
            review_summary = slice_root / "审核结论.md"
            required_review_files = [
                development_index,
                implementation_record,
                *review_files,
                review_summary,
            ]

            missing_review_files = [
                path for path in required_review_files if not path.exists()
            ]
            for path in missing_review_files:
                errors.append(f"开发切片缺少实现或审核记录：{path}")

            if missing_review_files:
                return errors, warnings

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
            for path in (implementation_record, review_summary):
                if path.resolve() not in development_targets:
                    errors.append(f"开发记录入口未直接链接切片文档：{path}")

            implementation_text = implementation_record.read_text(
                encoding="utf-8"
            )
            implementation_targets = {
                local_link_path(implementation_record, raw_target)
                for raw_target in LINK_RE.findall(implementation_text)
            }
            if baseline.resolve() not in implementation_targets:
                errors.append(
                    f"实现记录未直接链接当前开发基线：{implementation_record}"
                )
            implementation_headings = re.findall(
                r"^##\s+(.+?)\s*$", implementation_text, re.MULTILINE
            )
            if implementation_headings != IMPLEMENTATION_HEADINGS:
                errors.append(
                    "实现记录必须且只能按顺序包含六个二级标题"
                    f"（{' / '.join(IMPLEMENTATION_HEADINGS)}）："
                    f"{implementation_record}"
                )

            for field in (
                "开发基线",
                "代码快照",
                "实现范围",
                "未覆盖范围",
            ):
                matches = re.findall(
                    rf"^{field}[ \t]*[：:][ \t]*(\S.*)$",
                    implementation_text,
                    re.MULTILINE,
                )
                if len(matches) != 1:
                    errors.append(
                        f"实现记录必须且只能声明一个非空“{field}”："
                        f"{implementation_record}"
                    )

            snapshots = CODE_SNAPSHOT_RE.findall(implementation_text)
            implementation_snapshot = (
                snapshots[0] if len(snapshots) == 1 else None
            )

            for review_file in review_files:
                review_text = review_file.read_text(encoding="utf-8")
                for field in (
                    "审核对象",
                    "依据的开发基线",
                    "审核范围",
                    "未覆盖范围",
                ):
                    matches = re.findall(
                        rf"^{field}[ \t]*[：:][ \t]*(\S.*)$",
                        review_text,
                        re.MULTILINE,
                    )
                    if len(matches) != 1:
                        errors.append(
                            f"审核记录必须且只能声明一个非空“{field}”："
                            f"{review_file}"
                        )
                review_objects = REVIEW_OBJECT_RE.findall(review_text)
                if (
                    implementation_snapshot is not None
                    and review_objects != [implementation_snapshot]
                ):
                    errors.append(
                        "审核对象必须与实现记录代码快照一致："
                        f"{review_file}"
                    )
                if len(REVIEW_RESULT_RE.findall(review_text)) != 1:
                    errors.append(
                        "审核记录必须且只能声明一个审核结论"
                        f"（通过/有条件通过/不通过）：{review_file}"
                    )

            summary_text = review_summary.read_text(encoding="utf-8")
            summary_snapshots = CODE_SNAPSHOT_RE.findall(summary_text)
            if (
                implementation_snapshot is not None
                and summary_snapshots != [implementation_snapshot]
            ):
                errors.append(
                    f"审核结论代码快照必须与实现记录一致：{review_summary}"
                )
            if len(SUMMARY_RESULT_RE.findall(summary_text)) != 1:
                errors.append(
                    "审核结论必须且只能声明一个当前结论"
                    f"（通过/需修改/需重写/等待上游修订）：{review_summary}"
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
                for path in required_review_files:
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
                            f"实现或审核记录尚未纳入版本管理：{path}"
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
            "[示例任务](示例任务/index.md)\n",
            encoding="utf-8",
        )
        (vcddd_root / "systems" / "index.md").write_text(
            "[示例系统](示例系统/index.md)\n", encoding="utf-8"
        )
        (system_root / "index.md").write_text(
            "[系统拆分](系统拆分.md)\n"
            "[模块拆分](模块拆分.md)\n"
            "[API设计](API设计.md)\n"
            "[数据库设计](数据库设计.md)\n"
            "[开发基线](开发基线.md)\n"
            "[开发记录](开发记录/index.md)\n",
            encoding="utf-8",
        )
        for name in SYSTEM_FACT_FILES:
            metadata = (
                "所有权确认：已确认\n"
                "确认依据：示例任务中的用户确认\n"
                if name == "系统拆分.md"
                else ""
            )
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
            "- [模块拆分](模块拆分.md)\n"
            "- [API设计](API设计.md)\n"
            "- [数据库设计](数据库设计.md)\n\n"
            "## Domain\n\n"
            "## 业务线与 API\n\n"
            "## 数据库设计\n"
        )
        (system_root / "开发基线.md").write_text(
            baseline_text, encoding="utf-8"
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
        development_root = system_root / "开发记录"
        slice_root = development_root / "示例切片"
        review_root = slice_root / "审核"
        review_root.mkdir(parents=True)
        (development_root / "index.md").write_text(
            "[实现记录](示例切片/实现记录.md)\n"
            "[审核结论](示例切片/审核结论.md)\n",
            encoding="utf-8",
        )
        implementation_text = (
            "# 实现记录\n\n"
            "开发基线：[当前基线](../../开发基线.md)\n"
            "代码快照：abc123\n"
            "实现范围：示例切片\n"
            "未覆盖范围：无\n\n"
            "## 业务结果\n\n"
            "## 设计与代码对应\n\n"
            "## 关键实现\n\n"
            "## 验证证据\n\n"
            "## 与设计的偏离\n\n"
            "## 剩余风险\n"
        )
        (slice_root / "实现记录.md").write_text(
            implementation_text, encoding="utf-8"
        )
        review_text = (
            "审核对象：abc123\n"
            "依据的开发基线：当前基线\n"
            "审核范围：示例切片\n"
            "未覆盖范围：无\n"
            "审核结论：通过\n"
        )
        for name in CORE_REVIEW_FILES:
            (review_root / name).write_text(review_text, encoding="utf-8")
        (slice_root / "审核结论.md").write_text(
            "# 审核结论\n\n"
            "代码快照：abc123\n"
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

        system_split = system_root / "系统拆分.md"
        valid_system_split_text = system_split.read_text(encoding="utf-8")
        system_split.write_text(
            valid_system_split_text.replace(
                "所有权确认：已确认",
                "所有权确认：待确认",
            ),
            encoding="utf-8",
        )
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("所有权确认：已确认" in error for error in errors):
            print("自检失败：Coding 检查未拒绝待确认的所有权。")
            return 1
        system_split.write_text(valid_system_split_text, encoding="utf-8")

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
            coding_system="示例系统",
            review_slice="示例切片",
        )
        if errors:
            print("自检失败：有效实现与审核样例未通过。")
            for error in errors:
                print(f"ERROR: {error}")
            return 1

        missing_review = review_root / "工程质量.md"
        missing_review.unlink()
        errors, _ = validate(
            repo_root,
            coding_system="示例系统",
            review_slice="示例切片",
        )
        if not any(
            "缺少实现或审核记录" in error
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
            "缺少固定设计文档" in error and "API设计.md" in error
            for error in errors
        ):
            print("自检失败：Coding 检查未识别缺失 API 设计。")
            return 1
        (system_root / "API设计.md").write_text(
            "# API设计\n", encoding="utf-8"
        )

        (system_root / "index.md").write_text(
            "[系统拆分](系统拆分.md)\n"
            "[模块拆分](模块拆分.md)\n"
            "[API设计](API设计.md)\n"
            "[数据库设计](数据库设计.md)\n",
            encoding="utf-8",
        )
        errors, _ = validate(repo_root)
        if not any("孤儿开发基线" in error for error in errors):
            print("自检失败：未识别孤儿开发基线。")
            return 1

        (system_root / "index.md").write_text(
            "[系统拆分](系统拆分.md)\n"
            "[模块拆分](模块拆分.md)\n"
            "[API设计](API设计.md)\n"
            "[数据库设计](数据库设计.md)\n"
            "[开发基线](开发基线.md)\n"
            "[开发记录](开发记录/index.md)\n",
            encoding="utf-8",
        )
        (system_root / "开发基线.md").unlink()
        errors, _ = validate(repo_root, coding_system="示例系统")
        if not any("缺少固定设计文档" in error for error in errors):
            print("自检失败：Coding 检查未识别缺失开发基线。")
            return 1

    print("自检通过。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="检查 VCDDD 必要入口、Markdown 断链和孤儿开发基线。"
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
        help="准备进入 Coding 的系统；额外要求当前、三段式且已纳入版本管理的开发基线。",
    )
    parser.add_argument(
        "--review-slice",
        metavar="中文开发切片",
        help="检查指定系统开发切片的实现记录、两个核心审核和审核结论；必须同时指定 --coding-system。",
    )
    parser.add_argument(
        "--recovery-task",
        metavar="中文任务名",
        help="检查指定任务的七段式恢复合同、必填字段和工作入口链接。",
    )
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    repo_root = Path(args.repo).expanduser().resolve()
    errors, warnings = validate(
        repo_root,
        coding_system=args.coding_system,
        review_slice=args.review_slice,
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

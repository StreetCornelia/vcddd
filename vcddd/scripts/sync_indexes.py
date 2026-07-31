#!/usr/bin/env python3
"""Synchronize generated VCDDD index sections from single status owners."""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path


GENERATED_START = "<!-- vcddd:generated:start -->"
GENERATED_END = "<!-- vcddd:generated:end -->"
GENERATED_RE = re.compile(
    rf"{re.escape(GENERATED_START)}.*?{re.escape(GENERATED_END)}",
    re.DOTALL,
)
TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Entry:
    title: str
    target: Path
    details: tuple[str, ...] = ()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def first_title(path: Path, fallback: str) -> str:
    if not path.exists():
        return fallback
    match = TITLE_RE.search(read_text(path))
    return match.group(1).strip() if match else fallback


def field(path: Path, *names: str) -> str | None:
    if not path.exists():
        return None
    text = read_text(path)
    for name in names:
        match = re.search(
            rf"^{re.escape(name)}[ \t]*[：:][ \t]*(\S.*)$",
            text,
            re.MULTILINE,
        )
        if match:
            return match.group(1).strip()
    return None


def relative_link(index_path: Path, target: Path) -> str:
    return Path(os.path.relpath(target, index_path.parent)).as_posix()


def render_block(index_path: Path, entries: list[Entry]) -> str:
    lines = [GENERATED_START]
    if not entries:
        lines.append("- 无。")
    for entry in sorted(entries, key=lambda item: item.target.as_posix()):
        details = f" — {'；'.join(entry.details)}" if entry.details else ""
        lines.append(
            f"- [{entry.title}]({relative_link(index_path, entry.target)})"
            f"{details}"
        )
    lines.append(GENERATED_END)
    return "\n".join(lines)


def index_specs(repo_root: Path) -> list[tuple[Path, str, list[Entry]]]:
    vcddd_root = repo_root / "vcddd"
    business_root = vcddd_root / "business"
    systems_root = vcddd_root / "systems"
    work_root = vcddd_root / "work"

    specs: list[tuple[Path, str, list[Entry]]] = [
        (
            vcddd_root / "index.md",
            "VCDDD 项目入口",
            [
                Entry("业务目标", business_root / "index.md"),
                Entry("系统", systems_root / "index.md"),
                Entry("工作任务", work_root / "index.md"),
            ],
        )
    ]

    business_entries: list[Entry] = []
    if business_root.exists():
        for design in sorted(business_root.glob("*/业务设计.md")):
            status = field(design, "状态", "业务设计状态")
            details = (f"状态：{status}",) if status else ()
            business_entries.append(
                Entry(first_title(design, design.parent.name), design, details)
            )
    specs.append((business_root / "index.md", "业务目标", business_entries))

    system_entries: list[Entry] = []
    if systems_root.exists():
        for system_index in sorted(systems_root.glob("*/index.md")):
            status = field(system_index, "系统状态", "状态")
            details = (f"状态：{status}",) if status else ()
            system_entries.append(
                Entry(
                    first_title(system_index, system_index.parent.name),
                    system_index,
                    details,
                )
            )
    specs.append((systems_root / "index.md", "系统", system_entries))

    work_entries: list[Entry] = []
    if work_root.exists():
        for state in sorted(work_root.glob("*/主控状态.md")):
            status = field(state, "通信状态")
            role = field(state, "当前负责角色")
            details = tuple(
                item
                for item in (
                    f"状态：{status}" if status else None,
                    f"角色：{role}" if role else None,
                )
                if item
            )
            work_entries.append(
                Entry(first_title(state, state.parent.name), state, details)
            )
    specs.append((work_root / "index.md", "工作任务", work_entries))

    if systems_root.exists():
        for system_root in sorted(
            path for path in systems_root.iterdir() if path.is_dir()
        ):
            validation_root = system_root / "validation"
            validation_entries: list[Entry] = []
            if validation_root.exists():
                for validation_index in sorted(
                    validation_root.glob("*/index.md")
                ):
                    status = field(validation_index, "验证状态")
                    method = field(validation_index, "验证方法")
                    details = tuple(
                        item
                        for item in (
                            f"状态：{status}" if status else None,
                            f"方法：{method}" if method else None,
                        )
                        if item
                    )
                    validation_entries.append(
                        Entry(
                            first_title(
                                validation_index,
                                validation_index.parent.name,
                            ),
                            validation_index,
                            details,
                        )
                    )
            if validation_root.exists() or validation_entries:
                specs.append(
                    (
                        validation_root / "index.md",
                        f"{system_root.name} 验证",
                        validation_entries,
                    )
                )

            delivery_root = system_root / "delivery"
            delivery_entries: list[Entry] = []
            if delivery_root.exists():
                for delivery_index in sorted(
                    delivery_root.glob("*/index.md")
                ):
                    status = field(delivery_index, "交付状态", "状态")
                    stage = field(delivery_index, "当前阶段")
                    details = tuple(
                        item
                        for item in (
                            f"状态：{status}" if status else None,
                            f"阶段：{stage}" if stage else None,
                        )
                        if item
                    )
                    delivery_entries.append(
                        Entry(
                            first_title(
                                delivery_index,
                                delivery_index.parent.name,
                            ),
                            delivery_index,
                            details,
                        )
                    )
            if delivery_root.exists() or delivery_entries:
                specs.append(
                    (
                        delivery_root / "index.md",
                        f"{system_root.name} 交付",
                        delivery_entries,
                    )
                )

    return specs


def expected_text(path: Path, title: str, entries: list[Entry]) -> str:
    block = render_block(path, entries)
    if not path.exists():
        return f"# {title}\n\n## 自动索引\n\n{block}\n"

    current = read_text(path)
    if GENERATED_RE.search(current):
        return GENERATED_RE.sub(block, current, count=1)

    suffix = "" if current.endswith("\n") else "\n"
    return f"{current}{suffix}\n## 自动索引\n\n{block}\n"


def find_drift(repo_root: Path) -> list[tuple[Path, str]]:
    vcddd_root = repo_root / "vcddd"
    if not vcddd_root.exists():
        return [(vcddd_root, "缺少 VCDDD 工作空间")]

    drift: list[tuple[Path, str]] = []
    for path, title, entries in index_specs(repo_root):
        expected = expected_text(path, title, entries)
        if not path.exists():
            drift.append((path, "缺少索引"))
        elif read_text(path) != expected:
            reason = (
                "缺少受控生成区"
                if GENERATED_START not in read_text(path)
                else "生成区与状态拥有者不同步"
            )
            drift.append((path, reason))
    return drift


def sync(repo_root: Path) -> list[Path]:
    changed: list[Path] = []
    for path, title, entries in index_specs(repo_root):
        expected = expected_text(path, title, entries)
        if not path.exists() or read_text(path) != expected:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(expected, encoding="utf-8")
            changed.append(path)
    return changed


def self_test() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        repo_root = Path(temporary)
        validation = (
            repo_root
            / "vcddd"
            / "systems"
            / "router"
            / "validation"
            / "VAL-ROUTER-001-prototype"
        )
        validation.mkdir(parents=True)
        (validation / "index.md").write_text(
            "# Router 原型验证\n\n"
            "验证状态：已运行\n"
            "验证方法：prototype\n",
            encoding="utf-8",
        )
        delivery = (
            repo_root
            / "vcddd"
            / "systems"
            / "router"
            / "delivery"
            / "B1"
        )
        delivery.mkdir(parents=True)
        (delivery / "index.md").write_text(
            "# B1 交付\n\n"
            "交付状态：阶段确认中\n"
            "当前阶段：stage-01\n",
            encoding="utf-8",
        )
        state = repo_root / "vcddd" / "work" / "router-check" / "主控状态.md"
        state.parent.mkdir(parents=True)
        state.write_text(
            "# 主控状态：Router 核对\n\n"
            "通信状态：可继续\n"
            "当前负责角色：系统验证 Agent\n",
            encoding="utf-8",
        )

        changed = sync(repo_root)
        if not changed or find_drift(repo_root):
            print("自检失败：首次同步未形成稳定索引。")
            return 1
        delivery_index = (
            repo_root
            / "vcddd"
            / "systems"
            / "router"
            / "delivery"
            / "index.md"
        )
        if (
            "状态：阶段确认中" not in read_text(delivery_index)
            or "阶段：stage-01" not in read_text(delivery_index)
        ):
            print("自检失败：交付索引未投影交付状态与当前阶段。")
            return 1

        validation_text = read_text(validation / "index.md")
        (validation / "index.md").write_text(
            validation_text.replace("验证状态：已运行", "验证状态：已确认"),
            encoding="utf-8",
        )
        if not find_drift(repo_root):
            print("自检失败：未发现状态源变化造成的索引漂移。")
            return 1
        sync(repo_root)
        if find_drift(repo_root):
            print("自检失败：二次同步后仍存在漂移。")
            return 1

    print("索引同步自检通过。")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="从 VCDDD 单一状态源同步受控索引区。"
    )
    parser.add_argument(
        "repo",
        nargs="?",
        default=".",
        help="目标仓库根目录，默认当前目录。",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--write",
        action="store_true",
        help="写入或更新受控生成区。",
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="只检查索引是否同步；这是默认行为。",
    )
    mode.add_argument(
        "--self-test",
        action="store_true",
        help="运行内置索引同步自检。",
    )
    args = parser.parse_args()

    if args.self_test:
        return self_test()

    repo_root = Path(args.repo).expanduser().resolve()
    if args.write:
        changed = sync(repo_root)
        for path in changed:
            print(f"UPDATED: {path}")
        print(f"索引同步完成：更新 {len(changed)} 个文件。")
        return 0

    drift = find_drift(repo_root)
    for path, reason in drift:
        print(f"ERROR: {reason}：{path}")
    if drift:
        print(f"索引不同步：{len(drift)} 个问题。")
        return 1
    print("索引同步：0 个问题。")
    return 0


if __name__ == "__main__":
    sys.exit(main())

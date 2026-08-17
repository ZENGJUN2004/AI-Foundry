"""
AI Foundry v0.9 — Command Line Interface
==========================================

用法示例：

    # 文本分析（Python）
    python -m ai_foundry.cli run "我需要一个做文本情感分析的Python库"

    # HTTP 客户端 + CLI 框架 组合需求
    python -m ai_foundry.cli run "python项目需要异步HTTP客户端和现代化CLI框架"

    # 输出 Markdown 报告到文件
    python -m ai_foundry.cli run "机器学习框架Python" -f markdown -o report.md

    # 输出 JSON
    python -m ai_foundry.cli run "图像处理 python" -f json

    # 强制离线模式（使用内置高质量 mock 数据集，不连 GitHub）
    python -m ai_foundry.cli run "文本分析 python" --offline

    # 运行内置演示（不依赖外部输入）
    python -m ai_foundry.cli demo
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Optional

from . import __version__
from .pipeline import FoundryPipeline, ReportRenderer
from .providers.github import GitHubProvider


# ═══════════════════════════════════════════════════════════════════
#  内置 Demo：覆盖多种典型场景
# ═══════════════════════════════════════════════════════════════════

DEMO_SCENARIOS: list[tuple[str, str]] = [
    (
        "文本分析/NLP（展示 ARCHIVED 风险 + UNKNOWN_LICENSE 阻塞）",
        "我需要一个做情感分析、文本分词的Python库",
    ),
    (
        "异步 HTTP 客户端（展示 STRONG_COPYLEFT + 对比 Python vs JS）",
        "Python项目需要一个异步的HTTP请求客户端库",
    ),
    (
        "计算机视觉/图像处理（展示 AGPL 强传染风险）",
        "做一个目标检测项目，需要Python图像处理和CV库",
    ),
    (
        "CLI框架 + 日志（展示多个能力需求并行处理）",
        "用Python写命令行工具，需要CLI框架和结构化日志库",
    ),
    (
        "数据库 ORM + 可视化（展示 STALE + HIGH_ISSUE_LOAD 组合风险）",
        "Python后台需要异步数据库ORM加上数据可视化图表库",
    ),
    (
        "加解密 / 安全（展示依赖完整性 + License 差异）",
        "Python项目需要对称和非对称加密、加解密库",
    ),
]


def _setup_logging(verbose: bool) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    fmt = "%(asctime)s  %(levelname)-6s  %(name)s  %(message)s" if verbose \
        else "%(levelname)-6s  %(message)s"
    logging.basicConfig(level=level, format=fmt, datefmt="%H:%M:%S")
    # 调静一些内部噪声
    logging.getLogger("urllib3").setLevel(logging.WARNING)


# ═══════════════════════════════════════════════════════════════════
#  子命令实现
# ═══════════════════════════════════════════════════════════════════

def cmd_run(args: argparse.Namespace) -> int:
    provider = GitHubProvider(prefer_online=not args.offline)
    pipeline = FoundryPipeline(
        provider=provider,
        limit_per_capability=args.limit,
    )
    report = pipeline.run(args.query, language=args.lang)

    renderer = ReportRenderer()
    fmt = args.format
    if fmt == "text":
        output = renderer.render_text(report)
    elif fmt == "json":
        output = renderer.render_json(report)
    elif fmt == "markdown":
        output = renderer.render_markdown(report)
    else:
        print(f"未知格式: {fmt}", file=sys.stderr)
        return 2

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✓ 报告已写入 {args.output}", file=sys.stderr)
    else:
        # 只有 text 直接 stdout；json/md 可以管道
        sys.stdout.write(output)
        if not output.endswith("\n"):
            sys.stdout.write("\n")
    return 0


def cmd_demo(args: argparse.Namespace) -> int:
    provider = GitHubProvider(prefer_online=not args.offline)
    pipeline = FoundryPipeline(
        provider=provider,
        limit_per_capability=args.limit,
    )
    renderer = ReportRenderer()

    total = len(DEMO_SCENARIOS)
    reports = []
    for i, (title, query) in enumerate(DEMO_SCENARIOS, 1):
        header = f"\n{'='*72}\n  DEMO {i}/{total} — {title}\n  输入: {query}\n{'='*72}"
        print(header, file=sys.stderr)
        report = pipeline.run(query)
        reports.append((title, report))
        # 只输出 text 概览到 stdout（stderr 已打印 header，stdout 直接接报告）
        if args.format == "text":
            print(renderer.render_text(report))
        elif args.format == "json":
            print(json.dumps({"demo_title": title, **report.to_dict()},
                             ensure_ascii=False, indent=2))
        # markdown 模式下最后合并输出

    if args.format == "markdown":
        out_parts = ["# AI Foundry v0.9 — Demo Scenarios Bundle\n"]
        for idx, (title, rep) in enumerate(reports, 1):
            out_parts.append(f"\n---\n## Scenario {idx}. {title}\n")
            out_parts.append(renderer.render_markdown(rep))
        merged = "\n".join(out_parts)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(merged)
            print(f"✓ Markdown 报告已写入 {args.output}", file=sys.stderr)
        else:
            sys.stdout.write(merged + "\n")

    print(f"\n✓ 完成 {total} 个 Demo 场景。", file=sys.stderr)
    return 0


def cmd_list_caps(_args: argparse.Namespace) -> int:
    """列出 A 层可识别的能力类目（调试用）。"""
    from .layers import _CAPABILITY_PATTERNS
    print("AI Foundry v0.9 可识别的能力类目：\n")
    for i, (name, triggers, category, _expand) in enumerate(_CAPABILITY_PATTERNS, 1):
        print(f"  {i:2}. {name:<20}  category={category:<18}  触发词: {', '.join(triggers[:6])}{'…' if len(triggers)>6 else ''}")
    print(f"\n共 {len(_CAPABILITY_PATTERNS)} 个。未命中时走通用关键词搜索。")
    return 0


# ═══════════════════════════════════════════════════════════════════
#  入口
# ═══════════════════════════════════════════════════════════════════

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ai-foundry",
        description="AI Foundry v0.9 — Software Component Decision Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "示例:\n"
            "  ai-foundry run \"Python文本情感分析库\"\n"
            "  ai-foundry run \"异步HTTP客户端 python\" -f json\n"
            "  ai-foundry demo --offline -f markdown -o demo-report.md\n"
        ),
    )
    p.add_argument("--version", action="version",
                   version=f"ai-foundry {__version__}")
    p.add_argument("-v", "--verbose", action="store_true", help="DEBUG 日志")
    p.add_argument("--offline", action="store_true",
                   help="使用内置离线数据集，不连接 GitHub API")
    p.add_argument("--limit", type=int, default=8,
                   help="每条能力需求最多搜索多少候选（默认 8）")

    sub = p.add_subparsers(dest="command", required=True)

    # run
    pr = sub.add_parser("run", help="对用户输入执行一次完整的 A→B→C→D 流程")
    pr.add_argument("query", help="自然语言需求，例如 \"python 需要一个文本情感分析库\"")
    pr.add_argument("--lang", default=None,
                    help="强制语言倾向（默认按输入自动检测）")
    pr.add_argument("-f", "--format", choices=["text", "json", "markdown"],
                    default="text", help="输出格式（默认 text）")
    pr.add_argument("-o", "--output", default=None, help="写入文件而不是 stdout")
    # 为了"在子命令后也能写 --offline/--limit/--verbose"的直觉体验，子 parser 也接受同名参数
    # （dest 加前缀避免与全局冲突，稍后 merge）
    pr.add_argument("--offline", dest="sub_offline", action="store_true", default=None,
                    help=argparse.SUPPRESS)
    pr.add_argument("--limit", dest="sub_limit", type=int, default=None,
                    help=argparse.SUPPRESS)
    pr.add_argument("-v", "--verbose", dest="sub_verbose", action="store_true", default=None,
                    help=argparse.SUPPRESS)

    # demo
    pd = sub.add_parser("demo", help="运行内置演示场景集")
    pd.add_argument("-f", "--format", choices=["text", "json", "markdown"],
                    default="text")
    pd.add_argument("-o", "--output", default=None)
    pd.add_argument("--offline", dest="sub_offline", action="store_true", default=None,
                    help=argparse.SUPPRESS)
    pd.add_argument("--limit", dest="sub_limit", type=int, default=None,
                    help=argparse.SUPPRESS)
    pd.add_argument("-v", "--verbose", dest="sub_verbose", action="store_true", default=None,
                    help=argparse.SUPPRESS)

    # list-caps
    lc = sub.add_parser("list-caps", help="列出 A 层可识别的能力类目")
    lc.add_argument("--offline", dest="sub_offline", action="store_true", default=None,
                    help=argparse.SUPPRESS)
    lc.add_argument("--limit", dest="sub_limit", type=int, default=None,
                    help=argparse.SUPPRESS)
    lc.add_argument("-v", "--verbose", dest="sub_verbose", action="store_true", default=None,
                    help=argparse.SUPPRESS)

    return p


def _merge_args(args) -> argparse.Namespace:
    """把"子 parser 接受的位置灵活参数"合并到全局字段上。"""
    args.offline = bool(getattr(args, "sub_offline", None) if getattr(args, "sub_offline", None) is not None else args.offline)
    args.verbose = bool(getattr(args, "sub_verbose", None) if getattr(args, "sub_verbose", None) is not None else args.verbose)
    sub_limit = getattr(args, "sub_limit", None)
    if sub_limit is not None:
        args.limit = sub_limit
    return args


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args = _merge_args(args)
    _setup_logging(args.verbose)

    if args.command == "run":
        return cmd_run(args)
    if args.command == "demo":
        return cmd_demo(args)
    if args.command == "list-caps":
        return cmd_list_caps(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

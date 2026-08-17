"""
快速演示脚本 — 直接双击 / `python demo.py` 即可运行
=========================================================

这个脚本会以**离线模式**跑 2 个典型场景（不需要 GitHub token / 网络），
把结果打印到终端并同时保存为 report.md / report.json。

覆盖的 Foundry v0.9 能力：
  ✅ A 层：自然语言 → 结构化能力需求
  ✅ B 层：Provider 搜索 + 证据采集
  ✅ C 层：Component Intelligence Score 8 维评分 + 风险识别
  ✅ D 层：Primary + Alternatives + WHY / WHY NOT / Governance
  ✅ Provider Abstraction（Provider 抽象已预留 GitLab/HuggingFace 等接口）
  ✅ 风险阻塞：UNKNOWN_LICENSE / ARCHIVED / STALE / HIGH_ISSUE_LOAD 等
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# 保证从当前目录直接跑也能 import 到 ai_foundry
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ai_foundry.pipeline import FoundryPipeline, ReportRenderer
from ai_foundry.providers.github import GitHubProvider


SCENARIOS = [
    (
        "场景 1：文本 / NLP 组件决策",
        "我需要一个做文本情感分析、分词处理的Python库",
    ),
    (
        "场景 2：异步 HTTP + 结构化日志",
        "Python 项目需要异步的 HTTP 客户端和结构化日志库",
    ),
]


def main() -> int:
    out_dir = ROOT / "outputs"
    out_dir.mkdir(exist_ok=True)

    provider = GitHubProvider(prefer_online=False)  # 使用高质量离线数据集
    pipeline = FoundryPipeline(provider=provider, limit_per_capability=8)
    renderer = ReportRenderer()

    all_text = []
    all_md = ["# AI Foundry v0.9 — Demo Outputs\n"]
    all_json = {"version": "0.9", "scenarios": []}

    for title, query in SCENARIOS:
        print("=" * 72)
        print(f"▶  {title}")
        print(f"   输入: {query}")
        print("=" * 72)

        report = pipeline.run(query)

        # Text 输出到控制台
        txt = renderer.render_text(report)
        print(txt)
        all_text.append(f"\n\n{'#'*72}\n# {title}\n{'#'*72}\n\n{txt}")

        # Markdown
        all_md.append(f"\n---\n## {title}\n> 输入：{query}\n\n")
        all_md.append(renderer.render_markdown(report))

        # JSON
        all_json["scenarios"].append({
            "title": title,
            "query": query,
            "report": report.to_dict(),
        })

    # 持久化
    text_path = out_dir / "report.txt"
    md_path = out_dir / "report.md"
    json_path = out_dir / "report.json"

    text_path.write_text("\n".join(all_text), encoding="utf-8")
    md_path.write_text("\n".join(all_md), encoding="utf-8")
    json_path.write_text(json.dumps(all_json, ensure_ascii=False, indent=2), encoding="utf-8")

    print()
    print("=" * 72)
    print("✓ Demo 完成。报告已保存在 outputs/ 目录下：")
    print(f"   - {text_path}")
    print(f"   - {md_path}")
    print(f"   - {json_path}")
    print("=" * 72)
    print()
    print("  下一步可用的命令：")
    print("    python -m ai_foundry run \"你的自然语言需求\" --offline")
    print("    python -m ai_foundry demo --offline -f markdown -o all-demos.md")
    print("    python -m ai_foundry list-caps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""
Foundry Pipeline — A → B → C → D 主流程编排
==============================================

这是 v0.9 的核心入口：把 A/B/C/D 四层串成完整的软件组件决策引擎。
未来 v1.0 会在这里扩展：E Build / F Governance / G Deploy 的闭环学习。
"""

from __future__ import annotations

import json
import logging
from typing import Optional

from .layers import AssemblyPlanner, RequirementIntelligence, ResourceScout
from .models import FoundryReport, Requirement
from .providers import OpenSourceProvider
from .providers.github import GitHubProvider
from .registry import ComponentRegistry

log = logging.getLogger(__name__)


class FoundryPipeline:
    """Facade：端到端跑通 A → B → C → D。"""

    def __init__(
        self,
        provider: Optional[OpenSourceProvider] = None,
        limit_per_capability: int = 8,
    ) -> None:
        self.provider = provider or GitHubProvider()
        self.a_layer = RequirementIntelligence()
        self.b_layer = ResourceScout(self.provider, limit_per_capability=limit_per_capability)
        self.c_layer = ComponentRegistry()
        self.d_layer = AssemblyPlanner()

    # ── 端到端入口 ──────────────────────────────────────────────

    def run(
        self,
        user_input: str,
        language: Optional[str] = None,
    ) -> FoundryReport:
        log.info("═" * 60)
        log.info("AI Foundry v0.9 Pipeline start")
        log.info("═" * 60)

        # A 层：需求 → 能力需求
        requirement = self.a_layer.analyze(user_input, language=language)
        log.info("A 层完成：%d 条能力需求", len(requirement.capabilities))
        for cap in requirement.capabilities:
            log.info("   • %s (prio=%d, kw=%s)", cap.name, cap.priority, cap.keywords[:5])

        # B 层：搜索 + 拉证据
        evidences_by_cap = self.b_layer.scout(requirement)

        # C 层：注册 + 评分 + 风险
        decisions = []
        for cap in requirement.capabilities:
            ev_list = evidences_by_cap.get(cap.name, [])
            log.info("C 层注册 [%s]: %d 个候选组件", cap.name, len(ev_list))
            components = self.c_layer.register_many(ev_list, capability=cap)
            if not components:
                log.warning("  注册结果为空，跳过 D 层。")
                continue
            # 打印前 3 的评分
            components_sorted = sorted(components, key=lambda c: c.total_score, reverse=True)
            for i, c in enumerate(components_sorted[:3]):
                log.info("   #%d %s  Score=%.1f  Blocked=%s  Risks=%d",
                         i + 1, c.name, c.total_score, c.is_blocked, len(c.risks))

            # D 层：组装决策
            decision = self.d_layer.plan(cap, components)
            decisions.append(decision)

        report = FoundryReport(requirement=requirement, decisions=decisions)
        log.info("═" * 60)
        log.info("Pipeline 完成：%d 条 AssemblyDecision", len(decisions))
        log.info("═" * 60)
        return report

    # ── 便捷：已经有 Requirement 就跳过 A 层 ──────────────────────

    def run_with_requirement(self, requirement: Requirement) -> FoundryReport:
        evidences_by_cap = self.b_layer.scout(requirement)
        decisions = []
        for cap in requirement.capabilities:
            ev_list = evidences_by_cap.get(cap.name, [])
            components = self.c_layer.register_many(ev_list, capability=cap)
            if components:
                decisions.append(self.d_layer.plan(cap, components))
        return FoundryReport(requirement=requirement, decisions=decisions)


# ═══════════════════════════════════════════════════════════════════
#  报告渲染（人类可读）
# ═══════════════════════════════════════════════════════════════════

class ReportRenderer:
    """把 FoundryReport 渲染成人类可读的文本 / Markdown。"""

    BAR = "─" * 72

    def render_text(self, report: FoundryReport) -> str:
        lines: list[str] = []
        lines.append("╔" + "═" * 70 + "╗")
        lines.append("║  AI Foundry v0.9  —  Software Component Decision Report       ║")
        lines.append("╚" + "═" * 70 + "╝")
        lines.append("")
        lines.append(f"  原始需求 : {report.requirement.raw_input}")
        lines.append(f"  需求摘要 : {report.requirement.summary}")
        lines.append(f"  生成时间 : {report.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        lines.append(f"  决策数量 : {len(report.decisions)}")
        lines.append("")

        for idx, d in enumerate(report.decisions, 1):
            lines.extend(self._render_decision(idx, d))

        # 架构说明
        lines.append("")
        lines.append(self.BAR)
        lines.append("  评分维度 (Component Intelligence Score, 满分 100)")
        lines.append("    Relevance 25%   Maintenance 20%   Code Quality 15%   Community 10%")
        lines.append("    Issue Health 10%   PR Health 5%   License 10%   Dependency Health 5%")
        lines.append("")
        lines.append("  风险类型：ARCHIVED / UNKNOWN_LICENSE / STALE / HIGH_ISSUE_LOAD /")
        lines.append("             LOW_SCORE / STRONG_COPYLEFT / FEW_CONTRIBUTORS / OUTDATED_DEPENDENCIES")
        lines.append("  CRITICAL 级风险或 ARCHIVED / UNKNOWN_LICENSE 会阻塞组件进入 Primary。")
        return "\n".join(lines)

    def render_json(self, report: FoundryReport, indent: int = 2) -> str:
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=indent)

    def render_markdown(self, report: FoundryReport) -> str:
        md: list[str] = []
        md.append("# AI Foundry v0.9 — Component Decision Report\n")
        md.append(f"> 生成时间：{report.generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}  \n")
        md.append(f"**原始需求**：{report.requirement.raw_input}  \n")
        md.append(f"**需求摘要**：{report.requirement.summary}\n")

        for idx, d in enumerate(report.decisions, 1):
            md.append(f"\n## {idx}. {d.capability.name}\n")
            md.append(f"- 搜索关键词：`{', '.join(d.capability.keywords[:6])}`")
            if d.capability.language:
                md.append(f"- 语言倾向：**{d.capability.language}**")
            md.append("")

            if d.primary:
                p = d.primary
                s = p.score.as_dict()
                md.append(f"### ✅ Primary：[{p.name}]({p.evidence.url})  `Score: {s['total']}`\n")
                md.append(f"> {p.evidence.description or '—'}\n")
                md.append("| 维度 | 得分 |")
                md.append("|---|---|")
                for k in ["relevance", "maintenance", "code_quality", "community",
                          "issue_health", "pr_health", "license", "dependency_health", "total"]:
                    md.append(f"| {k} | {s[k]} |")
                md.append("")
                md.append("**为什么选它？**")
                for r in d.why_primary:
                    md.append(f"- {r}")
                md.append("")
                if d.risks_of_primary:
                    md.append("**⚠️  存在的风险**")
                    for r in d.risks_of_primary:
                        md.append(f"- {r}")
                    md.append("")
            else:
                md.append("### ⛔ 无 Primary（全部候选被阻塞）\n")

            if d.alternatives:
                md.append("**🔀 替代方案**")
                for alt in d.alternatives:
                    block_tag = " 🚫BLOCKED" if alt.is_blocked else ""
                    md.append(f"- **{alt.name}** `Score: {alt.total_score}`{block_tag}  ")
                    why_nots = d.why_not_alternatives.get(alt.id, [])
                    for w in why_nots:
                        md.append(f"  - {w}")
                md.append("")

            if d.governance_actions:
                md.append("**🛡️  F Governance 建议**")
                for g in d.governance_actions:
                    md.append(f"- {g}")
                md.append("")

        md.append("\n---\n")
        md.append("### v0.9 架构升级说明\n")
        md.append("本系统已不是「GitHub 推荐器」，而是 **Software Component Decision Engine**：\n")
        md.append("A(需求) → B(Scout 搜索 + 采集) → C(Registry 8维评分 + 风险识别) → D(Assembly 主候选 + 替代 + 治理)\n")
        return "\n".join(md)

    # ── 单条 decision 文本渲染 ─────────────────────────────────

    def _render_decision(self, idx: int, d) -> list[str]:
        lines: list[str] = []
        lines.append(self.BAR)
        cap_prio = {1: "★必选", 2: "●应该", 3: "○可选"}.get(d.capability.priority, "")
        lines.append(f"【能力需求 #{idx}】 {d.capability.name}  {cap_prio}")
        lines.append(f"  关键词 : {', '.join(d.capability.keywords[:8])}")
        if d.capability.language:
            lines.append(f"  语言倾向: {d.capability.language}")
        lines.append("")

        # 候选集表格
        all_cands = []
        if d.primary:
            all_cands.append(("P", d.primary))
        for i, alt in enumerate(d.alternatives, 1):
            tag = f"A{i}"
            all_cands.append((tag, alt))
        if all_cands:
            lines.append("  ┌─────────┬──────────────────────────────┬────────┬─────────┬──────────┐")
            lines.append("  │ 角色    │ 组件                        │ 评分   │ Stars   │ 状态     │")
            lines.append("  ├─────────┼──────────────────────────────┼────────┼─────────┼──────────┤")
            for tag, c in all_cands:
                name = (c.name[:26] + "…") if len(c.name) > 27 else c.name
                blocked = "🚫阻塞" if c.is_blocked else "  可用"
                lines.append(
                    f"  │ {tag:<7} │ {name:<28} │ {c.total_score:>6.1f} │ "
                    f"{c.evidence.stars:>7,} │ {blocked} │"
                )
            lines.append("  └─────────┴──────────────────────────────┴────────┴─────────┴──────────┘")
            lines.append("")

        # WHY PRIMARY
        if d.primary:
            lines.append(f"  🎯 为什么选 Primary → {d.primary.name}")
            for r in d.why_primary:
                lines.append(f"     ✓ {r}")
            lines.append("")
            if d.risks_of_primary:
                lines.append(f"  ⚠️  Primary 的风险")
                for r in d.risks_of_primary:
                    lines.append(f"     ! {r}")
                lines.append("")

        # WHY NOT ALTERNATIVES
        if d.alternatives:
            lines.append("  ❓ 为什么不选替代方案")
            for alt in d.alternatives:
                lines.append(f"     - {alt.name}  (Score {alt.total_score})")
                for w in d.why_not_alternatives.get(alt.id, []):
                    lines.append(f"         × {w}")
            lines.append("")

        # Governance
        if d.governance_actions:
            lines.append("  🛡️  F Governance 介入事项")
            for g in d.governance_actions:
                lines.append(f"     → {g}")
            lines.append("")
        return lines

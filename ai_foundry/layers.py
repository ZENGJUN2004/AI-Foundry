"""
Layers A, B, D
===============

A  Requirement Intelligence  →  自然语言 → 结构化能力需求
B  Resource Scout            →  用 Provider 搜索 + 拉取证据
D  Assembly Planner          →  Primary + Alternatives + 可解释决策

注：C 层已在 registry.py（ComponentRegistry + ScoringEngine + RiskAnalyzer）。
"""

from __future__ import annotations

import logging
import re
from typing import Optional

from .models import (
    AssemblyDecision,
    CapabilityNeed,
    Component,
    Requirement,
    RiskSeverity,
    RiskType,
)
from .providers import OpenSourceProvider
from .registry import ComponentRegistry

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
#  A Layer — Requirement Intelligence
# ═══════════════════════════════════════════════════════════════════

# 简单的内置"能力词典"：把关键词归类到已知能力类目，自动补全搜索词
# 规则式足够支撑 v0.9；v1.0 可接入 LLM 做更智能拆解
_CAPABILITY_PATTERNS: list[tuple[str, list[str], str, list[str]]] = [
    # (能力名, 触发关键词, 类目, 扩展搜索词)
    ("文本分析/NLP",
     ["text", "nlp", "natural language", "sentiment", "情感", "文本", "分词",
      "ner", "named entity", "pos", "词性", "语义", "embedding"],
     "nlp",
     ["text analysis", "sentiment", "nlp", "processing", "tokenize"]),
    ("HTTP客户端/网络请求",
     ["http", "https", "request", "client", "rest", "api", "请求", "网络",
      "curl", "fetch", "async http"],
     "http-client",
     ["http client", "requests", "async", "httpx", "aiohttp"]),
    ("图像处理/计算机视觉",
     ["image", "cv", "vision", "computer vision", "ocr", "object detection",
      "图像", "图片", "视觉", "识别", "yolo", "pillow", "opencv"],
     "computer-vision",
     ["image processing", "computer vision", "opencv", "pillow", "detection"]),
    ("CLI框架/命令行工具",
     ["cli", "command-line", "command line", "terminal", "console", "命令行",
      "终端", "argparse", "typer", "click"],
     "cli-framework",
     ["cli", "command-line", "typer", "click", "terminal"]),
    ("数据库/ORM",
     ["database", "db", "orm", "sql", "redis", "postgres", "mysql", "sqlite",
      "数据库", "缓存", "mongo"],
     "database",
     ["database", "orm", "sqlalchemy", "redis", "driver"]),
    ("数据可视化/图表",
     ["chart", "plot", "visualization", "visualize", "graph", "dashboard",
      "图表", "可视化", "绘图", "matplotlib", "plotly"],
     "visualization",
     ["visualization", "chart", "plot", "matplotlib", "plotly", "dashboard"]),
    ("日志/监控",
     ["log", "logging", "logger", "monitor", "metric", "tracing",
      "日志", "监控", "指标", "追踪"],
     "logging",
     ["logging", "logger", "monitoring", "tracing", "metrics"]),
    ("机器学习框架",
     ["machine learning", "ml", "deep learning", "neural network", "pytorch",
      "tensorflow", "scikit", "sklearn", "机器学习", "深度学习", "模型训练"],
     "ml-framework",
     ["machine learning", "deep learning", "pytorch", "tensorflow", "sklearn"]),
    ("测试框架",
     ["test", "testing", "unit test", "pytest", "jest", "单元测试",
      "集成测试", "断言"],
     "testing",
     ["testing", "unit-test", "pytest", "jest", "assertion"]),
    ("加解密/安全",
     ["crypto", "encrypt", "decrypt", "cipher", "security", "aes", "rsa",
      "signature", "加密", "解密", "签名", "安全", "hash"],
     "security",
     ["cryptography", "encryption", "security", "rsa", "aes"]),
]


class RequirementIntelligence:
    """A 层：用户自然语言需求 → Requirement。"""

    # 简单的语言检测
    _LANG_HINTS = {
        "python": ["python", "py"],
        "javascript": ["javascript", "js", "node", "nodejs"],
        "typescript": ["typescript", "ts"],
        "go": ["golang", " go ", "go语言"],
        "rust": ["rust"],
        "java": ["java"],
    }

    def analyze(self, raw_input: str, language: Optional[str] = None) -> Requirement:
        text = raw_input.strip()
        lower = text.lower()

        # 1) 语言检测
        target_lang = language or self._detect_language(lower)

        # 2) 对每个能力模式，看触发了多少关键词
        caps: list[CapabilityNeed] = []
        used_names: set[str] = set()
        for name, triggers, category, expand_terms in _CAPABILITY_PATTERNS:
            hit_triggers = [t for t in triggers if t.lower() in lower]
            if hit_triggers:
                # 搜索关键词 = 触发词 + 扩展词 + 语言约束
                keywords = list(dict.fromkeys(
                    [*hit_triggers, *expand_terms]
                ))
                priority = 1 if len(hit_triggers) >= 2 else 2
                caps.append(CapabilityNeed(
                    name=name,
                    keywords=keywords,
                    language=target_lang,
                    category=category,
                    priority=priority,
                    description=f"基于关键词触发: {', '.join(hit_triggers)}",
                ))
                used_names.add(name)

        # 3) 如果没有匹配到内置模式，兜底：把用户输入切词作为通用搜索能力
        if not caps:
            keywords = self._extract_keywords(text)
            caps.append(CapabilityNeed(
                name="通用组件搜索",
                keywords=keywords,
                language=target_lang,
                category="general",
                priority=1,
                description="未匹配内置能力模式，按用户输入关键词搜索。",
            ))

        # 4) 摘要
        summary = self._summarize(text, caps, target_lang)

        req = Requirement(
            raw_input=raw_input,
            summary=summary,
            capabilities=caps,
            target_language=target_lang,
            extra_constraints={},
        )
        log.info(
            "A 层完成: 需求拆解出 %d 条能力需求 (lang=%s)",
            len(req.capabilities), req.target_language,
        )
        return req

    # ── helpers ───────────────────────────────────────────────

    def _detect_language(self, lower: str) -> Optional[str]:
        scores: dict[str, int] = {}
        for lang, hints in self._LANG_HINTS.items():
            scores[lang] = sum(1 for h in hints if h in lower)
        # 必须有至少 1 次命中才返回，否则 None（不限制语言）
        best_lang, best_score = max(scores.items(), key=lambda x: x[1])
        return best_lang if best_score >= 1 else None

    @staticmethod
    def _extract_keywords(text: str) -> list[str]:
        # 中英文标点 + 空白切分，过滤停用词
        tokens = re.findall(r"[\w\u4e00-\u9fa5]+", text.lower())
        stop = {
            "the", "and", "or", "for", "with", "using", "use", "need",
            "a", "an", "to", "of", "in", "on", "is", "are", "be",
            "我", "需要", "一个", "做", "和", "的", "在", "用", "使用",
            "可以", "能够", "应该", "能", "是", "了", "就",
        }
        return [t for t in tokens if t not in stop and len(t) >= 2]

    @staticmethod
    def _summarize(raw: str, caps: list[CapabilityNeed], lang: Optional[str]) -> str:
        head = raw[:60] + ("…" if len(raw) > 60 else "")
        cap_names = "、".join(c.name for c in caps)
        lang_part = f" (语言倾向: {lang})" if lang else ""
        return f"{head} → 能力: {cap_names}{lang_part}"


# ═══════════════════════════════════════════════════════════════════
#  B Layer — Resource Scout
# ═══════════════════════════════════════════════════════════════════

class ResourceScout:
    """B 层：对每条 CapabilityNeed 分别执行 search → fetch_evidence。"""

    def __init__(self, provider: OpenSourceProvider, limit_per_capability: int = 8):
        self.provider = provider
        self.limit = limit_per_capability

    def scout(self, requirement: Requirement) -> dict[str, list]:
        """返回 {capability.name: [RepoEvidence,...]}。"""
        results: dict[str, list] = {}
        for cap in requirement.capabilities:
            log.info(
                "B 层搜索: [%s] keywords=%s lang=%s",
                cap.name, cap.keywords, cap.language,
            )
            evidences = self.provider.search_and_fetch(cap, limit=self.limit)
            log.info("  → 命中 %d 个候选仓库", len(evidences))
            results[cap.name] = evidences
        return results


# ═══════════════════════════════════════════════════════════════════
#  D Layer — Assembly Planner
# ═══════════════════════════════════════════════════════════════════

class AssemblyPlanner:
    """D 层：挑选 Primary + Alternatives，形成可解释决策。

    策略：
      1. 过滤 BLOCKED 组件（CRITICAL 风险 / ARCHIVED / UNKNOWN_LICENSE）
         → 不进入 Primary 候选，但仍可能出现在 Alternatives 并标明"被阻塞"
      2. 按 total_score 降序
      3. Top-1 = Primary, 2~5 = Alternatives
      4. 生成 WHY_PRIMARY / WHY_NOT_xx / RISKS 等解释文本
    """

    MAX_ALTERNATIVES = 4

    def plan(
        self,
        capability: CapabilityNeed,
        components: list[Component],
    ) -> AssemblyDecision:
        decision = AssemblyDecision(capability=capability)

        # 1) 排序：按总分降序，blocked 沉底
        ranked = sorted(
            components,
            key=lambda c: (0 if c.is_blocked else 1, c.total_score),
            reverse=True,
        )

        # 2) 取 Primary = 第一个未被阻塞的
        unblocked = [c for c in ranked if not c.is_blocked]
        if unblocked:
            decision.primary = unblocked[0]
            decision.alternatives = [
                c for c in unblocked[1:]
            ][: self.MAX_ALTERNATIVES]
        else:
            # 全被阻塞，也给出阻塞后的 Top-1 让用户知道"搜到了但不能用"
            if ranked:
                decision.primary = None
                decision.alternatives = ranked[: self.MAX_ALTERNATIVES]
                decision.governance_actions.append(
                    "所有候选组件均被风险规则阻塞，需 F Governance 人工介入：放宽限制或寻找私有替代。"
                )

        # 3) 生成解释
        decision.why_primary = self._explain_primary(decision.primary, capability)
        for alt in decision.alternatives:
            decision.why_not_alternatives[alt.id] = self._explain_why_not(
                decision.primary, alt, capability
            )
        decision.risks_of_primary = self._list_primary_risks(decision.primary)
        decision.governance_actions.extend(
            self._governance_actions(decision.primary)
        )
        return decision

    # ── 解释器 ────────────────────────────────────────────────

    @staticmethod
    def _explain_primary(primary: Optional[Component], cap: CapabilityNeed) -> list[str]:
        if primary is None:
            return ["无合格的 Primary 候选（所有组件均被阻塞）。"]
        reasons: list[str] = []
        score = primary.score
        reasons.append(
            f"综合评分 {score.total} 在候选集中排名第 1。"
        )
        # 找出 2 个最强维度
        dims = [
            ("Relevance 需求契合度", score.relevance, 25),
            ("Maintenance 维护活跃度", score.maintenance, 20),
            ("Code Quality 代码质量", score.code_quality, 15),
            ("Community 社区规模", score.community, 10),
            ("Issue Health Issue处理", score.issue_health, 10),
            ("PR Health PR健康度", score.pr_health, 5),
            ("License 许可协议", score.license, 10),
            ("Dependency 依赖健康", score.dependency_health, 5),
        ]
        dims.sort(key=lambda x: x[1], reverse=True)
        for name, val, _ in dims[:2]:
            if val >= 80:
                reasons.append(f"{name} 维度得分 {val}，表现突出。")
        # 关键词匹配
        if primary.matched_keywords:
            reasons.append(
                "命中需求关键词：" + ", ".join(primary.matched_keywords[:5]) + "。"
            )
        # 量级信号
        ev = primary.evidence
        if ev.stars >= 1000:
            reasons.append(f"社区成熟：{ev.stars:,} Stars / {ev.forks:,} Forks。")
        return reasons

    @staticmethod
    def _explain_why_not(
        primary: Optional[Component],
        alt: Component,
        cap: CapabilityNeed,
    ) -> list[str]:
        reasons: list[str] = []

        if alt.is_blocked:
            # 具体是哪条阻塞规则
            for r in alt.risks:
                if r.severity == RiskSeverity.CRITICAL or r.type in (
                    RiskType.ARCHIVED, RiskType.UNKNOWN_LICENSE
                ):
                    reasons.append(f"[阻塞] {r.type.value}: {r.message}")
            if not reasons:
                reasons.append("[阻塞] 组件处于 BLOCKED 状态，禁止进入 Primary。")
            return reasons

        if primary is None:
            return ["No primary candidate."]

        delta = primary.total_score - alt.total_score
        if delta > 0:
            reasons.append(f"总分比 Primary 低 {delta:.1f} 分。")

        # 挑 1 个明显落后的维度
        dim_names = [
            ("relevance", "Relevance"),
            ("maintenance", "Maintenance"),
            ("code_quality", "Code Quality"),
            ("community", "Community"),
            ("issue_health", "Issue Health"),
            ("pr_health", "PR Health"),
            ("license", "License"),
            ("dependency_health", "Dependency Health"),
        ]
        biggest_gap = 0.0
        biggest_name = ""
        for attr, label in dim_names:
            p_val = getattr(primary.score, attr)
            a_val = getattr(alt.score, attr)
            gap = p_val - a_val
            if gap > biggest_gap:
                biggest_gap = gap
                biggest_name = label
        if biggest_gap >= 15:
            reasons.append(f"{biggest_name} 维度落后 {biggest_gap:.0f} 分。")

        # 如果这个替代存在额外风险，点出来
        extra_risks = [
            r for r in alt.risks
            if r.severity in {RiskSeverity.HIGH, RiskSeverity.CRITICAL}
            and not any(
                rr.type == r.type
                for rr in primary.risks
                if rr.severity in {RiskSeverity.HIGH, RiskSeverity.CRITICAL}
            )
        ]
        for r in extra_risks:
            reasons.append(f"额外风险 {r.type.value}: {r.message}")

        if not reasons:
            reasons.append("和 Primary 非常接近，可作为备胎方案。")
        return reasons

    @staticmethod
    def _list_primary_risks(primary: Optional[Component]) -> list[str]:
        if primary is None:
            return []
        return [
            f"[{r.severity.value.upper()}] {r.type.value}: {r.message}"
            for r in primary.risks
        ]

    @staticmethod
    def _governance_actions(primary: Optional[Component]) -> list[str]:
        if primary is None:
            return []
        actions: list[str] = []
        types = {r.type for r in primary.risks}
        if RiskType.STRONG_COPYLEFT in types:
            actions.append(
                f"F Governance: {primary.name} 为强 Copyleft License，法务需确认是否可以集成。"
            )
        if RiskType.STALE in types:
            actions.append(
                f"F Governance: {primary.name} 维护停滞，建议在 Assembly 中注入被动升级 watcher。"
            )
        if RiskType.FEW_CONTRIBUTORS in types:
            actions.append(
                f"F Governance: {primary.name} 存在单一维护者风险，可考虑 fork 作为备份。"
            )
        if RiskType.HIGH_ISSUE_LOAD in types:
            actions.append(
                f"F Governance: {primary.name} Issue 负载高，遇到问题可能响应较慢，需预留替代通道。"
            )
        return actions

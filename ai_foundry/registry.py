"""
C Layer — Component Registry
=============================

    Evidence (RepoEvidence)
          │
          ▼
    ┌────────────────────┐
    │  Scoring Engine    │  →  ScoreBreakdown (8 维加权 → 0-100)
    └─────────┬──────────┘
              ▼
    ┌────────────────────┐
    │  Risk Analyzer     │  →  List[Risk] (阻塞 / 降级 / 警告)
    └─────────┬──────────┘
              ▼
         Component (已注册组件)

核心设计原则：
    1) 所有子分数都映射到 0.0 ~ 100.0 区间，保证加权后的总分有物理意义
    2) 每一步都尽量「可解释」：ScoreBreakdown 保留各维度的单独分数
    3) 单调：指标越好 → 分数越高（不对用户心智做反向操作）
"""

from __future__ import annotations

import logging
import math
from datetime import datetime, timezone
from typing import Optional

from .models import (
    CapabilityNeed,
    Component,
    LicenseCategory,
    RepoEvidence,
    Risk,
    RiskSeverity,
    RiskType,
    ScoreBreakdown,
)

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
#  Scoring Engine
# ═══════════════════════════════════════════════════════════════════

class ScoringEngine:
    """Component Intelligence Score — 8 维加权评分。

    每个评分函数都单独测试，确保：最小值 → 0、满分标准合理、单调不减。
    """

    # ── 入口 ──────────────────────────────────────────────────

    def score(
        self,
        evidence: RepoEvidence,
        capability: Optional[CapabilityNeed] = None,
    ) -> ScoreBreakdown:
        sb = ScoreBreakdown()
        sb.relevance = self._score_relevance(evidence, capability)
        sb.maintenance = self._score_maintenance(evidence)
        sb.code_quality = self._score_code_quality(evidence)
        sb.community = self._score_community(evidence)
        sb.issue_health = self._score_issue_health(evidence)
        sb.pr_health = self._score_pr_health(evidence)
        sb.license = self._score_license(evidence)
        sb.dependency_health = self._score_dependency_health(evidence)
        return sb

    # ── 1) Relevance 25% ──────────────────────────────────────

    @staticmethod
    def _score_relevance(
        evidence: RepoEvidence,
        capability: Optional[CapabilityNeed],
    ) -> float:
        """基于需求关键词在 repo 元数据中的覆盖率打分。"""
        if not capability or not capability.keywords:
            # 没有关键词时，默认中性分 50（不拖后腿也不加分）
            return 50.0

        keywords = [k.lower() for k in capability.keywords if k]
        if not keywords:
            return 50.0

        haystack = " ".join([
            evidence.full_name.lower(),
            (evidence.description or "").lower(),
            " ".join(t.lower() for t in evidence.topics),
            (evidence.language or "").lower(),
        ])

        hit_count = 0
        for kw in keywords:
            if kw in haystack:
                hit_count += 1
            else:
                # 关键词拆分：每个 word 部分命中给半分
                parts = kw.split()
                if len(parts) >= 2 and all(p in haystack for p in parts if len(p) >= 3):
                    hit_count += 0.5

        ratio = hit_count / len(keywords)
        # 覆盖率 → 0-100；命中 60% 就给到 80 分，避免"所有词全命中才高分"的苛刻
        score = min(100.0, (ratio * 130.0) + 10.0)
        return round(score, 1)

    # ── 2) Maintenance 20% ────────────────────────────────────

    @staticmethod
    def _score_maintenance(evidence: RepoEvidence) -> float:
        """最近 30/90 天提交 + 最后 push 时间的联合估计。"""
        now = datetime.now(timezone.utc)

        # a. 最后 push 时间
        pushed = evidence.pushed_at or evidence.commits.last_commit_date
        days_since_push = (now - pushed).days if pushed else 9999
        # <7d = 100, <30d = 80, <90d = 55, <180d = 30, >365d = 0
        if days_since_push <= 7:
            t_score = 100.0
        elif days_since_push <= 30:
            t_score = 80.0 + (30 - days_since_push) / 23 * 20
        elif days_since_push <= 90:
            t_score = 30.0 + (90 - days_since_push) / 60 * 50
        elif days_since_push <= 365:
            t_score = max(0.0, 30.0 - (days_since_push - 90) / 275 * 30)
        else:
            t_score = 0.0

        # b. 30 天提交量（log 曲线：20+ 就 100）
        commits_30 = evidence.commits.commits_30d
        c_score = min(100.0, math.log1p(commits_30) / math.log1p(20) * 100.0)

        # c. 90 天贡献者数（5+ 就 100，单一维护者风险）
        contribs = evidence.commits.contributors_90d
        contr_score = min(100.0, contribs / 5 * 100.0)

        # 加权：推送时效更重要
        score = t_score * 0.5 + c_score * 0.3 + contr_score * 0.2
        # 归档仓库直接清零（风险层会再打 ARCHIVED）
        if evidence.archived:
            score = min(score, 10.0)
        return round(score, 1)

    # ── 3) Code Quality 15% ───────────────────────────────────

    @staticmethod
    def _score_code_quality(evidence: RepoEvidence) -> float:
        """间接指标：README 规模（文档完善度）、homepage、wiki/pages 等元数据完整性。"""
        score = 40.0  # 基础分
        # README 质量：4000+ 字节给 30 分
        readme = evidence.readme_size_bytes
        if readme >= 15000:
            score += 30.0
        elif readme >= 8000:
            score += 22.0
        elif readme >= 3000:
            score += 12.0
        elif readme > 0:
            score += 5.0
        # 有独立主页 +8
        if evidence.homepage:
            score += 8.0
        # 有文档 / Pages +7
        if evidence.has_pages or evidence.has_wiki:
            score += 7.0
        # fork 仓库扣 10（通常不是上游）
        if evidence.is_fork:
            score -= 10.0
        # 有 topics 元数据 +5
        if evidence.topics:
            score += min(15.0, len(evidence.topics) * 1.5)
        return round(max(0.0, min(100.0, score)), 1)

    # ── 4) Community 10% ──────────────────────────────────────

    @staticmethod
    def _score_community(evidence: RepoEvidence) -> float:
        """stars / forks / watchers 的对数归一化。"""
        stars = max(0, evidence.stars)
        forks = max(0, evidence.forks)
        watchers = max(0, evidence.watchers or evidence.subscribers)

        # stars：100 为及格点，5000+ 接近满分
        s_score = min(100.0, math.log1p(stars) / math.log1p(5000) * 100.0)
        # forks：200 及格点，1000 接近满分
        f_score = min(100.0, math.log1p(forks) / math.log1p(1000) * 100.0)
        # watchers：100 及格
        w_score = min(100.0, math.log1p(watchers) / math.log1p(500) * 100.0)

        score = s_score * 0.5 + f_score * 0.3 + w_score * 0.2
        return round(score, 1)

    # ── 5) Issue Health 10% ───────────────────────────────────

    @staticmethod
    def _score_issue_health(evidence: RepoEvidence) -> float:
        """关闭率 + 响应速度 + 近期活跃度。"""
        issues = evidence.issues
        total = issues.open_count + issues.closed_count
        if total == 0:
            # 没有 issue 数据：给中性 60，不算差
            return 60.0

        # a. 关闭率（权重 50%）：closed/total。85%+ = 100
        close_rate = issues.closed_count / total
        close_rate_score = min(100.0, (close_rate / 0.85) * 100.0)

        # b. 平均 open 天数（权重 30%）：<14d = 100, >180d = 0
        avg_days = issues.avg_days_open
        if avg_days <= 14:
            days_score = 100.0
        elif avg_days >= 180:
            days_score = 0.0
        else:
            days_score = (180 - avg_days) / 166 * 100.0

        # c. 近 30 天活跃度（权重 20%）：有开 + 有关 = 健康
        recent_sum = issues.recent_30d_opened + issues.recent_30d_closed
        active_score = min(100.0, recent_sum / 20 * 100.0)

        # open 绝对数量极高（>300）的重灾区扣分
        penalty = 0.0
        if issues.open_count > 500:
            penalty = 30.0
        elif issues.open_count > 300:
            penalty = 15.0
        elif issues.open_count > 150:
            penalty = 5.0

        score = close_rate_score * 0.5 + days_score * 0.3 + active_score * 0.2 - penalty
        return round(max(0.0, min(100.0, score)), 1)

    # ── 6) PR Health 5% ───────────────────────────────────────

    @staticmethod
    def _score_pr_health(evidence: RepoEvidence) -> float:
        pr = evidence.pull_requests
        if pr.open_count == 0 and pr.merged_30d == 0:
            return 50.0  # 中性

        # a. 合并速率：merged_30d 越多越好（20+ → 100）
        merge_score = min(100.0, math.log1p(pr.merged_30d) / math.log1p(20) * 100.0)
        # b. 合并延迟：<3d → 100, >30d → 0
        if pr.avg_days_to_merge <= 0 or pr.merged_30d == 0:
            delay_score = 0.0 if pr.open_count > 10 else 50.0
        elif pr.avg_days_to_merge <= 3:
            delay_score = 100.0
        elif pr.avg_days_to_merge >= 30:
            delay_score = 0.0
        else:
            delay_score = (30 - pr.avg_days_to_merge) / 27 * 100.0
        score = merge_score * 0.6 + delay_score * 0.4
        return round(score, 1)

    # ── 7) License 10% ────────────────────────────────────────

    @staticmethod
    def _score_license(evidence: RepoEvidence) -> float:
        cat = evidence.license_category
        return {
            LicenseCategory.PERMISSIVE: 100.0,
            LicenseCategory.WEAK_COPYLEFT: 65.0,
            LicenseCategory.STRONG_COPYLEFT: 30.0,
            LicenseCategory.PROPRIETARY: 0.0,
            LicenseCategory.UNKNOWN: 0.0,
        }.get(cat, 0.0)

    # ── 8) Dependency Health 5% ───────────────────────────────

    @staticmethod
    def _score_dependency_health(evidence: RepoEvidence) -> float:
        deps = evidence.dependencies
        if not deps:
            return 65.0  # 无数据给中性
        total = len(deps)
        outdated = sum(1 for d in deps if d.outdated)
        severe = sum(1 for d in deps if d.severity in {"high", "critical"})
        ratio_outdated = outdated / total
        severe_penalty = severe * 15.0
        base = 100.0 - ratio_outdated * 80.0 - severe_penalty
        return round(max(0.0, min(100.0, base)), 1)


# ═══════════════════════════════════════════════════════════════════
#  Risk Analyzer
# ═══════════════════════════════════════════════════════════════════

class RiskAnalyzer:
    """基于证据 + 评分的风险识别。

    风险会在 D 层影响：
      • CRITICAL / UNKNOWN_LICENSE / ARCHIVED → 阻塞 (is_blocked=True)
      • HIGH / MEDIUM                          → 写入风险说明 + 触发 F Governance
    """

    # 可调阈值
    STALE_DAYS = 240           # 超过此天数无更新 = STALE
    HIGH_ISSUE_OPEN = 300      # 未关闭 Issue 超此值 = HIGH_ISSUE_LOAD
    SCORE_DANGER = 45.0        # 总分低于此 = LOW_SCORE (HIGH)
    SCORE_WARN = 60.0          # 总分低于此 = LOW_SCORE (MEDIUM)
    FEW_CONTRIBUTORS = 1       # 90 天贡献者 <= 此值 = 单一维护者风险
    OUTDATED_DEPS_RATIO = 0.4  # 依赖过期率 > 此值 = OUTDATED_DEPENDENCIES

    def analyze(self, component: Component) -> list[Risk]:
        risks: list[Risk] = []
        ev = component.evidence
        now = datetime.now(timezone.utc)

        # 1) ARCHIVED (CRITICAL — 阻塞)
        if ev.archived:
            risks.append(Risk(
                type=RiskType.ARCHIVED,
                severity=RiskSeverity.CRITICAL,
                message="仓库已归档，不再接收任何维护更新。",
                data={"archived": True},
            ))

        # 2) UNKNOWN_LICENSE (CRITICAL — 阻塞)
        if ev.license_category == LicenseCategory.UNKNOWN:
            risks.append(Risk(
                type=RiskType.UNKNOWN_LICENSE,
                severity=RiskSeverity.CRITICAL,
                message="无法识别 License，不能直接引入，需 F Governance 人工审核。",
                data={"license_name": ev.license_name},
            ))

        # 3) STRONG_COPYLEFT (HIGH — 传染风险)
        if ev.license_category == LicenseCategory.STRONG_COPYLEFT:
            risks.append(Risk(
                type=RiskType.STRONG_COPYLEFT,
                severity=RiskSeverity.HIGH,
                message=f"License 为 {ev.license_name}（强 Copyleft），可能导致项目代码受 GPL/AGPL 传染条款约束。",
                data={"license": ev.license_name},
            ))

        # 4) STALE
        pushed = ev.pushed_at or ev.commits.last_commit_date
        days_since = (now - pushed).days if pushed else 9999
        if days_since >= self.STALE_DAYS and not ev.archived:
            sev = RiskSeverity.HIGH if days_since >= 2 * self.STALE_DAYS else RiskSeverity.MEDIUM
            risks.append(Risk(
                type=RiskType.STALE,
                severity=sev,
                message=f"最近一次代码推送距今 {days_since} 天，超过 STALE 阈值 {self.STALE_DAYS} 天。",
                data={"days_since_push": days_since, "threshold": self.STALE_DAYS},
            ))

        # 5) HIGH_ISSUE_LOAD
        if ev.issues.open_count >= self.HIGH_ISSUE_OPEN:
            sev = RiskSeverity.HIGH if ev.issues.open_count >= 2 * self.HIGH_ISSUE_OPEN else RiskSeverity.MEDIUM
            risks.append(Risk(
                type=RiskType.HIGH_ISSUE_LOAD,
                severity=sev,
                message=f"当前有 {ev.issues.open_count} 个未关闭 Issue，维护负载偏高。",
                data={"open_issues": ev.issues.open_count, "threshold": self.HIGH_ISSUE_OPEN},
            ))

        # 6) LOW_SCORE
        total = component.total_score
        if total < self.SCORE_DANGER:
            risks.append(Risk(
                type=RiskType.LOW_SCORE,
                severity=RiskSeverity.HIGH,
                message=f"综合评分 {total} 低于危险阈值 {self.SCORE_DANGER}，不建议直接使用。",
                data={"total_score": total, "threshold": self.SCORE_DANGER},
            ))
        elif total < self.SCORE_WARN:
            risks.append(Risk(
                type=RiskType.LOW_SCORE,
                severity=RiskSeverity.MEDIUM,
                message=f"综合评分 {total} 低于警告阈值 {self.SCORE_WARN}，请评估替代方案。",
                data={"total_score": total, "threshold": self.SCORE_WARN},
            ))

        # 7) FEW_CONTRIBUTORS
        if (
            ev.commits.contributors_90d > 0
            and ev.commits.contributors_90d <= self.FEW_CONTRIBUTORS
            and ev.stars > 200
        ):
            risks.append(Risk(
                type=RiskType.FEW_CONTRIBUTORS,
                severity=RiskSeverity.MEDIUM,
                message=f"近 90 天仅 {ev.commits.contributors_90d} 位贡献者提交代码，存在单一维护者风险。",
                data={"contributors_90d": ev.commits.contributors_90d,
                      "threshold": self.FEW_CONTRIBUTORS},
            ))

        # 8) OUTDATED_DEPENDENCIES
        if ev.dependencies:
            total_deps = len(ev.dependencies)
            outdated = sum(1 for d in ev.dependencies if d.outdated)
            if total_deps > 0 and outdated / total_deps > self.OUTDATED_DEPS_RATIO:
                risks.append(Risk(
                    type=RiskType.OUTDATED_DEPENDENCIES,
                    severity=RiskSeverity.MEDIUM,
                    message=f"依赖中 {outdated}/{total_deps} 不是最新版本，过期率 > {self.OUTDATED_DEPS_RATIO*100:.0f}%。",
                    data={"outdated": outdated, "total": total_deps},
                ))
        return risks


# ═══════════════════════════════════════════════════════════════════
#  Component Registry  (Facade)
# ═══════════════════════════════════════════════════════════════════

class ComponentRegistry:
    """C 层 Facade：接收 B 层采集的证据 → 注册为评分+风险的 Component。"""

    def __init__(
        self,
        scoring_engine: Optional[ScoringEngine] = None,
        risk_analyzer: Optional[RiskAnalyzer] = None,
    ) -> None:
        self.scoring = scoring_engine or ScoringEngine()
        self.risk = risk_analyzer or RiskAnalyzer()
        self._store: dict[str, Component] = {}

    def register(
        self,
        evidence: RepoEvidence,
        capability: Optional[CapabilityNeed] = None,
    ) -> Component:
        comp_id = f"{evidence.source}:{evidence.full_name.lower()}"
        score = self.scoring.score(evidence, capability)
        matched = self._matched_keywords(evidence, capability)
        comp = Component(
            id=comp_id,
            name=evidence.full_name,
            evidence=evidence,
            score=score,
            matched_keywords=matched,
            tags=list(evidence.topics),
        )
        comp.risks = self.risk.analyze(comp)
        self._store[comp_id] = comp
        return comp

    def register_many(
        self,
        evidences: list[RepoEvidence],
        capability: Optional[CapabilityNeed] = None,
    ) -> list[Component]:
        return [self.register(e, capability) for e in evidences]

    def get(self, comp_id: str) -> Optional[Component]:
        return self._store.get(comp_id)

    def all(self) -> list[Component]:
        return list(self._store.values())

    # ── Helper ────────────────────────────────────────────────

    @staticmethod
    def _matched_keywords(
        evidence: RepoEvidence,
        capability: Optional[CapabilityNeed],
    ) -> list[str]:
        if not capability or not capability.keywords:
            return []
        haystack = " ".join([
            evidence.full_name.lower(),
            (evidence.description or "").lower(),
            " ".join(t.lower() for t in evidence.topics),
        ])
        return [kw for kw in capability.keywords if kw.lower() in haystack]

"""
核心数据模型 (Internal Evidence Model)
=========================================

将 GitHub / PyPI / npm 等外部来源的异构数据统一映射成
Foundry 内部的证据模型，供评分引擎和风险分析消费。
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Optional, Any


# ──────────────────────────────────────────────
#  License
# ──────────────────────────────────────────────

class LicenseCategory(str, Enum):
    PERMISSIVE = "permissive"          # MIT / Apache-2.0 / BSD
    WEAK_COPYLEFT = "weak_copyleft"    # LGPL
    STRONG_COPYLEFT = "strong_copyleft"  # GPL / AGPL
    UNKNOWN = "unknown"
    PROPRIETARY = "proprietary"


PERMISSIVE_LICENSES = {
    "mit", "apache-2.0", "apache 2.0", "bsd-2-clause", "bsd-3-clause",
    "bsd", "isc", "cc0-1.0", "unlicense", "wtfpl", "mpl-2.0",
}
WEAK_COPYLEFT_LICENSES = {"lgpl-2.1", "lgpl-3.0", "lgpl"}
STRONG_COPYLEFT_LICENSES = {"gpl-2.0", "gpl-3.0", "agpl-3.0", "gpl", "agpl"}


def classify_license(license_name: Optional[str]) -> LicenseCategory:
    if not license_name:
        return LicenseCategory.UNKNOWN
    key = license_name.strip().lower().replace(" license", "")
    if key in PERMISSIVE_LICENSES:
        return LicenseCategory.PERMISSIVE
    if key in WEAK_COPYLEFT_LICENSES:
        return LicenseCategory.WEAK_COPYLEFT
    if key in STRONG_COPYLEFT_LICENSES:
        return LicenseCategory.STRONG_COPYLEFT
    if "commercial" in key or "proprietary" in key:
        return LicenseCategory.PROPRIETARY
    # 尝试关键词模糊匹配
    for kw in PERMISSIVE_LICENSES:
        if kw in key:
            return LicenseCategory.PERMISSIVE
    for kw in STRONG_COPYLEFT_LICENSES:
        if kw in key:
            return LicenseCategory.STRONG_COPYLEFT
    return LicenseCategory.UNKNOWN


# ──────────────────────────────────────────────
#  Requirement  (A 层输出)
# ──────────────────────────────────────────────

@dataclass
class CapabilityNeed:
    """拆解后的单条能力需求。"""
    name: str                               # e.g. "文本情感分析"
    keywords: list[str] = field(default_factory=list)   # 用于 B 层搜索
    language: Optional[str] = None          # e.g. "python"
    category: Optional[str] = None          # e.g. "nlp", "http-client"
    priority: int = 1                       # 1=must, 2=should, 3=nice-to-have
    description: str = ""


@dataclass
class Requirement:
    """A 层产物：用户需求 → 结构化能力需求集。"""
    raw_input: str                          # 用户原始输入
    summary: str = ""                       # 一句话摘要
    capabilities: list[CapabilityNeed] = field(default_factory=list)
    target_language: Optional[str] = None   # 全局语言倾向
    extra_constraints: dict[str, Any] = field(default_factory=dict)


# ──────────────────────────────────────────────
#  Evidence  (B 层采集 → C 层消费)
# ──────────────────────────────────────────────

@dataclass
class DependencyInfo:
    name: str
    current_version: Optional[str] = None
    latest_version: Optional[str] = None
    outdated: Optional[bool] = None
    severity: Optional[str] = None          # low / medium / high / critical


@dataclass
class IssueEvidence:
    open_count: int = 0
    closed_count: int = 0
    avg_days_open: float = 0.0
    recent_30d_opened: int = 0
    recent_30d_closed: int = 0
    bug_label_count: int = 0


@dataclass
class PREvidence:
    open_count: int = 0
    merged_30d: int = 0
    avg_days_to_merge: float = 0.0


@dataclass
class CommitEvidence:
    last_commit_date: Optional[datetime] = None
    commits_30d: int = 0
    commits_90d: int = 0
    contributors_90d: int = 0


@dataclass
class RepoEvidence:
    """统一的仓库证据快照。"""
    # 基础元数据
    source: str = "github"                  # github / gitlab / pypi / ...
    full_name: str = ""                      # sloria/TextBlob
    url: str = ""
    description: str = ""
    default_branch: str = "main"
    language: Optional[str] = None
    license_name: Optional[str] = None
    license_category: LicenseCategory = LicenseCategory.UNKNOWN

    # 流行度
    stars: int = 0
    forks: int = 0
    watchers: int = 0
    subscribers: int = 0

    # 维护信号
    created_at: Optional[datetime] = None
    pushed_at: Optional[datetime] = None
    archived: bool = False
    is_fork: bool = False
    homepage: Optional[str] = None
    has_wiki: bool = False
    has_pages: bool = False

    # 细粒度证据
    issues: IssueEvidence = field(default_factory=IssueEvidence)
    pull_requests: PREvidence = field(default_factory=PREvidence)
    commits: CommitEvidence = field(default_factory=CommitEvidence)
    dependencies: list[DependencyInfo] = field(default_factory=list)
    readme_size_bytes: int = 0
    topics: list[str] = field(default_factory=list)

    # 抓取时间戳
    snapshot_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return asdict(self)


# ──────────────────────────────────────────────
#  Score  (C 层输出)
# ──────────────────────────────────────────────

@dataclass
class ScoreBreakdown:
    """Component Intelligence Score — 8 个加权维度。"""
    relevance: float = 0.0          # 25%  与需求关键词的匹配度
    maintenance: float = 0.0        # 20%  近期提交、最后更新时间
    code_quality: float = 0.0       # 15%  代码规模、依赖健康、README等
    community: float = 0.0          # 10%  stars / forks / watchers
    issue_health: float = 0.0       # 10%  Issue 关闭率、响应速度
    pr_health: float = 0.0          #  5%  PR 合并速度、活跃度
    license: float = 0.0            # 10%  License 友好度
    dependency_health: float = 0.0  #  5%  依赖过期、漏洞

    @property
    def total(self) -> float:
        return round(
            self.relevance * 0.25
            + self.maintenance * 0.20
            + self.code_quality * 0.15
            + self.community * 0.10
            + self.issue_health * 0.10
            + self.pr_health * 0.05
            + self.license * 0.10
            + self.dependency_health * 0.05,
            1,
        )

    def as_dict(self) -> dict:
        return {
            "relevance": round(self.relevance, 1),
            "maintenance": round(self.maintenance, 1),
            "code_quality": round(self.code_quality, 1),
            "community": round(self.community, 1),
            "issue_health": round(self.issue_health, 1),
            "pr_health": round(self.pr_health, 1),
            "license": round(self.license, 1),
            "dependency_health": round(self.dependency_health, 1),
            "total": self.total,
        }


# ──────────────────────────────────────────────
#  Risk  (C 层风险分析)
# ──────────────────────────────────────────────

class RiskType(str, Enum):
    ARCHIVED = "ARCHIVED"                     # 仓库已归档
    UNKNOWN_LICENSE = "UNKNOWN_LICENSE"       # License 不明
    STALE = "STALE"                           # 长期无更新
    HIGH_ISSUE_LOAD = "HIGH_ISSUE_LOAD"       # 大量未解决 Issue
    LOW_SCORE = "LOW_SCORE"                   # 综合评分低于阈值
    STRONG_COPYLEFT = "STRONG_COPYLEFT"       # GPL/AGPL 传染风险
    FEW_CONTRIBUTORS = "FEW_CONTRIBUTORS"     # 单一维护者风险
    OUTDATED_DEPENDENCIES = "OUTDATED_DEPENDENCIES"


class RiskSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Risk:
    type: RiskType
    severity: RiskSeverity
    message: str
    data: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "type": self.type.value,
            "severity": self.severity.value,
            "message": self.message,
            "data": self.data,
        }


# ──────────────────────────────────────────────
#  Component  (C 层注册后的组件对象)
# ──────────────────────────────────────────────

@dataclass
class Component:
    """C 层产物：一个被评估的开源组件。"""
    id: str                                      # 内部 ID, e.g. "github:sloria/TextBlob"
    name: str
    evidence: RepoEvidence
    score: ScoreBreakdown = field(default_factory=ScoreBreakdown)
    risks: list[Risk] = field(default_factory=list)
    matched_keywords: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def total_score(self) -> float:
        return self.score.total

    @property
    def is_blocked(self) -> bool:
        """是否被风险阻塞（禁止进入 Assembly）。"""
        return any(
            r.severity == RiskSeverity.CRITICAL
            or r.type == RiskType.UNKNOWN_LICENSE
            or r.type == RiskType.ARCHIVED
            for r in self.risks
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "url": self.evidence.url,
            "description": self.evidence.description,
            "language": self.evidence.language,
            "license": self.evidence.license_name,
            "stars": self.evidence.stars,
            "score": self.score.as_dict(),
            "risks": [r.to_dict() for r in self.risks],
            "matched_keywords": self.matched_keywords,
            "blocked": self.is_blocked,
        }


# ──────────────────────────────────────────────
#  Assembly Decision  (D 层输出)
# ──────────────────────────────────────────────

@dataclass
class AssemblyDecision:
    """D 层产物：针对一条能力需求的组装决策。"""
    capability: CapabilityNeed
    primary: Optional[Component] = None
    alternatives: list[Component] = field(default_factory=list)   # 按评分降序
    why_primary: list[str] = field(default_factory=list)
    why_not_alternatives: dict[str, list[str]] = field(default_factory=dict)  # comp_id → 理由
    risks_of_primary: list[str] = field(default_factory=list)
    governance_actions: list[str] = field(default_factory=list)   # 需要 F 层介入的事项

    def to_dict(self) -> dict:
        return {
            "capability": {
                "name": self.capability.name,
                "keywords": self.capability.keywords,
                "language": self.capability.language,
                "priority": self.capability.priority,
            },
            "primary": self.primary.to_dict() if self.primary else None,
            "alternatives": [a.to_dict() for a in self.alternatives[:4]],
            "why_primary": self.why_primary,
            "why_not_alternatives": self.why_not_alternatives,
            "risks_of_primary": self.risks_of_primary,
            "governance_actions": self.governance_actions,
        }


@dataclass
class FoundryReport:
    """最终报告：一个需求 → 多条 AssemblyDecision。"""
    requirement: Requirement
    decisions: list[AssemblyDecision] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            "version": "0.9",
            "generated_at": self.generated_at.isoformat() + "Z",
            "requirement": {
                "raw": self.requirement.raw_input,
                "summary": self.requirement.summary,
                "capabilities": [c.name for c in self.requirement.capabilities],
            },
            "decisions": [d.to_dict() for d in self.decisions],
        }

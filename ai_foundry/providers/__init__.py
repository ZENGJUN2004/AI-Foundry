"""
Provider Abstraction Layer  (开源情报源抽象)
==============================================

核心思想：
    IntelligenceEngine ── OpenSourceProvider
                              ├─ GitHubProvider     ← 已实现
                              ├─ GitLabProvider     ← 预留接口
                              ├─ HuggingFaceProvider
                              ├─ PyPIProvider
                              └─ npmProvider

这样 Foundry 就不是 "GitHub Search Tool"，而是 "Open Source Intelligence Graph"。
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Optional

from ..models import RepoEvidence, CapabilityNeed

log = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
#  抽象基类
# ═══════════════════════════════════════════════════════════════════

class OpenSourceProvider(ABC):
    """所有开源情报源的通用接口。"""

    name: str = "base"

    # ── 搜索 ──────────────────────────────────────────────────

    @abstractmethod
    def search(
        self,
        keywords: list[str],
        language: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        """根据能力需求搜索候选仓库，返回候选元数据列表。

        每个候选至少包含: full_name, url, description, stars
        """
        ...

    # ── 拉取完整证据 ────────────────────────────────────────────

    @abstractmethod
    def fetch_evidence(self, full_name: str) -> Optional[RepoEvidence]:
        """拉取单个仓库的完整证据快照 (RepoEvidence)。

        失败 / 不存在 返回 None。
        """
        ...

    # ── 便捷：搜索 + 批量拉取 ───────────────────────────────────

    def search_and_fetch(
        self,
        capability: CapabilityNeed,
        limit: int = 10,
    ) -> list[RepoEvidence]:
        """对一条 CapabilityNeed 执行 search → 逐个 fetch_evidence。"""
        candidates = self.search(
            keywords=capability.keywords,
            language=capability.language,
            category=capability.category,
            limit=limit,
        )
        evidences: list[RepoEvidence] = []
        for c in candidates:
            full_name = c.get("full_name")
            if not full_name:
                continue
            ev = self.fetch_evidence(full_name)
            if ev:
                evidences.append(ev)
        return evidences

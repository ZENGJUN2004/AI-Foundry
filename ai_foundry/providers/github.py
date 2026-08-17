"""
GitHub Provider  —  真实 GitHub API + 离线 Mock 双通道
==========================================================

策略：
  1) 如果配置了 GITHUB_TOKEN 或 gh CLI 可用，调用真实 REST API
  2) 否则使用高质量离线数据集兜底，保证系统可在没有网络 / 凭证时完整演示

真实模式下，会尽可能把 GitHub 返回的数据映射到内部 RepoEvidence 证据模型：
    GET /search/repositories          →  candidates
    GET /repos/{owner}/{repo}         →  基础元数据
    GET /repos/{owner}/{repo}/issues  →  Issue 统计 (state=all)
    GET /repos/{owner}/{repo}/pulls   →  PR 统计
    GET /repos/{owner}/{repo}/commits →  最近 90 天提交活跃度
"""

from __future__ import annotations

import json
import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from ..models import (
    CommitEvidence,
    IssueEvidence,
    LicenseCategory,
    PREvidence,
    RepoEvidence,
    classify_license,
)
from . import OpenSourceProvider
from .github_mock_data import MOCK_REPOS, MOCK_EVIDENCE

log = logging.getLogger(__name__)

GITHUB_API = "https://api.github.com"
USER_AGENT = "AI-Foundry/0.9"


# ═══════════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════════

def _parse_dt(s: Optional[str]) -> Optional[datetime]:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def _http_get_json(url: str, token: Optional[str], timeout: int = 15) -> Optional[dict | list]:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
        return json.loads(raw.decode("utf-8"))
    except HTTPError as e:
        log.warning("GitHub HTTP %s on %s", e.code, url)
        return None
    except (URLError, TimeoutError, json.JSONDecodeError) as e:
        log.info("GitHub fetch failed (%s): %s", type(e).__name__, url)
        return None


def _is_online(token: Optional[str]) -> bool:
    """快速探测：能否访问 GitHub API。"""
    url = f"{GITHUB_API}/rate_limit"
    return _http_get_json(url, token, timeout=5) is not None


# ═══════════════════════════════════════════════════════════════════
#  GitHub Provider
# ═══════════════════════════════════════════════════════════════════

class GitHubProvider(OpenSourceProvider):
    name = "github"

    def __init__(self, token: Optional[str] = None, prefer_online: bool = True):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self._online: Optional[bool] = None
        self._prefer_online = prefer_online
        # 限流：每请求之间最小间隔 0.8s，避免打爆
        self._last_call_ts = 0.0

    # ── 在线检测 ──────────────────────────────────────────────

    def _check_online(self) -> bool:
        if self._online is not None:
            return self._online
        if not self._prefer_online:
            self._online = False
            log.info("GitHubProvider: offline mode (prefer_online=False)")
            return False
        self._online = _is_online(self.token)
        if self._online:
            log.info("GitHubProvider: online mode (connected)")
        else:
            log.info("GitHubProvider: falling back to offline dataset")
        return self._online

    def _throttle(self) -> None:
        dt = time.monotonic() - self._last_call_ts
        if dt < 0.8:
            time.sleep(0.8 - dt)
        self._last_call_ts = time.monotonic()

    # ── 搜索 ──────────────────────────────────────────────────

    def search(
        self,
        keywords: list[str],
        language: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 10,
    ) -> list[dict]:
        if not self._check_online():
            return self._offline_search(keywords, language, category, limit)

        query_parts: list[str] = list(keywords)
        if language:
            query_parts.append(f"language:{language}")
        query_parts.append("sort:stars-desc")
        q = quote(" ".join(query_parts))
        url = f"{GITHUB_API}/search/repositories?q={q}&per_page={limit}"
        self._throttle()
        data = _http_get_json(url, self.token)
        if not isinstance(data, dict):
            return self._offline_search(keywords, language, category, limit)
        items = data.get("items") or []
        results: list[dict] = []
        for it in items[:limit]:
            results.append({
                "full_name": it.get("full_name", ""),
                "url": it.get("html_url", ""),
                "description": it.get("description") or "",
                "stars": it.get("stargazers_count", 0),
                "language": it.get("language"),
            })
        return results

    # ── 拉取完整证据 ────────────────────────────────────────────

    def fetch_evidence(self, full_name: str) -> Optional[RepoEvidence]:
        if not self._check_online():
            return self._offline_fetch(full_name)

        self._throttle()
        repo = _http_get_json(f"{GITHUB_API}/repos/{full_name}", self.token)
        if not isinstance(repo, dict):
            log.info("repo not found online, try offline: %s", full_name)
            return self._offline_fetch(full_name)

        ev = self._repo_dict_to_evidence(repo)

        # 额外数据：Issue / PR / Commits
        ev.issues = self._fetch_issue_stats(full_name)
        ev.pull_requests = self._fetch_pr_stats(full_name)
        ev.commits = self._fetch_commit_stats(full_name)

        return ev

    # ── 在线 → 证据映射 ──────────────────────────────────────────

    @staticmethod
    def _repo_dict_to_evidence(repo: dict) -> RepoEvidence:
        lic = repo.get("license") or {}
        lic_name = lic.get("spdx_id") or lic.get("name") or repo.get("license")
        if isinstance(lic_name, str) and lic_name.lower() == "other":
            lic_name = lic.get("name") or None

        return RepoEvidence(
            source="github",
            full_name=repo.get("full_name", ""),
            url=repo.get("html_url", ""),
            description=repo.get("description") or "",
            default_branch=repo.get("default_branch") or "main",
            language=repo.get("language"),
            license_name=lic_name,
            license_category=classify_license(lic_name),
            stars=repo.get("stargazers_count", 0) or 0,
            forks=repo.get("forks_count", 0) or 0,
            watchers=repo.get("subscribers_count", 0) or 0,
            subscribers=repo.get("watchers_count", 0) or 0,
            created_at=_parse_dt(repo.get("created_at")),
            pushed_at=_parse_dt(repo.get("pushed_at")),
            archived=bool(repo.get("archived")),
            is_fork=bool(repo.get("fork")),
            homepage=repo.get("homepage") or None,
            has_wiki=bool(repo.get("has_wiki")),
            has_pages=bool(repo.get("has_pages")),
            topics=repo.get("topics") or [],
            readme_size_bytes=0,  # 单独接口获取，成本较高，先留空
        )

    def _fetch_issue_stats(self, full_name: str) -> IssueEvidence:
        """拉取 Issue 概览：状态=all，统计最近 30 天。"""
        stats = IssueEvidence()
        since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
        self._throttle()
        # 取最近 100 条 all-state issue 做统计估计
        data = _http_get_json(
            f"{GITHUB_API}/repos/{full_name}/issues?state=all&per_page=100"
            f"&sort=updated&since={quote(since)}",
            self.token,
        )
        if not isinstance(data, list):
            return stats
        open_list = [i for i in data if i.get("state") == "open" and "pull_request" not in i]
        closed_list = [i for i in data if i.get("state") == "closed" and "pull_request" not in i]
        stats.open_count = len(open_list)
        stats.closed_count = len(closed_list)
        stats.recent_30d_opened = sum(
            1 for i in open_list
            if _parse_dt(i.get("created_at"))
            and _parse_dt(i.get("created_at")) >= (datetime.now(timezone.utc) - timedelta(days=30))
        )
        stats.recent_30d_closed = len(closed_list)
        days = []
        now = datetime.now(timezone.utc)
        for i in open_list:
            created = _parse_dt(i.get("created_at"))
            if created:
                days.append((now - created).total_seconds() / 86400)
        stats.avg_days_open = round(sum(days) / len(days), 1) if days else 0.0
        stats.bug_label_count = sum(
            1 for i in (open_list + closed_list)
            if any("bug" in (lbl.get("name") or "").lower() for lbl in i.get("labels", []))
        )
        return stats

    def _fetch_pr_stats(self, full_name: str) -> PREvidence:
        stats = PREvidence()
        self._throttle()
        data = _http_get_json(
            f"{GITHUB_API}/repos/{full_name}/pulls?state=all&per_page=50&sort=updated",
            self.token,
        )
        if not isinstance(data, list):
            return stats
        open_list = [p for p in data if p.get("state") == "open"]
        stats.open_count = len(open_list)
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=30)
        merge_days = []
        for p in data:
            merged_at = _parse_dt(p.get("merged_at"))
            if merged_at and merged_at >= cutoff:
                stats.merged_30d += 1
                created = _parse_dt(p.get("created_at"))
                if created:
                    merge_days.append((merged_at - created).total_seconds() / 86400)
        stats.avg_days_to_merge = round(sum(merge_days) / len(merge_days), 1) if merge_days else 0.0
        return stats

    def _fetch_commit_stats(self, full_name: str) -> CommitEvidence:
        stats = CommitEvidence()
        self._throttle()
        since = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
        data = _http_get_json(
            f"{GITHUB_API}/repos/{full_name}/commits?per_page=100&since={quote(since)}",
            self.token,
        )
        if not isinstance(data, list):
            return stats
        cutoff_30 = datetime.now(timezone.utc) - timedelta(days=30)
        contributors_90: set[str] = set()
        for c in data:
            dt = _parse_dt((c.get("commit") or {}).get("committer", {}).get("date"))
            if not dt:
                continue
            if dt >= cutoff_30:
                stats.commits_30d += 1
            stats.commits_90d += 1
            author = c.get("author") or {}
            if author.get("login"):
                contributors_90.add(author["login"])
        if data:
            last = data[0]
            dt = _parse_dt((last.get("commit") or {}).get("committer", {}).get("date"))
            if dt:
                stats.last_commit_date = dt
        stats.contributors_90d = len(contributors_90)
        return stats

    # ── 离线兜底（使用 github_mock_data 数据集） ───────────────────

    def _offline_search(
        self,
        keywords: list[str],
        language: Optional[str],
        category: Optional[str],
        limit: int,
    ) -> list[dict]:
        kw_lower = [k.lower() for k in keywords if k]
        lang_lower = (language or "").lower()
        scored: list[tuple[int, dict]] = []
        for repo in MOCK_REPOS:
            # 1) 关键词匹配分 —— **这是入场券**：必须命中至少 1 个关键词才能入围
            #    （语言匹配只做锦上添花，不能仅凭语言匹配就拉进来）
            kw_score = 0
            haystack = " ".join([
                repo.get("full_name", ""),
                repo.get("description", ""),
                " ".join(repo.get("topics", [])),
            ]).lower()
            for kw in kw_lower:
                if kw in haystack:
                    kw_score += 3
                # 子串片段命中（对长词，取前半段做宽松匹配）给一点小分
                elif len(kw) >= 4:
                    kw_prefix = kw[: len(kw) // 2]
                    if any(kw_prefix in part for part in haystack.split()):
                        kw_score += 1

            # 如果定义了关键词，但一个都没命中 → 直接跳过
            if kw_lower and kw_score == 0:
                continue

            score = kw_score
            # 2) 语言匹配：锦上添花 +2
            if lang_lower and (repo.get("language") or "").lower() == lang_lower:
                score += 2

            scored.append((score, repo))
        scored.sort(key=lambda x: (x[0], x[1].get("stars", 0)), reverse=True)
        return [r for _, r in scored[:limit]]

    def _offline_fetch(self, full_name: str) -> Optional[RepoEvidence]:
        ev_dict = MOCK_EVIDENCE.get(full_name.lower())
        if ev_dict is None:
            return None
        return self._evidence_from_dict(ev_dict)

    @staticmethod
    def _evidence_from_dict(d: dict) -> RepoEvidence:
        """把 mock 字典反序列化成 RepoEvidence。"""
        return RepoEvidence(
            source=d.get("source", "github"),
            full_name=d.get("full_name", ""),
            url=d.get("url", ""),
            description=d.get("description", ""),
            default_branch=d.get("default_branch", "main"),
            language=d.get("language"),
            license_name=d.get("license_name"),
            license_category=LicenseCategory(d.get("license_category", "unknown")),
            stars=d.get("stars", 0),
            forks=d.get("forks", 0),
            watchers=d.get("watchers", 0),
            subscribers=d.get("subscribers", 0),
            created_at=_parse_dt(d.get("created_at")),
            pushed_at=_parse_dt(d.get("pushed_at")),
            archived=bool(d.get("archived", False)),
            is_fork=bool(d.get("is_fork", False)),
            homepage=d.get("homepage"),
            has_wiki=bool(d.get("has_wiki", False)),
            has_pages=bool(d.get("has_pages", False)),
            readme_size_bytes=d.get("readme_size_bytes", 0),
            topics=d.get("topics", []),
            issues=IssueEvidence(**(d.get("issues") or {})),
            pull_requests=PREvidence(**(d.get("pull_requests") or {})),
            commits=CommitEvidence(
                last_commit_date=_parse_dt((d.get("commits") or {}).get("last_commit_date")),
                commits_30d=(d.get("commits") or {}).get("commits_30d", 0),
                commits_90d=(d.get("commits") or {}).get("commits_90d", 0),
                contributors_90d=(d.get("commits") or {}).get("contributors_90d", 0),
            ),
            snapshot_at=datetime.now(timezone.utc),
        )

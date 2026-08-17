"""
AI Foundry v0.9 — Foundry Intelligence Layer
=============================================

Autonomous Software Component Decision Engine.

Layers:
    A  Requirement Intelligence   →  需求 → 能力需求
    B  Resource Scout             →  GitHub / Open Source 搜索
    C  Component Registry         →  证据 → 指标 → 综合评分 (Component Intelligence Score)
    D  Assembly Planner           →  最优组件 + 风险 + 替代方案
    E  Build                      →  构建占位
    F  Governance                 →  质量/安全/治理 占位
    G  Deploy                     →  部署占位

Architecture Upgrade:
    Provider-Abstraction: OpenSourceProvider → GitHubProvider / GitLabProvider / HuggingFaceProvider / PyPIProvider
"""

__version__ = "0.9.0"
__all__ = ["__version__"]

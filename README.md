<p align="center">
  <strong>AI Foundry v0.9</strong><br>
  Software Component Decision Engine —<br>
  Autonomous A(Req)→B(Scout)→C(Registry+Score+Risk)→D(Assembly)<br>
  open-source intelligence layer.
</p>

<p align="center">
  <em>新大众 AI · 人人都能成为开发者</em><br>
  <strong>Never Reinvent the Wheel.</strong><br>
  <strong>Build less. Reuse more. Create more.</strong><br>
  <sub>少造轮子 · 多用积木 · 创造更多</sub>
</p>

<p align="center">
  <a href="#features">Features</a> ·
  <a href="#install">Install</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#real-decision">Real Decision</a> ·
  <a href="#architecture">Architecture</a> ·
  <a href="#component-intelligence-score">Component Intelligence Score</a> ·
  <a href="#roadmap">Roadmap</a> ·
  <a href="#vision">Vision</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-%E2%89%A53.10-3776AB?logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  <img alt="Zero deps" src="https://img.shields.io/badge/Dependencies-0-0a7ea4">
  <img alt="Version" src="https://img.shields.io/badge/version-0.9.0-blueviolet">
  <img alt="Status" src="https://img.shields.io/badge/status-beta-green">
  <img alt="GitHub stars" src="https://img.shields.io/github/stars/ZENGJUN2004/AI-Foundry?style=social">
  <img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/ZENGJUN2004/AI-Foundry">
  <img alt="Repo URL" src="https://img.shields.io/badge/GitHub-ZENGJUN2004%2FAI--Foundry-181717?logo=github&logoColor=white&link=https%3A%2F%2Fgithub.com%2FZENGJUN2004%2FAI-Foundry">
</p>

---

## TL;DR

> Before you `pip install` the 5th github-search result for "python http client"
> just because it has the most stars — ask AI Foundry.
>
> It runs a full closed-loop decision in one command,
> weighs **8 scoring dimensions**, checks **8 risk types** across **4 severity tiers**,
> and gives you a Primary + 1–2 alternatives with a textual *why this / why not the rest* trace.
>
> **Zero third-party dependencies. Runs fully offline on a curated 30+ repo dataset.**

```bash
pip install -e "git+https://github.com/ZENGJUN2004/AI-Foundry.git#egg=ai-foundry"
ai-foundry run "Python async HTTP client library" --offline
```

---

<h2 id="vision">🌟 Vision — 新大众 AI</h2>

> **这是 AI Foundry 与今天绝大多数 AI 编程软件最大的不同。**
>
> 现在的 AI Coding，通常是在帮助你：**更快地写代码。**
> 而 AI Foundry 想做的，是让你：**尽可能少写代码。**
>
> 因为今天的开源生态中，世界上已经存在数以百万计的优秀软件、开源项目、模型、算法、框架和工具。
> **为什么要重新造一个轮子？**
>
> AI Foundry 的第一原则：**Never Reinvent the Wheel. 不重复造轮子。**
>
> 你提出一个需求，AI Foundry 首先不会急着写代码。它会先替你走遍全球开源生态：
> **寻找 → 筛选 → 比较 → 评估 → 组合**
> 分析每一个候选组件的 8 个维度：功能适配度、GitHub 活跃度、Issue/PR 状况、代码质量、依赖关系、开源许可证、社区规模、维护者健康度、安全与技术风险。
>
> 然后，从已经存在的"软件积木"中，找到最适合你的那一组。
>
> **先组装，再开发。** 这可能是 AI Foundry 与传统软件开发、乃至今天大多数 AI Coding 工具之间最重要的区别。
>
> | 模式 | 流程 |
> |---|---|
> | 传统方式 | 需求 → 设计 → 写代码 → 测试 → 部署 |
> | AI Coding | 需求 → AI 写代码 → 测试 → 修复 → 部署 |
> | **AI Foundry** | 需求 → **搜索全球已有能力 → 智能选材 → 积木式组装** → 个性化开发 → 自动测试 → 自主修复 → 安全治理 → 自动部署 |
>
> 能用现成的，就不重新开发；能组装的，就不重复编写；必须定制的，才进行个性化开发。
> AI Foundry 并不是让 AI"写更多代码"——恰恰相反：**让 AI 帮你写更少、但更有价值的代码。**
>
> ### 从"造轮子"走向"造汽车"
>
> 汽车不是从一块钢铁开始，每一个零件都重新发明。发动机、轮胎、芯片、传感器、导航系统……都是成熟的工业组件。真正高级的工程，不是重新发明每一个零件，而是：**找到最好的零件，并把它们组合成一辆更好的汽车。**
>
> GitHub、PyPI、npm、Hugging Face 以及整个全球开源生态，就是 AI Foundry 的"软件零部件世界"。AI Foundry 就像一座新的：**Software Foundry｜软件铸造厂**
>
> 它不要求每一个人都成为程序员。它让 AI 成为你的：软件架构师 + 开源侦察员 + 组件采购员 + 工程师 + 测试员 + 修复工程师 + 安全审查员 + 部署工程师。而你，只需要告诉它：*"我想做什么。"*
>
> ### 谁有资格创造软件
>
> AI Foundry 真正想改变的，不是软件开发方式，而是：**谁有资格创造软件。**
>
> 当过去只有专业程序员才能开发软件，而今天，一个文学研究者、教师、设计师、记者、学生、艺术家、企业家……都可以告诉 AI *"我有一个想法，我需要一个这样的工具"*，然后 AI 帮他：寻找 → 组装 → 开发 → 测试 → 修复 → 部署。那么 **"开发者"就不再只是一个职业身份，而开始成为一种人人可以拥有的创造能力。**
>
> ### 历史的演进
>
> - 个人电脑让：人人拥有**计算能力**。
> - 互联网让：人人拥有**连接世界的能力**。
> - Web 让：人人拥有**信息发布能力**。
> - 生成式 AI 让：人人拥有**内容生成能力**。
> - **AI Foundry 要进一步实现：人人拥有软件创造能力。**
>
> 这就是 **新大众 AI · 人人都能成为开发者**。
>
> 不重复造轮子。先利用世界已经创造出来的东西，再进行属于你的个性化创造。
> 让软件开发从"从零编码"，走向"智能组装"。让开发成本从"重复生产"，走向"复用 + 优化"。让软件从专业程序员的专属工具，变成每一个人的创造工具。
>
> **从一个想法，到一个成品。**
> **你负责想象。AI 负责工程。**
>
> ### AI Foundry — Build less. Reuse more. Create more.
> **少造轮子 · 多用积木 · 创造更多。**

> **📍 v0.9 status**: 实现了上述闭环的前 4 步（需求理解 → 全球搜索 → 组件评估 → 智能组装）。
> 后 6 步（个性化开发 / 自动测试 / 自主修复 / 安全治理 / 自动部署 / 持续监控）是 v1.0 Roadmap，详见 [Roadmap](#roadmap)。
> 我们诚实地标注进度，因为技术社区的信任比虚假的"已完工"更值钱。

---

<h2 id="features">✨ Why AI Foundry</h2>

| | Conventional tool-selection | **AI Foundry** |
|---|---|---|
| Signal | Star count + GitHub search ranking | **8-dim weighted Component Intelligence Score** normalised 0–100 |
| Risk awareness | Manual `LICENSE` tab reading | **8 risk types × 4 severity tiers**; CRITICAL risks automatically block a Primary |
| Process | Open 15 tabs, compare manually | **A→B→C→D closed loop** with a machine-readable JSON decision trace |
| Offline needs | Needs internet / GitHub API | **Built-in offline dataset** (30+ curated repos) — perfect for air-gapped CI |
| Install cost | Transitive dependency stack | **Zero runtime dependencies**, pure Python stdlib |
| Output | None / a starred tab | **Markdown / JSON / Text** reports for docs, chatbots or PR comments |

---

<h2 id="install">📦 Install</h2>

### Prerequisite

- **Python 3.10+** (3.10 / 3.11 / 3.12 / 3.13 / 3.14 all tested)
- No other runtime dependencies.

### Option A — from PyPI once published *(future)*
```bash
pip install ai-foundry
```

### Option B — from a GitHub clone *(today)*
```bash
git clone https://github.com/ZENGJUN2004/AI-Foundry.git ai-foundry
cd ai-foundry
pip install --no-build-isolation -e .
ai-foundry --version          # ai-foundry 0.9.0
```

### Option C — zero-install *(always works, even without pip)*
```bash
git clone https://github.com/ZENGJUN2004/AI-Foundry.git ai-foundry
cd ai-foundry
python -m ai_foundry --version
```

### Windows users
Double-click or run `ai-foundry.bat` from the repo root. It auto-corrects
the working directory and prepends the user-level `Scripts/` folder to `PATH`
when `pip install --user` has placed `ai-foundry.exe` off the global PATH.

---

<h2 id="quick-start">🚀 Quick Start</h2>

```bash
# 1. What capability categories does Layer-A understand?
ai-foundry list-caps

# 2. Single requirement — one full A→B→C→D pass
ai-foundry run "Python sentiment analysis library" --offline

# 3. Same, but machine-readable JSON and save to disk
ai-foundry run "Async HTTP client + CLI framework python" --offline \
  -f json -o decision.json

# 4. Six built-in demos (NLP / HTTP / CV / CLI / DB / Crypto)
ai-foundry demo --offline -f markdown -o demo-report.md

# 5. Online mode (requires GITHUB_TOKEN with public-repo scope)
export GITHUB_TOKEN=ghp_xxx
ai-foundry run "GO structured logging library" -f text
```

---

<h2 id="real-decision">🎬 Real Decision — what an AI Foundry run actually looks like</h2>

Below is the **unedited output** of one real run. The user typed:

```bash
ai-foundry run "我需要一个做情感分析、文本分词的Python库" --offline
```

AI Foundry's Layer A recognised this as a *文本分析/NLP* capability
requirement, Layer B pulled 7 candidate repos from the offline dataset,
Layer C scored them on 8 dimensions, Layer D picked the Primary and
explained — per scoring dimension — why each alternative lost.

### ✅ Primary：[sloria/TextBlob](https://github.com/sloria/TextBlob)  · `Score: 81.8`

> Simple, Pythonic text processing: sentiment, POS tagging, noun phrase extraction, translation.

| Dimension | Score |
|---|---:|
| relevance | 66.9 |
| maintenance | 86.7 |
| code_quality | 83.0 |
| community | 97.5 |
| issue_health | 89.9 |
| pr_health | 65.5 |
| license | 100.0 |
| dependency_health | 65.0 |
| **total** | **81.8** |

**🎯 为什么选它？**
- ✓ 综合评分 81.8 在候选集中排名第 1。
- ✓ License 许可协议 维度得分 100.0，表现突出。
- ✓ Community 社区规模 维度得分 97.5，表现突出。
- ✓ Issue Health 维度得分 89.9，表现突出。

**❌ 为什么不是 [explosion/spaCy](https://github.com/explosion/spaCy)？**（Score 81.6，排名第 2）
- × 总分比 Primary 低 0.2 分。
- × Issue Health 维度落后 10 分。

**❌ 为什么不是 [nltk/nltk](https://github.com/nltk/nltk)？**（Score 75.7，排名第 3）
- × 总分比 Primary 低 6.1 分。
- × Community 维度落后 24 分。
- × Issue Health 维度落后 17 分。

> **这是 AI Foundry 的核心承诺**：决策是可审计的（auditable），不是黑盒 LLM 的" vibes "。
> 每一个 ✓ 和 × 都对应 8 维评分里的具体得分差距，可以从 JSON 报告里逐条复核。

---

<h2 id="architecture">🏗️ Architecture — A→B→C→D closed loop</h2>

```
User requirement (NL)
        │
        ▼
 ┌──────────────┐       ┌──────────────────┐       ┌────────────────────────┐
 │  A  Req Intel │──────▶│  B  Resource Scout│──────▶│  C  Component Registry │
 │              │       │                  │       │                        │
 │ 10 capability│       │ OpenSourceProv.  │       │  ScoringEngine  (8-dim)│
 │ categories   │       │   GitHubProv.    │       │  RiskAnalyzer   (8×4)  │
 │ keyword+lang │       │   · offline data │       │  Registry (dedup/merge)│
 └──────────────┘       │   · REST (online)│       └───────────┬────────────┘
                        └──────────────────┘                   │
                                                               ▼
                                                  ┌────────────────────────┐
                                                  │  D  Assembly Planner   │
                                                  │                        │
                                                  │ 1 Primary + 1–2 Alts   │
                                                  │ "Why this / why-not"   │
                                                  │ textual decision trace │
                                                  └───────────┬────────────┘
                                                              ▼
                                         FoundryReport (text|json|markdown)
```

### Layer A — Requirement Intelligence
Splits a free-form NL query into one or more typed **CapabilityRequirements**
(currently 10 categories: NLP, HTTP client, CV, CLI framework, DB/ORM,
visualisation, logging, ML framework, testing, crypto/security).

### Layer B — Resource Scout
Searches heterogeneous source via the `OpenSourceProvider` abstract base class.
The concrete `GitHubProvider` ships with **two channels**:

| Channel | Data source | Use when |
|---|---|---|
| **Offline** *(default with `--offline`)* | Curated 30+ repo dataset embedded in the wheel | Sandboxes, CI, air-gapped, demos, reproducibility |
| **Online** | `api.github.com/search/repositories` (urllib, stdlib) | Real-time freshness, larger candidate set |

### Layer C — Component Registry
Normalises every candidate into the internal `Component` evidence model,
runs the 8-dim **Component Intelligence Score** (see below), then the
**RiskAnalyzer** flags CRITICAL/HIGH/MEDIUM/LOW issues. `ARCHIVED`,
`UNKNOWN_LICENSE` and any other CRITICAL risk **disqualify a Primary
selection**; they still appear as Alts with the block reason clearly stated.

### Layer D — Assembly Planner
For each capability requirement produces:

- **1 Primary** — highest-score risk-clean component.
- **1–2 Alternatives** — strong runners-up.
- **Why this / why-not list** — human-readable prose comparing the Primary
  to every alternative on every scoring dimension where a meaningful gap
  exists.

---

<h2 id="component-intelligence-score">📊 Component Intelligence Score (0–100)</h2>

Weighted 8-dimension scoring. Weights have been tuned so that "relevance to
the requirement" and "maintenance continuity" dominate the total, while
ecosystem and supply-chain signals act as strong tiebreakers.

| Dimension | Weight | What it measures |
|---|---:|---|
| **Relevance** | 25% | Keyword / description / topic match vs. the specific CapabilityRequirement |
| **Maintenance** | 20% | Last commit age, release cadence, owner activity |
| **Code Quality** | 15% | Open / total issue ratio, stale PR ratio, code-scan proxies |
| **Community** | 10% | Stargazer slope, contributor count, fork diversity |
| **Issue Health** | 10% | Open-issue load, median age of open bugs, response ratio |
| **PR Health** | 5% | Merge ratio, stale-PR rate, turnaround |
| **License** | 10% | SPDX classification (permissive > weak copyleft > strong copyleft > unknown) |
| **Dependency Health** | 5% | Declared dependencies, pinned majors, last-update lag |

**Rule of thumb:** scores ≥ 85 → strong Primary material. 65–84 → fine Alt.
< 65 or any CRITICAL flag → never selected as Primary.

### Risk taxonomy (8 types × 4 severity tiers)

| Type | Trigger (simplified) | Auto-block Primary when… |
|---|---|---|
| `ARCHIVED` | `repo.archived = true` | Always |
| `UNKNOWN_LICENSE` | `license.spdx = NOASSERTION` | Always |
| `STALE` | Last commit older than 24 months | Always |
| `HIGH_ISSUE_LOAD` | Open issue density > threshold | If it also crushes Issue Health dim below 40 |
| `LOW_SCORE` | Overall score < 65 | Always (disqualification threshold) |
| `STRONG_COPYLEFT` | AGPL-3.0 / SSPL / GPL | Never auto-blocks, but shows warning |
| `FEW_CONTRIBUTORS` | Solo maintainer + low bus-factor | Paired with `STALE` → escalates to CRITICAL |
| `OUTDATED_DEPENDENCIES` | Major-lagging pinned deps | Escalates via Dependency Health gate |

Severity tiers: **CRITICAL · HIGH · MEDIUM · LOW**.

---

## 🔌 Output formats

| `-f` value | Snippet of what you get |
|---|---|
| `text` *(default)* | ANSI-friendly sectioned report with ✓ / × bullets for the "why" trace |
| `json` | Full `FoundryReport` schema: `requirements_used`, `searches[]`, `components_in_registry[]`, `decisions[{primary, alternatives, why_primary, why_not_each_alt}]`, `summary_totals`, `elapsed_ms` |
| `markdown` | Heading-structured Markdown, safe to paste into GitHub PR comments, Notion docs, or LLM chat |

Pipe any of them through `-o report.<ext>`; `-` writes to stdout.

---

## 🧪 Health check (post-deploy)

A deployment is only complete when all three of these return exit code `0`:

```bash
ai-foundry --version                                          # H1: version string
ai-foundry list-caps                                          # H2: 10 categories printed
ai-foundry run "deploy health test nlp python" --offline      # H3: Primary = TextBlob exit 0
```

---

<h2 id="roadmap">🗺️ Roadmap</h2>

| Layer | v0.9 (today) | v0.10 | v1.0 |
|---|---|---|---|
| **A** | 10 capability categories, keyword + lang heuristics | LLM-backed Requirement decomposition | Multi-lang queries + domain taxonomies |
| **B** | GitHubProvider (offline + REST) | GitLabProvider, PyPIProvider | HuggingFaceProvider, crates.io, npm |
| **C** | 8-dim scoring + 8-type risk | SBOM + CPE / CVE integration (OSV.dev) | Supply-chain graph + transitive risk propagation |
| **D** | 1 Primary + 1–2 Alts, textual trace | Auto-generate `requirements.txt` snippet | Conflict resolution across multi-package assemblies |
| **E Build** | Placeholder | Hatch / PDM skeletons | Full scaffold + first test run |
| **F Governance** | Placeholder | Weekly score drift email | Policy engine (allowed licenses, score floors) |
| **G Deploy** | Placeholder | Dockerfile + GitHub Actions job | Publish-to-package-repo gate |

Feature requests welcome as GitHub issues — please include the output of
`ai-foundry --version` and your failing query.

---

## 🛟 Common pitfalls

| Symptom | Fix |
|---|---|
| `ai-foundry: command not found` after `pip install -e .` | Use the **absolute path** pip prints in its "Scripts is not on PATH" warning, or run `python -m ai_foundry`, or use `ai-foundry.bat` on Windows. |
| `setlocal recursion limit` (old `.bat`) | Re-pull — current launcher uses explicit `.exe` extension + PATH prepend. |
| Only Python results for a JS query | Fixed in v0.9: keyword match is a hard gate; language preference is now a tiebreaker bonus, not a sole filter. |
| Write error on `outputs/` in a sandbox | Pass an absolute writable path, e.g. `-o /tmp/decision.md`; folders are auto-created. |
| I claimed "deployed" but H1/H2/H3 are red | Always run and paste the three health checks above. Never claim success without them. |

---

## 🧑‍🤝‍🧑 Contributing

```bash
pip install -e ".[dev,online]"
ruff check ai_foundry
# TODO: unit-tests for ScoringEngine / RiskAnalyzer / Layer A keyword matrix
```

PRs that **add a new OpenSourceProvider** or that ship a **high-quality offline
dataset** (e.g. 20+ well-tagged repos for a currently under-covered language /
domain) are especially warmly reviewed.

---

## 📄 License

MIT © AI Foundry Team. See [LICENSE](LICENSE).

The offline dataset (`ai_foundry/providers/github_mock_data.py`) contains only
public, freely observable metadata about open-source repositories (description,
star count, last commit date, SPDX license id, issue counts, etc.) and does
not redistribute source code or copyrighted assets from the respective
upstreams. If you are a maintainer of a project listed there and would prefer
to be excluded, please open an issue.

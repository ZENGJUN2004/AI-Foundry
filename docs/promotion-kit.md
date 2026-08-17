# AI Foundry — Promotion Kit

> This file is a complete, copy-paste-ready promotion kit for AI Foundry v0.9.
> All URLs have been verified to point to the real GitHub repo:
> **https://github.com/ZENGJUN2004/AI-Foundry**
>
> Use any block below verbatim — they are designed to be posted as-is to
> WeChat Moments / V2EX / Juejin / Zhihu / X / Reddit / Hacker News.

---

## 0. Brand Narrative — 新大众 AI

> **这是 AI Foundry 的品牌叙事。它是所有推广文案的精神内核。**
> **任何长文投放（知乎/掘金/Medium/HN）开头都建议先放这一段，建立情绪锚点。**

```
AI Foundry
人人都能成为开发者
新大众 AI

你不需要从零开始学习如何造轮子。
世界上已经有数以百万计的开源项目、模型、框架和工具。

AI Foundry 做的事情，是替你去寻找它们、理解它们、比较它们、组合它们，并把它们变成属于你的工具。

你负责提出想法。
AI 负责完成工程。

从一句自然语言需求开始：
"我想要一个能够分析文学文本的工具。"

AI Foundry 自动完成：
需求理解 → 全球搜索 → 组件评估 → 智能组装 → 自动编程 → 测试 → 修复 → 安全治理 → 部署 → 监控。

你看到的，不再是一堆代码。
而是一个 真正可以使用的软件。

所以，AI Foundry 想改变的，不只是软件开发方式。
它想改变的是：
谁有资格创造软件。

当过去只有程序员才能开发软件，
而今天任何人都可以借助 AI 定义、构建和部署自己的工具时，
"开发者"就不再是一个职业身份，而开始成为一种人人可以拥有的创造能力。

这就是：
新大众 AI
人人都能成为开发者。
人人都可以创造自己的工具。

从一个想法，到一个成品。

AI Foundry —— Build less. Create more.
```

### 🎯 品牌叙事里的「诚实」

在对外投放上述广告词时，请同时记住：**v0.9 已实现前 4 步，后 6 步是 Roadmap**。

| 广告词中的步骤 | v0.9 状态 | v1.0 目标 |
|---|---|---|
| 需求理解 | ✅ 已实现（Layer A，10 类能力） | LLM 增强 + 多语言 |
| 全球搜索 | ✅ 已实现（Layer B，GitHub 离线+在线） | GitLab/PyPI/npm/crates |
| 组件评估 | ✅ 已实现（Layer C，8 维评分 + 8 风险） | OSV.dev CVE 集成 |
| 智能组装 | ✅ 已实现（Layer D，Primary + Alts + 决策链） | 多包冲突解决 |
| 自动编程 | 🚧 占位（Layer E） | Hatch/PDM scaffold |
| 测试 | 🚧 占位（Layer E） | 自动 pytest 生成 |
| 修复 | 🚧 占位（Layer E/F） | LLM 修复循环 |
| 安全治理 | 🚧 占位（Layer F） | Policy 引擎 + 周报 |
| 部署 | 🚧 占位（Layer G） | Dockerfile + GH Actions |
| 监控 | 🚧 占位（Layer G） | 上线后漂移监控 |

广告词里的"完整闭环"是 v1.0 的愿景；v0.9 是这条路上的第一个公开里程碑，已经能独立交付价值。**在长文里诚实标注这一点，比假装"已经全做完"更能赢得技术社区的信任**。

---

## 1. Repo Quick Facts（所有平台通用前置信息）

| 字段 | 值（直接复制） |
|---|---|
| 仓库 URL | https://github.com/ZENGJUN2004/AI-Foundry |
| 仓库短链（用于字数受限平台） | https://github.com/ZENGJUN2004/AI-Foundry |
| 一句话定位 | Autonomous A→B→C→D decision engine that picks your next OSS library. Zero deps · offline by default · pure Python stdlib. |
| License | MIT |
| 语言 | Python 3.10+（也支持 3.11 / 3.12 / 3.13 / 3.14） |
| 依赖数 | 0（纯标准库） |
| 30s 试用 | `pip install --no-build-isolation -e git+https://github.com/ZENGJUN2004/AI-Foundry.git` 然后 `ai-foundry demo --offline` |
| Issues 入口 | https://github.com/ZENGJUN2004/AI-Foundry/issues |
| Discussions 入口 | https://github.com/ZENGJUN2004/AI-Foundry/discussions |
| 仓库所有者 | ZENGJUN2004 |
| 当前版本 | v0.9.0 |

---

## 2. Stage 1 — Cold Start (0 → 200 stars, Week 1)

**Goal**: Escape the 0-star / 0-content "zombie repo" trap. The first
real visitor must immediately believe "this works".

### 2.1 Tasks

1. **README hero with real demo output** — already embedded in repo README.
2. **Topics on the repo** — set in GitHub → Settings → About → Topics:
   `python`, `cli`, `developer-tools`, `supply-chain`,
   `open-source-intelligence`, `decision-engine`, `software-analysis`,
   `component-scoring`, `github-search`, `zero-dependencies`.
3. **GitHub Community Standards green** — LICENSE ✓, README ✓,
   CONTRIBUTING ✓, CODE_OF_CONDUCT ✓, Issue Templates (next batch).
4. **Release v0.9.0** — tag pushed; Release Notes in §5 below.
5. **Personal circle first** — post §3.1 (WeChat Moments / Feishu group)
   to get first 10-20 real stars before algorithmic cold-start.

### 2.2 Copy — WeChat Moments / Feishu group / Twitter (CN)

```
最近花了一段时间把「选型一个 Python/Go/JS 开源库」这个高频动作做成了一个可复用的 CLI：

AI Foundry v0.9 — 输入自然语言需求，自动跑 A(需求拆解)→B(仓库搜索)→C(8 维评分 + 风险识别)→D(最优+备选+决策解释) 的完整闭环。

零第三方依赖，纯 Python 标准库，离线也能用（内置 30+ 精心标注的仓库数据集，沙箱/CI 可直接跑）。

今天刚开源 MIT：
https://github.com/ZENGJUN2004/AI-Foundry

我们的愿景是「新大众 AI」——人人都能成为开发者。你负责提出想法，AI 负责完成工程。

求 star、欢迎提 issue：你平时选型最纠结的那个库是什么？我先让 AI Foundry 跑一次给你看结果。😉
```

### 2.3 Copy — V2EX「分享创造」节点 / 知乎 / 掘金

**标题**：分享创造：我做了一个开源组件选型 CLI——AI Foundry v0.9，零依赖，离线可用

**正文**：

```
# 分享创造：我做了一个开源组件选型 CLI——AI Foundry v0.9，零依赖，离线可用

## 先说痛点

我每次在 GitHub 搜索"python http client"，star 榜第一、文档好、许可友好、还在维护的不一定是同一个项目。打开十几个 tab 横向比较太烦。

更烦的是，"还在不在维护"这种关键信息常常要到 README 最底部、或者 Issues 列表第三页才能看出来——而那时候我已经花掉半小时了。

## 所以我做了 AI Foundry

一个 A→B→C→D 的开源情报决策引擎：

- **A 层** 把自然语言需求拆成 10 类能力需求（NLP/HTTP/CV/CLI/DB/可视化/日志/ML/测试/加解密）；
- **B 层** 通过 `OpenSourceProvider` 抽象走 GitHub，离线数据集兜底 30+ 仓库；
- **C 层** 8 维加权评分（相关性 25%·维护度 20%·代码质量 15%·社区 10%·Issue Health 10%·PR Health 5%·许可 10%·依赖健康 5%），加 8 类 4 级风险，ARCHIVED / UNKNOWN_LICENSE / 24 个月未提交 直接被 BLOCK；
- **D 层** 输出 1 个 Primary + 1–2 个 Alt，带完整"为什么选这个、为什么不选那些"的文本决策链。

## 三个特点我觉得挺重要的

1. 纯标准库，`pip install -e .` 就能用；
2. 默认 `--offline` 安全、可复现；设 GITHUB_TOKEN 就切到真实 API；
3. 输出 JSON / Markdown / Text 三种，报告可以直接贴到 PR comments 或 Notion。

## 更大的愿景：新大众 AI

我们做的不是"又一个 GitHub 搜索工具"。我们想做的是：

> 你负责提出想法。AI 负责完成工程。
> 从一个想法，到一个成品。
> AI Foundry —— Build less. Create more.

v0.9 实现了闭环的前 4 步（需求理解→搜索→评估→组装），v1.0 目标是把自动编程 / 测试 / 修复 / 治理 / 部署 / 监控 也接上。让"人人都能成为开发者"真正成立。

## 仓库 / 试用

仓库：https://github.com/ZENGJUN2004/AI-Foundry
30 秒试用：
  pip install --no-build-isolation -e git+https://github.com/ZENGJUN2004/AI-Foundry.git
  ai-foundry demo --offline

欢迎任何反馈，尤其是「你给我一个真实需求，我跑它的决策结果贴回来」。🙏
```

### 2.4 Copy — Hacker News (Show HN) / Reddit r/programming

**Title**: Show HN: AI Foundry – Zero-dep CLI that picks OSS libraries via an 8-dim score + risk audit

**Body**:

```
Hi HN,

Every time I search GitHub for "best python async http client" I end up with 15 tabs open, manually cross-referencing stars, last commit, open issue ratio, license, and whether the project is archived. I got tired of it and built a decision engine that does the full closed loop in one command.

**AI Foundry v0.9** runs:
  A (Requirement Intel: 10 capability categories) →
  B (Resource Scout: GitHub provider with an offline 30+ repo dataset **and** a live REST channel) →
  C (Registry: 8-dim weighted Component Intelligence Score, normalized 0–100; 8-type × 4-tier risk analyzer; CRITICAL risks auto-block a Primary) →
  D (Assembly Planner: 1 Primary + 1–2 alternatives, with a textual "why this / why not the rest" trace per scoring-dimension gap).

Details I care about:
- **Zero runtime dependencies.** Pure Python stdlib, 3.10–3.14.
- **Offline by default.** Works in air-gapped CI, reproducible demos.
- **No black-box LLMs in the v0.9 loop** — the decision trace is pure heuristics + weighted scoring, fully auditable from the JSON report.

Repo: https://github.com/ZENGJUN2004/AI-Foundry
Try it in 30s:
  `pip install --no-build-isolation -e git+https://github.com/ZENGJUN2004/AI-Foundry.git`
  `ai-foundry demo --offline`

The bigger vision is what we call "新大众 AI" (the New Popular AI): a world where anyone can assemble software from the open-source commons. v0.9 ships the first 4 steps of that loop (requirement → search → score → assemble). The v1.0 roadmap adds auto-coding, testing, governance, deploy and monitoring layers.

Feedback & pull requests extremely welcome — especially new `OpenSourceProvider`s (GitLab, PyPI, crates.io, npm).

(Posted because I couldn't find another OSS tool that combined scoring + risk + textual decision trace. Cheers.)
```

### 2.5 Copy — X (Twitter) thread

**Tweet 1** (with the ASCII architecture diagram or a screenshot of a real decision):

```
Tired of 15 open GitHub tabs just to pick a Python HTTP client?

I built AI Foundry v0.9 🛠️ — a zero-dep CLI that runs A→B→C→D:
• A. Requirement Intel (10 capability cats)
• B. Resource Scout (offline 30+ repo dataset + REST)
• C. 8-dim weighted score + 8-type risk audit w/ CRITICAL gates
• D. 1 Primary + Alts + "why this / why-not" trace

Pure Python stdlib · MIT · offline by default
https://github.com/ZENGJUN2004/AI-Foundry

#Python #OpenSource #DevTools #SupplyChain
```

**Tweet 2** (follow-up, with a screenshot of `ai-foundry demo --offline`):

```
Real run: AI Foundry picked sloria/TextBlob for sentiment analysis.

Here's the exact "why primary / why-not-the-rest" output — every ✓ and × ties back to one of the 8 scoring dimensions, no black-box LLM in the loop.

That's the whole point: an auditable decision, not a vibe. 🧮
```

**Tweet 3** (vision, 2-4 hours later):

```
The bigger vision behind AI Foundry is what we call "新大众 AI":

> You handle the idea. AI handles the engineering.

v0.9 ships steps 1-4 (requirement → search → score → assemble).
v1.0 adds auto-coding, testing, governance, deploy, monitoring.

Build less. Create more. 🌱
```

---

## 3. Stage 2 — Content-Driven (200 → 2k stars, Weeks 2-4)

**Goal**: Turn the tool into a content asset. Every real-world selection
becomes a viral post.

### 3.1 Weekly cadence

| Day | Action |
|---|---|
| **Mon** | Pick a controversial selection (requests vs httpx vs aiohttp; pytest vs unittest; Typer vs Click; numpy vs pandas vs polars) |
| **Tue** | Run `ai-foundry run "..." --offline -f markdown -o case-studies/<week>-<topic>.md` |
| **Wed** | Write a 3-min comparison post from the Markdown report |
| **Thu** | Post to Reddit / HN / Juejin with "I ran an 8-dim scoring tool on this, results were counter-intuitive" framing |
| **Fri** | Update README's `## Case studies this week` section |

### 3.2 Amplifiers

- **Supply-chain-security creators** — their audience eats "8-dim scoring + risk identification + ARCHIVED BLOCK" narrative. One repost = 500 stars.
- **Awesome List PRs** — send a one-line PR to each of:
  - `awesome-python`
  - `awesome-python-applications`
  - `awesome-developer-tools`
  - `awesome-cli-apps`
  - `awesome-supply-chain`
  
  Suggested entry:
  ```
  - [AI Foundry](https://github.com/ZENGJUN2004/AI-Foundry) — Zero-dependency CLI that picks OSS libraries via 8-dim score + 8-type risk audit + textual decision trace.
  ```
- **GitHub Actions workflow** — add `.github/workflows/demo.yml` that runs `ai-foundry demo --offline` weekly and uploads the Markdown as an Artifact. The green check + pipeline signal boosts visitor trust.

---

## 4. Stage 3 — Community-isation (2k → 10k stars, Months 2-6)

**Goal**: Turn "your project" into "everyone's project". Make users
write Providers and datasets for you.

### 4.1 Provider Bounty

Open a GitHub issue titled **"Provider Bounty: ship GitLabProvider / PyPIProvider / npmProvider / cratesProvider, get listed in CONTRIBUTORS + a sticker"**. First contributor of each gets:

- Public thanks in next Release Notes
- Name in README `## Contributors` section
- A physical sticker / mug mailed (small cost, strong emotional lock-in)

### 4.2 Discussions

Open GitHub Discussions → create an "Ideas" poll: **"Which ecosystem do you most want AI Foundry to support?"** with options: GitLab, PyPI, npm, crates.io, HuggingFace, RubyGems, Packagist.

### 4.3 v0.10 Roadmap Issue (pin it)

Open an issue titled **"Roadmap to v0.10"**, pin it, list:
- OSV.dev CVE integration (Layer C)
- SBOM export (Layer C)
- LLM-enhanced Layer A requirement decomposition
- At least one new Provider (community-contributed)

### 4.4 Product Hunt Launch

Once you have 1k+ stars and 3+ language Providers, schedule a
Tuesday 00:01 PST launch. Suggested tagline:

> AI Foundry — the autonomous 8-dim decision engine that picks your next OSS library before you open 15 tabs.

Find a hunter with a Top-5 track record on Twitter (search "PH hunter").
The first 4 hours determine the whole trajectory — get your Stage-1
friends to upvote in that window.

---

## 5. Release v0.9.0 Notes (paste into GitHub Releases UI)

```
# AI Foundry v0.9.0 — First Open Source Release

## 🎯 TL;DR

AI Foundry is an autonomous decision engine that picks the best open-source library for a natural-language requirement. Zero runtime dependencies. Runs offline by default.

    ai-foundry run "Python async HTTP client" --offline

## ✨ What's in v0.9.0

### A→B→C→D closed loop

- **Layer A — Requirement Intelligence**: splits NL query into 1-N typed CapabilityRequirements (10 categories: NLP, HTTP, CV, CLI, DB, Visualization, Logging, ML, Testing, Crypto).
- **Layer B — Resource Scout**: `OpenSourceProvider` abstract base + concrete `GitHubProvider` with dual channel:
  - Offline: 30+ curated repos embedded in the wheel (reproducible, sandbox-safe).
  - Online: `api.github.com/search/repositories` via stdlib `urllib`, activated by `GITHUB_TOKEN` env var.
- **Layer C — Component Registry**:
  - `ScoringEngine` — 8-dim weighted Component Intelligence Score (Relevance 25%, Maintenance 20%, Code Quality 15%, Community 10%, Issue Health 10%, PR Health 5%, License 10%, Dependency Health 5%), normalized to 0-100.
  - `RiskAnalyzer` — 8 risk types × 4 severity tiers. ARCHIVED / UNKNOWN_LICENSE / STALE / LOW_SCORE auto-block Primary selection.
- **Layer D — Assembly Planner**: 1 Primary + 1-2 Alternatives per requirement, with a textual "why this / why-not-the-rest" decision trace per scoring-dimension gap.

### Packaging & deployment

- `pyproject.toml` with `console_scripts` entry → `pip install -e .` gives you `ai-foundry` globally.
- `ai-foundry.bat` Windows launcher — auto-corrects working directory and prepends user Scripts to PATH.
- Zero third-party runtime dependencies. Python 3.10 / 3.11 / 3.12 / 3.13 / 3.14 all supported.

### Output formats

- `text` (default): ANSI-friendly sectioned report with ✓ / × bullets for the decision trace.
- `json`: full FoundryReport schema (`requirements_used`, `searches`, `components_in_registry`, `decisions`, `summary_totals`, `elapsed_ms`).
- `markdown`: heading-structured Markdown, safe to paste into GitHub PR comments / Notion / chat.

### Community files

- MIT LICENSE
- README with architecture diagram, 8-dim score table, risk taxonomy, install, quick start, health checks, roadmap.
- CONTRIBUTING.md + CODE_OF_CONDUCT.md (Contributor Covenant 2.1).
- Python-standard .gitignore (outputs/, .env, .trae/, secrets all excluded).

## 🧪 Health check (post-deploy)

    ai-foundry --version                                          # H1: ai-foundry 0.9.0
    ai-foundry list-caps                                          # H2: 10 categories
    ai-foundry run "deploy health test nlp python" --offline      # H3: Primary = TextBlob, exit 0

## 🗺️ Roadmap (v0.10 → v1.0)

| Layer | v0.9 (today) | v0.10 | v1.0 |
|---|---|---|---|
| A Requirement Intel | 10 categories, keyword + lang | LLM-backed decomposition | Multi-lang + domain taxonomies |
| B Resource Scout | GitHubProvider (offline + REST) | GitLabProvider, PyPIProvider | HuggingFace, crates.io, npm |
| C Registry | 8-dim score + 8-type risk | SBOM + OSV.dev CVE | Supply-chain graph + transitive risk |
| D Assembly | 1 Primary + 1-2 Alts | Auto-generate requirements.txt | Multi-package conflict resolution |
| E Build | Placeholder | Hatch / PDM skeletons | Full scaffold + first test run |
| F Governance | Placeholder | Weekly score drift email | Policy engine (allowed licenses, score floors) |
| G Deploy | Placeholder | Dockerfile + GitHub Actions job | Publish-to-package-repo gate |

## 💬 Feedback

- Bugs & feature requests: https://github.com/ZENGJUN2004/AI-Foundry/issues
- Open-ended design discussions: https://github.com/ZENGJUN2004/AI-Foundry/discussions

## 🙏 Vision

> 你负责提出想法。AI 负责完成工程。
> 从一个想法，到一个成品。
> AI Foundry —— Build less. Create more.
```

---

## 6. Quick verification commands (for promoters / reviewers)

Anyone who wants to verify AI Foundry works before posting about it:

```bash
git clone https://github.com/ZENGJUN2004/AI-Foundry.git
cd AI-Foundry
pip install --no-build-isolation -e .
ai-foundry --version          # expect: ai-foundry 0.9.0
ai-foundry list-caps          # expect: 10 capability categories
ai-foundry demo --offline     # expect: 6 scenarios, all exit 0
```

If any of those fail, open an issue at
https://github.com/ZENGJUN2004/AI-Foundry/issues with the full command
output — we treat reproducibility bugs as P0.

---

## 7. Visual assets (to be produced)

| Asset | Where it goes | How to produce |
|---|---|---|
| ASCII architecture diagram | README (already embedded) | already in repo |
| Real decision screenshot | README hero, Tweet 1 | screenshot of `ai-foundry run "Python sentiment analysis library" --offline` |
| 6-scenario demo bundle | Release Notes attachment | `ai-foundry demo --offline -f markdown -o demo.md`, attach to GitHub Release |
| "Why Primary / why-not" detail shot | Tweet 2 | screenshot of the ✓ / × decision trace section |
| 30-sec terminal recording | README hero, Product Hunt | `asciinema rec` → upload to asciinema.org → embed |

---

## 8. Who to ping when you post

After you post on any platform, drop a line in GitHub Discussions under
"Show & Tell" with the platform + link. We (and future contributors)
will come star / upvote / comment within the first hour — that's the
window that determines whether the platform's algorithm picks it up.

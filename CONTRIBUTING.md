# Contributing to AI Foundry

First of all — thank you for considering a contribution. AI Foundry is
built on the belief that *anyone* should be able to assemble software
from the open-source commons, so every improvement you make directly
advances that mission.

> **The one-sentence version**: open an issue first, run
> `ai-foundry --version` and `ai-foundry run "..." --offline` to confirm
> the bug reproduces, then send a PR with the fix and the new/updated
> demo output pasted into the PR description.

---

## ✅ What we especially welcome

| Type of contribution | Why it matters | Examples |
|---|---|---|
| **New `OpenSourceProvider`** | Layer B is only as useful as the sources it can search | `GitLabProvider`, `PyPIProvider`, `npmProvider`, `cratesProvider`, `HuggingFaceProvider` |
| **High-quality offline datasets** | Offline mode is what makes AI Foundry reproducible in sandboxes/CI | 20+ well-tagged repos for an under-covered language or domain |
| **Layer A capability categories** | v0.9 ships 10; real-world usage will surface more | `data-validation`, `task-queue`, `configuration`, `secrets-management` |
| **Risk analyzer rules** | The 8-type taxonomy is intentionally minimal; real supply-chain risks are more nuanced | `CVE_EXPOSED`, `SINGLE_MAINTAINER_BUS_FACTOR`, `LICENSE_CONFLICT_TRANSITIVE` |
| **Scoring dimension calibration** | The 8 weights are tuned by hand; empirical calibration is welcome | A reproduction script comparing AI Foundry's Primary vs. expert choice on 50 known selections |
| **Case studies** | Each real-world "AI Foundry decided X over Y" is worth 1000 stars of cold advertising | `case-studies/2026-W33-http-clients.md` |
| **Translations of the README** | "新大众 AI" means *everyone* — non-English speakers first | `README.zh-CN.md`, `README.es.md`, `README.ja.md` |

---

## 🧑‍💻 Local development setup

```bash
git clone https://github.com/ZENGJUN2004/AI-Foundry.git
cd AI-Foundry
pip install --no-build-isolation -e ".[dev,online]"
```

This gives you:

- `ai-foundry` console script (editable, changes to `ai_foundry/*.py` take effect immediately)
- `pytest` + `ruff` for dev
- `PyGithub` for the optional online channel

### Before you push

```bash
ruff check ai_foundry
# (tests are still being added — if you touch ScoringEngine / RiskAnalyzer,
#  please also add a focused pytest case)
python -m ai_foundry --version         # sanity
python -m ai_foundry list-caps         # Layer A still intact
python -m ai_foundry run "contrib sanity check nlp python" --offline  # full loop
```

All three must return exit code `0`. If any of them breaks, the CI we
will add in v0.10 will reject the PR anyway — better to catch it locally.

---

## 🧭 How we make decisions

AI Foundry follows a lightweight *layered consent* model:

1. **Bug fixes** — PR directly, maintainer reviews within 48h.
2. **New providers / new risk types / new scoring dimensions** — open an
   issue with the word `Design:` in the title first. We'll align on the
   public surface (class signature, data model, risk enum value) before
   you write 500 lines that have to be reshaped.
3. **Changes to existing weights or risk severity** — open an issue with
   `Calibration:` in the title, and ideally attach a 10-case comparison
   showing your new weights produce better Primaries than the current
   ones.

We do not require a CLA, but we do require that every commit message
follows the existing style: a short imperative subject line, blank line,
then a body explaining the *why*. Look at `git log --oneline` for the
house style.

---

## 🧪 Tests (the honest status)

There are **no committed unit tests yet** — this is intentional for the
v0.9 open-source release, because we did not want to ship a test suite
that gives false confidence. The most valuable tests to contribute right
now are:

- `tests/test_scoring_engine.py` — golden scores for the 30+ repos in
  `github_mock_data.py` (these numbers should be stable across releases).
- `tests/test_risk_analyzer.py` — ARCHIVED / UNKNOWN_LICENSE / STALE
  blocking behaviour, one assertion per risk type.
- `tests/test_layer_a_keyword_matrix.py` — the 10 capability categories
  and their trigger keywords; regression-test that adding a keyword
  doesn't reclassify an unrelated category.

If you write any of these, we will publicly thank you in the next
Release Notes.

---

## 📜 Code of Conduct

Participation in this project is governed by the
[Contributor Covenant 2.1](CODE_OF_CONDUCT.md). Please read it before
your first interaction. The short version: be kind, be concrete, be
accountable — "新大众 AI" only works if the community is safe for the
newcomers we are trying to welcome.

---

## 🏷️ Licensing of your contribution

All contributions are submitted under the project's
[MIT license](LICENSE). If you contribute a file that was originally
authored elsewhere (e.g. a curated dataset of repo metadata from a
third-party source), please note the original source in the file header
and confirm the upstream license permits redistribution.

---

## 💬 Where to talk

- **Bugs & feature requests**: [GitHub Issues](https://github.com/ZENGJUN2004/AI-Foundry/issues)
- **Open-ended design discussions**: [GitHub Discussions](https://github.com/ZENGJUN2004/AI-Foundry/discussions)
- **Off-platform** (only if you need to reach the maintainer privately):
  open an issue with `Private:` in the title first, we'll move the
  sensitive part to email.

Thank you for helping build the "新大众 AI" — a world where *anyone*
can create software.

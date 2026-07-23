# Agentic AI & Skills Sistemi (Akademik & Kodlama Şablonu)

Claude Code ve Antigravity IDE ortamlarında çalışan hiyerarşik çok-ajanlı sistem, MCP (Model Context Protocol) sunucuları ve akademik + kodlama/RL skills kütüphanesi.

---

## 🏛️ Ajan Hiyerarşisi ve Çalışma Prensipleri

Sistemimiz iki temel katmanda çalışır:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏛️ TASARIM & İŞLEVSELLİK KATMANI (PLAN-FIRST — KULLANICI ONAYI ZORUNLU)    │
│                                                                             │
│  • @architect  (Opus/Fable-5)   → Mimari karar, ADR'ler, FORMULATION.md, MCP │
│  • @module-planner (Sonnet)     → Domain-aware (RL/Sim/ML) spec tasarımları │
│  • @paper-writer (Sonnet)       → Akademik yazı taslağı & LaTeX outlineleri │
│                                                                             │
│  👉 Kural: Tasarım ve işlevsellik kullanıcıya sunulur.                      │
│     Siz "onaylıyorum / uygula" demediğiniz sürece spec ve dosya yazılmaz.  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │  (Sizin Onayınız)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚙️ UYGULAMA & TEST KATMANI (OTONOM VE HIZLI İCRA)                          │
│                                                                             │
│  • @worker-coder (Haiku)        → Spec'e uygun kod yazımı & PyTest           │
│  • @unit-tester (Sonnet)       → 3x TIER 2 retry & otonom test debug        │
│  • @integration-verifier (Sonnet) → Modüller arası otonom entegrasyon      │
│  • @experiment-runner (Sonnet)  → Arka planda 5-seed RL eğitimi koşturma    │
│                                                                             │
│  👉 Kural: Onaylı spec dahilinde unit testler, retry'lar ve kod içi         │
│     düzeltmeler sizi bekletmeden OTONOM yürütülür.                         │
│     (İşlevsellik/spec değişecekse FREN basar ve size sorar).                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Yeni Bir Projede Nasıl Kullanacaksınız?

Bu sistemi **Antigravity IDE** ve **Claude Code CLI** ortamlarında zahmetsizce kullanabilirsiniz:

### 🌟 Yöntem A: Antigravity IDE İle Kullanım (Sıfır Çaba — Tam Otomatik)
Özelleştirmeler bilgisayarınızda **Global** olarak (`C:\Users\Erdemhan\.gemini\config\`) kurulu olduğu için:
1. **İstediğiniz yeni bir klasör açın** ve Antigravity IDE'yi başlatın.
2. Sohbet penceresine doğrudan fikrinizi anlatın veya kısayol etiketi kullanın:
   > *"Yeni bir RL / Simülasyon projesi başlatmak istiyorum. Projemin amacı: [Fikrinizi yazın]"*  
   > *(Veya doğrudan: `@architect yeni proje tasarlayalım`)*
3. **Arka Planda Ne Olur?**
   - Global 39 Skill ve anayasa otomatik yüklenir.
   - Projenizde varsayılan `.gitignore` ve kilitli `FORMULATION.md` dosyası oluşturulur.
   - `codebase-memory` MCP sunucusu projeyi otomatik indeksler.

---

### 💻 Yöntem B: Claude Code CLI İle Kullanım (Şablon Klonlama)
1. **Repository'yi Yeni Klasörünüze Kopyalayın:**
   ```bash
   git clone https://github.com/Erdemhan/Experimental-Skills.git yeni-projem
   cd yeni-projem
   ```
2. **Kendi Git Repository'nizi Bağlayın:**
   ```bash
   # Windows PowerShell'de eski .git klasörünü temizleyin:
   Remove-Item -Path .git -Recurse -Force
   git init
   ```
3. **Claude Code'da Başlatın:**
   ```bash
   claude
   ```
   Sohbette: *"Yeni projemizi mimari olarak tasarlayalım."*

---

### 💡 `@tag` Kullanmak Zorunlu mu? (Esnek Kullanım)
- **HAYIR, ZORUNLU DEĞİLDİR!** `@architect`, `@worker-coder` gibi etiketler sadece isterseniz kullanabileceğiniz kısayollardır.
- Ne yapmak istediğinizi **Türkçe doğal dilinizle anlatmanız yeterlidir.** Sistem arka planda doğru ajanı ve skill'i otomatik tespit edip çalıştırır:
  - *"Sıfırdan mimari tasarlayalım"* ──► Otomatik `@architect` devrededir.
  - *"Şu koddaki hatayı bulup çözelim"* ──► Otomatik `@worker-coder`, `@unit-tester` ve `research-debug` devrededir.
  - *"Deneyleri 5 seed ile koşturalım"* ──► Otomatik `@experiment-runner` ve `empirical-rigor` devrededir.
  - *"Sonuçlardan LaTeX makale üret"* ──► Otomatik `@paper-writer` ve `latex-bibtex-manager` devrededir.

---

## 📐 FORMULATION.md (Akademik Formülasyon Kütüğü)

Akademik projelerde matematiksel denklemler, semboller, teorik açıklamalar ve hiperparametre kaynakları `.claude/context/FORMULATION.md` dosyasında tutulur:
- ⚠️ **Kullanıcı Kilitli (User-Locked)**: Kullanıcı açık onay vermeden HİÇBİR AJAN tarafından bu dosyadaki formüller veya parametreler değiştirilemez.
- Koddaki bir fonksiyon veya `yaml` config bu kütükle çelişirse, koddaki hata düzeltilir; `FORMULATION.md` dosyasına dokunulmaz.

---

## 🔌 Entegre MCP Sunucuları (Model Context Protocol)

`.claude/settings.json` içerisinde 4 güçlü MCP sunucusu konfigüre edilmiştir:

| MCP Server | İşlev | Kullanan Ajanlar |
|---|---|---|
| `codebase-memory` | AST Kod Bağımlılık Grafiği, Mimari Arama | `@architect`, `@module-planner`, `@worker-coder` |
| `memory` | Knowledge Graph (Deney & Hipotez Hafızası) | `@context-manager`, `@experiment-runner` |
| `sequential-thinking` | Adım Adım Mantıksal Algoritma Düşünme | `@architect`, `@module-planner` |
| `fetch` | ArXiv & Web Doküman/Paper Çekme | `@architect`, `@paper-writer` |

---

## 📚 Detailed Skills Library Guide (39 Skills)

### 1. 🎓 Academic Research & Methodology Skills (11 Skills)

| Skill | Trigger | Detailed Description |
|---|---|---|
| **`academic-integrity`** | Citation, claim, reference | Guarantees all factual claims have verified sources. Prevents hallucinated citations, enforcing DOI/Scholar verification protocols. |
| **`empirical-rigor`** | Experiment design, benchmark | Enforces minimum 5 random seeds, hyperparameter freezing, and reproducibility standards for empirical experiments. |
| **`fair-comparison`** | Method baseline evaluation | Guarantees equal computational budget (steps/GPUs) and equal tuning effort between proposed methods and baselines. |
| **`bias-audit`** | Dataset/analysis audit | Detects selection bias, evaluation bias, data leakage, and selective metric reporting risks. |
| **`statistical-validity`** | Numerical result interpretation | Computes 95% Confidence Intervals (CI), Welch's t-test p-values, and Cohen's d effect sizes for statistical rigor. |
| **`literature-review`** | Alanyazın / Literature review | Summarizes related research across methodology, dataset, and performance axes; identifies research gaps. |
| **`hypothesis-framing`** | Research Question design | Formulates falsifiable Research Questions (RQs) and hypotheses (H1/H0). |
| **`paper-structure`** | Academic writing outline | Organizes paper section structure (Abstract, Intro, Method, Experiments) and logical argument flow. |
| **`latex-bibtex-manager`** | LaTeX template, BibTeX | Compiles NeurIPS/ICML/IEEE/ACM LaTeX templates, cleans duplicate BibTeX keys, and resolves `latexmk` errors. |
| **`dataset-documentation`** | Dataset card | Produces *Datasheets for Datasets* documentation detailing data collection, annotation, and usage limits. |
| **`replication-package`** | Work sharing | Generates single-command `reproduce_all.py` scripts and full environment packaging for Zenodo/GitHub publication. |

---

### 2. 🤖 Reinforcement Learning & Simulation Skills (6 Skills)

| Skill | Trigger | Detailed Description |
|---|---|---|
| **`rl-environment-design`** | Gymnasium / RL environment | Designs Gymnasium/PettingZoo compliant observation/action spaces, `reset()`, `step()`, and reward bounds. |
| **`rl-reward-shaping`** | Reward function, hacking | Implements potential-based reward shaping ($\Phi(s)$); prevents reward hacking and perverse agent incentives. |
| **`rl-experiment-tracking`** | RL experiment tracking | Monitors multi-seed training curves, evaluation episode metrics, and model checkpoints. |
| **`rl-paper-implementation`** | Paper → RL Code | Converts published RL paper pseudocode into executable PyTorch code, logging all implementation deviations. |
| **`simulation-experiment-design`** | Simulation experiment | Designs time-step ($dt$) integration, state update loops, and parameter sweep grids for physical/agent-based simulations. |
| **`ray-rllib`** | Ray & RLlib distributed | Sets up Ray Tune and RLlib for multi-GPU / multi-core cluster distributed RL training and hyperparameter search. |

---

### 3. 🌉 Academic & Coding Bridge Skills (6 Skills)

| Skill | Trigger | Detailed Description |
|---|---|---|
| **`research-debug`** | Academic debugging | Classifies bugs by academic impact (Type A: Isolated, Type B: Result-altering, Type C: Methodology-breaking) before fixing. |
| **`paper-to-reproducible-code`** | Paper table ↔ Code audit | Performs 1-to-1 parameter audits between published paper tables/`FORMULATION.md` and codebase `configs/*.yaml`. |
| **`result-analysis-pipeline`** | Log → Stats → Figure | Parses raw logs, computes statistical tests, plots colorblind-friendly PDF figures, and exports TeX table fragments. |
| **`academic-code-release`** | Code release with paper | Prepares clean READMEs, Zenodo DOIs, and standalone reproduction scripts for code release alongside papers. |
| **`wandb-mlflow-api`** | WandB / MLflow API | Programmatically queries and fetches run metrics from Weights & Biases or MLflow cloud servers into Pandas DataFrames. |
| **`git-research`** | Academic Git workflow | Manages academic commit types (`exp:`, `data:`, `result:`) and `paper/` branching models while excluding large model weights. |

---

### 4. 💻 Software Engineering & Coding Skills (16 Skills)

| Skill | Trigger | Detailed Description |
|---|---|---|
| **`code-architect`** | New project / refactor | Designs modular, layered, clean-dependency software architectures and component interfaces. |
| **`function-spec-writer`** | Function spec design | Generates detailed `FunctionSpec` JSON files containing signatures, type hints, Google-style docstrings, and test cases. |
| **`unit-test-design`** | Unit test writing | Writes comprehensive PyTest suites covering boundary values, exceptions, and test fixtures. |
| **`debug-tracer`** | Software debugging | Applies hypothesis-driven debugging loops (Observation → Hypothesis → Test → Fix) and git bisect. |
| **`ml-experiment`** | ML experiment setup | Sets up standard ML train/val/test data splits, cross-validation, and pipeline evaluation loops. |
| **`pytorch-training`** | PyTorch training loop | Optimizes PyTorch GPU memory usage, mixed precision (AMP), gradient clipping, and checkpoint saving. |
| **`performance-profiler`** | Performance optimization | Profiles CPU/GPU code bottlenecks using cProfile, PyTorch Profiler, and memory-profiler. |
| **`api-design`** | API creation | Designs RESTful API endpoints, OpenAPI schemas, and Pydantic data validation models. |
| **`security-review`** | Security audit | Audits subprocess injections, Ray cluster port exposures, control APIs, and unsafe model pickle loading. |
| **`refactor-safe`** | Safe refactoring | Cleans and restructures code without breaking test coverage or observable behavior via atomic commits. |
| **`code-review`** | Code review | Reviews code readability, performance, type safety, and architectural compliance. |
| **`dependency-audit`** | Package audit | Scans `requirements.txt` / `pyproject.toml` dependencies for known security vulnerabilities (CVEs). |
| **`data-pipeline`** | Data pipeline design | Constructs data loading, cleaning, transformation, and preprocessing pipelines (ETL). |
| **`git-engineering`** | General Git workflow | Manages feature branches, conventional commits, interactive rebasing, and git bisect debugging. |
| **`documentation-writer`** | Code documentation | Writes Google-style docstrings and Sphinx/MkDocs compatible documentation suites. |
| **`ci-cd-design`** | Automation setup | Constructs GitHub Actions CI/CD workflows for automated PyTest runs and code quality enforcement. |

---

## 🛠️ Klasör Yapısı

```
skills/
├── CLAUDE.md                     ← Proje Anayasası (Kurallar & Hiyerarşi)
├── README.md                     ← Bu dosya
├── .agents/                      ← Antigravity IDE Yerel Konfigürasyonu
│   ├── AGENTS.md                 ← Antigravity IDE Anayasası
│   └── skills/                   ← 39 Skill Tanımı
├── .claude/
│   ├── settings.json             ← Lifecycle Hooks & MCP Server Ayarları
│   ├── agents/                   ← 8 Ajan Tanımı (Architect, Planner, Coder vb.)
│   ├── skills/                   ← 39 Skill Tanımı (Akademik & Kodlama)
│   ├── hooks/                    ← Hook Scriptleri (sync_skills, security_gate vb.)
│   ├── context/                  ← Oturum Belleği (ARCHITECTURE.md, context.db, FORMULATION.md)
│   └── templates/                ← Proje Şablonları (.gitignore, FORMULATION.md, git-hooks)
```

---

## 📜 Lisans
MIT License

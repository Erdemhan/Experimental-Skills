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
   - Global 43 Skill ve anayasa otomatik yüklenir.
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

## 🛠️ Mevcut Bir Projeye Nasıl Entegre Edeceksiniz?

Devam eden, kod yazılmış **mevcut bir projenize** bu sistemi entegre etmek son derece güvenlidir:

### 🌟 Antigravity IDE İle Mevcut Proje Entegrasyonu (Sıfır Çaba)
1. **Mevcut projenizin klasörünü Antigravity IDE ile açın.**
2. Sohbet penceresine yazın:
   > *"Mevcut projemizin mimarisini ve kod yapısını inceleyip geliştirmeye devam edelim."*  
   > *(Veya: `@architect mevcut projeyi analiz edelim`)*
3. **Sistem Ne Yapar?**
   - Global 43 Skill ve anayasa anında aktifleşir.
   - `codebase-memory` MCP sunucusu mevcut kod bağımlılıklarını ve AST yapısını haritalandırır (`index_repository`).
   - `@architect` mevcut kod yapısını bozmadan mimari haritayı (`ARCHITECTURE.md`) çıkarır ve onayınızla yeni özellikleri planlar.

---

### 💻 Claude Code CLI İle Mevcut Proje Entegrasyonu
1. **Şablon Konfigürasyonlarını Mevcut Projenize Kopyalayın:**
   ```powershell
   # Mevcut projenizin klasöründeyken PowerShell ile:
   Copy-Item -Path "path\to\skills\.claude" -Destination "." -Recurse -Force
   Copy-Item -Path "path\to\skills\CLAUDE.md" -Destination "." -Force
   ```
2. **Senkronizasyonu Çalıştırın:**
   ```powershell
   python .claude/hooks/sync_skills.py
   ```
3. **Claude Code'u Başlatın:**
   ```bash
   claude
   ```

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

## 📚 Detaylı Skills Kütüphanesi Rehberi (43 Skill)

### 1. 🎓 Akademik Araştırma & Metodoloji Skill'leri (11 Skill)

| Skill | Tetikleyici | Detaylı Açıklama |
|---|---|---|
| **`academic-integrity`** | Atıf, referans, iddia | Her bilimsel iddianın kaynağa dayalı olmasını sağlar. Doğrulanmamış veya uydurma atıfları engeller, DOI ve Google Scholar doğrulama protokolü uygular. |
| **`empirical-rigor`** | Deney tasarımı, benchmark | Akademik deneylerde en az 5 rastgele seed (tohum) zorunluluğu, hiperparametre sabitleme ve tekrarlanabilirlik standartları koyar. |
| **`fair-comparison`** | Yöntem karşılaştırması | Kendi yönteminiz ile baseline yöntemler arasında eşit hesaplama bütçesi (GPU/Step) ve adil değerlendirme şartlarını garanti eder. |
| **`bias-audit`** | Veri/analiz değerlendirme | Veri setindeki seçim yanlılığı (selection bias), overfitting ve seçici metrik raporlama risklerini tespit edip raporlar. |
| **`statistical-validity`** | Sayısal sonuç yorumu | Deney sonuçları için %95 Güven Aralığı (CI), Welch's t-testi ile p-değeri ve Cohen's d etki büyüklüğünü hesaplar. |
| **`literature-review`** | Alanyazın tarama | İlgili akademik çalışmaları metodoloji, veri seti ve performans ekseninde özetler; araştırma boşluğunu (gap) belirler. |
| **`hypothesis-framing`** | Araştırma sorusu tasarımı | Araştırma Sorusu (RQ) ve doğrulanabilir/yanlışlanabilir Hipotez (H1/H0) formatı oluşturur. |
| **`paper-structure`** | Akademik yazı üretimi | Makalenin bölüm mantığını (Abstract, Intro, Method, Experiments, Discussion) ve mantıksal argüman akışını düzenler. |
| **`latex-bibtex-manager`** | LaTeX şablonu, BibTeX | NeurIPS, ICML, ICLR, IEEE ve ACM LaTeX şablonlarını derler; BibTeX mükerrer atıflarını temizler ve `latexmk` hatalarını çözümler. |
| **`dataset-documentation`** | Veri seti kartı | *Datasheets for Datasets* standardında veri toplama, etiketleme ve kullanım kısıtlarını içeren belge hazırlar. |
| **`replication-package`** | Çalışma paylaşımı | Zenodo ve GitHub için tek komutluk `reproduce_all.py` scripti ve bağımlılıklarla tam tekrarlanabilirlik paketi oluşturur. |

---

### 2. 🤖 Reinforcement Learning & Simülasyon Skill'leri (8 Skill)

| Skill | Tetikleyici | Detaylı Açıklama |
|---|---|---|
| **`rl-environment-design`** | Gymnasium / RL ortamı | Gymnasium/PettingZoo uyumlu observation/action space, `reset()`, `step()`, `render()` ve reward aralıklarını tasarlar. |
| **`rl-reward-shaping`** | Ödül fonksiyonu, hacking | Potential-based reward shaping ($\Phi(s)$) kurar; ajanın sırtüstü sürüklenme gibi reward hacking yapmasını ve ters teşvikleri engeller. |
| **`rl-marl-design`** | Çok-Ajanlı RL (MARL) | PettingZoo uyumlu Çok-Ajanlı RL (CTDE, MAPPO, QMIX, IPPO) ortam ve algoritma mimarisi tasarlar. |
| **`rl-offline-dataset`** | Offline RL, D4RL | İnteraktif olmayan sabit veri setlerinden Offline RL eğitimi (CQL, IQL, D4RL formatı) ve Out-Of-Distribution denetimi yürütür. |
| **`rl-experiment-tracking`** | RL deney takibi, multi-seed | Multi-seed eğitim eğrilerini, evaluation episode metriklerini ve model checkpoint'lerini izler. |
| **`rl-paper-implementation`** | Makale → RL Kod | Yayınlanmış bir RL algoritmasını koda aktarırken pseudocode ile koddaki tüm sapmaları (deviations log) belgeler. |
| **`simulation-experiment-design`** | Simülasyon deneyi | Fiziksel ve ajan bazlı simülasyonların zaman adımı ($dt$), entegrasyon yöntemi (Euler/RK4) ve parametre tarama planını yapar. |
| **`ray-rllib`** | Ray & RLlib dağıtık | Ray Tune ve RLlib ile çok-GPU / çok-çekirdekli küme üzerinde dağıtık RL eğitimi ve hiperparametre arama kurar. |

---

### 3. 🌉 Akademik & Kodlama Köprü Skill'leri (6 Skill)

| Skill | Tetikleyici | Detaylı Açıklama |
|---|---|---|
| **`research-debug`** | Akademik hata ayıklama | Araştırma kodundaki hatanın metrikleri etkileyip etkilemediğini (Tip A: İzole, Tip B: Sonuç değiştiren, Tip C: Metodoloji bozucu) analiz eder; Tip B/C hatalarda git tag ve re-run planı çıkarır. |
| **`paper-to-reproducible-code`** | Makale tablosu ↔ Kod | Makaledeki Tablo 1/2 hiperparametreleri ve `FORMULATION.md` ile koddaki `configs/*.yaml` dosyaları arasında 1-e-1 parametre denetimi yapar. |
| **`result-analysis-pipeline`** | Log → İstatistik → Figür | Ham logları yükler, istatistiksel testleri hesaplar, renk körü dostu PDF figürler çizer ve yayın kalitesinde LaTeX tablosu üretir. |
| **`academic-code-release`** | Paper ile kod yayınlama | Kodu makale ile birlikte sunmak için temiz README, Zenodo DOI ve bağımsız makinede sınama kontrollerini yürütür. |
| **`wandb-mlflow-api`** | WandB / MLflow API | Weights & Biases veya MLflow bulut servislerinden koşu verilerini ve metrikleri programatik olarak Pandas DataFrame'e çeker. |
| **`git-research`** | Akademik Git yönetimi | Akademik projelerdeki `exp:`, `data:`, `result:` commit tiplerini ve `paper/` dallanma (branching) modelini yönetir. |

---

### 4. 💻 Yazılım Mühendisliği & Optimizasyon Skill'leri (18 Skill)

| Skill | Tetikleyici | Detaylı Açıklama |
|---|---|---|
| **`token-budget-optimizer`** | Token optimizasyonu, minimal context | Alt ajan context izolasyonu (Subagent context isolation), log budama (log pruning) ve AST parçalı kod okuma ile %70 token tasarrufu sağlar. |
| **`self-consistency-verifier`** | Hakem kontrolü, self-correction | Kod üreten ajan ile sınayan ajanı ayırarak bağımsız hakem kontrolü (Critique loop) ve sınır-değer (edge-case) denetimi yapar. |
| **`code-architect`** | Yeni proje / refactor | Modüler, katmanlı, bağımlılıkları temiz ve ölçeklenebilir yazılım mimarileri tasarlar. |
| **`function-spec-writer`** | Fonksiyon tasarımı | Fonksiyon imzası, type hints, Google-style docstring, edge case ve test case içeren `FunctionSpec` JSON üretir. |
| **`unit-test-design`** | Unit test yazımı | PyTest ile sınır değerler (boundary values), istisnalar (exceptions) ve fixture'lar içeren birim testler yazar. |
| **`debug-tracer`** | Hata ayıklama (yazılım) | Hipotez odaklı debug döngüsü (Gözlem → Hipotez → Test → Düzeltme) ve git bisect uygular. |
| **`ml-experiment`** | ML deneyi kurulumu | Standart ML modelleri için train/val/test veri ayrımı, cross-validation ve pipeline kurulumu yapar. |
| **`pytorch-training`** | PyTorch eğitim döngüsü | PyTorch GPU bellek optimizasyonu, mixed precision (AMP), gradient clipping ve checkpoint kaydetme düzenler. |
| **`performance-profiler`** | Optimizasyon talebi | cProfile, PyTorch Profiler ve memory-profiler ile kodun darboğazlarını (bottleneck) tespit eder. |
| **`api-design`** | API oluşturma | RESTful API endpoint'leri, OpenAPI şemaları ve Pydantic veri modelleri tasarlar. |
| **`security-review`** | Güvenlik kontrolü | Subprocess enjeksiyonu, Ray cluster port açıkları, FastAPI kontrol API'leri ve güvensiz model pickle yükleme açıklarını denetler. |
| **`refactor-safe`** | Yeniden yapılandırma | Test kapsamını bozmadan kodu temizler ve atomik commit'lerle refactor eder. |
| **`code-review`** | Kod incelemesi | Kodun okunabilirlik, performans, tip güvenliği ve mimari standartlara uyumunu denetler. |
| **`dependency-audit`** | Paket güncelleme | `requirements.txt` / `pyproject.toml` bağımlılıklarını ve bilinen güvenlik açıklarını (CVE) tarar. |
| **`data-pipeline`** | Veri akışı tasarımı | Veri yükleme, temizleme, dönüştürme ve ön işleme akışlarını (ETL) kurar. |
| **`git-engineering`** | Genel Git yönetimi | Feature branch, conventional commits, interactive rebasing ve git bisect süreçlerini yönetir. |
| **`documentation-writer`** | Kod belgeleme | Google-style docstring ve Sphinx/MkDocs uyumlu kod dokümantasyonu üretir. |
| **`ci-cd-design`** | Otomasyon kurulumu | GitHub Actions ile otomatik PyTest ve Codecov test akışı kurar. |

---

## 🛠️ Klasör Yapısı

```
skills/
├── CLAUDE.md                     ← Proje Anayasası (Kurallar & Hiyerarşi)
├── README.md                     ← Bu dosya
├── .agents/                      ← Antigravity IDE Yerel Konfigürasyonu
│   ├── AGENTS.md                 ← Antigravity IDE Anayasası
│   └── skills/                   ← 43 Skill Tanımı
├── .claude/
│   ├── settings.json             ← Lifecycle Hooks & MCP Server Ayarları
│   ├── agents/                   ← 8 Ajan Tanımı (Architect, Planner, Coder vb.)
│   ├── skills/                   ← 43 Skill Tanımı (Akademik & Kodlama)
│   ├── hooks/                    ← Hook Scriptleri (sync_skills, security_gate vb.)
│   ├── context/                  ← Oturum Belleği (ARCHITECTURE.md, context.db, FORMULATION.md)
│   └── templates/                ← Proje Şablonları (.gitignore, FORMULATION.md, git-hooks)
```

---

## 📜 Lisans
MIT License

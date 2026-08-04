# Agentic AI & Skills Sistemi — Global Kurulum Kaynağı

Bu repo, Claude Code (ve Antigravity IDE) için hiyerarşik çok-ajanlı bir sistemi,
MCP sunucu önerilerini ve otomasyon hook'larını **tek bir makineye değil, tüm
makinelerine** taşımanı sağlayan kaynak paket. İçindeki her şey `~/.claude`
altına kurulur ve kurulduğu andan itibaren **açtığın her projede** otomatik
geçerli olur — proje proje `.claude/` klasörü kopyalamana gerek kalmaz.

**Skill'ler bu repoda değil.** 40+ akademik/RL/mühendislik skill'i artık Claude
hesabında (Cowork / claude.ai) kullanıcı seviyesinde tutuluyor — bu repo sadece
ajan tanımlarını, hook'ları, izinleri ve şablonları taşıyor.

---

## Hızlı başlangıç — yeni bir bilgisayarda

```bash
git clone https://github.com/Erdemhan/Experimental-Skills.git
cd Experimental-Skills
./install-global.ps1        # Windows (PowerShell)
./install-global.sh         # Linux / macOS / HPC cluster
```

Bu, `_global/` içeriğini `~/.claude` altına kopyalar, mevcut dosyaları
`.bak-<zaman damgası>` olarak yedekler, çalışan Python yorumlayıcısını bulup
hook komutlarına mutlak yol olarak gömer ve sonunda 6 kontrol geçirerek
kurulumu doğrular (`-VerifyOnly` ile kurmadan sadece test de edebilirsin).

Ardından bir kereye mahsus, makine başına, MCP sunucularını kaydet (script
çıktısının sonunda tam komutlar basılır):

```bash
claude mcp add -s user memory -- npx -y @modelcontextprotocol/server-memory
claude mcp add -s user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking
npm install -g codebase-memory-mcp   # ya da: pip install codebase-memory-mcp
claude mcp add -s user codebase-memory-mcp -- codebase-memory-mcp
claude mcp list   # üçü de "Connected" görünmeli
```

Bundan sonra herhangi bir klasörde `claude` açtığında 9 ajan (`@architect`,
`@worker-coder`, ...) ve hesabındaki skill'ler hazır.

---

## Yeni ya da mevcut bir projede kullanmak

Proje kök dizininde tek komut, detayı `NEW-PROJECT.md`'de:

```bash
python3 ~/.claude/scripts/startup_project.py
```

`CLAUDE.md`'yi (projeye özgü kısacık bir dosya) şablondan üretir,
`.claude/context/` + `context.db`'yi kurar, `.gitignore`'u kopyalar, `.git/`
varsa commit/pre-commit/pre-push hook'larını yükler. Var olan bir dosyaya asla
sessizce dokunmaz. Antigravity IDE de kullanacaksan `--antigravity` ekle —
`CLAUDE.md`'yi `.agents/AGENTS.md` olarak aynalar ki iki araç da aynı kuralları
görsün.

---

## Ajan Hiyerarşisi ve Çalışma Prensipleri

Sistem üç katmanda tanımlanmış 9 uzman ajandan oluşur:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🏛️ TASARIM & İŞLEVSELLİK KATMANI (PLAN-FIRST — KULLANICI ONAYI ZORUNLU)    │
│                                                                             │
│  • @architect  (Opus)         → Mimari karar, ADR'ler, FORMULATION.md, MCP  │
│  • @module-planner (Sonnet)   → Domain-aware (RL/Sim/ML) spec tasarımları   │
│  • @paper-writer (Sonnet)     → Akademik yazı taslağı & LaTeX outlineleri   │
│  • @advisor-reporter (Sonnet) → Danışman hocaya özel ilerleme & sunum raporu│
│                                                                             │
│  👉 Kural: Tasarım ve işlevsellik kullanıcıya sunulur.                      │
│     Siz "onaylıyorum / uygula" demediğiniz sürece spec ve dosya yazılmaz.  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │  (Sizin Onayınız)
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ ⚙️ UYGULAMA & TEST KATMANI (OTONOM VE HIZLI İCRA)                          │
│                                                                             │
│  • @worker-coder (Haiku)          → Spec'e uygun kod yazımı & PyTest        │
│  • @unit-tester (Sonnet)          → 3x Tier 2 retry & otonom test debug     │
│  • @integration-verifier (Sonnet) → Modüller arası otonom entegrasyon      │
│  • @experiment-runner (Sonnet)    → Arka planda 5-seed RL eğitimi koşturma  │
│                                                                             │
│  👉 Kural: Onaylı spec dahilinde unit testler, retry'lar ve kod içi         │
│     düzeltmeler sizi bekletmeden OTONOM yürütülür.                         │
└─────────────────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────────────────┐
│ 🔄 OTURUM VE DURUM YÖNETİMİ (OTOMATİK BAŞLANGIÇ)                            │
│                                                                             │
│  • @context-manager (Haiku)   → Oturum başında state sync & sonraki adım    │
└─────────────────────────────────────────────────────────────────────────────┘
```

Golden Rule: **Architect asla kod yazmaz. Worker asla tasarım kararı vermez.**
Tam kural seti: `_global/CLAUDE.md` (kurulunca `~/.claude/CLAUDE.md` olur).

### Ajan özet tablosu

| Ajan | Katman | Onay Modu | Temel Görevi |
|---|---|---|---|
| `@architect` | Tasarım & Mimari | Plan-First | Sistem mimarisi, ADR'ler, `ARCHITECTURE.md`, MCP indeksleme, kilitli kütükler. |
| `@module-planner` | Tasarım & Spec | Plan-First | Modül ayrıştırma ve domain-aware `FunctionSpec` JSON üretimi (RL/Sim/ML). |
| `@paper-writer` | Akademik Yazım | Plan-First | NeurIPS/ICML/IEEE formatlarında LaTeX makale taslağı ve BibTeX yönetimi. |
| `@advisor-reporter` | Akademik Raporlama | Plan-First | Danışman hocaya özel ilerleme raporu ve stratejik karar sunumu. |
| `@worker-coder` | Kod Uygulama | Otonom | `FunctionSpec` tabanlı tekil fonksiyon kodlama & PyTest, 3x otonom retry. |
| `@unit-tester` | Test & Debug | Otonom | Tier 2 hata ayıklama, karmaşık fixture/mocking, gerektiğinde kullanıcı eskalasyonu. |
| `@integration-verifier` | Entegrasyon | Otonom | Modüller arası arayüz kontratları ve uçtan uca entegrasyon testleri. |
| `@experiment-runner` | Deney Yürütme | Otonom | Arka planda multi-seed RL/Simülasyon eğitimi, sessiz log takibi, NaN tespiti. |
| `@context-manager` | Oturum Yönetimi | Otomatik | Oturum açılışında bağlam senkronizasyonu ve durum raporu. |

---

## Lifecycle Hooks (6 script)

`~/.claude/settings.json` içinde tanımlı, `~/.claude/hooks/` altında yaşayan
6 Python script'i güvenliği, kod kalitesini ve oturum belleğini otonom yönetir:

| Script | Hook Tipi | İşlevi |
|---|---|---|
| `security_gate.py` | `PreToolUse` | Yıkıcı komutları (`rm -rf`, disk format, fork bomb, main/master'a force push) engeller. Regex tabanlı bir "kaza freni" — saldırgan koruması değil. |
| `context_sync.py` | `PreToolUse` | Proje kökünde `.claude/context/` varsa aktif görev durumunu SQLite'tan okuyup hatırlatır; yoksa sessizce çıkar, hiçbir dosya yaratmaz (opt-in). |
| `auto_format.py` | `PostToolUse` | Kaydedilen kod dosyalarını otomatik formatlar (`black`, `ruff`). |
| `test_watcher.py` | `PostToolUse` | PyTest çıktısını parse edip başarısız testleri özetler. |
| `context_db.py` | CLI | SQLite WAL veritabanı (`context.db`) ile eşzamanlı, ACID garantili oturum/görev takibi. `init`, `summary`, `add-task`, `complete` komutları. |
| `sync_agents_md.py` | CLI | Proje `CLAUDE.md`'sini `.agents/AGENTS.md` olarak aynalar (Antigravity IDE uyumluluğu). `ANTIGRAVITY_CONFIG` ortam değişkenini ya da `~/.gemini/config` varsayılanını kullanır — makineye sabit yol yazmaz. |

---

## MCP Sunucuları

`settings.json` üzerinden yüklenmiyor — makine başına bir kere `claude mcp add -s user` ile kaydediliyor:

| Sunucu | İşlev | Kullanan Ajanlar |
|---|---|---|
| `codebase-memory-mcp` | Kod grafiği: `index_repository`, `search_code`, `trace_path`, `get_architecture`, `search_graph` | `@architect`, `@context-manager`, `@worker-coder` |
| `memory` | Knowledge graph (deney & hipotez hafızası) | `@context-manager`, `@experiment-runner` |
| `sequential-thinking` | Adım adım mantıksal düşünme | `@architect`, `@module-planner` |

Üç sunucu da kayıtlı değilse ajanlar built-in `Grep`/`Glob`/`Read`'e düşer,
çağrının başarısız olduğunu varsaymaz. `fetch` bilerek önerilmiyor — Claude
Code zaten yerleşik `WebFetch` taşıyor.

---

## FORMULATION.md (Akademik Formülasyon Kütüğü)

Denklem/parametre içeren projelerde matematiksel formülasyon `.claude/context/FORMULATION.md`'de tutulur:

- **Kullanıcı-kilitli**: açık onay olmadan hiçbir ajan içeriğini değiştiremez.
- Kod ile kayıt çelişirse düzeltilen koddur, kayıt değil.
- `python3 ~/.claude/scripts/startup_project.py --with-formulation` ile projeye eklenir.

---

## Klasör Yapısı

```
Experimental-Skills/
├── CLAUDE.md                      ← Bu reponun kendi amacını anlatan not (Claude'a)
├── README.md                      ← Bu dosya
├── NEW-PROJECT.md                 ← Yeni/mevcut proje kontrol listesi
├── install-global.ps1             ← Windows kurulum scripti
├── install-global.sh              ← Linux/macOS/cluster kurulum scripti
├── _global/                       ← ~/.claude olarak kurulan KAYNAK — değişiklik hep burada
│   ├── CLAUDE.md                  ← Global anayasa (ajan hiyerarşisi, kurallar)
│   ├── settings.json              ← Hook + izin tanımları (Windows)
│   ├── settings.linux.json        ← Aynısı, Linux/macOS varyantı
│   ├── agents/                    ← 9 ajan tanımı (architect.md, worker-coder.md, ...)
│   ├── hooks/                     ← 6 lifecycle hook scripti
│   ├── scripts/                   ← startup_project.py
│   └── templates/                 ← .gitignore, FORMULATION.md, pre-commit, git-hooks/
└── _new-project/
    └── CLAUDE.md                  ← Yeni proje CLAUDE.md şablonunun tek kaynağı
```

`.claude/` ve `.agents/` bu repoda **yok** — onlar sadece kurulumdan sonra
*senin çalıştığın diğer projelerde* oluşur (`startup_project.py` ile).

---

## Bu Repoyu Güncellerken

Değişiklik her zaman `_global/` altında yapılır, `~/.claude`'a elle değil —
oradaki her şey bir sonraki kurulumda ezilir. Şablonlarda (`settings.json`,
`settings.linux.json`) gerçek bir kullanıcı adı ya da mutlak yol olmamalı; hook
komutları `<CLAUDE_HOME>` yer tutucusu taşır ve bunu install script'leri
kurulum anında gerçek yola çevirir. Değişiklikten sonra doğrula:

```bash
./install-global.ps1 -VerifyOnly   # Windows
```

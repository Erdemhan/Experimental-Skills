# Yeni Proje Kontrol Listesi

Global kurulum (`install-global.ps1`) bir kere yapıldıktan sonra, yeni bir projede
eklemen gereken **harici şeyler** aşağıdakilerden ibaret.

---

## Otomatik gelenler — hiçbir şey yapmana gerek yok

| Ne | Nereden |
|---|---|
| **29 skill** (rl-*, academic, paper, git-research…) | Claude hesabın — hiçbir dosyaya bağlı değil |
| **9 ajan** (`@architect`, `@worker-coder`, …) | `~/.claude/agents/` |
| **4 hook** (security_gate, auto_format, test_watcher, context_sync) | `~/.claude/settings.json` |
| **İzinler** (pytest, git, black, ruff, mypy, latexmk) | `~/.claude/settings.json` — izinler katmanlar arası **birleşir** |
| **Genel kurallar** (ajan hiyerarşisi, kodlama standartları, token bütçesi, akademik kurallar) | `~/.claude/CLAUDE.md` |
| **Template'ler** (.gitignore, pre-commit, git-hooks, FORMULATION iskeleti) | `~/.claude/templates/` |
| **MCP sunucuları** (codebase-memory, memory, sequential-thinking, fetch) | `claude mcp add -s user` ile bir kere eklenir |

---

## Yeni projede yapılacaklar — 4 adım, ~2 dakika

### 1. Proje CLAUDE.md'sini yaz

```bash
cp ~/.claude/templates/../../_new-project/CLAUDE.md ./CLAUDE.md   # ya da elle
```

Sadece **bu projeye özgü** olanları doldur: araştırma sorusu, ortam/algoritma/sürümler,
seed seti, deney bütçesi, tracking yeri. Global'de yazan hiçbir kuralı tekrar etme.

### 2. Bağlam dizinini oluştur

```bash
mkdir -p .claude/context
python3 ~/.claude/hooks/context_db.py init
```

> `context_sync.py` hook'u yalnızca `.claude/context/` **varsa** çalışır. Bu adımı
> atlarsan hook sessizce devre dışı kalır — bilinçli bir tasarım, deney yürütmeyen
> küçük projelerde gereksiz `context.db` oluşmasın diye.

### 3. Formülasyon kaydını koy (yalnızca denklem içeren projelerde)

```bash
cp ~/.claude/templates/FORMULATION.md .claude/context/FORMULATION.md
```

Denklem/parametre içermeyen bir projeyse atla. Ajanlar dosyayı bulamazsa hangi belgenin
bağlayıcı olduğunu sana sorar, varsaymaz.

### 4. .gitignore ve git hook'ları

```bash
cp ~/.claude/templates/.gitignore .gitignore
python3 ~/.claude/templates/git-hooks/install_hooks.py
```

`.gitignore`'a şunların girdiğini doğrula:

```gitignore
.claude/context/*.db
.claude/context/*.db-wal
.claude/context/*.db-shm
.claude/context/sync.log
```

---

## İsteğe bağlı

| Durum | Yapılacak |
|---|---|
| Projeye özgü MCP sunucusu gerekiyor | Proje kökünde `.mcp.json` oluştur |
| Bu projede farklı izinler lazım | `.claude/settings.json` yaz — global ayarı ezer, izinler birleşir |
| Sadece sende geçerli, repoya girmeyecek ayar | `.claude/settings.local.json` |
| Antigravity IDE de kullanılacak | `python3 ~/.claude/hooks/sync_agents_md.py` → `.agents/AGENTS.md` üretir |

---

## Minimum yeni proje iskeleti

```
yeni-proje/
├── CLAUDE.md                      ← projeye özgü, ~20 satır
├── .gitignore                     ← template'ten
└── .claude/
    └── context/
        ├── context.db             ← context_db.py init üretir, git'e girmez
        ├── FORMULATION.md         ← denklem varsa
        └── ARCHITECTURE.md        ← ilk mimari kararda oluşur
```

Bu kadar. `.claude/skills/`, `.claude/agents/`, `.claude/hooks/`, `.claude/settings.json`
artık proje içine **kopyalanmıyor**.

---

## Doğrulama

Yeni projede Claude Code'u açıp:

```
/            → 29 skill görünmeli
@            → 9 ajan görünmeli
```

Hook'ların çalıştığını test et:

```bash
# security_gate devrede mi (engellenmeli):
rm -rf /tmp/deneme

# test_watcher devrede mi (özet raporlamalı):
pytest -q
```

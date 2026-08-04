# Bu Repo Ne İşe Yarıyor

Bu repo bir araştırma projesi **değil** — `~/.claude` global kurulumunun kaynak
paketi. İçindeki her şey (`_global/`) `install-global.ps1` / `install-global.sh`
ile herhangi bir bilgisayarda `~/.claude` altına kurulur ve o andan itibaren
**tüm projelerde** otomatik geçerli olur (ajan hiyerarşisi, hook'lar, izinler,
akademik/mühendislik kuralları — bkz. `_global/CLAUDE.md`).

Yeni bir bilgisayara geçtiğinde ya da bu repoyu ilk kez bir makineye
kopyaladığında yapman gereken tek şey:

```bash
git clone https://github.com/Erdemhan/Experimental-Skills.git
cd Experimental-Skills
./install-global.ps1        # Windows
./install-global.sh         # Linux / macOS / cluster
```

Ardından bir kereye mahsus MCP sunucu kaydı (`claude mcp add -s user ...` —
script sonunda tam komutları basar). Detay ve yeni-proje akışı için
`NEW-PROJECT.md`'ye bak.

---

## Bu Repo Üzerinde Çalışırken (Claude'a not)

- **Kaynak `_global/`'dir, `~/.claude` değil.** Hook, ajan, kural değişikliği
  hep `_global/` altında yapılır; `~/.claude`'a asla elle yazılmaz — oradaki
  her şey bir sonraki `install-global` çalıştırmasında ezilir.
- **Şablonlar makineden bağımsız olmalı.** `_global/settings.json` ve
  `_global/settings.linux.json` içinde gerçek bir kullanıcı adı ya da mutlak
  yol GÖRMEMELİSİN — hook komutları `<CLAUDE_HOME>` yer tutucusu taşır, bunu
  `install-global.ps1`/`.sh` kurulum anında gerçek yola çevirir. Bir template
  dosyasında hardcoded `C:/Users/...` ya da `/home/...` görürsen bu bir bug'dır
  (bir kere oldu — bkz. commit geçmişi).
- **`_new-project/CLAUDE.md`** yeni proje şablonunun tek kaynağıdır; kurulum
  scriptleri onu `~/.claude/templates/PROJECT_CLAUDE.md` olarak kopyalar.
  İçeriği burada değil, orada değiştir.
- Değişiklik yaptıktan sonra `install-global.ps1 -VerifyOnly` (ya da eşdeğer
  `.sh` doğrulaması) ile hook'ların hâlâ çalıştığını doğrula.

Ajan hiyerarşisi, plan-first/otonom yürütme kuralları, kodlama standartları ve
akademik kurallar için: `_global/CLAUDE.md` (bu, kurulunca `~/.claude/CLAUDE.md`
olur ve gerçekten yürürlükte olan metindir).

# <Proje Adı>

> Genel kurallar (ajan hiyerarşisi, kodlama standartları, akademik kurallar, token bütçesi)
> `~/.claude/CLAUDE.md` içinde ve otomatik yükleniyor. Bu dosya **yalnızca bu projeye özgü**
> olanları içerir. Global'de zaten yazan hiçbir şeyi burada tekrar etme.

---

## Proje Özeti

<Bir paragraf: bu proje ne yapıyor, hangi araştırma sorusunu hedefliyor.>

**Araştırma sorusu**: <hypothesis-framing çıktısı, tek cümle>

---

## Bağlam Dosyaları

| Dosya | Rol |
|---|---|
| `.claude/context/FORMULATION.md` | Kanonik denklemler, semboller, parametre değerleri. **Kullanıcı-kilitli.** |
| `.claude/context/ARCHITECTURE.md` | Mimari kararlar. Her mimari karardan sonra güncellenir. |
| `.claude/context/context.db` | SQLite görev/oturum durumu. Git'e girmez. |

Oturum başlangıcında `@context-manager` çalışır ve `context.db` yoksa oluşturur:

```bash
python3 ~/.claude/hooks/context_db.py init      # ilk kurulum
python3 ~/.claude/hooks/context_db.py summary   # durum özeti
```

---

## Bu Projeye Özgü Teknik Kısıtlar

<Örnekler — geçerli olmayanları sil:>

- **Ortam**: `<CustomEnv-v1>`, `gymnasium==<sürüm>`, `mujoco==<sürüm>`
- **Algoritma**: `<PPO / SAC / MAPPO>`, framework `<Ray RLlib <sürüm> / SB3 <sürüm>>`
- **Donanım**: `<RTX 4090 / cluster kuyruğu>`; deneyler `<yerel / SLURM>` üzerinde koşuyor
- **Seed seti**: `[42, 123, 456, 789, 1024]`
- **Deney bütçesi**: konfigürasyon başına `<N>` GPU saati

---

## Deney Kayıt Yeri

- Tracking: `<WandB projesi / MLflow sunucusu>`
- Ham loglar: `results/<exp_name>/`
- Figür ve tablolar: `paper/figures/` — `python scripts/analyze_results.py` ile yeniden üretilir

---

## Açık Kararlar / Bilinen Sınırlılıklar

- <Danışman onayı bekleyen madde>
- <Etkisi bilinmeyen implementation deviation>

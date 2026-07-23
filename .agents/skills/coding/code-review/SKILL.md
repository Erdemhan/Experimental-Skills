---
name: code-review
description: >
  Activate this skill when performing or requesting a code review. This skill 
  provides a structured review checklist covering correctness, security, performance, 
  maintainability, and test coverage. Also guides constructive review feedback.
---

# Code Review Skill — Kod İncelemesi

## Temel Kural
> Kod incelemesi hata bulmak değil, kaliteyi garanti altına almaktır.

---

## İnceleme Kontrol Listesi

### Doğruluk
- [ ] Kod tanımlanan iş gereksinimini karşılıyor mu?
- [ ] Edge case'ler ele alınmış mı?
- [ ] Hata yönetimi uygun mu?
- [ ] Async/concurrent kod varsa race condition riski?

### Güvenlik
- [ ] Kullanıcı girdisi validate ve sanitize ediliyor mu?
- [ ] Kimlik doğrulama/yetkilendirme doğru mu?
- [ ] Hassas veri loglanıyor mu?
- [ ] Bağımlılıklar güvenli ve güncel mi?

### Performans
- [ ] N+1 sorgu problemi var mı?
- [ ] Büyük veri için bellek tasarrufu düşünüldü mü?
- [ ] Gereksiz hesaplama / tekrar var mı?
- [ ] Caching uygun yerde mi?

### Bakım Kolaylığı
- [ ] Değişken/fonksiyon isimleri anlamlı mı?
- [ ] Fonksiyon/metod boyutu makul mü? (max ~30 satır)
- [ ] DRY prensibi ihlal ediliyor mu?
- [ ] Bağımlılıklar minimal mü?
- [ ] Gelecekte değişiklik yapılırken anlaşılır mı?

### Test Kalitesi
- [ ] Test kapsamı yeterli mi? (%80+)
- [ ] Test isimleri davranışı açıklıyor mu?
- [ ] Edge case'ler test edilmiş mi?
- [ ] Mock'lar gerçekçi mi?

### Dokümantasyon
- [ ] Public API için docstring var mı?
- [ ] Karmaşık mantık için yorum var mı?
- [ ] Neden öyle yapıldığı açıklanıyor mu (Ne değil, Neden)?
- [ ] README veya dokümantasyon güncellendi mi?

---

## Yapıcı Geri Bildirim Dili

```
✅ Yapıcı: "Bu fonksiyon çok büyüdü; `validate_input()` ve `process_data()` 
           olarak ayırmanı öneririm — böylece her biri tek sorumluluğa sahip olur."

❌ Yıkıcı: "Bu kod berbat, nasıl böyle yazarsın?"

✅ Yapıcı: "Burada `Optional[str]` yerine `str | None` (Python 3.10+) 
           kullanabilirsin — daha modern ve okunabilir."

✅ Yapıcı (zorunlu değil): "Nit: Bu değişken adını `d` → `data` olarak 
           değiştirsen daha açık olur. (Zorunlu değil, tercih meselesi)"
```

### Yorum Kategorileri
```
[BLOCKER]   Merge'i engelleyen kritik sorun
[MAJOR]     Önemli ama merge'i engellemez, düzeltilmeli
[MINOR]     Küçük iyileştirme önerisi
[NIT]       Küçük stil/yazım sorunları (opsiyonel)
[QUESTION]  Anlamadığım bir şeyi soruyorum
[PRAISE]    İyi yapılmış bir şeyi vurguluyorum
```

---

## Review Özet Raporu

```
## Code Review Özeti

**PR**: #123 — Feature: Add sentiment analysis endpoint
**Gözden Geçiren**: [İsim]
**Tarih**: YYYY-MM-DD

### Genel Değerlendirme
🟡 Bazı düzeltmeler gerekiyor (merge öncesi)

### Blocker'lar (Zorunlu Düzeltme)
1. [BLOCKER] auth.py:42 — SQL injection açığı

### Major Sorunlar
1. [MAJOR] service.py:78 — Test kapsamı eksik (sadece %45)
2. [MAJOR] api.py:15 — Hata formatı standarda uymuyor

### Minor/Nit
1. [NIT] utils.py:23 — Değişken adı daha açık olabilir

### Olumlu
- Test organization çok iyi
- Error handling düşünülmüş
```

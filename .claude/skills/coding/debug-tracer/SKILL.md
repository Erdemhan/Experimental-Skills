---
name: debug-tracer
description: >
  Activate this skill when debugging an error, investigating unexpected behavior, 
  or tracing a bug in code. This skill enforces a hypothesis-driven debugging 
  approach: form a hypothesis, add targeted logging, verify or falsify, then fix. 
  Prevents random trial-and-error debugging.
---

# Debug Tracer Skill — Hata İzleyici

## Temel Kural
> Rastgele değiştirme debug değildir. Varsayımla kod düzeltme yasaktır. Önce log ve traceback kanıtı topla, ampirik olarak doğrula.

> [!IMPORTANT]
> **Akademik Araştırma Bağlamı**: Eğer bu kodu bir araştırma projesinde (RL deneyi, simülosyon, paper kodu) düzenleyecekseniz,
> `debug-tracer`'dan ÖNCE `research-debug` skill'ini çalıştırın.
> Neden: Bir fix, önceden raporlanan sonuçları geçersiz kılabilir.
> Sadece saf yazılım hatası olduğundan (sonucu etkilemiyor) emin değilseniz,
> bug'u önce **Tip A / B / C** olarak sınıflandırın.

---

## Hipotez-Odaklı Debug Döngüsü

```
1. GÖZLEM   → "Hata nedir? Ne zaman oluşuyor?"
2. HİPOTEZ  → "Bu hatanın kaynağı [X] çünkü [Y]"
3. KANIT    → "Bunu kanıtlamak için [Z] log/test ekleyeceğim"
4. TEST     → Log ekle, çalıştır, gözlemle
5. DEĞERLE  → Hipotez doğrulandı mı? Hayırsa → 2'ye dön
6. DÜZELTMİ → Kök nedeni düzelt (semptomu değil)
7. DOĞRULA  → Düzeltme çalıştı mı? Regresyon var mı?
```

---

## Gözlem Aşaması — Bilgi Toplama

Hata raporunu şu sorularla yapılandır:

```
1. Hata mesajı tam olarak nedir? (Stack trace dahil)
2. Hata ne zaman başladı? (Son çalışan versiyon ne?)
3. Her zaman mı oluşuyor yoksa aralıklı mı (flaky)?
4. Hangi koşulda oluşuyor? (Hangi girdi, hangi ortam?)
5. Hangi koşulda oluşmuyor?
6. Son değişiklik ne oldu? (git log --oneline -20)
```

---

## Bisect Yöntemi (Regresyon için)

Bir değişiklikle ortaya çıkan hatalar için:

```bash
# Git bisect ile hata giren commit'i bul
git bisect start
git bisect bad HEAD        # Şu an hatalı
git bisect good v1.2.3    # Bu versiyonda sorun yoktu

# Git otomatik olarak ikili arama yapar
# Her adımda: git bisect good / git bisect bad
git bisect run pytest tests/test_failing.py
```

---

## Hedefli Logging

Logging stratejisi — neyi, nereye ekleyeceğiniz:

```python
import logging

# Logger kurulumu
logger = logging.getLogger(__name__)

def suspicious_function(data: list) -> dict:
    logger.debug("Input: len=%d, first=%s", len(data), data[:3] if data else [])
    
    result = {}
    for i, item in enumerate(data):
        logger.debug("Processing item %d: %s", i, item)
        
        try:
            processed = transform(item)
            result[item['id']] = processed
        except KeyError as e:
            logger.error("Missing key %s in item %d: %s", e, i, item)
            raise
    
    logger.debug("Output: %d items", len(result))
    return result
```

---

## Stack Trace Okuma Kılavuzu

```
Traceback (most recent call last):
  File "main.py", line 42, in <module>     ← Çağrı zinciri (üstten alta)
    result = process(data)
  File "processor.py", line 15, in process
    return transform(item)                  ← Hata burada!
  File "transformer.py", line 8, in transform
    return item['key']                      ← Gerçek hata satırı
KeyError: 'key'                             ← Hata tipi ve mesajı
```

**Okuma stratejisi**: En alttan başla, yukarı doğru çık.

---

## Yaygın Hata Kategorileri ve İpuçları

| Hata Tipi | Belirti | İlk Bakılacak Yer |
|---|---|---|
| `KeyError` | Dict'te olmayan anahtar | Veri yapısını print et, key kontrol et |
| `AttributeError` | None veya yanlış tip | `type(obj)` ve `print(obj)` ekle |
| `IndexError` | Liste sınırı aşımı | `len(lst)` ve index değerini logla |
| `ValueError` | Yanlış değer | Fonksiyon girdisini logla |
| Off-by-one | Yanlış sonuç | Sınır değerlerini test et |
| Flaky test | Bazen geçer bazen geçmez | Race condition / random seed / external dep |
| Memory leak | Bellek büyüyor | tracemalloc veya memory-profiler kullan |
| Infinite loop | Program asılı kalıyor | Loop değişkenini ve koşulunu logla |

---

## Debug Araç Seti

```python
# 1. pdb — Breakpoint debugging
import pdb; pdb.set_trace()  # Buraya gelince dur
# veya
breakpoint()  # Python 3.7+

# 2. Hızlı değer incelemesi
print(f"DEBUG: {var=}")  # Python 3.8+ walrus print

# 3. Traceback
import traceback
try:
    risky_operation()
except Exception:
    traceback.print_exc()  # Tam stack trace

# 4. Bellek profili
from tracemalloc import start, take_snapshot, compare_to
start()
# ... kod ...
snapshot = take_snapshot()
```

---

## Düzeltme Sonrası Doğrulama

Düzeltme yapıldıktan sonra:
- [ ] Orijinal hata giderildi mi?
- [ ] Unit test eklendi mi? (aynı hatanın tekrarlamaması için)
- [ ] Regresyon testleri hala geçiyor mu?
- [ ] Edge case'ler test edildi mi?
- [ ] Kök neden (semptom değil) düzeltildi mi?

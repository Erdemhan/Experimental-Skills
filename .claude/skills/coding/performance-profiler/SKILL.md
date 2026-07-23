---
name: performance-profiler
description: >
  Activate this skill before any performance optimization work. This skill enforces 
  the "measure first" rule: profile before optimizing, identify actual bottlenecks 
  with data, and document before/after improvements. Prevents premature optimization.
---

# Performance Profiler Skill — Performans Profiler

## Temel Kural
> Önce ölç, sonra optimize et. Varsayıma dayalı optimizasyon tehlikelidir.

---

## Profil Araçları

### CPU Profiling (Python)
```bash
# cProfile — standart kütüphane
python -m cProfile -o output.prof your_script.py

# Görselleştirme
pip install snakeviz
snakeviz output.prof
```

```python
# Kod içinde belirli bir bölümü profile et
import cProfile
import pstats

with cProfile.Profile() as pr:
    slow_function()

stats = pstats.Stats(pr)
stats.sort_stats("cumulative")
stats.print_stats(20)  # İlk 20 satır
```

### Line-by-Line Profiling
```bash
pip install line-profiler

# @profile decorator ekle, sonra:
kernprof -l -v your_script.py
```

### Bellek Profiling
```bash
pip install memory-profiler

# @profile decorator ile:
python -m memory_profiler your_script.py

# Tracemalloc (built-in)
```python
import tracemalloc
tracemalloc.start()
# ... kod ...
snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics("lineno")
for stat in top_stats[:10]:
    print(stat)
```

---

## Performans Ölçüm Formatı

Optimizasyon öncesi ve sonrası her zaman kaydet:

```
Fonksiyon: process_dataset()
Veri: 10,000 örnek

ÖNCE:
  Çalışma süresi: 45.2s (±1.3s, N=5)
  Bellek: 2.3 GB peak
  CPU kullanımı: %95 (tek çekirdek)
  Bottleneck: pandas.DataFrame.apply() — %78 süre

SONRA (vektörizasyon):
  Çalışma süresi: 2.1s (±0.2s, N=5)  ← 21.5x hızlanma
  Bellek: 1.8 GB peak                 ← %22 düşüş
  CPU kullanımı: %40

Uygulanan Optimizasyon: apply() → numpy vektörizasyonu
Trade-off: Kod karmaşıklığı arttı, okunabilirlik azaldı
```

---

## Yaygın Python Optimizasyonları

| Yavaş | Hızlı | Ne Zaman |
|---|---|---|
| `for` döngüsü | NumPy vektörizasyonu | Sayısal işlemler |
| `list.append()` döngüsü | List comprehension | Liste oluşturma |
| Pandas `apply()` | `df['col'].map()` | Basit dönüşümler |
| String `+` birleştirme | `"".join(list)` | Çok sayıda string |
| `re.compile()` tekrar | Önceden derle | Pattern tekrar kullanımı |
| Gereksiz kopyalama | In-place işlem | Büyük veri |

---

## Optimizasyon Öncelik Sırası

```
1. Algoritma seçimi   → O(n²) → O(n log n) en büyük kazanç
2. Veri yapısı        → list → set (arama O(1) vs O(n))
3. I/O optimizasyonu  → batch okuma, async I/O
4. Bellek yönetimi    → generator vs list
5. Vektörizasyon      → numpy, pandas yerine
6. Paralelizasyon     → multiprocessing, concurrent.futures
7. Cache              → lru_cache, Redis
8. Düşük seviye       → Cython, numba (son çare)
```

---

## Hedef Belirleme

Optimizasyon başlamadan önce hedef tanımla:
```
Mevcut: P95 latency = 800ms
Hedef:  P95 latency < 200ms
Neden:  User experience threshold (Google: <200ms hissedilmez)
Yöntem: [profile sonrası belirlenir]
Kabul Kriteri: 5 farklı veri seti ile ölçüm
```

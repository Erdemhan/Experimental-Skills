---
name: refactor-safe
description: >
  Activate this skill when refactoring existing code. This skill enforces the 
  safe refactoring protocol: ensure test coverage first, make atomic changes, 
  preserve observable behavior, and verify with tests at each step. Prevents 
  behavior-breaking refactors.
---

# Refactor Safe Skill — Güvenli Yeniden Yapılandırma

## Temel Kural
> Refactoring davranışı değiştirmez, sadece kodu düzenler. Test olmadan refactoring yapma.

> [!IMPORTANT]
> **Plan-First Kuralı**: Kodu yeniden yapılandırmadan önce refactoring planını (hangi sınıflar/fonksiyonlar değişecek) kullanıcıya açıklayın. Kullanıcı "uygula / devam et" onayı vermediği sürece dosyalara dokunmayın.

---

## Güvenli Refactoring Protokolü

### Adım 0 — Test Kapsamını Doğrula
```bash
# Önce mevcut kapsam
pytest --cov=src --cov-report=term-missing

# Refactoring yapılacak kod için kapsam %80 altındaysa
# ÖNCE test yaz, SONRA refactor et
```

### Adım 1 — Güvenli Git State
```bash
# Refactoring başlamadan önce temiz commit
git add -A && git commit -m "chore: before refactoring <module_name>"
git checkout -b refactor/<feature_name>
```

### Adım 2 — Atomik Değişiklikler
Her commit TEK bir refactoring tekniği içermeli:
```bash
# ✅ Atomik commit'ler
git commit -m "refactor: extract validate_email() from UserService"
git commit -m "refactor: rename process_data() to transform_records()"
git commit -m "refactor: inline unnecessary helper _get_temp()"

# ❌ Karmaşık commit
git commit -m "refactor: cleaned up everything"
```

### Adım 3 — Test → Refactor → Test Döngüsü
```
[Testler Yeşil] → Küçük Değişiklik → [Testler Tekrar Çalıştır] → [Yeşil mi?]
                                                                    ├── Evet → Sonraki adım
                                                                    └── Hayır → Git revert, analiz et
```

---

## Refactoring Teknikleri Kataloğu

### Extract Function
```python
# ÖNCE
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Negative total")
    # Process
    ...

# SONRA
def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Negative total")

def process_order(order):
    validate_order(order)
    ...
```

### Rename (Davranış Değiştirmez)
```python
# Rename ettikten sonra eski adı alias olarak koru (API varsa)
def transform_records(data):  # Yeni ad
    ...

# Geriye uyumluluk (deprecation)
def process_data(data):  # Eski ad
    import warnings
    warnings.warn("process_data() deprecated, use transform_records()", DeprecationWarning, stacklevel=2)
    return transform_records(data)
```

### Magic Number → Named Constant
```python
# ❌ Magic number
if score > 0.75:
    label = "high"

# ✅ Named constant
HIGH_SCORE_THRESHOLD = 0.75
if score > HIGH_SCORE_THRESHOLD:
    label = "high"
```

---

## Refactoring Kontrol Listesi

**Başlamadan Önce**
- [ ] Test kapsamı %80+ mi?
- [ ] Temiz git state var mı?
- [ ] Refactoring kapsamı net tanımlandı mı?

**Sırasında**
- [ ] Her commit atomik mi (tek teknik)?
- [ ] Her değişiklikten sonra testler çalıştırıldı mı?
- [ ] Public interface değişiyor mu? (Breaking change?)
- [ ] Gereksiz değişiklik eklendi mi? (Scope creep)

**Sonrasında**
- [ ] Tüm testler geçiyor mu?
- [ ] Yeni test yazılması gereken davranış ortaya çıktı mı?
- [ ] Performans değişti mi? (Profil al)

---

## Ne Zaman Refactoring YAPMA

- Production'da aktif incident varken
- Test olmayan legacy koda (önce test yaz)
- Deadline yakınken (technical debt sonra ödenir)
- Bir özellik geliştirirken aynı anda (ayrı branch açılır)

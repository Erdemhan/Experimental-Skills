---
name: documentation-writer
description: >
  Activate this skill when writing code documentation, docstrings, README files, 
  API references, or any technical documentation. This skill enforces Google-style 
  docstrings, structured README format, and the principle of documenting WHY not WHAT.
---

# Documentation Writer Skill — Dokümantasyon Yazarı

## Temel Kural
> Kod ne yaptığını söyler. Yorum neden yaptığını söyler. İkisi birden olmak zorunda değildir.

---

## Google Style Docstring Standardı

```python
def calculate_weighted_f1(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    weights: list[float] | None = None,
) -> float:
    """Calculate weighted F1 score across multiple classes.

    Computes F1 for each class independently, then takes a weighted average.
    If weights are not provided, class frequencies in y_true are used.

    Args:
        y_true: Ground truth labels of shape (n_samples,).
            Values must be integers in range [0, n_classes).
        y_pred: Predicted labels of shape (n_samples,).
            Must have the same shape as y_true.
        weights: Optional list of per-class weights of length n_classes.
            If None, class frequencies are used as weights.
            Weights are normalized to sum to 1.

    Returns:
        Weighted F1 score as float in [0.0, 1.0].
        Returns 0.0 if no positive predictions exist.

    Raises:
        ValueError: If y_true and y_pred have different shapes.
        ValueError: If y_true is empty.
        ValueError: If weights length does not match number of classes.

    Example:
        >>> y_true = np.array([0, 1, 2, 1, 0])
        >>> y_pred = np.array([0, 1, 1, 1, 0])
        >>> score = calculate_weighted_f1(y_true, y_pred)
        >>> print(f"Weighted F1: {score:.3f}")
        Weighted F1: 0.867

    Note:
        This implementation differs from sklearn's weighted F1 in that it
        handles zero-division by returning 0.0 instead of raising an error.
        For sklearn compatibility, use sklearn.metrics.f1_score with
        average='weighted' and zero_division=0.
    """
```

---

## README.md Yapısı

```markdown
# Proje Adı

> Tek cümle açıklama — ne yapıyor, neden özel.

[![Tests](badge)](link) [![Coverage](badge)](link) [![License](badge)](link)

## Neden Bu Proje?
[Problem nedir? Mevcut çözümler neden yetersiz? Bu proje farkı nedir?]

## Hızlı Başlangıç (Quick Start)
[5 dakikada çalışan örnek — kod ile]

```bash
pip install my-package
```

```python
from my_package import analyze
result = analyze("Merhaba dünya")
print(result)  # {'sentiment': 'positive', 'score': 0.95}
```

## Kurulum
[Detaylı kurulum adımları]

## Kullanım
[Ana kullanım senaryoları, örneklerle]

## API Referansı
[Tüm public fonksiyon/class listesi]

## Katkı Sağlama
[Geliştirme kurulumu, PR süreci]

## Lisans
[Lisans bilgisi]
```

---

## Yorum Yazma Kılavuzu

### Neden Yorum Yaz (Ne Değil)
```python
# ❌ Gereksiz (kodu tekrar ediyor)
# i değişkenini 1 artır
i += 1

# ✅ Anlamlı (neden açıklıyor)
# Skip the header row — first row contains column names, not data
for row in data[1:]:

# ✅ Karmaşık mantık açıklamak
# Leaky ReLU: allows small gradient when unit is not active,
# preventing "dying ReLU" problem (Xu et al., 2015)
output = max(0.1 * x, x)

# ✅ Geçici çözüm veya workaround
# TODO(erdemhan): Remove this workaround after upgrading to numpy 2.0
# np.bool is deprecated but still needed for compatibility with library X
arr = arr.astype(np.bool_)
```

### TODO/FIXME Formatı
```python
# TODO(kullanıcı-adı): Ne yapılacak [ISSUE-123]
# FIXME(kullanıcı-adı): Bilinen hata açıklaması [ISSUE-456]  
# HACK: Neden hack gerekti, gerçek çözüm ne olmalı
# NOTE: Önemli ama değiştirilmeyecek bir bilgi
```

---

## Changelog Formatı (Keep a Changelog)

```markdown
# Changelog

## [Unreleased]

## [2.1.0] — 2026-07-23
### Added
- `calculate_weighted_f1()` fonksiyonu eklendi

### Changed  
- `analyze()` fonksiyonu artık batch processing destekliyor

### Deprecated
- `process_text()` — `analyze()` kullanın (v3.0'da kaldırılacak)

### Fixed
- Boş string girdisinde `ValueError` yerine `None` döndürme sorunu

### Security
- Dependencies güncellendi (CVE-2026-XXXXX)
```

---

## Dokümantasyon Kontrol Listesi

- [ ] Her public fonksiyon/class/method docstring'e sahip mi?
- [ ] Args, Returns, Raises eksiksiz mi?
- [ ] En az bir code example var mı?
- [ ] README Quick Start çalışıyor mu? (test et)
- [ ] Yeni özellik CHANGELOG'a eklendi mi?
- [ ] Breaking change upgrade guide var mı?
- [ ] Tip açıklamaları (type hints) eksiksiz mi?

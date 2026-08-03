# Akademik Formülasyon ve Parametre Kütüğü (FORMULATION.md)

> ⚠️ KİLİTLİ DOKÜMAN: Bu dosyadaki denklemler, semboller, açıklamalar ve parametreler 
> kullanıcı onayı olmadan HİÇBİR AJAN TARAFINDAN DEĞİŞTİRİLEMEZ.

---

## 1. Matematiksel Denklemler ve Teori Kaynakları

### EQ-01: [Denklem/Formül Başlığı]
- **Formül**: $\mathcal{L}(\theta) = \dots$
- **Kaynak / Derleme**: [Yazar et al., Yıl — Denklem No, Sayfa No]
- **Açıklama & Yorum**: 
  [Bu denklemin nereden geldiği, fiziksel/matematiksel anlamı ve neden kullanıldığı]
- **Koddaki Karşılığı**: `src/path/to/file.py::function_name()`

---

## 2. Parametre Sözlüğü ve Hiperparametreler

| Sembol / Parametre | Değer | Birim / Kapsam | Kaynak / Açıklama & Yorum |
|---|---|---|---|
| $\gamma$ (gamma) | 0.99 | [0, 1) | İndirim faktörü — Uzun vadeli ödül ağırlığı (Sutton & Barto Sec 3.3) |
| $\epsilon$ (clip_eps) | 0.2 | (0, 0.5] | PPO clipping threshold — Aşırı büyük update'leri engeller |

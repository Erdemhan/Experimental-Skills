---
name: literature-review
description: >
  Activate this skill when conducting a systematic literature review, searching for 
  related work, mapping the research landscape, or writing a "Related Work" section. 
  This skill enforces a structured search protocol (PRISMA-inspired), source diversity, 
  and balanced coverage of both supporting and contradicting findings.
---

# Literature Review Skill — Alanyazın Tarama

## Temel Kural
> Sistematik tarama rastgele taramadan üstündür. Her adım belgelenir.

---

## Arama Protokolü (PRISMA-İlhamlı)

### Aşama 1 — Arama Stratejisi Belirleme

**Anahtar Kelime Matrisi:**
```
Ana Kavram 1 × Ana Kavram 2 × Bağlam

Örnek — "Federe Öğrenme + Gizlilik":
["federated learning" OR "distributed learning"] 
AND ["privacy" OR "differential privacy" OR "data privacy"]
AND ["machine learning" OR "deep learning"]
```

**Zaman Aralığı**: Genellikle son 5 yıl (+ temel/seminal çalışmalar için zaman sınırı yok)

### Aşama 2 — Arama Kaynakları

Akademik çalışmalar için kullanılacak kaynaklar (önem sırasıyla):

1. **Google Scholar** — Geniş kapsam
2. **Semantic Scholar** — AI/CS için güçlü
3. **arXiv** — Preprint için
4. **ACM Digital Library** — Bilgisayar bilimleri
5. **IEEE Xplore** — Mühendislik
6. **PubMed** — Biyomedikal
7. **Scopus / Web of Science** — Multidisipliner

### Aşama 3 — Dahil/Dışlama Kriterleri

```markdown
Dahil Kriterleri:
- Hakemli dergi veya A/B konferans bildirisi
- 20XX-20XX yıl aralığı
- [araştırma sorusunu] ele alan çalışmalar
- İngilizce veya Türkçe

Dışlama Kriterleri:
- Teknik raporlar (temel çalışmalar hariç)
- Duplike yayınlar
- [araştırma sorusunu] ele almayan
- Veri eksikliği (tam metin erişilemeyen)
```

### Aşama 4 — Eleme Süreci

```
Başlangıç: N = [toplam bulunan kayıt]
    │
    ▼ Duplike eleme
    N = [kalan]
    │
    ▼ Başlık + özet taraması
    N = [kalan]
    │
    ▼ Tam metin incelemesi
    N = [kalan]
    │
    ▼ Kalite değerlendirmesi
    Final: N = [dahil edilen]
```

---

## Kayıt Tutma Şablonu

Her çalışma için şu bilgiler tutulmalı:

```csv
Yazar,Yıl,Başlık,Dergi/Konferans,DOI,Konu,Yöntem,Bulgular,Sınırlılıklar,Alıntı Sayısı,Notlar
```

---

## Related Work Yazım Kılavuzu

### Yapı
1. **Tematik Gruplandırma** (kronolojik DEĞİL)
2. **Eleştirel Sentez** (sadece özet DEĞİL)
3. **Kendi Çalışmanıza Bağlantı**

### Yazım Kalıpları
```
✅ "Farklı yaklaşımlar önerilmiş olsa da (A, 2021; B, 2022), bu çalışmalar [eksik yön]'i ele almamaktadır."

✅ "X yöntemi [sonuç] elde etmiş (Yazar, Yıl); ancak [sınırlılık] nedeniyle [bağlam]'a uygulanabilirliği kısıtlıdır."

❌ "X (2021) şunu yaptı. Y (2022) şunu yaptı. Z (2023) şunu yaptı."  → Özet listesi, sentez değil
```

---

## Kapsam Dengesi

Related work şu grupları dengeli kapsamalıdır:
- [ ] Destekleyen çalışmalar
- [ ] Zıt bulgu sunan çalışmalar
- [ ] Farklı yöntem kullanan çalışmalar
- [ ] Temel/seminal çalışmalar
- [ ] Güncel (son 2 yıl) çalışmalar

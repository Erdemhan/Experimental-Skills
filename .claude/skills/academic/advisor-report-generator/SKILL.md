---
name: advisor-report-generator
description: >
  Activate this skill when generating academic progress reports, executive 
  briefings, milestone updates, or diagnostic reports for academic advisors 
  or supervisors. Ensures high-level conceptual clarity, mathematical 
  consistency with FORMULATION.md, statistical rigor, and actionable decision points.
---

# Advisor Report Generator Skill — Danışman Raporlama Yeteneği

## Temel İlke
> Danışman hocaya sunulan rapor koddaki ayrıntılarda boğulmamalı; yüksek seviyeli akademik motivasyon, sağlam teorik temeller (FORMULATION.md), istatistiksel kanıtlar ve net karar seçenekleri sunmalıdır.

---

## Rapor Türleri ve Yapıları

### 1. Haftalık / Dönemsel İlerleme Raporu (Weekly Progress Report)
- **1. Yönetici Özeti (Executive Summary):** Bu hafta ne başarıldı? (3-4 maddelik yüksek seviyeli özet)
- **2. Araştırma Bağlamı ve Motivasyon:** Bu haftaki çalışmanın genel projedeki yeri ve hipotezlerle (`@hypothesis-framing`) ilişkisi.
- **3. Yöntem ve Teorik Güncellemeler:** Algoritmik/matematiksel değişiklikler (`FORMULATION.md` sembolleriyle).
- **4. Deneysel Bulgular ve İstatistiksel Analiz:** Tablo/grafik destekli sonuçlar (`@statistical-validity`).
- **5. Karşılaşılan Engeller ve Olumsuz Sonuçlar:** Neden çalışmadı? Ampirik kanıtlar (`@empirical-rigor`).
- **6. Danışman Görüşüne Sunulan Maddeler ve Sonraki Adımlar:** Hocadan onay/tavsiye beklenen net kararlar.

### 2. Deney & Derin İnceleme Raporu (Experiment Deep-Dive Report)
- **1. Deneyin Amacı ve Hipotez:** Hangi H₀/H₁ hipotezi test ediliyor?
- **2. Deney Kurulumu:** Basitleştirilmiş parametre tablosu (kod detayları olmadan).
- **3. Karşılaştırmalı Analiz:** Baseline'lar ile kıyaslama (`@fair-comparison`).
- **4. Ana Çıkarımlar ve Teorik Yorum:** Bulguların literatürdeki karşılığı.

---

## Danışman Raporlama Kuralları

1. **Ham Kod Yerine Pseudocode / Akış Şeması:** Rapora asla 50 satırlık ham Python kodu koymayın. Bunun yerine pseudocode veya yüksek seviyeli mimari şeması sunun.
2. **Formülasyon Bütünlüğü:** `FORMULATION.md` dosyasındaki matematiksel sembolizm ile %100 uyumlu olun.
3. **Dürüst Raporlama (Negative Results):** Olumsuz sonuçları gizlemeyin; neden başarısız olduğunu ampirik verilerle açıklayın.
4. **Zaman Tasarruflu Tasarım:** Hocanın raporu 2 dakikada tarayıp ana mesajı anlayabileceği kalın punto (bold) vurgular ve özet tablolar kullanın.

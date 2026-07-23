---
name: replication-package
description: >
  Activate this skill when preparing a research paper for submission, archiving 
  a study, or packaging code and data for sharing. This skill provides a complete 
  checklist and templates for creating a replication package that allows others to 
  independently reproduce the study's findings.
---

# Replication Package Skill — Tekrarlama Paketi

## Temel Kural
> "Kodu paylaşıyorum" yeterli değildir. Çalıştırılabilir, belgelenmiş bir paket zorunludur.

ACM/IEEE artifact evaluation standartları temel alınmıştır.

---

## Paket İçeriği Kontrol Listesi

### Zorunlu Bileşenler
- [ ] **README.md** — Kurulum ve çalıştırma talimatları
- [ ] **requirements.txt veya environment.yml** — Tüm bağımlılıklar sürüm numarasıyla
- [ ] **Kaynak Kodu** — Temiz, yorumlanmış
- [ ] **Veri veya Veri İndirme Scripti** — Ham ve işlenmiş veri
- [ ] **Çalıştırma Scriptleri** — Her deneyi tekrar eden script
- [ ] **Çıktı Örnekleri** — Beklenen sonuçlar (referans için)
- [ ] **SEED dosyası veya yapılandırması** — Tüm random seed değerleri

### Önerilen Bileşenler (Opsiyonel)
- [ ] **Dockerfile** — Çevre izolasyonu (her zaman gerekmez — conda genellikle yeterli)
- [ ] **Makefile** — Tek komutla çalıştırma
- [ ] **Jupyter Notebook** — Analiz için
- [ ] **Figür Üretim Scripti** — Her figürü yeniden üreten script

---

## README.md Şablonu

```markdown
# [Makale Başlığı] — Tekrarlama Paketi

## Gereksinimler
- İşletim Sistemi: [Ubuntu 20.04 / macOS 12 / Windows 10]
- Python: 3.XX
- GPU: [gerekli/opsiyonel — model adı]
- Disk: XX GB
- RAM: XX GB

## Kurulum

### Conda ile
```bash
conda env create -f environment.yml
conda activate [env-name]
```

### pip ile
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Veri İndirme
```bash
bash scripts/download_data.sh
```
Beklenen veri boyutu: ~XX GB
Beklenen süre: ~XX dakika

## Deneyleri Çalıştırma

### Ana Deneyi Tekrarlama (Tablo 2)
```bash
python run_experiments.py --config configs/main.yaml
```
Beklenen çalışma süresi: ~XX saat (GPU olmadan: ~XX saat)

### Tek Bir Deneyi Çalıştırma
```bash
python run_experiments.py --config configs/main.yaml --experiment [exp_name]
```

## Beklenen Sonuçlar
| Metrik | Makale | Beklenen Aralık |
|---|---|---|
| Accuracy | 0.923 | 0.920 – 0.926 |
| F1-Macro | 0.918 | 0.915 – 0.921 |

Not: Küçük sayısal farklar kabul edilebilir (±0.005); 
     donanım farklılığı ve kütüphane versiyonundan kaynaklanabilir.

## Sorun Giderme
- [Yaygın hata 1]: [Çözüm]
- [Yaygın hata 2]: [Çözüm]

## Atıf
```bibtex
@article{...}
```
```

---

## Çevre Sabitleme

```bash
# Tam çevre dışa aktarımı
pip freeze > requirements_exact.txt
conda env export > environment_exact.yml

# Platform bağımsız (sadece direkt bağımlılıklar)
pip-compile requirements.in > requirements.txt

# Versiyon doğrulama scripti
python scripts/check_environment.py
```

---

## Artifact Evaluation Badge Kriterleri

Modern konferanslar (NeurIPS, ICML, ACL vb.) üç rozet sunar:

| Rozet | Kriter |
|---|---|
| **Artifacts Available** | Kod ve veri erişilebilir arşivde (Zenodo, GitHub Release) |
| **Artifacts Evaluated — Functional** | Çalışıyor, temel işlevleri doğrulandı |
| **Results Reproduced** | Bağımsız ekip orijinal sonuçları yeniden üretti |

---

## Arşivleme

Uzun süreli erişilebilirlik için:
- **Zenodo**: https://zenodo.org — DOI ataması yapıyor
- **OSF**: https://osf.io — Akademik araştırma odaklı
- **GitHub + Release**: Kod için; veri için LFS kullan
- **HuggingFace Hub**: ML modelleri ve veri setleri için

> ⚠️ GitHub URL'si tek başına yeterli değildir — silinebilir. Zenodo DOI oluşturun.

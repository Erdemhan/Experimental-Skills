---
name: academic-code-release
description: >
  Activate this skill when preparing code for public release alongside an academic 
  paper submission or camera-ready. Combines replication-package (what to include), 
  git-research (versioning), documentation-writer (what to document), and paper 
  structure to produce a self-contained, reproducible research artifact.
---

# Academic Code Release Skill — Akademik Kod Yayını

## Temel Kural
> "Kod mevcuttur, talep üzerine gönderilebilir" kabul edilemez.  
> Kod, paper ile birlikte ve bağımsız olarak çalışabilir olmalıdır.

---

## Yayın Kontrol Listesi

### Temizlik
- [ ] Tüm hardcoded path'ler kaldırıldı (örn. `/home/erdem/data/`)
- [ ] Debug print'ler temizlendi
- [ ] Kullanılmayan import'lar kaldırıldı
- [ ] TODO/FIXME'ler ya çözüldü ya belgelendi
- [ ] Büyük dosyalar (model ağırlıkları, veri) `.gitignore`'da
- [ ] Git geçmişinde hassas veri yok (`git log -S "password"` ile kontrol)

### Tekrarlanabilirlik
- [ ] `requirements.txt` veya `environment.yml` tam ve versiyonlu
- [ ] Tüm seed'ler konfigürasyon dosyasında
- [ ] `reproduce_main_results.sh` veya `reproduce_all.py` çalışıyor
- [ ] Bağımsız bir makinede sıfırdan test edildi

### Dokümantasyon
- [ ] `README.md` Paper kılavuzu içeriyor (aşağıdaki şablon)
- [ ] Her konfigürasyon dosyası comment'li
- [ ] Public fonksiyonların docstring'i var

---

## README.md Şablonu (Akademik Kod)

```markdown
# <Paper Başlığı>

[![Paper](badge)](arxiv_link) [![License: MIT](badge)](LICENSE)

Resmi implementasyon: "**<Paper Tam Başlığı>**"  
<Author 1>, <Author 2> · <Venue> <Year>

> **Özet**: [Paper abstract'ından 1-2 cümle]

---

## Kurulum

```bash
# Conda ile (önerilen)
conda create -n <proje_adi> python=3.11
conda activate <proje_adi>
pip install -r requirements.txt

# veya pip ile
pip install -r requirements.txt
```

**Bağımlılıklar**: Python 3.11, PyTorch 2.1, Ray 2.8, Gymnasium 0.29

---

## Temel Sonuçları Yeniden Üret

```bash
# Tablo 1 — Tüm yöntem karşılaştırması (5 seed × 3 yöntem ≈ 15 saat GPU)
python scripts/reproduce_all.py --table 1

# Şekil 3 — Öğrenme eğrileri (hızlı, 1 seed)
python scripts/reproduce_all.py --figure 3 --quick

# Tek deney çalıştır
python train.py --config configs/ppo_reward_shaped.yaml --seed 42
```

---

## Proje Yapısı

```
├── configs/           ← Deney konfigürasyonları (her deney için bir dosya)
├── src/
│   ├── envs/          ← Özel ortam tanımları
│   ├── algorithms/    ← Algoritma implementasyonları
│   └── utils/         ← Yardımcı araçlar
├── scripts/
│   ├── train.py       ← Tek deney eğitimi
│   ├── evaluate.py    ← Policy değerlendirme
│   └── reproduce_all.py  ← Tüm sonuçları yeniden üret
├── results/           ← Önceden hesaplanmış sonuçlar (figür üretimi için)
├── figures/           ← Üretilen figürler
└── tests/             ← Unit testler
```

---

## Önceden Hesaplanmış Sonuçlar

Tam eğitim yerine önceden hesaplanmış loglardan figür üretmek için:

```bash
# Önceden hesaplanmış sonuçları indir
wget https://zenodo.org/record/XXXXXXX/files/results.zip
unzip results.zip -d results/

# Figürleri üret (eğitim gerekmez)
python scripts/generate_figures.py --results_dir results/
```

---

## Alıntı

```bibtex
@inproceedings{author2026title,
  title     = {<Paper Başlığı>},
  author    = {Author, First and Author, Second},
  booktitle = {<Venue>},
  year      = {2026},
  url       = {https://arxiv.org/abs/XXXX.XXXXX},
}
```

---

## Lisans

MIT License — Bkz. [LICENSE](LICENSE)
```

---

## Git Tag ve Zenodo Arşivleme

```bash
# 1. Camera-ready versiyonunu tag'le
git tag -a "v1.0.0-paper" -m "
Camera-ready code release

Corresponds to: <Paper Title>
Venue: <ICML/NeurIPS/ICLR 2026>
ArXiv: arxiv.org/abs/XXXX.XXXXX

Reproducibility:
  python scripts/reproduce_all.py --table 1
"

git push origin v1.0.0-paper

# 2. GitHub → Releases → "Create release from tag"
# 3. Zenodo bağlantısı varsa otomatik DOI alır
#    (github.com/settings → Zenodo integration)

# 4. README'ye DOI badge ekle
# [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](...)
```

---

## Koda Erişim Beyanı (Paper'a Eklenmeli)

```latex
\section*{Code and Data Availability}
The source code, trained models, and experiment configurations 
are publicly available at \url{https://github.com/username/repo} 
(DOI: \url{https://doi.org/10.5281/zenodo.XXXXXXX}).
All experiments can be reproduced using:
\texttt{python scripts/reproduce\_all.py --paper <venue>-2026}.
```

---

## Gönderim Öncesi Son Kontrol

```bash
# Repo temizliği
git status  # Uncommitted dosya olmamalı
git log --oneline -10  # Geçmiş temiz mi?

# Büyük dosya kontrolü
find . -size +50M -not -path "./.git/*"

# Hassas veri kontrolü
git log --all -S "password" --oneline
git log --all -S "api_key" --oneline

# Sıfırdan kurulum testi (conda clean environment)
conda create -n release_test python=3.11 -y
conda activate release_test
pip install -r requirements.txt
python scripts/reproduce_all.py --quick  # 1 seed, hızlı doğrulama
```

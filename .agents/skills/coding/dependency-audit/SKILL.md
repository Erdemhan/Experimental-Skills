---
name: dependency-audit
description: >
  Activate this skill when adding a new dependency, upgrading packages, or 
  auditing existing dependencies. This skill checks security vulnerabilities, 
  license compatibility, maintenance status, and alternative options before 
  adding any new package.
---

# Dependency Audit Skill — Bağımlılık Denetimi

## Temel Kural
> Her yeni bağımlılık bir risktir. Ekleme kararı bilinçli olmalıdır.

---

## Yeni Bağımlılık Ekleme Kontrol Listesi

### 1. Gerçekten Gerekli Mi?
- [ ] Standart kütüphane ile çözülebilir mi? (önce stdlib bak)
- [ ] Mevcut bağımlılık bu ihtiyacı karşılamıyor mu?
- [ ] 50 satır kod mı yoksa tam kütüphane mi gerekiyor?

### 2. Güvenlik Kontrolü
```bash
# pip-audit ile bilinen zafiyet taraması
pip install pip-audit
pip-audit -r requirements.txt

# Safety ile
pip install safety
safety check -r requirements.txt

# snyk ile
npm install -g snyk  # node yöntemi
snyk test
```

- [ ] Bilinen güvenlik açığı var mı? (CVE)
- [ ] Son güvenlik güncellemesi ne zaman yapıldı?

### 3. Bakım Durumu
```bash
# PyPI istatistiklerini kontrol et
pip show <package_name>

# GitHub activity kontrol et
# → Son commit tarihi, issue'lar, PR'lar, star sayısı
```

| Gösterge | İyi | Dikkat | Kötü |
|---|---|---|---|
| Son commit | < 6 ay | 6-18 ay | > 18 ay |
| Open issues | < 50 | 50-200 | > 200 |
| Maintainer sayısı | 3+ | 1-2 | 0 aktif |
| Star sayısı | 1000+ | 100-1000 | < 100 |
| Download/hafta | 100k+ | 10k-100k | < 10k |

### 4. Lisans Uyumluluğu

```
Lisans Uyumluluk Matrisi (Proje Lisansınıza Göre):

Projeniz MIT/Apache ise:
  ✅ Kullanabilirsiniz: MIT, Apache 2.0, BSD, ISC, CC0
  ⚠️ Dikkatli olun:    LGPL (dinamik link şartları)
  ❌ Kullanmayın:      GPL, AGPL (copyleft)

Projeniz GPL ise:
  ✅ MIT, Apache, BSD, LGPL, GPL
  ❌ AGPL (farklı copyleft koşulları)

Ticari proje:
  ❌ GPL, AGPL (ticari kullanım kısıtları)
```

```bash
# Lisans taraması
pip install pip-licenses
pip-licenses --format=table
```

### 5. Alternatif Karşılaştırma

Paket eklemeden önce alternatiflerle karşılaştır:
```
| Paket     | Stars | Size  | Last Update | License | Seçim Nedeni |
|-----------|-------|-------|-------------|---------|--------------|
| requests  | 51k   | 900KB | 2026-06     | Apache  | De facto std |
| httpx     | 13k   | 1.2MB | 2026-07     | BSD     | Async support|
| aiohttp   | 14k   | 2.1MB | 2026-07     | Apache  | Full async   |
```

---

## Bağımlılık Yönetim Araçları

```bash
# Güncel olmayan paketleri listele
pip list --outdated

# Bağımlılık ağacını görselleştir
pip install pipdeptree
pipdeptree

# Kullanılmayan bağımlılıkları bul
pip install pip-check-reqs
pip-extra-reqs .
pip-missing-reqs .

# requirements.txt sabitle (production güvenliği)
pip freeze > requirements.txt
# veya daha iyi: pip-tools kullan
pip-compile requirements.in --generate-hashes
```

---

## Güvenlik Güncelleme Protokolü

CVE bildirimi alındığında:
1. Etkilenen versiyon aralığını kontrol et
2. Kritiklik skorunu (CVSS) değerlendir
3. Güncelleme veya geçici önlem uygula
4. Test et
5. Deploy et ve log tut

```bash
# Acil güvenlik güncellemesi
pip install --upgrade <vulnerable_package>
pytest  # Regresyon kontrolü
git commit -m "security: update <package> to fix CVE-XXXX-XXXXX"
```

---
name: api-design
description: >
  Activate this skill when designing or reviewing a REST API, gRPC interface, 
  Python library API, or any public interface. This skill enforces consistent 
  naming, versioning strategy, error format standardization, and backward 
  compatibility rules.
---

# API Design Skill — API Tasarımı

## Temel Kural
> Bir API'yi değiştirmek onu tasarlamaktan çok daha pahalıdır. İlk seferinde doğru tasarla.

---

## REST API Kuralları

### URL Yapısı
```
✅ GET    /api/v1/users            # Koleksiyon listele
✅ POST   /api/v1/users            # Yeni oluştur
✅ GET    /api/v1/users/{id}       # Tek kayıt getir
✅ PUT    /api/v1/users/{id}       # Tam güncelleme
✅ PATCH  /api/v1/users/{id}       # Kısmi güncelleme
✅ DELETE /api/v1/users/{id}       # Sil

❌ GET    /api/v1/getUsers         # Fiil kullanma
❌ POST   /api/v1/user/create      # Tekrar fiil
❌ GET    /api/v1/Users            # Büyük harf değil
```

### HTTP Durum Kodları
```
200 OK           — Başarılı GET/PUT/PATCH
201 Created      — Başarılı POST (Location header ile)
204 No Content   — Başarılı DELETE
400 Bad Request  — Geçersiz istek (validation hatası)
401 Unauthorized — Kimlik doğrulanmadı
403 Forbidden    — Yetki yok
404 Not Found    — Kayıt bulunamadı
409 Conflict     — Çakışma (duplike kayıt)
422 Unprocessable— İş kuralı ihlali
429 Too Many Req — Rate limit aşıldı
500 Internal Err — Sunucu hatası (client'a detay verme)
```

### Standart Hata Formatı
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "value": "not-an-email"
      }
    ],
    "request_id": "req_abc123",
    "timestamp": "2026-07-23T14:00:00Z"
  }
}
```

---

## Versiyonlama Stratejisi

```
URL Versiyonlama (Önerilen):  /api/v1/, /api/v2/
Header Versiyonlama:          Accept: application/vnd.api+json;version=2
Query Param:                  /api/users?version=2  (en az tercih edilen)
```

Versiyon yükseltme kuralları:
- **Patch (v1.0 → v1.1)**: Yeni opsiyonel alan ekleme — geriye uyumlu
- **Minor (v1 → v2)**: Kırıcı değişiklikler — yeni endpoint, eski korunur
- **Eski versiyon Deprecation**: En az 6 ay önceden duyur, sunset header ile

---

## Python Library API Tasarımı

```python
# ✅ Açık, tutarlı, tip-annotated
def analyze_sentiment(
    text: str,
    *,  # keyword-only
    language: str = "tr",
    model: str = "default",
    return_scores: bool = False,
) -> str | dict:
    """Analyze sentiment of input text.
    
    Args:
        text: Input text to analyze.
        language: Language code (ISO 639-1). Default: 'tr' (Turkish).
        model: Model identifier. Use 'default' for recommended model.
        return_scores: If True, return score dict instead of label string.
    
    Returns:
        If return_scores=False: One of 'positive', 'negative', 'neutral'.
        If return_scores=True: {'positive': float, 'negative': float, 'neutral': float}
    
    Raises:
        ValueError: If text is empty or language is not supported.
        ModelNotFoundError: If specified model does not exist.
    """
```

---

## API Tasarım Kontrol Listesi

- [ ] URL isimlendirme tutarlı ve fiilsiz mi?
- [ ] HTTP metodları doğru kullanılıyor mu?
- [ ] Hata formatı standart mı?
- [ ] Versiyonlama stratejisi tanımlı mı?
- [ ] Geriye uyumluluk kırılıyor mu? (Breaking change?)
- [ ] Rate limiting tanımlandı mı?
- [ ] Authentication/Authorization şeması tanımlandı mı?
- [ ] Pagination (sayfalama) büyük koleksiyonlarda var mı?
- [ ] OpenAPI/Swagger dökümantasyonu güncel mi?

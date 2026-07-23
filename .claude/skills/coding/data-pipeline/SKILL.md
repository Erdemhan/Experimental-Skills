---
name: data-pipeline
description: >
  Activate this skill when designing or reviewing a data processing pipeline, 
  ETL workflow, or data transformation system. This skill enforces idempotency, 
  schema validation, error handling, and observability patterns for reliable 
  data pipelines.
---

# Data Pipeline Skill — Veri Hattı Tasarımı

## Temel Kural
> Güvenilir bir veri hattı; hata durumunda kayıp verisi değil, tekrar çalıştırılabilir bir kayıt bırakır.

---

## Temel Prensipler

### 1. Idempotency (Yeniden Çalıştırılabilirlik)
```python
# ✅ Idempotent — aynı sonucu verir, duplike oluşturmaz
def upsert_record(record: dict) -> None:
    """Insert or update — safe to run multiple times."""
    db.execute("""
        INSERT INTO records (id, data, updated_at)
        VALUES (%(id)s, %(data)s, NOW())
        ON CONFLICT (id) DO UPDATE SET
            data = EXCLUDED.data,
            updated_at = EXCLUDED.updated_at
    """, record)

# ❌ Non-idempotent — her çalıştırmada duplike oluşturur
def insert_record(record: dict) -> None:
    db.execute("INSERT INTO records (id, data) VALUES (%(id)s, %(data)s)", record)
```

### 2. Schema Validation
```python
from pydantic import BaseModel, validator
from typing import Optional

class InputRecord(BaseModel):
    """Validate pipeline input schema."""
    id: str
    timestamp: datetime
    value: float
    category: str
    
    @validator('value')
    def value_must_be_finite(cls, v):
        if not isfinite(v):
            raise ValueError(f"Non-finite value: {v}")
        return v
    
    @validator('category')
    def category_must_be_valid(cls, v):
        valid = {"A", "B", "C"}
        if v not in valid:
            raise ValueError(f"Invalid category: {v}. Must be one of {valid}")
        return v
```

### 3. Hata Yönetimi Stratejisi
```python
from enum import Enum

class ErrorStrategy(Enum):
    FAIL_FAST = "fail_fast"      # İlk hata → dur
    SKIP_RECORD = "skip"         # Hatalı kaydı atla, devam et
    DEAD_LETTER = "dead_letter"  # Hatalı kaydı ayrı yere yaz, devam et

def process_batch(records: list, strategy: ErrorStrategy = ErrorStrategy.DEAD_LETTER):
    results = []
    errors = []
    
    for record in records:
        try:
            result = transform(record)
            results.append(result)
        except ValidationError as e:
            if strategy == ErrorStrategy.FAIL_FAST:
                raise
            elif strategy == ErrorStrategy.SKIP_RECORD:
                logger.warning("Skipping invalid record %s: %s", record.get('id'), e)
            elif strategy == ErrorStrategy.DEAD_LETTER:
                errors.append({"record": record, "error": str(e)})
    
    if errors:
        write_dead_letter_queue(errors)
    
    return results
```

---

## Pipeline Katmanları

```
[Kaynak]
  ↓ Extract (Çekme)
[Ham Veri] ← Kaynak formatı korunur
  ↓ Validate (Doğrulama)
[Geçerli Kayıtlar] + [Dead Letter]
  ↓ Transform (Dönüşüm)
[İşlenmiş Veri]
  ↓ Load (Yükleme)
[Hedef]
  ↓ Verify (Doğrulama)
[Kontrol Metrikleri]
```

---

## Observability (Gözlemlenebilirlik)

```python
import time
from contextlib import contextmanager
from dataclasses import dataclass

@dataclass
class PipelineMetrics:
    total_records: int = 0
    processed: int = 0
    skipped: int = 0
    failed: int = 0
    duration_s: float = 0.0

@contextmanager
def pipeline_run(name: str):
    metrics = PipelineMetrics()
    start = time.time()
    try:
        yield metrics
    finally:
        metrics.duration_s = time.time() - start
        logger.info(
            "Pipeline '%s' completed: total=%d, ok=%d, skip=%d, fail=%d, time=%.2fs",
            name, metrics.total_records, metrics.processed, 
            metrics.skipped, metrics.failed, metrics.duration_s
        )

# Kullanım
with pipeline_run("daily_etl") as metrics:
    for record in source.read():
        metrics.total_records += 1
        try:
            process(record)
            metrics.processed += 1
        except Exception:
            metrics.failed += 1
```

---

## Pipeline Kontrol Listesi

- [ ] Idempotent mi? (Tekrar çalıştırılabilir)
- [ ] Schema validation var mı?
- [ ] Dead letter queue tanımlı mı?
- [ ] Checkpoint/resume mekanizması var mı? (büyük veri için)
- [ ] Metrikler loglanıyor mu? (başarılı, başarısız, atılan kayıt sayısı)
- [ ] Backpressure yönetimi var mı? (kaynak hızlı, hedef yavaşsa)
- [ ] Veri tutarlılığı kontrolleri yapılıyor mu? (kayıt sayısı, checksum)
- [ ] Test: küçük örnekle unit test, tam veriyle smoke test yapıldı mı?

---
name: unit-test-design
description: >
  Activate this skill when writing unit tests, reviewing test coverage, designing 
  test strategies, or setting up testing infrastructure. This skill enforces 
  Arrange-Act-Assert pattern, test isolation, meaningful assertions, and systematic 
  edge case coverage.
---

# Unit Test Design Skill — Unit Test Tasarımı

## Temel Kural
> Test, ürün kodundan önce düşünülür. Test olmayan kod teslim edilmiş değildir.

---

## Arrange — Act — Assert (AAA) Yapısı

Her test fonksiyonu bu 3 adımı net olarak içermelidir:

```python
def test_calculate_mean_with_positive_numbers():
    """Test that mean is calculated correctly for positive numbers."""
    # Arrange — Test için gerekli veriler ve bağımlılıklar hazırla
    numbers = [1.0, 2.0, 3.0, 4.0, 5.0]
    expected_mean = 3.0

    # Act — Test edilen fonksiyonu çalıştır
    result = calculate_mean(numbers)

    # Assert — Beklenen sonucu doğrula
    assert result == pytest.approx(expected_mean), (
        f"Expected mean={expected_mean}, got {result}"
    )
```

---

## Test Kategorileri

### 1. Happy Path Tests
Normal, beklenen girdilerle doğru çalışma:
```python
def test_addition_with_positive_integers():
    assert add(2, 3) == 5
```

### 2. Edge Case Tests
Sınır değerleri ve özel durumlar:
```python
def test_addition_with_zero():
    assert add(0, 5) == 5

def test_addition_with_negative_numbers():
    assert add(-2, -3) == -5
```

### 3. Error/Exception Tests
Hata durumlarının doğru fırlatılması:
```python
def test_division_raises_on_zero_divisor():
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(10, 0)

def test_empty_list_raises_value_error():
    with pytest.raises(ValueError, match="Cannot calculate mean of empty list"):
        calculate_mean([])
```

### 4. Parametrize Tests
Benzer testleri tekrarsız gruplama:
```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
    (100, -50, 50),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

---

## Mock ve Fixture Kullanımı

### Fixture — Ortak Setup
```python
import pytest

@pytest.fixture
def sample_data():
    """Shared test data fixture."""
    return {
        "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
        "config": {"threshold": 0.5}
    }

def test_process_users(sample_data):
    result = process_users(sample_data["users"])
    assert len(result) == 2
```

### Mock — Dış Bağımlılık İzolasyonu
```python
from unittest.mock import patch, MagicMock

def test_api_call_uses_correct_endpoint():
    with patch("mymodule.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        mock_get.return_value.status_code = 200
        
        result = fetch_data("https://api.example.com/data")
        
        mock_get.assert_called_once_with(
            "https://api.example.com/data",
            timeout=30
        )
        assert result == {"status": "ok"}
```

---

## Test İsimlendirme Konvansiyonu

```python
# Format: test_[unit]_[scenario]_[expected_behavior]

def test_calculate_mean_with_empty_list_raises_value_error():  ✅
def test_mean():  ❌ — çok belirsiz
def test_empty():  ❌ — ne boş?
def testMean():   ❌ — camelCase değil snake_case

# Sınıf bazlı (daha iyi organizasyon için):
class TestCalculateMean:
    def test_with_positive_numbers_returns_correct_mean(self): ...
    def test_with_empty_list_raises_value_error(self): ...
    def test_with_single_element_returns_that_element(self): ...
```

---

## Test Kapsam Kontrol Listesi

Her fonksiyon için şunlar test edilmeli:
- [ ] Normal girdi ile doğru çıktı
- [ ] Boş/None girdi
- [ ] Sınır değerleri (min, max)
- [ ] Hata durumları (her `raise` ifadesi)
- [ ] Dönüş tipi doğruluğu
- [ ] Yan etkiler (dosya yazımı, DB, vb. — mock ile)

```bash
# Kapsam ölçümü
pytest --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## Anti-Pattern'ler

| Anti-Pattern | Örnek | Düzeltme |
|---|---|---|
| Birden fazla şey test etme | `assert len(x) > 0 and x[0] == 5` | Ayrı test fonksiyonları |
| Belirsiz assertion | `assert result` | `assert result == expected_value` |
| Test içinde mantık | `if condition: assert ...` | Parametrize kullan |
| Magic number | `assert result == 42` | `expected = 42; assert result == expected` |
| Sleep kullanımı | `time.sleep(1)` | Mock time veya async test |
| Global state | Test'ler birbirine bağlı | Fixture ile izole et |

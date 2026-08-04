# Git Hooks Şablonları

Bu dizin `~/.claude/templates/git-hooks/` olarak kurulur (proje içine
kopyalanmaz — kaynak tek yerde durur). Herhangi bir proje kök dizininden
buradaki hook'ları kendi `.git/hooks/`'una yükleyebilir.

## Kurulum

### Otomatik (Önerilen) — tek komutla hepsi
```bash
# Proje kök dizininde, .git/ zaten varsa:
python3 ~/.claude/scripts/startup_project.py
```
Bu, `.gitignore`'u da kopyalar ve aşağıdaki `install_hooks.py`'yi otomatik
çalıştırır. Sadece git hook'larını tekrar kurmak istiyorsan:
```bash
python3 ~/.claude/templates/git-hooks/install_hooks.py
```

### Manuel
```bash
cp ~/.claude/templates/git-hooks/commit-msg .git/hooks/commit-msg
cp ~/.claude/templates/git-hooks/pre-commit .git/hooks/pre-commit
cp ~/.claude/templates/git-hooks/pre-push   .git/hooks/pre-push
chmod +x .git/hooks/commit-msg .git/hooks/pre-commit .git/hooks/pre-push
```

### pre-commit framework ile (Daha Güçlü)
```bash
pip install pre-commit
cp ~/.claude/templates/.pre-commit-config.yaml .pre-commit-config.yaml
pre-commit install
pre-commit install --hook-type commit-msg  # commit-msg hook'u da ekle
```

### .gitignore Şablonunu Kopyalama
```bash
cp ~/.claude/templates/.gitignore .gitignore
```

---

## Hook'lar

| Hook | İşlev |
|---|---|
| `commit-msg` | Conventional Commits formatını zorunlu kılar |
| `pre-commit` | ruff, black, büyük dosya, gizli anahtar kontrolü |
| `pre-push` | WIP commit, main'e doğrudan push uyarısı |

## Commit Tipler (Bu Proje İçin)

| Tip | Kullanım |
|---|---|
| `feat` | Yeni özellik |
| `fix` | Hata düzeltme |
| `docs` | Dokümantasyon |
| `refactor` | Düzenleme |
| `test` | Test |
| `chore` | Bakım |
| `exp` | Akademik deney |
| `data` | Veri işleme |
| `result` | Sonuç, figür, rapor |

## Örnekler

```bash
git commit -m "exp(ppo): add reward shaping with potential function"
git commit -m "result(ablation): seed 42-1024 all runs complete"
git commit -m "data(env): add 500 new training scenarios"
git commit -m "fix(trainer): handle NaN loss at epoch 5"
```

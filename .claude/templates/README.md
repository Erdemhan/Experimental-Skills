# Git Hooks Şablonları

Bu dizin, herhangi bir projeye kopyalanabilecek Git hook şablonları içerir.

## Kurulum

### Otomatik (Önerilen)
```bash
# Proje kök dizininde:
python3 .claude/templates/git-hooks/install_hooks.py
```

### Manuel
```bash
cp .claude/templates/git-hooks/commit-msg .git/hooks/commit-msg
cp .claude/templates/git-hooks/pre-commit .git/hooks/pre-commit
cp .claude/templates/git-hooks/pre-push   .git/hooks/pre-push
chmod +x .git/hooks/commit-msg .git/hooks/pre-commit .git/hooks/pre-push
```

### pre-commit framework ile (Daha Güçlü)
```bash
pip install pre-commit
cp .claude/templates/.pre-commit-config.yaml .pre-commit-config.yaml
pre-commit install
pre-commit install --hook-type commit-msg  # commit-msg hook'u da ekle
```

### .gitignore Şablonunu Kopyalama
```bash
cp .claude/templates/.gitignore .gitignore
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

# Contribuição

## Pré-requisitos

- Python 3.11+
- `uv` instalado (preferencial)

## Fluxo recomendado

```bash
git checkout -b feat/minha-mudanca
uv sync
uv run --no-project python -m py_compile app.py
```

## Padrões

- Python com 4 espaços de indentação
- `snake_case` para funções/variáveis
- Constantes em `UPPER_CASE`

## Pull Request

Inclua sempre:

- Objetivo da mudança
- Como validar localmente
- Screenshot/GIF em mudanças visuais
- Impactos em deploy (se houver)

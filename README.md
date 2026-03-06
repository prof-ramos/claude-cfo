---
title: PMDF CFO 2025 - Dashboard de Estudos
emoji: 🎖️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# 🎖️ PMDF – CFO 2025 | Dashboard de Estudos

[![Tests](https://github.com/prof-ramos/claude-cfo/actions/workflows/test.yml/badge.svg)](https://github.com/prof-ramos/claude-cfo/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/prof-ramos/claude-cfo/graph/badge.svg)](https://codecov.io/gh/prof-ramos/claude-cfo)

Dashboard em Streamlit para acompanhar progresso por disciplina e tópico do edital PMDF CFO 2025.

## Quick Start

### Com `uv` (recomendado)

```bash
uv sync
uv run streamlit run app.py
```

### Alternativa sem `uv`

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Features

- Controle de estudo por checkbox em cada tópico
- Filtro por status (`Todas`, `Pendentes`, `Concluídas`)
- Filtro por disciplina na sidebar
- Métricas no topo em modo `Filtro` ou `Global`
- Persistência local automática em `progress.json`

## Configuração

| Variável/Arquivo | Descrição | Padrão |
|---|---|---|
| `PROGRESS_FILE` (`app.py`) | Arquivo de persistência | `progress.json` |
| `PORT` (Docker/Space) | Porta do Streamlit | `7860` |

## Documentação

- [Arquitetura](./docs/architecture.md)
- [Contribuição](./docs/contributing.md)
- [Changelog](./CHANGELOG.md)
- [Plano de UI (Mermaid)](./docs/plans/2026-03-06-sidebar-filtros-design.md)

## API Reference

Este projeto não expõe API HTTP pública; toda a interação ocorre na interface Streamlit.

## Contribuindo

1. Crie branch a partir de `main`
2. Rode `uv run --no-project python -m py_compile app.py`
3. Abra PR com descrição, validação e screenshots quando houver mudança visual

Detalhes completos em [docs/contributing.md](./docs/contributing.md).

## License

Uso educacional/pessoal. Defina licença formal antes de distribuição comercial.

# Repository Guidelines

## Project Structure & Module Organization
Este repositório é um app Streamlit simples e direto:
- `app.py`: aplicação principal (UI, estado e persistência em `progress.json`).
- `script.py`: script gerador que recria `app.py`, `pyproject.toml` e `README.md`.
- `pyproject.toml`: metadados e dependências Python.
- `README.md`: instruções rápidas de execução.
- `progress.json`: arquivo local gerado em runtime (progresso do usuário).

Mantenha novos módulos utilitários na raiz apenas se forem pequenos; para expansão maior, crie pastas como `src/` e `tests/`.

## Build, Test, and Development Commands
Use `uv` como padrão e garanta o ambiente virtual configurado:
- `uv sync`: cria/atualiza `.venv` e instala dependências.
- `uv run streamlit run app.py`: inicia o dashboard local.
- `uv run python script.py`: regenera arquivos-base do projeto.
- `uv run python -m py_compile app.py`: valida sintaxe rapidamente.

Exemplo de fluxo local:
```bash
uv sync
uv run streamlit run app.py
```

## Coding Style & Naming Conventions
- Python 3.11+ com 4 espaços por indentação.
- Siga PEP 8 (linhas legíveis, funções curtas e nomes descritivos).
- Use `snake_case` para funções/variáveis e `UPPER_CASE` para constantes (ex.: `PROGRESS_FILE`).
- Prefira tipagem e funções puras para lógica de cálculo quando adicionar novas features.

## Testing Guidelines
Atualmente não há suíte de testes automatizados. Para contribuições:
- Faça teste manual com `uv run streamlit run app.py`.
- Verifique persistência: marcar/desmarcar tópicos e reiniciar app.
- Ao introduzir lógica nova, adicione `pytest` e crie testes em `tests/test_*.py`.

## Commit & Pull Request Guidelines
Não há histórico Git disponível neste diretório para inferir padrão prévio. Adote este padrão:
- Commits no imperativo e curtos, preferencialmente Conventional Commits (`feat:`, `fix:`, `docs:`).
- PRs devem incluir: objetivo, impacto funcional, passos de validação e screenshots da UI quando houver mudança visual.
- Evite PRs grandes; prefira mudanças pequenas e revisáveis.

## Security & Configuration Tips
- Não versione dados pessoais em `progress.json`.
- Revise dependências no `pyproject.toml` antes de atualizar versões.
- Para configuração futura, use variáveis de ambiente e documente no `README.md`.

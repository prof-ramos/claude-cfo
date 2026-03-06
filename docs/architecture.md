# Arquitetura

## Visão Geral

Aplicação monolítica em Streamlit (`app.py`) com estado em memória de sessão e persistência em JSON local.

## Componentes

- `app.py`: UI, regras de filtro, métricas e escrita de progresso.
- `progress.json`: armazenamento local de marcações do usuário.
- `Dockerfile`: execução no Hugging Face Spaces (SDK Docker).
- `requirements.txt`: dependências mínimas para runtime.

## Fluxo de Dados

1. App inicia e carrega `progress.json`.
2. Usuário interage com filtros/checkboxes.
3. Estado em `st.session_state` é atualizado.
4. Alterações são salvas em `progress.json`.
5. Interface renderiza grupos/tópicos conforme filtros ativos.

## Decisões

- UI guiada por estado único (`ui_status_filter`, `ui_selected_discipline`, `ui_metrics_mode`).
- Deploy em HF via Docker para compatibilidade estável.

# 🎖️ PMDF – CFO 2025 | Dashboard de Estudos

## Como rodar

### Com `uv` (recomendado)

```bash
# 1. Crie o ambiente virtual e instale as dependências
uv sync

# 2. Rode o app
uv run streamlit run app.py
```

### Alternativa sem uv
```bash
pip install streamlit
streamlit run app.py
```

## Funcionalidades

- ✅ Checkbox por tópico — marque o que já estudou
- 📊 Barra de progresso por disciplina (sidebar + card)
- 📈 Progresso geral do edital em tempo real
- 💾 Persistência automática em `progress.json`
- 🗑️ Botão para resetar tudo
- 🎨 Cor distinta por disciplina

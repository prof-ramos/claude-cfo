# Testes E2E com AppTest (Streamlit)

Testes End-to-End usando **AppTest**, o framework oficial de testes do Streamlit.

## 📖 Sobre AppTest

**AppTest** (`streamlit.testing.v1.AppTest`) é o framework oficial de testes do Streamlit, disponível desde a versão 1.32.0.

**Vantagens sobre Playwright/Selenium:**
- ✅ Mais rápido (não requer navegador real)
- ✅ Integrado nativamente com Streamlit
- ✅ Melhor para CI/CD (menor uso de recursos)
- ✅ Não requer instalação de browsers
- ✅ API Python nativa

## 🚀 Quick Start

### Executar todos os testes E2E
```bash
uv run pytest tests/e2e/ -v
```

### Executar teste específico
```bash
uv run pytest tests/e2e/test_topic_checkboxes.py -v
```

### Executar com coverage
```bash
uv run pytest tests/e2e/ --cov=app --cov-report=term-missing
```

## 📁 Estrutura

```
tests/e2e/
├── __init__.py                 # Marcação de pacote
├── conftest.py                 # Fixtures pytest
├── test_topic_checkboxes.py    # Testes de checkboxes
├── test_filters.py             # Testes de filtros
├── test_edge_cases.py          # Testes de edge cases
└── README.md                   # Este arquivo
```

## 🔧 Fixtures

### `app_test`
Fixture principal que inicializa o AppTest com um arquivo de progresso isolado.

```python
def test_example(app_test):
    at = app_test.run()
    # ... teste aqui
```

### `known_topic_key`
Retorna uma key de tópico conhecido do EDITAL.

```python
def test_example(known_topic_key):
    print(known_topic_key)  # "Língua Portuguesa||1 Compreensão..."
```

### `known_checkbox_key`
Retorna a key de checkbox correspondente ao tópico conhecido.

```python
def test_example(known_checkbox_key):
    at = app_test.run()
    at.checkbox[known_checkbox_key].check().run()
```

## 📝 Padrões de Widget Keys

### Checkboxes
```python
# Padrão: cb_{disciplina}||{tópico}
cb_Língua Portuguesa||1 Compreensão e interpretação de textos de gêneros variados

# Uso
at.checkbox[key].check().run()
at.checkbox[key].uncheck().run()
at.checkbox[key].value  # True/False
```

### Sidebar Buttons (Disciplinas)
```python
# Padrão: disc_filter_{disciplina}
disc_filter_Língua Portuguesa

# Uso
at.sidebar.button[key].click().run()
```

### Sidebar Radio (Status)
```python
# Sem key explícita (usar índice)
list(at.sidebar.radio)[0].set_value("Pendentes").run()
```

## ⚠️ Critical Architecture Notes

### Isolamento de PROGRESS_FILE

`PROGRESS_FILE` é uma **constante de módulo** (`app.py:31`) avaliada no import.

```python
# app.py:31
PROGRESS_FILE = resolve_progress_file()  # Avaliado no import
```

Como `AppTest.from_file()` carrega o app em subprocesso isolado, `monkeypatch.setattr` **não funciona**.

**Solução:** Usar variável de ambiente:
```python
monkeypatch.setenv("PROGRESS_FILE", str(progress_file))
```

A função `resolve_progress_file()` verifica `os.getenv("PROGRESS_FILE")` **primeiro** (`app.py:8-10`), então essa abordagem funciona corretamente.

### Keys Dinâmicas

Widgets têm keys dinâmicas baseadas no conteúdo:
- Checkboxes usam `f"cb_{topic_key}"` onde `topic_key = f"{disc}||{topic}"`
- Botões de disciplina usam `f"disc_filter_{disciplina}"`

**IMPORTANTE:** Sempre usar keys explícitas em vez de índices para evitar quebras em mudanças de ordem.

## 📊 Cobertura Atual

| Suite | Testes | Status |
|-------|--------|--------|
| `test_topic_checkboxes.py` | 6 | ✅ |
| `test_filters.py` | 9 | ✅ |
| `test_edge_cases.py` | 7 | ✅ |
| **Total** | **22** | ✅ |

## 🐛 Troubleshooting

### Erro: "KeyError: 'app'"
Se ocorrer `KeyError: 'app'`, adicione:
```python
if 'app' in sys.modules:
    del sys.modules['app']
```
Antes de criar uma nova instância de `AppTest`.

### Checkbox não encontrado
Verifique se a key segue exatamente o padrão `cb_{disciplina}||{tópico}`. O nome do tópico deve ser **idêntico** ao que está no `EDITAL` em `app.py`.

## 📚 Referências

- [Streamlit App Testing Documentation](https://docs.streamlit.io/develop/concepts/app-testing)
- [AppTest Cheat Sheet](https://docs.streamlit.io/develop/concepts/app-testing/cheat-sheet)
- [AppTest API Reference](https://docs.streamlit.io/develop/concepts/app-testing/api)

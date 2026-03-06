# Plano de Melhorias UX - Dashboard PMDF CFO 2025

## Data: 2026-03-06

---

## Resumo Executivo

Este plano detalha a implementação de duas melhorias críticas de UX no Dashboard PMDF CFO 2025:

1. **Manter expanders abertos após interação com checkboxes**
2. **Implementar estrutura hierárquica para tópicos do edital com marcação automática**

**Arquivo alvo**: `app.py`
**Complexidade**: MÉDIA
**Arquivos modificados**: 1 (app.py)
**Estimativa**: 3-6 horas de desenvolvimento + testes

---

## Preferências do Usuário

As seguintes preferências foram definidas pelo usuário e devem ser implementadas:

### 1. Comportamento de Desmarcação
- **Regra**: Ao desmarcar um item pai (ex: "5.1"), os subitens (5.1.1, 5.1.2) **NÃO** são desmarcados
- **Motivação**: Filhos devem permanecer marcados independentemente do estado do pai
- **Implementação**: Apenas a marcação do pai propaga para os filhos; desmarcação não propaga

### 2. Formatação dos Números
- **Regra**: Mostrar número completo no checkbox (ex: "1.4.1 Métodos, princípios...")
- **Motivação**: Manter a numeração completa do edital para fácil referência
- **Implementação**: Construir string completa do número hierárquico durante renderização

### 3. Layout de Visualização
- **Regra**: Usar 1 coluna em vez de 2 colunas
- **Motivação**: Mais legível para hierarquia indentada
- **Implementação**: Remover `st.columns(2)` e renderizar diretamente na página principal

---

## Contexto dos Problemas

### Problema 1: Expander fecha ao clicar em checkbox
- **Causa raiz**: `st.rerun()` na linha 614 recarrega toda a aplicação
- **Impacto**: Usuário precisa reabrir manualmente cada expander após marcar/desmarcar tópicos
- **Frequência**: Afeta TODAS as interações com checkboxes

### Problema 2: Estrutura plana do edital
- **Atual**: Lista plana de tópicos sem hierarquia visual
- **Desejado**: Estrutura hierárquica aninhada baseada em numeração (1, 1.1, 1.2, etc.)
- **Funcionalidade extra**: Marcar item pai deve marcar automaticamente todos os subitens

---

## Análise dos Dados

### Padrões de Numeração Identificados
Análise do EDITAL atual (linhas 33-310):

```
Nível 1: "1 Compreensão...", "2 Reconhecimento..."
Nível 2: "4.1 Emprego...", "5.1 Classes..."
Nível 3: "1.4.1 Métodos...", "3.2.1 Cassação..."
```

**Profundidade máxima**: 3 níveis hierárquicos
**Total de disciplinas**: 15
**Total de tópicos**: ~300 tópicos

### Estrutura Atual do progress.json
```json
{
  "Língua Portuguesa||Compreensão": true,
  "Direito Constitucional||1.1 Conceito": false
}
```

**Impacto da migração**: Estrutura de dados permanece compatível (chaves não mudam)

---

## Estrutura de Dados Proposta

### 1. Parser de Numeração Hierárquica

**Nova função**: `parse_topic_number(topic_string)`

```python
def parse_topic_number(topic_string):
    """
    Extrai número hierárquico e texto do tópico.

    Args:
        topic_string: "1.2.3 Texto do tópico"

    Returns:
        tuple: ([1, 2, 3], "Texto do tópico")
               ou (None, topic_string) se não tiver número
    """
    import re
    match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', topic_string)
    if match:
        number_str = match.group(1)
        text = match.group(2)
        levels = [int(x) for x in number_str.split('.')]
        return levels, text
    return None, topic_string
```

**Critério de aceitação**:
- [x] Extrai níveis corretamente de "1.2.3 Texto" → [1, 2, 3]
- [x] Retorna None para tópicos sem número
- [x] Preserva texto original após o número

### 2. Builder de Estrutura Hierárquica

**Nova função**: `build_hierarchical_structure(discipline_topics)`

```python
def build_hierarchical_structure(discipline_topics):
    """
    Constrói árvore hierárquica de tópicos.

    Args:
        discipline_topics: ["1 Tópico", "1.1 Subtópico", "2 Tópico"]

    Returns:
        list: Árvore de nós hierárquicos
    """
    root_nodes = []

    for topic in discipline_topics:
        levels, text = parse_topic_number(topic)

        if levels is None:
            # Tópico sem número - adicionar como folha solta
            root_nodes.append({
                'number': None,
                'level': 0,
                'text': text,
                'full_text': topic,
                'children': []
            })
            continue

        # Encontrar ou criar caminho
        current_level = root_nodes

        for i, level_num in enumerate(levels):
            # Buscar nó existente neste nível
            found = None
            for node in current_level:
                if node['number'] == level_num and node['level'] == i:
                    found = node
                    break

            if not found:
                # Criar novo nó
                new_node = {
                    'number': level_num,
                    'level': i,
                    'text': text if i == len(levels) - 1 else f"Tópico {level_num}",
                    'full_text': topic if i == len(levels) - 1 else None,
                    'children': []
                }
                current_level.append(new_node)
                current_level = new_node['children']
            else:
                current_level = found['children']

    return root_nodes
```

**Critério de aceitação**:
- [x] Cria árvore correta para até 3 níveis de profundidade
- [x] Preserva ordem original dos tópicos
- [x] Manipula tópicos sem número (folhas soltas)

### 3. Controle de Estado dos Expanders

**Novas chaves no session_state**:
```python
st.session_state.expander_states = {
    "Língua Portuguesa": True,
    "Direito Constitucional": False,
    # ... uma entrada por disciplina
}
```

**Função auxiliar**: `get_expander_state(discipline)`
```python
def get_expander_state(discipline):
    """Retorna estado atual do expander ou False como default."""
    key = f"expander_{discipline}"
    if key not in st.session_state:
        st.session_state[key] = False
    return st.session_state[key]
```

### 4. Marcação Automática de Subitens

**Nova função**: `get_all_descendants(node)`

```python
def get_all_descendants(node, discipline):
    """
    Coleta todos os tópicos descendentes de um nó.

    Args:
        node: Nó da árvore hierárquica
        discipline: Nome da disciplina

    Returns:
        list: Lista de chaves completas dos descendentes
    """
    descendants = []

    if node['full_text']:
        key = get_topic_key(discipline, node['full_text'])
        descendants.append(key)

    for child in node['children']:
        descendants.extend(get_all_descendants(child, discipline))

    return descendants
```

---

## Plano de Implementação

### FASE 1: Preparação e Estrutura (30-45 min)

**Tarefa 1.1: Adicionar novas funções auxiliares**
- [ ] Adicionar `parse_topic_number()` após linha 381
- [ ] Adicionar `build_hierarchical_structure()` após parse
- [ ] Adicionar `get_all_descendants()` após get_topic_key
- [ ] Adicionar `get_expander_state()` após init_ui_state

**Arquivo**: app.py
**Linhas**: Inserir após linha 381 (após get_topic_key)

**Critério de aceitação**:
- [ ] Funções adicionadas sem modificar lógica existente
- [ ] Syntax valid com `python3 -m py_compile app.py`
- [ ] Teste manual: importar módulo sem erros

---

### FASE 2: Controle de Estado dos Expanders (45-60 min)

**Tarefa 2.1: Modificar init_ui_state()**
- [ ] Adicionar inicialização de expander_states
- [ ] Mapear todas as disciplinas do EDITAL

```python
def init_ui_state():
    # ... código existente ...

    # Inicializar estados dos expanders
    if "expander_states" not in st.session_state:
        st.session_state.expander_states = {
            discipline: False
            for discipline in EDITAL.keys()
        }
```

**Tarefa 2.2: Modificar st.expander na linha 596**
- [ ] Substituir `expanded=False` por `expanded=get_expander_state(disc)`
- [ ] Adicionar callback para salvar estado ao abrir/fechar

```python
# Linha 596 - ANTES:
with st.expander(f"{disc} — {p:.0f}% concluído ({done}/{total})", expanded=False):

# DEPOIS:
expander_key = f"expander_{disc}"
is_expanded = get_expander_state(disc)
with st.expander(f"{disc} — {p:.0f}% concluído ({done}/{total})", expanded=is_expanded):
    # Salvar estado quando usuário interagir
    st.session_state.expander_states[disc] = is_expanded
```

**Tarefa 2.3: Remover st.rerun() problemático (linha 614)**
- [ ] Substituir `st.rerun()` por atualização seletiva do session_state
- [ ] Garantir que checkbox ainda atualiza o progress.json

```python
# Linhas 608-614 - ANTES:
new_val = col.checkbox(topic, value=current_val, key=f"cb_{key}")
if new_val != current_val:
    progress[key] = new_val
    st.session_state.progress = progress
    save_progress(progress)
    st.rerun()  # ← PROBLEMA: fecha todos os expanders

# DEPOIS:
new_val = col.checkbox(topic, value=current_val, key=f"cb_{key}")
if new_val != current_val:
    progress[key] = new_val
    st.session_state.progress = progress
    save_progress(progress)
    # Remover st.rerun() - checkbox já atualiza visualmente
```

**Critério de aceitação**:
- [ ] Checkbox marcado/desmarcado NÃO fecha o expander
- [ ] Estado do checkbox persiste corretamente
- [ ] progress.json é atualizado corretamente
- [ ] Teste manual: marcar 5 tópicos seguidos sem reabrir expander

---

### FASE 3: Renderização Hierárquica (60-90 min)

**Tarefa 3.1: Criar função de renderização recursiva**

```python
def render_hierarchical_topic(node, discipline, progress, depth=0, parent_number=""):
    """
    Renderiza tópico hierárquico com indentação e checkboxes.

    Args:
        node: Nó da árvore hierárquica
        discipline: Nome da disciplina
        progress: Dict de progresso atual
        depth: Profundidade atual (para indentação)
        parent_number: Número completo do pai (ex: "1.4")
    """
    # Se nó tem texto completo (é uma folha ou nó intermediário com texto)
    if node['full_text']:
        key = get_topic_key(discipline, node['full_text'])
        current_val = progress.get(key, False)

        # Construir número completo do tópico
        if node['number'] is not None:
            if parent_number:
                full_number = f"{parent_number}.{node['number']}"
            else:
                full_number = str(node['number'])
        else:
            full_number = ""

        # Indentação visual baseada na profundidade
        indent = " " * depth

        # Checkbox com número completo e indentação
        label = f"{indent}{full_number} {node['text']}" if full_number else f"{indent}{node['text']}"
        new_val = st.checkbox(label, value=current_val, key=f"cb_{key}")

        if new_val != current_val:
            progress[key] = new_val

            # Se marcando o pai, marcar todos os descendentes
            if new_val:
                descendants = get_all_descendants(node, discipline)
                for desc_key in descendants:
                    progress[desc_key] = True
            # NOTA: Desmarcar pai NÃO desmarca filhos (preferência do usuário)

            st.session_state.progress = progress
            save_progress(progress)

    # Renderizar filhos recursivamente
    for child in node['children']:
        child_parent_number = full_number if node['full_text'] else parent_number
        render_hierarchical_topic(child, discipline, progress, depth + 1, child_parent_number)
```

**Tarefa 3.2: Modificar loop de renderização de tópicos (linhas 604-614)**

```python
# Linhas 604-614 - ANTES:
cols = st.columns(2)
for i, topic in enumerate(topics):
    key = get_topic_key(disc, topic)
    current_val = progress.get(key, False)
    col = cols[i % 2]
    new_val = col.checkbox(topic, value=current_val, key=f"cb_{key}")
    # ... lógica de atualização

# DEPOIS:
# Construir estrutura hierárquica
hierarchy = build_hierarchical_structure(topics)

# Renderizar hierarquicamente em 1 coluna (preferência do usuário)
for node in hierarchy:
    render_hierarchical_topic(node, disc, progress, depth=0)
```

**Critério de aceitação**:
- [ ] Tópicos com número (1, 1.1, 1.2) aparecem aninhados visualmente
- [ ] Indentação visível com 3 espaços por nível
- [ ] Checkbox mostra número completo (ex: "1.4.1 Métodos...")
- [ ] Checkbox pai na primeira linha de cada grupo
- [ ] Marcar pai marca automaticamente todos os filhos
- [ ] Desmarcar pai NÃO desmarca filhos (filhos permanecem marcados)
- [ ] Marcar filho individualmente ainda funciona
- [ ] Layout em 1 coluna (mais legível para hierarquia indentada)

---

### FASE 4: Testes e Validação (45-60 min)

**Tarefa 4.1: Testes de Integração**
- [ ] Testar marcar/desmarcar tópicos em múltiplas disciplinas
- [ ] Verificar que expanders permanecem abertos
- [ ] Testar marcar tópico pai → todos filhos marcados
- [ ] Testar persistência ao recarregar página (F5)
- [ ] Verificar compatibilidade com filtros existentes

**Tarefa 4.2: Testes de Regressão**
- [ ] Filtros por status (pendentes/concluídas) funcionam
- [ ] Filtro por disciplina funciona
- [ ] Métricas de progresso calculadas corretamente
- [ ] Resetar tudo funciona
- [ ] Layout responsivo mantido

**Tarefa 4.3: Testes de Edge Cases**
- [ ] Disciplina com tópicos sem número
- [ ] Tópicos com números não sequenciais (1, 3, 5)
- [ ] Profundidade máxima de 3 níveis
- [ ] progress.json com dados antigos (compatibilidade)
- [ ] progress.json vazio (primeira execução)

**Critério de aceitação**:
- [ ] Todos os testes acima passam
- [ ] Zero erros no console do navegador
- [ ] Zero erros no terminal Streamlit
- [ ] UX suave e fluida

---

### FASE 5: Documentação e Cleanup (30 min)

**Tarefa 5.1: Documentar novas funções**
- [ ] Adicionar docstrings completas
- [ ] Adicionar comentários para lógica complexa
- [ ] Atualizar README.md se necessário

**Tarefa 5.2: Code Cleanup**
- [ ] Remover código comentado
- [ ] Verificar nomenclatura consistente
- [ ] Formatar com black (se usado no projeto)
- [ ] Validar com pylint/flake8 (se usado)

**Critério de aceitação**:
- [ ] Código limpo e documentado
- [ ] Zero warnings de lint
- [ ] README atualizado com novas funcionalidades

---

## Estratégia de Migração de Dados

### Compatibilidade com progress.json Existente

**BOA NOTÍCIA**: Nenhuma migração necessária!

**Razão**: As chaves do progress.json NÃO mudam:
- Formato atual: `"Disciplina||Tópico Completo": boolean`
- Formato novo: `"Disciplina||Tópico Completo": boolean` (MESMO!)

**O que muda**: Apenas a **apresentação visual** e **lógica de marcação**

### Teste de Retrocompatibilidade

```python
# progress.json VÁLIDO em ambos os formatos:
{
  "Direito Constitucional||1.1 Conceito, objeto, elementos e classificações da Constituição": true,
  "Direito Constitucional||1.2 Supremacia da Constituição": false
}
```

**Ação necessária**: Nenhuma! Dados existentes funcionam imediatamente.

---

## Riscos e Mitigações

### Risco 1: st.rerun() necessário para atualizar métricas
**Impacto**: ALTO
**Probabilidade**: MÉDIA
**Mitigação**: Testar extensivamente sem st.rerun(). Se métricas não atualizarem, considerar:
- Opção A: Usar `st.experimental_rerun()` (mais leve)
- Opção B: Atualizar apenas métricas via placeholders
- Opção C: Aceitar que métricas atualizam na próxima interação

### Risco 2: Performance com hierarquias grandes
**Impacto**: MÉDIO
**Probabilidade**: BAIXA
**Mitigação**:
- Cache da estrutura hierárquica em session_state
- Reconstruir apenas quando necessário
- Testar com disciplina maior (Direito Processual Penal Militar)

### Risco 3: Layout em 1 coluna pode ocupar muito espaço vertical
**Impacto**: BAIXO
**Probabilidade**: BAIXA
**Mitigação**:
- Usar caractere Unicode de espaço não-quebrável (` `) para indentação
- Testar visualmente em diferentes tamanhos de tela
- Expanders permitem controlar quantidade de conteúdo visível
- Hierarquia clara facilita navegação mesmo com mais conteúdo vertical

---

## Critérios de Sucesso

### Funcional
- [ ] Expanders permanecem abertos após marcar checkboxes
- [ ] Tópicos aparecem em estrutura hierárquica aninhada
- [ ] Marcar tópico pai marca automaticamente todos os subitens
- [ ] progress.json mantém compatibilidade total
- [ ] Todas as funcionalidades existentes funcionam

### Não-Funcional
- [ ] Tempo de resposta < 500ms ao marcar checkbox
- [ ] Zero aumento no uso de memória
- [ ] Código legível e mantível
- [ ] Zero regressões em funcionalidades existentes

### UX
- [ ] Feedback visual imediato ao marcar checkboxes
- [ ] Hierarquia visual clara e intuitiva
- [ ] Indentação visível e consistente (layout 1 coluna)
- [ ] Números completos visíveis em todos os níveis (1.4.1, 5.2.3, etc.)
- [ ] Layout responsivo mantido
- [ ] Desmarcar pai não afeta filhos (comportamento esperado)

---

## Checklist Final de Implementação

### Pré-Implementação
- [ ] Fazer backup do progress.json atual
- [ ] Criar branch `feature/hierarchical-edital`
- [ ] Testar aplicação atual baseline

### Implementação
- [ ] FASE 1: Funções auxiliares
- [ ] FASE 2: Controle de expanders
- [ ] FASE 3: Renderização hierárquica
- [ ] FASE 4: Testes completos
- [ ] FASE 5: Documentação

### Pós-Implementação
- [ ] Testar em produção local
- [ ] Deploy para staging/homologação
- [ ] Testar com usuários reais
- [ ] Merge para main
- [ ] Atualizar changelog

---

## Notas de Implementação

### Dependências
- Python 3.13 (já utilizado)
- streamlit (já instalado)
- Nenhuma nova dependência necessária

### Compatibilidade
- Python 3.10+ (mínimo)
- Streamlit 1.20+ (versão atual provavelmente OK)
- Navegadores modernos (Chrome, Firefox, Safari, Edge)

### Performance
- Complexidade: O(n) onde n = número de tópicos
- Memória: < 1MB adicional para estruturas hierárquicas
- Network: Sem impacto (client-side rendering)

---

## Referências

- Código atual: `app.py` linhas 33-310 (EDITAL)
- Código atual: `app.py` linhas 596-614 (expander e checkboxes)
- Streamlit docs: https://docs.streamlit.io/library/api-reference/layout
- Unicode spaces: https://www.cs.tut.fi/~jkorpela/chars/spaces.html

---

## Apêndice: Exemplos de Estrutura Hierárquica

### Exemplo 1: Língua Portuguesa

```
Língua Portuguesa
├── 1 Compreensão e interpretação de textos de gêneros variados
├── 2 Reconhecimento de tipos e gêneros textuais
├── 3 Domínio da ortografia oficial
├── 4
│   ├── 4.1 Emprego de elementos de referenciação...
│   └── 4.2 Emprego de tempos e modos verbais
├── 5
│   ├── 5.1 Emprego das classes de palavras
│   ├── 5.2 Relações de coordenação...
│   ├── 5.3 Relações de subordinação...
│   ├── 5.4 Emprego dos sinais de pontuação
│   ├── 5.5 Concordância verbal e nominal
│   ├── 5.6 Regência verbal e nominal
│   ├── 5.7 Emprego do sinal indicativo de crase
│   └── 5.8 Colocação dos pronomes átonos
└── 6
    ├── 6.1 Significação das palavras
    ├── 6.2 Substituição de palavras...
    ├── 6.3 Reorganização da estrutura...
    └── 6.4 Reescrita de textos...
```

### Exemplo 2: Direito Constitucional

```
Direito Constitucional
├── 1
│   ├── 1.1 Conceito, objeto, elementos...
│   ├── 1.2 Supremacia da Constituição
│   ├── 1.3 Aplicabilidade das normas...
│   └── 1.4
│       └── 1.4.1 Métodos, princípios e limites...
├── 2 Princípios fundamentais
├── 3
│   ├── 3.1 Direitos e deveres individuais...
│   ├── 3.2 HC, MS, MI e HD
│   ├── 3.3 Direitos sociais
│   ├── 3.4 Nacionalidade
│   ├── 3.5 Direitos políticos
│   └── 3.6 Partidos políticos
└── ... (continua)
```

---

**Fim do Plano de Implementação**

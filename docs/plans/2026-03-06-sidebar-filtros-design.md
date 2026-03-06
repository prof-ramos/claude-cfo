# Design: Sidebar com Filtros Globais (V1)

## Objetivo
Implementar uma sidebar mais poderosa para navegação e organização, com:
- Lista de disciplinas com progresso (`%` e `x/y`)
- Filtro de status global (`Todas`, `Pendentes`, `Concluídas`)
- Clique em disciplina para mostrar apenas aquela disciplina

A filtragem deve afetar **sidebar e conteúdo principal**.

## Decisões Validadas
- Abordagem escolhida: **estado único de UI + renderização derivada**
- Estado principal: `selected_discipline` e `status_filter`
- Clique em disciplina: **filtra a tela para somente a disciplina selecionada**
- Filtro de status: afeta **toda a experiência** (sidebar e conteúdo)

## Diagrama (Mermaid)
```mermaid
flowchart TD
    A[Init App] --> B[init_ui_state]
    B --> C[Render Sidebar]
    C --> D{Ação do usuário}

    D -->|Seleciona status| E[Atualiza status_filter]
    D -->|Clica disciplina| F[Atualiza selected_discipline]
    D -->|Limpar filtros| G[status_filter=todas\nselected_discipline=None]

    E --> H[apply_filters]
    F --> H
    G --> H

    H --> I[Dados visíveis\n(disciplinas + tópicos)]
    I --> J[Render Sidebar Filtrada]
    I --> K[Render Conteúdo Principal]

    K --> L{Checkbox mudou?}
    L -->|Sim| M[Salvar em progress.json]
    L -->|Não| N[Manter estado]
    M --> H
    N --> H
```

## Estrutura Técnica
Funções sugeridas:
- `init_ui_state()`
- `apply_filters(progress, edital, selected_discipline, status_filter)`
- `render_sidebar(progress, edital, state)`
- `render_main_content(filtered_data, progress)`

## Critérios de Aceite
- Sidebar e conteúdo sempre sincronizados com os filtros
- Troca de disciplina e status sem inconsistência visual
- Persistência de progresso mantida após restart
- `Limpar filtros` restaura visão completa

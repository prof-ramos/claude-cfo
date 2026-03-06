import streamlit as st
import json
import os
from pathlib import Path
from datetime import datetime


def resolve_progress_file():
    env_path = os.getenv("PROGRESS_FILE")
    candidates = []
    if env_path:
        candidates.append(Path(env_path))
    candidates.extend([
        Path("/data/progress.json"),
        Path("progress.json"),
        Path("/tmp/progress.json"),
    ])

    for candidate in candidates:
        try:
            candidate.parent.mkdir(parents=True, exist_ok=True)
            with open(candidate, "a", encoding="utf-8"):
                pass
            return candidate
        except OSError:
            continue

    return Path("/tmp/progress.json")


PROGRESS_FILE = resolve_progress_file()

EDITAL = {
    "Língua Portuguesa": [
        "1 Compreensão e interpretação de textos de gêneros variados",
        "2 Reconhecimento de tipos e gêneros textuais",
        "3 Domínio da ortografia oficial",
        "4.1 Emprego de elementos de referenciação, substituição e repetição, conectores e sequenciação textual",
        "4.2 Emprego de tempos e modos verbais",
        "5.1 Emprego das classes de palavras",
        "5.2 Relações de coordenação entre orações e entre termos da oração",
        "5.3 Relações de subordinação entre orações e entre termos da oração",
        "5.4 Emprego dos sinais de pontuação",
        "5.5 Concordância verbal e nominal",
        "5.6 Regência verbal e nominal",
        "5.7 Emprego do sinal indicativo de crase",
        "5.8 Colocação dos pronomes átonos",
        "6.1 Significação das palavras",
        "6.2 Substituição de palavras ou de trechos de texto",
        "6.3 Reorganização da estrutura de orações e de períodos do texto",
        "6.4 Reescrita de textos de diferentes gêneros e níveis de formalidade",
    ],
    "Legislação (PMDF)": [
        "1 Lei nº 7.289/1984 – Estatuto dos Policiais Militares da PMDF",
        "2 Lei nº 12.086/2009 – Título I",
        "3 Decreto nº 88.777/1983 – R-200 (Regulamento PM e CBM)",
        "4 Decreto nº 10.443/2020 – Organização básica da PMDF",
        "5 LODF – Art. 1º ao 30",
        "5 LODF – Art. 87 ao 99",
        "5 LODF – Art. 117-A ao 124-A",
        "5 LODF – Art. 200 ao 203",
        "5 LODF – Art. 263 ao 311",
        "6 Lei nº 14.751/2023 – Lei Orgânica Nacional das PMs e CBMs",
    ],
    "Distrito Federal e Política para Mulheres": [
        "1 Realidade étnica, social, histórica, geográfica, cultural, política e econômica do DF e RIDE",
        "2 Plano Distrital de Política para Mulheres",
    ],
    "Direitos Humanos": [
        "1.1 Conceitos, terminologia, estrutura normativa, fundamentação",
        "2 Afirmação histórica dos direitos humanos",
        "3 Direitos humanos e responsabilidade do Estado",
        "4 Direitos humanos na Constituição Federal",
        "5 Política Nacional de Direitos Humanos; segurança pública e grupos vulneráveis",
        "6 Constituição brasileira e tratados internacionais de DH (EC nº 45/2024)",
        "7 Declaração Universal dos Direitos Humanos",
    ],
    "Noções de Criminologia": [
        "1.1 Conceito de criminologia",
        "1.2 Métodos: empirismo e interdisciplinaridade",
        "1.3 Objetos: delito, delinquente, vítima, controle social",
        "2.1 Criminologia e política criminal",
        "2.2 Direito penal",
        "3.1 Teorias sociológicas",
        "3.2 Prevenção no Estado democrático de direito",
        "3.3 Prevenção primária",
        "3.4 Prevenção secundária",
        "3.5 Prevenção terciária",
        "3.6 Modelos de reação ao crime",
        "4 Criminologia ambiental",
    ],
    "Raciocínio Lógico": [
        "1 Conjuntos numéricos: inteiros, racionais e reais",
        "2 Sistema legal de medidas",
        "3.1 Divisão proporcional",
        "3.2 Regras de três simples e compostas",
        "3.3 Porcentagens",
        "4 Equações e inequações de 1º e 2º graus",
        "5 Sistemas lineares",
        "6 Funções e gráficos",
        "7 Princípios de contagem",
        "8 Progressões aritméticas e geométricas",
        "9 Compreensão de estruturas lógicas",
        "10 Lógica de argumentação: analogias, inferências, deduções e conclusões",
        "11.1 Proposições simples e compostas",
        "11.2 Tabelas-verdade",
        "11.3 Equivalências",
        "11.4 Leis de De Morgan",
        "11.5 Diagramas lógicos",
        "12 Lógica de primeira ordem",
        "13 Princípios de contagem e probabilidade",
        "14 Operações com conjuntos",
        "15 Raciocínio lógico: problemas aritméticos, geométricos e matriciais",
    ],
    "Língua Inglesa": [
        "1 Compreensão de textos variados: vocabulário e estrutura",
        "2 Itens gramaticais relevantes para compreensão semântica",
        "3 Conhecimento e uso das formas contemporâneas da língua inglesa",
    ],
    "Administração": [
        "1.1 Evolução da administração pública no Brasil após 1930; nova gestão pública",
        "2.1 Funções da administração: planejamento, organização, direção e controle",
        "2.2 Estrutura organizacional",
        "2.3 Cultura organizacional",
        "3.1 Equilíbrio organizacional",
        "3.2 Objetivos, desafios e características da gestão de pessoas",
        "3.3 Comportamento organizacional: motivação, liderança, desempenho",
        "4.1 Principais teóricos da gestão da qualidade",
        "4.2 Ciclo PDCA",
        "4.3 Ferramentas de gestão da qualidade",
        "4.4 Modelo do Gespública",
        "5 Noções de gestão de processos: mapeamento, análise e melhoria",
        "6 Noções de administração de recursos materiais",
    ],
    "Direito Constitucional": [
        "1.1 Conceito, objeto, elementos e classificações da Constituição",
        "1.2 Supremacia da Constituição",
        "1.3 Aplicabilidade das normas constitucionais",
        "1.4.1 Métodos, princípios e limites de interpretação",
        "2 Princípios fundamentais",
        "3.1 Direitos e deveres individuais e coletivos",
        "3.2 HC, MS, MI e HD",
        "3.3 Direitos sociais",
        "3.4 Nacionalidade",
        "3.5 Direitos políticos",
        "3.6 Partidos políticos",
        "4.1 Organização político-administrativa",
        "4.2 União, estados, municípios, DF e territórios",
        "4.3 Intervenção federal e estado de sítio",
        "4.4 Intervenção dos estados nos municípios",
        "5.1 Disposições gerais – Administração pública",
        "5.2 Militares dos estados, DF e territórios",
        "6.1 Mecanismos de freios e contrapesos",
        "6.2.1 Prerrogativas parlamentares",
        "6.3 Conselho da República e Conselho de Defesa Nacional",
        "6.4.1 Poder Judiciário – Disposições gerais",
        "6.4.2 Justiça militar da União e dos estados",
        "7 Defesa do Estado, segurança pública e forças armadas",
        "8 Jurisprudência aplicada dos tribunais superiores",
    ],
    "Direito Administrativo": [
        "1 Estado, governo e administração pública: conceitos e elementos",
        "2 Direito administrativo: conceito, objeto e fontes",
        "3.1 Ato administrativo: conceito, requisitos, atributos, classificação",
        "3.2.1 Cassação, anulação, revogação e convalidação",
        "3.3 Decadência administrativa",
        "4.1 Poderes hierárquico, disciplinar, regulamentar e de polícia",
        "4.2 Uso e abuso do poder",
        "5 Regime jurídico-administrativo: conceito e princípios",
        "6.1 Responsabilidade civil do Estado – evolução histórica",
        "6.2.1 Responsabilidade por ato comissivo",
        "6.2.2 Responsabilidade por omissão",
        "6.3 Requisitos para demonstração da responsabilidade",
        "6.4 Causas excludentes e atenuantes",
        "6.5 Reparação do dano",
        "6.6 Direito de regresso",
        "7.1 Controle pela administração pública",
        "7.2 Controle judicial",
        "7.3 Controle legislativo",
        "7.4.1 Improbidade administrativa – Lei nº 8.429/1992",
        "8.1 Processo administrativo – Lei nº 9.784/1999",
        "9.1.1 Licitações – Lei nº 14.133/2021",
        "9.1.2 Decreto nº 11.531/2023 e Portaria Conjunta MGI/MF/CGU nº 33/2023",
    ],
    "Direito Penal": [
        "1 Princípios aplicáveis ao direito penal",
        "2.1 A lei penal no tempo e no espaço",
        "2.2 Tempo e lugar do crime",
        "2.3 Interpretação da lei penal",
        "2.4 Analogia",
        "2.5 Irretroatividade da lei penal",
        "2.6 Conflito aparente de normas penais",
        "3 Ilicitude",
        "4 Culpabilidade",
        "5 Concurso de pessoas",
        "6.1 Espécies de penas",
        "6.2 Cominação das penas",
        "7 Ação penal",
        "8 Punibilidade e causas de extinção",
        "9 Prescrição",
        "10 Crimes contra a fé pública",
        "11 Crimes contra a administração pública",
        "12 Crimes contra a pessoa",
        "13 Crimes contra o patrimônio",
        "14 Crimes contra a dignidade sexual",
        "15 Crimes contra a incolumidade pública",
        "16 Disposições constitucionais aplicáveis ao direito penal",
        "17 Crimes e sanções penais na licitação (Lei nº 14.133/2021)",
    ],
    "Direito Processual Penal": [
        "1 Processo penal brasileiro e constitucional",
        "2 Sistemas e princípios fundamentais",
        "3.1 Disposições preliminares do CPP",
        "4 Inquérito policial",
        "5.1 Princípios gerais e informadores do processo",
        "5.2 Pretensão punitiva",
        "6 Ação penal",
        "7 Prova",
        "8 Sujeitos do processo",
        "9 Prisão, medidas cautelares e liberdade provisória",
        "10.1 Prazos: características, princípios e contagem",
        "11 Nulidades",
        "12 Jurisprudência aplicada dos tribunais superiores",
    ],
    "Legislação Extravagante": [
        "1 Lei nº 2.889/1956 – Crime de genocídio",
        "2 Lei nº 7.716/1989 – Crimes de preconceito de raça ou cor",
        "3 Lei nº 8.072/1990 e 8.930/1994 – Crimes hediondos",
        "4 Lei nº 12.850/2013 – Crime organizado",
        "5 Lei nº 9.455/1997 – Crimes de tortura",
        "6 Lei nº 9.605/1998 – Crimes contra o meio ambiente",
        "7 Lei nº 10.826/2003 – Estatuto do Desarmamento",
        "8 Lei nº 11.343/2006 – Lei de Drogas",
        "9 Lei nº 11.340/2006 – Lei Maria da Penha",
        "10 Lei nº 9.503/1997 – CTB: Capítulos I, II, VIII, XVII e XIX",
        "11.1 ECA – Parte Geral: Títulos I, II (cap. I e II)",
        "11.2 ECA – Parte Especial: Título III, VI (cap. III – Seção V); Título VII",
        "12 Lei nº 8.429/1992 – Improbidade Administrativa",
        "13 Lei nº 13.869/2019 – Abuso de autoridade",
        "14 Lei nº 7.960/1989 – Prisão temporária",
        "15 Lei nº 9.099/1995 – Juizados especiais",
        "16 Lei nº 10.259/2001 – Juizados especiais federais",
    ],
    "Direito Penal Militar": [
        "1 Aplicação da lei penal militar",
        "2 Crime",
        "3 Imputabilidade penal",
        "4 Concurso de agentes",
        "5 Penas",
        "6 Aplicação da pena",
        "7 Suspensão condicional da pena",
        "8 Livramento condicional",
        "9 Penas acessórias",
        "10 Efeitos da condenação",
        "11 Medidas de segurança",
        "12 Ação penal",
        "13 Extinção da punibilidade",
        "14 Crimes militares em tempo de paz",
        "15 Crimes própria e impropriamente militares; critérios de classificação",
        "16 Princípios constitucionais penais com reflexos na lei penal militar",
    ],
    "Direito Processual Penal Militar": [
        "1 Processo penal militar e sua aplicação",
        "2 Polícia judiciária militar",
        "3 Inquérito policial militar",
        "4 Ação penal militar e seu exercício",
        "5 Processo",
        "6 Juiz, auxiliares e partes do processo",
        "7 Denúncia",
        "8.1 Lei nº 8.457/1992 – Organização da Justiça Militar da União",
        "8.2 Defensoria Pública da União junto à JMU",
        "8.3 Competência da Justiça Militar da União",
        "9 Questões prejudiciais",
        "10 Exceções",
        "11 Incidente de sanidade mental",
        "12 Incidente de falsidade de documento",
        "13 Medidas preventivas e assecuratórias",
        "14 Providências que recaem sobre coisas",
        "15.1 Prisão em flagrante",
        "15.2 Prisão preventiva",
        "15.3 Liberdade provisória",
        "16 Citação, intimação e notificação",
        "17.1 Interrogatório",
        "17.2 Confissão",
        "17.3 Perícias e exames",
        "17.4 Testemunhas",
        "17.5 Acareação",
        "17.6 Reconhecimento de pessoa e coisa",
        "17.7 Documentos",
        "17.8 Indícios",
        "18.1 Processo ordinário",
        "18.2 Processos especiais",
        "18.3 Deserção de oficial e de praça",
        "18.4 Insubmissão",
        "19 Nulidades",
        "20.1 Recurso em sentido estrito",
        "20.2 Correição parcial",
        "20.3 Apelação",
        "20.4 Embargos",
        "20.5 Revisão",
        "20.6 Recurso extraordinário",
        "20.7 Reclamação",
        "21.1 Incidentes de execução",
        "21.2 Suspensão condicional da pena",
        "21.3 Livramento condicional",
        "21.4 Indulto, comutação, anistia e reabilitação",
        "21.5 Execução das medidas de segurança",
        "22 Princípios constitucionais com reflexos na lei processual penal militar",
    ],
}

DISCIPLINE_GROUPS = {
    "📚 Conhecimentos Gerais": [
        "Língua Portuguesa",
        "Legislação (PMDF)",
        "Distrito Federal e Política para Mulheres",
        "Direitos Humanos",
        "Noções de Criminologia",
        "Raciocínio Lógico",
        "Língua Inglesa",
    ],
    "⚖️ Conhecimentos Específicos": [
        "Administração",
        "Direito Constitucional",
        "Direito Administrativo",
        "Direito Penal",
        "Direito Processual Penal",
        "Legislação Extravagante",
        "Direito Penal Militar",
        "Direito Processual Penal Militar",
    ],
}

DISC_COLORS = {
    "Língua Portuguesa": "#4A90D9",
    "Legislação (PMDF)": "#7B68EE",
    "Distrito Federal e Política para Mulheres": "#20B2AA",
    "Direitos Humanos": "#FF7F50",
    "Noções de Criminologia": "#DA70D6",
    "Raciocínio Lógico": "#32CD32",
    "Língua Inglesa": "#FFD700",
    "Administração": "#FF6347",
    "Direito Constitucional": "#1E90FF",
    "Direito Administrativo": "#00CED1",
    "Direito Penal": "#DC143C",
    "Direito Processual Penal": "#FF8C00",
    "Legislação Extravagante": "#9370DB",
    "Direito Penal Militar": "#B22222",
    "Direito Processual Penal Militar": "#CD853F",
}


def load_progress():
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except (json.JSONDecodeError, OSError):
            # Preserve invalid content for debugging and start with a clean state.
            try:
                backup = PROGRESS_FILE.with_name(
                    f"{PROGRESS_FILE.stem}.invalid-{datetime.now().strftime('%Y%m%d-%H%M%S')}{PROGRESS_FILE.suffix}"
                )
                PROGRESS_FILE.replace(backup)
            except OSError:
                pass
            return {}
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def get_topic_key(discipline, topic):
    return f"{discipline}||{topic}"


def calc_discipline_progress(progress, discipline):
    topics = EDITAL[discipline]
    total = len(topics)
    done = sum(1 for t in topics if progress.get(get_topic_key(discipline, t), False))
    return done, total


def calc_overall_progress(progress):
    total_done = 0
    total_all = 0
    for disc, topics in EDITAL.items():
        done, total = calc_discipline_progress(progress, disc)
        total_done += done
        total_all += total
    return total_done, total_all


def init_ui_state():
    if "ui_status_filter" not in st.session_state:
        st.session_state.ui_status_filter = "todas"
    if "ui_selected_discipline" not in st.session_state:
        st.session_state.ui_selected_discipline = None
    if "ui_metrics_mode" not in st.session_state:
        st.session_state.ui_metrics_mode = "filtro"


def topic_matches_filter(progress, discipline, topic, status_filter):
    is_done = progress.get(get_topic_key(discipline, topic), False)
    if status_filter == "pendentes":
        return not is_done
    if status_filter == "concluidas":
        return is_done
    return True


def get_filtered_groups(progress, status_filter, selected_discipline):
    filtered = {}
    for group_name, disciplines in DISCIPLINE_GROUPS.items():
        visible_disciplines = []
        for disc in disciplines:
            if selected_discipline and disc != selected_discipline:
                continue

            visible_topics = [
                topic
                for topic in EDITAL[disc]
                if topic_matches_filter(progress, disc, topic, status_filter)
            ]
            if visible_topics:
                visible_disciplines.append((disc, visible_topics))

        if visible_disciplines:
            filtered[group_name] = visible_disciplines
    return filtered


def calc_filtered_progress(filtered_groups, progress):
    total_done = 0
    total_all = 0
    for disciplines in filtered_groups.values():
        for disc, topics in disciplines:
            done = sum(
                1
                for topic in topics
                if progress.get(get_topic_key(disc, topic), False)
            )
            total_done += done
            total_all += len(topics)
    return total_done, total_all


def main():
    st.set_page_config(
        page_title="PMDF CFO 2025 – Progresso de Estudos",
        page_icon="🎖️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stProgress > div > div > div { height: 12px; border-radius: 6px; }
    .disc-header { font-size: 1.1rem; font-weight: 700; margin-bottom: 2px; }
    .group-title { font-size: 1.3rem; font-weight: 800; color: #ffffff;
                   background: #1a1d27; padding: 10px 16px;
                   border-radius: 8px; margin: 16px 0 8px 0; }
    .progress-label { font-size: 0.78rem; color: #aaaaaa; margin-bottom: 4px; }
    div[data-testid="stCheckbox"] label { font-size: 0.88rem; }
    </style>
    """, unsafe_allow_html=True)

    if "progress" not in st.session_state:
        st.session_state.progress = load_progress()
    init_ui_state()

    progress = st.session_state.progress
    selected_discipline = st.session_state.ui_selected_discipline
    status_filter = st.session_state.ui_status_filter
    status_labels = {
        "todas": "Todas",
        "pendentes": "Pendentes",
        "concluidas": "Concluídas",
    }

    # ── SIDEBAR ──────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 🎖️ PMDF – CFO 2025")
        st.markdown("---")

        total_done, total_all = calc_overall_progress(progress)
        pct = total_done / total_all * 100 if total_all else 0

        st.markdown(f"### 📊 Progresso Total")
        st.markdown(f"<h2 style='color:#4A90D9;margin:0'>{pct:.1f}%</h2>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#aaa'>{total_done} de {total_all} tópicos</span>", unsafe_allow_html=True)
        st.progress(pct / 100)

        st.markdown("---")
        st.markdown("### 🔎 Filtros")

        selected_status_label = st.radio(
            "Status",
            options=list(status_labels.values()),
            index=list(status_labels.keys()).index(status_filter),
            horizontal=True,
        )
        new_status_filter = next(
            key for key, value in status_labels.items() if value == selected_status_label
        )
        if new_status_filter != status_filter:
            st.session_state.ui_status_filter = new_status_filter
            st.rerun()

        if st.button("Limpar filtros", use_container_width=True):
            st.session_state.ui_status_filter = "todas"
            st.session_state.ui_selected_discipline = None
            st.rerun()

        st.markdown("---")
        st.markdown("### 📚 Disciplinas")

        sidebar_groups = get_filtered_groups(progress, st.session_state.ui_status_filter, st.session_state.ui_selected_discipline)

        if not sidebar_groups:
            st.caption("Nenhuma disciplina encontrada para os filtros atuais.")
        else:
            for group_name, disciplines in sidebar_groups.items():
                st.markdown(f"**{group_name}**")
                for disc, _ in disciplines:
                    done, total = calc_discipline_progress(progress, disc)
                    p = done / total * 100 if total else 0
                    is_active = st.session_state.ui_selected_discipline == disc
                    button_label = f"{'👉 ' if is_active else ''}{disc} — {p:.0f}% ({done}/{total})"
                    if st.button(button_label, key=f"disc_filter_{disc}", use_container_width=True):
                        st.session_state.ui_selected_discipline = disc
                        st.rerun()

        if st.session_state.ui_selected_discipline:
            if st.button("Mostrar todas as disciplinas", use_container_width=True):
                st.session_state.ui_selected_discipline = None
                st.rerun()

        st.markdown("---")
        if st.button("🗑️ Resetar tudo", type="secondary"):
            st.session_state.progress = {}
            save_progress({})
            st.rerun()

    # ── MAIN ─────────────────────────────────────────────────────────────
    st.markdown("# 🎖️ PMDF – CFO 2025 | Painel de Estudos")

    filtered_groups = get_filtered_groups(
        progress,
        st.session_state.ui_status_filter,
        st.session_state.ui_selected_discipline,
    )
    metrics_mode = st.radio(
        "Modo das métricas",
        options=["Filtro", "Global"],
        index=0 if st.session_state.ui_metrics_mode == "filtro" else 1,
        horizontal=True,
    )
    st.session_state.ui_metrics_mode = "global" if metrics_mode == "Global" else "filtro"

    if st.session_state.ui_metrics_mode == "global":
        total_done, total_all = calc_overall_progress(progress)
        metrics_suffix = " (Global)"
    else:
        total_done, total_all = calc_filtered_progress(filtered_groups, progress)
        metrics_suffix = " (Filtro)"
    pct = total_done / total_all * 100 if total_all else 0

    col1, col2, col3 = st.columns(3)
    col1.metric(f"✅ Tópicos Concluídos{metrics_suffix}", f"{total_done}")
    col2.metric(
        "📋 Total de Tópicos" if st.session_state.ui_metrics_mode == "global" else "📋 Tópicos Visíveis",
        f"{total_all}",
    )
    col3.metric(f"📈 Progresso{metrics_suffix}", f"{pct:.1f}%")

    st.markdown("---")

    if not filtered_groups:
        st.info("Nenhum tópico encontrado para os filtros selecionados.")

    for group_name, disciplines in filtered_groups.items():
        st.markdown(f"<div class='group-title'>{group_name}</div>", unsafe_allow_html=True)

        for disc, topics in disciplines:
            done, total = calc_discipline_progress(progress, disc)
            p = done / total * 100 if total else 0

            with st.expander(f"{disc}  —  {p:.0f}% concluído  ({done}/{total})", expanded=False):
                st.markdown(
                    f"<div class='progress-label'>{done} de {total} tópicos estudados</div>",
                    unsafe_allow_html=True,
                )
                st.progress(p / 100)
                st.markdown(" ")

                cols = st.columns(2)
                for i, topic in enumerate(topics):
                    key = get_topic_key(disc, topic)
                    current_val = progress.get(key, False)
                    col = cols[i % 2]
                    new_val = col.checkbox(topic, value=current_val, key=f"cb_{key}")
                    if new_val != current_val:
                        progress[key] = new_val
                        st.session_state.progress = progress
                        save_progress(progress)
                        st.rerun()


if __name__ == "__main__":
    main()

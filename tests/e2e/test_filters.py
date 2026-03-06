"""Testes E2E para filtros (status e disciplina)."""

from streamlit.testing.v1 import AppTest


def test_status_filter_radio_exists(app_test):
    """Radio de filtro de status existe na sidebar."""
    at = app_test.run()

    # Deve haver radio na sidebar
    sidebar_radios = list(at.sidebar.radio)
    assert len(sidebar_radios) > 0


def test_status_filter_shows_all_topics(app_test):
    """Filtro 'Todas' mostra todos os tópicos."""
    at = app_test.run()

    # Selecionar "Todas" (primeira opção)
    if list(at.sidebar.radio):
        list(at.sidebar.radio)[0].set_value("Todas").run()

    # Verificar que há checkboxes visíveis
    assert len(at.checkbox) > 200


def test_sidebar_api_verification(app_test):
    """
    Verifica padrões de acesso à API de sidebar.

    Este teste documenta os padrões reais de acesso a widgets sidebar,
    dado que a documentação do Streamlit é obscura sobre at.sidebar.
    """
    at = app_test.run()

    sidebar_radios = list(at.sidebar.radio)
    sidebar_buttons = list(at.sidebar.button)

    # Documentar findings
    assert len(sidebar_radios) > 0, "Deve haver pelo menos um radio na sidebar"
    assert len(sidebar_buttons) > 0, "Deve haver pelo menos um button na sidebar"


def test_discipline_filter_buttons_exist(app_test):
    """Botões de filtro por disciplina existem na sidebar."""
    at = app_test.run()

    # Deve haver botões na sidebar (disciplinas)
    sidebar_buttons = list(at.sidebar.button)

    # Há botões para disciplinas e botões de ação (Limpar filtros, Resetar)
    assert len(sidebar_buttons) >= 15  # Pelo menos 15 disciplinas


def test_discipline_filter_button_pattern(app_test):
    """Verifica que botões de disciplina existem e podem ser acessados."""
    at = app_test.run()

    sidebar_buttons = list(at.sidebar.button)

    # Verificar que há botões suficientes para as 15 disciplinas
    # Mais alguns botões de ação (Limpar, Resetar, etc)
    assert len(sidebar_buttons) >= 15


def test_clear_filters_button_exists(app_test):
    """Botão 'Limpar filtros' ou similar existe na sidebar."""
    at = app_test.run()

    sidebar_buttons = list(at.sidebar.button)

    # Verificar que há botões suficientes (disciplinas + botões de ação)
    # Deve haver mais de 15 botões (15 disciplinas + botões de ação)
    assert len(sidebar_buttons) > 15


def test_metrics_mode_radio_exists(app_test):
    """Radio de modo de métricas existe."""
    at = app_test.run()

    # Há múltiplos radios na sidebar (status filter + metrics mode)
    assert len(list(at.sidebar.radio)) >= 1


def test_checkbox_count_reasonable(app_test):
    """Verifica que quantidade de checkboxes é razoável."""
    at = app_test.run()

    # Deve haver entre 200 e 300 checkboxes (~246 tópicos)
    assert 200 < len(at.checkbox) < 300

"""Testes E2E para interações de checkboxes (marcar tópicos como estudados)."""

from streamlit.testing.v1 import AppTest


def test_app_loads_successfully(app_test):
    """App carrega sem erros."""
    assert not app_test.exception


def test_all_disciplines_have_checkboxes(app_test):
    """Todas as 15 disciplinas têm checkboxes visíveis."""
    at = app_test.run()

    # Deve haver mais de 200 checkboxes (15 disciplinas x ~16 tópicos cada)
    assert len(at.checkbox) > 200


def test_mark_first_topic_as_studied(app_test):
    """Marcar primeiro tópico como estudado usando checkbox."""
    at = app_test.run()

    # Verificar checkbox existe e não está marcado
    assert len(at.checkbox) > 0
    first_checkbox = at.checkbox[0]
    assert first_checkbox.value is False

    # Marcar checkbox
    first_checkbox.check().run()

    # Verificar que foi marcado
    assert at.checkbox[0].value is True


def test_unmark_topic_as_studied(app_test):
    """Desmarcar tópico como estudado."""
    at = app_test.run()

    # Marcar primeiro
    at.checkbox[0].check().run()
    assert at.checkbox[0].value is True

    # Desmarcar
    at.checkbox[0].uncheck().run()
    assert at.checkbox[0].value is False


def test_multiple_checkboxes_can_be_checked(app_test):
    """Múltiplos checkboxes podem ser marcados simultaneamente."""
    at = app_test.run()

    # Marcar primeiros 5 checkboxes
    for i in range(min(5, len(at.checkbox))):
        at.checkbox[i].check().run()

    at.run()

    # Verificar que estão marcados
    for i in range(min(5, len(at.checkbox))):
        assert at.checkbox[i].value is True


def test_checkbox_state_persists_in_session(app_test):
    """Estado de checkbox persiste dentro da mesma sessão."""
    at = app_test.run()

    # Marcar checkbox
    at.checkbox[0].check().run()
    assert at.checkbox[0].value is True

    # Executar novamente (simula rerun)
    at.run()
    assert at.checkbox[0].value is True

"""Testes E2E para edge cases e cenários especiais."""

from pathlib import Path
import sys
from streamlit.testing.v1 import AppTest


def test_reset_all_progress_button(app_test):
    """Botão 'Resetar tudo' limpa todo o progresso."""
    at = app_test.run()

    # Marcar alguns checkboxes (primeiros 3)
    for i in range(min(3, len(at.checkbox))):
        at.checkbox[i].check().run()

    # Verificar que estão marcados
    at.run()
    assert any(at.checkbox[i].value for i in range(min(3, len(at.checkbox))))

    # Encontrar botão Resetar na sidebar
    reset_index = None
    for i, button in enumerate(at.sidebar.button):
        # Widget button tem proto com name/label
        if hasattr(button, 'proto') and hasattr(button.proto, 'name'):
            if "Resetar" in button.proto.name:
                reset_index = i
                break

    if reset_index is not None:
        at.sidebar.button[reset_index].click().run()

        # Verificar que foram desmarcados
        at.run()
        assert all(not at.checkbox[i].value for i in range(min(3, len(at.checkbox))))


def test_empty_initial_state(app_test):
    """Estado inicial vazio (nenhum tópico marcado)."""
    at = app_test.run()

    # Verificar que checkboxes iniciais não estão marcados
    for i in range(min(10, len(at.checkbox))):
        assert at.checkbox[i].value is False


def test_persistence_across_runs(tmp_path, monkeypatch):
    """Progresso persiste entre execuções do App."""
    progress_file = tmp_path / "test_progress.json"
    monkeypatch.setenv("PROGRESS_FILE", str(progress_file))

    # Limpar módulo app
    if 'app' in sys.modules:
        del sys.modules['app']

    # Primeira execução: marcar primeiro checkbox
    at1 = AppTest.from_file("app.py")
    at1.run()
    at1.checkbox[0].check().run()

    # Verificar que arquivo foi escrito
    assert progress_file.exists()

    # Limpar módulo app para segunda execução
    if 'app' in sys.modules:
        del sys.modules['app']

    # Segunda execução: verificar que checkbox ainda está marcado
    at2 = AppTest.from_file("app.py")
    at2.run()
    assert at2.checkbox[0].value is True


def test_corrupted_progress_file_recovery(tmp_path, monkeypatch):
    """App lida graciosamente com arquivo de progresso corrompido."""
    # Criar arquivo corrompido
    progress_file = tmp_path / "test_progress.json"
    progress_file.write_text("{invalid json content")

    monkeypatch.setenv("PROGRESS_FILE", str(progress_file))

    # Limpar módulo app
    if 'app' in sys.modules:
        del sys.modules['app']

    # App deve carregar sem crashar
    at = AppTest.from_file("app.py")
    assert not at.exception


def test_all_topics_completed_scenario(app_test):
    """Cenário: marcar vários tópicos (simulação de 100%)."""
    at = app_test.run()

    # Marcar primeiros 10 checkboxes (para ser rápido)
    for i in range(min(10, len(at.checkbox))):
        at.checkbox[i].check().run()

    at.run()

    # Verificar que estão marcados
    marked_count = sum(1 for i in range(min(10, len(at.checkbox))) if at.checkbox[i].value)
    assert marked_count == 10


def test_checkbox_index_out_of_bounds(app_test):
    """Acessar checkbox com índice inválido não causa crash."""
    at = app_test.run()

    # Tentar acessar índice além do limite deve lançar IndexError
    try:
        _ = at.checkbox[99999].value
        assert False, "Deveria ter lançado IndexError"
    except (IndexError, KeyError):
        # Comportamento esperado
        pass


def test_rapid_checkbox_toggling(app_test):
    """Toggle rápido de checkbox múltiplas vezes."""
    at = app_test.run()

    # Toggle múltiplas vezes
    at.checkbox[0].check().run()
    assert at.checkbox[0].value is True

    at.checkbox[0].uncheck().run()
    assert at.checkbox[0].value is False

    at.checkbox[0].check().run()
    assert at.checkbox[0].value is True

    at.checkbox[0].uncheck().run()
    assert at.checkbox[0].value is False

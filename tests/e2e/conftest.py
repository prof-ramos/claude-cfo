"""Fixtures pytest para testes E2E."""

import sys
from pathlib import Path

import pytest


@pytest.fixture
def app_test(tmp_path, monkeypatch):
    """
    Fixture AppTest com PROGRESS_FILE isolado.

    NOTA CRÍTICA: PROGRESS_FILE é uma constante de módulo (app.py:31)
    avaliada no import. AppTest.from_file() carrega o app em subprocesso isolado,
    então monkeypatch.setattr não funciona.

    Solução: Usar variável de ambiente que é verificada PRIMEIRO em
    resolve_progress_file() (app.py:8-10).
    """
    progress_file = tmp_path / "test_progress.json"
    monkeypatch.setenv("PROGRESS_FILE", str(progress_file))

    # Remover módulo app do cache para recarregar com nova env var
    if 'app' in sys.modules:
        del sys.modules['app']

    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file("app.py")
    return at


@pytest.fixture
def known_topic_key():
    """
    Retorna uma key de tópico conhecido que existe no EDITAL.

    Usa o primeiro tópico da primeira disciplina.
    """
    return "Língua Portuguesa||1 Compreensão e interpretação de textos de gêneros variados"


@pytest.fixture
def known_checkbox_key(known_topic_key):
    """
    Retorna a key de checkbox correspondente ao tópico conhecido.

    Padrão em app.py:609: key=f"cb_{key}" onde key=get_topic_key(disc, topic)
    """
    return f"cb_{known_topic_key}"


@pytest.fixture
def sample_progress_data(known_topic_key):
    """
    Retorna dados de progresso de exemplo para setup de testes.
    """
    return {
        known_topic_key: True,
        "Língua Portuguesa||2 Reconhecimento de tipos e gêneros textuais": False,
        "Direito Penal||1 Princípios aplicáveis ao direito penal": False,
    }

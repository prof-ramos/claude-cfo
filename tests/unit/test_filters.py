"""Testes unitários para funções de filtro."""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app import (
    topic_matches_filter,
    get_filtered_groups,
    calc_filtered_progress,
    EDITAL,
    DISCIPLINE_GROUPS,
    get_topic_key,
)


class TestTopicMatchesFilter:
    """Testes para topic_matches_filter."""

    def test_filter_all_always_returns_true(self):
        """Filtro 'todas' retorna True sempre."""
        result = topic_matches_filter({}, "Qualquer Disciplina", "Qualquer Tópico", "todas")
        assert result is True

    def test_filter_pending_returns_true_when_not_done(self):
        """Filtro 'pendentes' retorna True para não marcados."""
        progress = {}
        result = topic_matches_filter(progress, "Direito", "Tópico", "pendentes")
        assert result is True

    def test_filter_pending_returns_false_when_done(self):
        """Filtro 'pendentes' retorna False para marcados."""
        progress = {"Direito||Tópico": True}
        result = topic_matches_filter(progress, "Direito", "Tópico", "pendentes")
        assert result is False

    def test_filter_completed_returns_true_when_done(self):
        """Filtro 'concluidas' retorna True para marcados."""
        progress = {"Direito||Tópico": True}
        result = topic_matches_filter(progress, "Direito", "Tópico", "concluidas")
        assert result is True

    def test_filter_completed_returns_false_when_not_done(self):
        """Filtro 'concluidas' retorna False para não marcados."""
        progress = {}
        result = topic_matches_filter(progress, "Direito", "Tópico", "concluidas")
        assert result is False


class TestGetFilteredGroups:
    """Testes para get_filtered_groups."""

    def test_filter_by_discipline(self):
        """Filtra corretamente por disciplina específica."""
        progress = {}
        selected = "Língua Portuguesa"

        result = get_filtered_groups(progress, "todas", selected)

        # Deve retornar apenas a disciplina selecionada
        assert len(result) > 0
        for group_name, disciplines in result.items():
            for disc, _ in disciplines:
                assert disc == selected

    def test_filter_by_status_pending(self):
        """Filtra corretamente por status pendente."""
        # Usar tópicos reais do EDITAL
        topic1 = EDITAL["Língua Portuguesa"][0]
        topic2 = EDITAL["Língua Portuguesa"][1]

        # Marcar alguns tópicos como concluídos
        progress = {
            get_topic_key("Língua Portuguesa", topic1): True,
            get_topic_key("Língua Portuguesa", topic2): False,
        }

        result = get_filtered_groups(progress, "pendentes", None)

        # Deve incluir apenas tópicos não marcados
        for group_name, disciplines in result.items():
            for disc, topics in disciplines:
                for topic in topics:
                    key = get_topic_key(disc, topic)
                    assert progress.get(key, False) is False

    def test_filter_by_status_completed(self):
        """Filtra corretamente por status concluído."""
        # Usar tópicos reais do EDITAL
        topic1 = EDITAL["Língua Portuguesa"][0]
        topic2 = EDITAL["Língua Portuguesa"][1]

        progress = {
            get_topic_key("Língua Portuguesa", topic1): True,
            get_topic_key("Língua Portuguesa", topic2): False,
        }

        result = get_filtered_groups(progress, "concluidas", None)

        # Deve incluir apenas tópicos marcados
        for group_name, disciplines in result.items():
            for disc, topics in disciplines:
                for topic in topics:
                    key = get_topic_key(disc, topic)
                    assert progress.get(key, False) is True

    def test_filter_combined_discipline_and_status(self):
        """Filtra corretamente com disciplina + status."""
        # Usar tópicos reais do EDITAL
        topic1 = EDITAL["Língua Portuguesa"][0]
        topic2 = EDITAL["Língua Portuguesa"][1]
        topic3 = EDITAL["Direito Penal"][0] if "Direito Penal" in EDITAL else EDITAL["Direito Constitucional"][0]

        progress = {
            get_topic_key("Língua Portuguesa", topic1): True,
            get_topic_key("Língua Portuguesa", topic2): False,
            get_topic_key("Direito Penal", topic3): True,
        }

        result = get_filtered_groups(progress, "concluidas", "Língua Portuguesa")

        # Deve incluir apenas tópicos marcados de Língua Portuguesa
        assert len(result) > 0
        for group_name, disciplines in result.items():
            for disc, topics in disciplines:
                assert disc == "Língua Portuguesa"
                for topic in topics:
                    key = get_topic_key(disc, topic)
                    assert progress.get(key, False) is True

    def test_filter_all_returns_everything(self):
        """Filtro 'todas' retorna todos os tópicos."""
        progress = {
            "Língua Portuguesa||1 Compreensão": True,
            "Direito Penal||1 Princípios": False,
        }

        result = get_filtered_groups(progress, "todas", None)

        # Deve retornar todos os grupos e disciplinas
        assert len(result) == len(DISCIPLINE_GROUPS)


class TestCalcFilteredProgress:
    """Testes para calc_filtered_progress."""

    def test_ignores_filtered_out_topics(self):
        """Ignora tópicos filtrados."""
        # Usar tópicos reais do EDITAL
        topic1 = EDITAL["Língua Portuguesa"][0]
        topic2 = EDITAL["Língua Portuguesa"][1]
        topic3 = EDITAL["Direito Penal"][0] if "Direito Penal" in EDITAL else EDITAL["Direito Constitucional"][0]

        progress = {
            get_topic_key("Língua Portuguesa", topic1): True,
            get_topic_key("Língua Portuguesa", topic2): True,
            get_topic_key("Direito Penal", topic3): False,
        }

        # Filtrar apenas Língua Portuguesa
        filtered = get_filtered_groups(progress, "todas", "Língua Portuguesa")

        done, total = calc_filtered_progress(filtered, progress)

        # Deve contar apenas tópicos de Língua Portuguesa
        assert done == 2

    def test_calculates_correctly_for_status_filter(self):
        """Calcula corretamente para filtro de status."""
        # Usar tópicos reais do EDITAL
        topic1 = EDITAL["Língua Portuguesa"][0]
        topic2 = EDITAL["Língua Portuguesa"][1]

        progress = {
            get_topic_key("Língua Portuguesa", topic1): True,
            get_topic_key("Língua Portuguesa", topic2): False,
        }

        # Filtrar apenas concluídos
        filtered = get_filtered_groups(progress, "concluidas", None)

        done, total = calc_filtered_progress(filtered, progress)

        assert done == 1  # Apenas 1 tópico marcado
        assert total == 1  # Apenas 1 tópico visível no filtro

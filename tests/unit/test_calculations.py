"""Testes unitários para funções de cálculo de progresso."""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app import (
    calc_discipline_progress,
    calc_overall_progress,
    EDITAL,
    get_topic_key,
)


class TestCalcDisciplineProgress:
    """Testes para calc_discipline_progress."""

    def test_all_topics_done_returns_100_percent(self):
        """100% quando todos tópicos marcados."""
        discipline = "Língua Portuguesa"
        progress = {}

        # Marcar todos os tópicos
        for topic in EDITAL[discipline]:
            progress[get_topic_key(discipline, topic)] = True

        done, total = calc_discipline_progress(progress, discipline)

        assert done == total
        assert total > 0

    def test_no_topics_done_returns_0_percent(self):
        """0% quando nenhum marcado."""
        discipline = "Direito Penal"
        progress = {}

        done, total = calc_discipline_progress(progress, discipline)

        assert done == 0
        assert total > 0

    def test_partial_progress_calculates_correctly(self):
        """Percentual correto para parcial."""
        discipline = "Raciocínio Lógico"
        progress = {}

        topics = EDITAL[discipline]
        # Marcar metade dos tópicos
        for i, topic in enumerate(topics):
            if i < len(topics) // 2:
                progress[get_topic_key(discipline, topic)] = True

        done, total = calc_discipline_progress(progress, discipline)

        assert done > 0
        assert done < total
        assert total == len(topics)

    def test_unknown_discipline_raises_keyerror(self):
        """Disciplina desconhecida lança KeyError."""
        discipline = "Disciplina Inexistente"
        progress = {}

        with pytest.raises(KeyError):
            calc_discipline_progress(progress, discipline)


class TestCalcOverallProgress:
    """Testes para calc_overall_progress."""

    def test_aggregates_all_disciplines(self):
        """Agrega corretamente todas disciplinas."""
        progress = {}

        # Marcar alguns tópicos de diferentes disciplinas
        for disc in ["Língua Portuguesa", "Direito Penal", "Raciocínio Lógico"]:
            for topic in EDITAL[disc][:2]:  # Primeiros 2 tópicos
                progress[get_topic_key(disc, topic)] = True

        total_done, total_all = calc_overall_progress(progress)

        assert total_done == 6  # 2 tópicos x 3 disciplinas
        assert total_all > 0

    def test_empty_progress_returns_zero(self):
        """Progresso vazio retorna 0/0."""
        progress = {}

        total_done, total_all = calc_overall_progress(progress)

        assert total_done == 0
        assert total_all > 0  # Total de todos os tópicos do edital

    def test_all_topics_done_returns_full_count(self):
        """Todos tópicos marcados retorna contagem total."""
        progress = {}

        # Marcar todos os tópicos de todas as disciplinas
        for disc, topics in EDITAL.items():
            for topic in topics:
                progress[get_topic_key(disc, topic)] = True

        total_done, total_all = calc_overall_progress(progress)

        assert total_done == total_all
        assert total_all > 200  # ~246 tópicos no total

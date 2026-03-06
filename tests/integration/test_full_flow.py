"""Testes de integração para fluxos completos da aplicação."""

import json
import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app import (
    load_progress,
    save_progress,
    calc_discipline_progress,
    calc_overall_progress,
    get_topic_key,
    EDITAL,
)


class TestFullFlow:
    """Testes de fluxo completo da aplicação."""

    def test_complete_mark_and_retrieve_flow(self, tmp_path, monkeypatch):
        """Fluxo completo: carregar -> marcar -> salvar -> recarregar -> verificar."""
        progress_file = tmp_path / "test_progress.json"
        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        # 1. Carregar estado inicial (arquivo não existe)
        progress = load_progress()
        assert progress == {}

        # 2. Marcar tópicos de duas disciplinas
        disciplina1 = "Língua Portuguesa"
        disciplina2 = "Direito Penal"

        # Marcar primeiro tópico de cada disciplina
        progress[get_topic_key(disciplina1, EDITAL[disciplina1][0])] = True
        progress[get_topic_key(disciplina2, EDITAL[disciplina2][0])] = True

        # 3. Salvar
        save_progress(progress)

        # 4. Recarregar e verificar persistência
        reloaded = load_progress()
        assert reloaded == progress
        assert len(reloaded) == 2

        # 5. Verificar cálculos de disciplina
        done1, total1 = calc_discipline_progress(reloaded, disciplina1)
        assert done1 == 1
        assert total1 == len(EDITAL[disciplina1])

        done2, total2 = calc_discipline_progress(reloaded, disciplina2)
        assert done2 == 1
        assert total2 == len(EDITAL[disciplina2])

    def test_flow_with_backup_on_corruption(self, tmp_path, monkeypatch):
        """Fluxo: salvar -> corromper -> carregar (deve criar backup)."""
        progress_file = tmp_path / "test_progress.json"
        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        # 1. Salvar dados válidos
        valid_data = {"Teste||Tópico": True}
        save_progress(valid_data)

        # 2. Corromper arquivo manualmente
        progress_file.write_text("{corrupted json data}")

        # 3. Tentar carregar (deve criar backup e retornar vazio)
        loaded = load_progress()
        assert loaded == {}

        # 4. Verificar que backup foi criado
        backup_files = list(tmp_path.glob("*.invalid-*"))
        assert len(backup_files) == 1

    def test_multi_discipline_progress_tracking(self, tmp_path, monkeypatch):
        """Acompanhamento de progresso em múltiplas disciplinas."""
        progress_file = tmp_path / "test_progress.json"
        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        progress = {}

        # Marcar progresso em 3 disciplinas diferentes
        disciplinas = ["Língua Portuguesa", "Raciocínio Lógico", "Direito Constitucional"]

        for disc in disciplinas:
            # Marcar primeiros 3 tópicos de cada disciplina
            for i, topic in enumerate(EDITAL[disc][:3]):
                progress[get_topic_key(disc, topic)] = True

        save_progress(progress)

        # Recarregar e verificar agregação
        reloaded = load_progress()
        total_done, total_all = calc_overall_progress(reloaded)

        assert total_done == 9  # 3 tópicos x 3 disciplinas

        # Verificar progresso individual por disciplina
        for disc in disciplinas:
            done, total = calc_discipline_progress(reloaded, disc)
            assert done == 3

    def test_persistence_across_sessions(self, tmp_path, monkeypatch):
        """Simula duas sessões de usuário com persistência."""
        progress_file = tmp_path / "test_progress.json"
        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        # === Sessão 1: Usuário marca alguns tópicos ===
        sessao1_progress = load_progress()
        sessao1_progress[get_topic_key("Língua Portuguesa", EDITAL["Língua Portuguesa"][0])] = True
        sessao1_progress[get_topic_key("Língua Portuguesa", EDITAL["Língua Portuguesa"][1])] = True
        save_progress(sessao1_progress)

        # === Sessão 2: Usuário retoma e marca mais ===
        sessao2_progress = load_progress()
        assert len(sessao2_progress) == 2  # Tópicos da sessão 1 persistidos

        # Marcar mais um tópico
        sessao2_progress[get_topic_key("Língua Portuguesa", EDITAL["Língua Portuguesa"][2])] = True
        save_progress(sessao2_progress)

        # === Verificar estado final ===
        final_progress = load_progress()
        assert len(final_progress) == 3
        done, total = calc_discipline_progress(final_progress, "Língua Portuguesa")
        assert done == 3

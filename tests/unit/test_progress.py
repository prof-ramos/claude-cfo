"""Testes unitários para funções de progresso e persistência."""

import json
import pytest
from pathlib import Path
from datetime import datetime

# Importar funções do app.py
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app import get_topic_key, load_progress, save_progress


class TestGetTopicKey:
    """Testes para get_topic_key."""

    def test_formats_with_pipe_separator(self):
        """Chave composta deve usar pipe como separador."""
        result = get_topic_key("Direito Penal", "1 Princípios")
        assert result == "Direito Penal||1 Princípios"

    def test_handles_special_characters(self):
        """Deve lidar com caracteres especiais."""
        result = get_topic_key("Direito Constitucional", "1.1 Conceito, objeto")
        assert result == "Direito Constitucional||1.1 Conceito, objeto"

    def test_handles_empty_strings(self):
        """Deve lidar com strings vazias."""
        result = get_topic_key("", "")
        assert result == "||"


class TestLoadProgress:
    """Testes para load_progress."""

    def test_load_empty_file_returns_empty_dict(self, tmp_path, monkeypatch):
        """Arquivo vazio retorna dict vazio."""
        progress_file = tmp_path / "test_progress.json"
        progress_file.write_text("")

        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        result = load_progress()

        assert result == {}

    def test_load_valid_json_returns_data(self, tmp_path, monkeypatch):
        """JSON válido carrega corretamente."""
        progress_file = tmp_path / "test_progress.json"
        data = {"Língua Portuguesa||1 Compreensão": True}
        progress_file.write_text(json.dumps(data))

        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        result = load_progress()

        assert result == data

    def test_load_invalid_json_creates_backup(self, tmp_path, monkeypatch):
        """JSON inválido cria backup e retorna dict vazio."""
        progress_file = tmp_path / "test_progress.json"
        progress_file.write_text("{invalid json}")

        # Mock PROGRESS_FILE
        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        result = load_progress()

        # Verifica retorno vazio
        assert result == {}

        # Verifica backup criado
        backup_files = list(tmp_path.glob("*.invalid-*"))
        assert len(backup_files) == 1
        assert "test_progress.invalid-" in backup_files[0].name

    def test_load_nonexistent_file_returns_empty_dict(self, tmp_path, monkeypatch):
        """Arquivo inexistente retorna dict vazio."""
        progress_file = tmp_path / "nonexistent.json"

        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        result = load_progress()

        assert result == {}


class TestSaveProgress:
    """Testes para save_progress."""

    def test_save_creates_file_with_data(self, tmp_path, monkeypatch):
        """Salva dados corretamente no arquivo."""
        progress_file = tmp_path / "test_progress.json"
        data = {"Disciplina||Tópico": True}

        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        save_progress(data)

        assert progress_file.exists()
        with open(progress_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == data

    def test_save_overwrites_existing_data(self, tmp_path, monkeypatch):
        """Sobrescreve dados existentes."""
        progress_file = tmp_path / "test_progress.json"
        progress_file.write_text('{"old": "data"}')

        new_data = {"new": "data"}

        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        save_progress(new_data)

        with open(progress_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == new_data

    def test_save_handles_unicode(self, tmp_path, monkeypatch):
        """Lida corretamente com caracteres Unicode."""
        progress_file = tmp_path / "test_progress.json"
        data = {"Língua Portuguesa||Compreensão": True, "Direito Constitucional||1.1 Conceito": False}

        import app
        monkeypatch.setattr(app, "PROGRESS_FILE", progress_file)

        save_progress(data)

        with open(progress_file, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        assert loaded == data

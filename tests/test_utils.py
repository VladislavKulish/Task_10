import json
import os
import logging
from unittest.mock import patch
from pathlib import Path

import pytest

from src.utils import load_transactions


class TestLoadTransactions:
    @pytest.fixture
    def tmp_data_dir(self, tmp_path):
        data_dir = tmp_path / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        yield data_dir

    def test_valid_list(self, tmp_data_dir):
        file_path = tmp_data_dir / "operations.json"
        data = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
        file_path.write_text(json.dumps(data), encoding="utf-8")

        result = load_transactions(str(file_path))
        assert result == data

    def test_empty_file(self, tmp_data_dir):
        file_path = tmp_data_dir / "empty.json"
        file_path.write_text("", encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_invalid_json(self, tmp_data_dir):
        file_path = tmp_data_dir / "bad.json"
        file_path.write_text("{not json}", encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_not_a_list(self, tmp_data_dir):
        file_path = tmp_data_dir / "not_list.json"
        file_path.write_text(json.dumps({"key": "value"}), encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_file_not_found(self):
        assert load_transactions("nonexistent_file.json") == []


class TestLogging:
    def test_log_file_created(self, tmp_path):
        file_path = tmp_path / "operations.json"
        data = [{"id": 1}]
        file_path.write_text(json.dumps(data), encoding="utf-8")

        result = load_transactions(str(file_path))
        assert result == data

    def test_warning_logged_for_missing_file(self, caplog):
        with caplog.at_level(logging.WARNING, logger="utils"):
            load_transactions("nonexistent.json")
        assert any("Файл не найден" in record.message for record in caplog.records)

    def test_error_logged_for_invalid_json(self, tmp_path, caplog):
        file_path = tmp_path / "bad.json"
        file_path.write_text("{not json}", encoding="utf-8")

        with caplog.at_level(logging.ERROR, logger="utils"):
            load_transactions(str(file_path))
        assert any("Ошибка чтения" in record.message for record in caplog.records)
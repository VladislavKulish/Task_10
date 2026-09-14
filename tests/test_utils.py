import json
import os
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